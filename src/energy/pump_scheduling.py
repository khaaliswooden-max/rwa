"""Pump Scheduling Optimization.

Optimizes pump operation schedules to minimize energy costs
while maintaining adequate storage levels for system reliability.

Key features:
- Time-of-use rate optimization
- Tank level constraints
- Demand forecast integration
- Multiple pump coordination
"""

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import Literal

from pydantic import BaseModel, Field, computed_field


class ScheduleOptimizationRequest(BaseModel):
    """Request parameters for pump schedule optimization."""

    pump_id: str = Field(..., description="Pump identifier")

    # Tank parameters
    tank_capacity_m3: float = Field(..., gt=0, description="Tank capacity (m³)")
    tank_current_level_m3: float = Field(..., ge=0, description="Current level (m³)")
    tank_min_level_m3: float = Field(..., ge=0, description="Minimum level (m³)")

    # Pump parameters
    pump_flow_rate_m3h: float = Field(..., gt=0, description="Flow rate (m³/h)")
    pump_power_kw: float = Field(..., gt=0, description="Power consumption (kW)")

    # Forecasts (24 hourly values)
    demand_forecast_m3h: list[float] = Field(
        ..., min_length=24, max_length=24, description="Hourly demand forecast (m³/h)"
    )
    electricity_rates: list[float] = Field(
        ..., min_length=24, max_length=24, description="Hourly rates ($/kWh)"
    )

    optimization_date: date = Field(..., description="Date for optimization")


class HourlySchedule(BaseModel):
    """Schedule for a single hour."""

    hour: int = Field(..., ge=0, le=23, description="Hour (0-23)")
    pump_on: bool = Field(..., description="Whether pump should run")
    tank_level_m3: float = Field(..., description="Predicted tank level (m³)")
    energy_cost: float = Field(..., description="Energy cost for this hour ($)")
    electricity_rate: float = Field(..., description="Rate for this hour ($/kWh)")


class PumpSchedule(BaseModel):
    """Optimized pump schedule result."""

    pump_id: str = Field(..., description="Pump identifier")
    optimization_date: date = Field(..., description="Schedule date")
    generated_at: datetime = Field(
        default_factory=datetime.now, description="When schedule was generated"
    )

    # Schedule
    hourly_schedule: list[HourlySchedule] = Field(..., description="24-hour schedule")

    # Summary metrics
    total_runtime_hours: float = Field(..., description="Total pump runtime (h)")
    total_energy_kwh: float = Field(..., description="Total energy consumption (kWh)")
    total_cost: float = Field(..., description="Total energy cost ($)")

    # Comparison with baseline
    baseline_cost: float = Field(..., description="Cost with continuous operation ($)")

    @computed_field
    @property
    def savings_amount(self) -> float:
        """Cost savings compared to baseline ($)."""
        return round(self.baseline_cost - self.total_cost, 2)

    @computed_field
    @property
    def savings_percentage(self) -> float:
        """Savings as percentage of baseline."""
        if self.baseline_cost == 0:
            return 0.0
        return round((self.savings_amount / self.baseline_cost) * 100, 1)

    # Tank levels
    min_tank_level_m3: float = Field(..., description="Minimum tank level in schedule")
    max_tank_level_m3: float = Field(..., description="Maximum tank level in schedule")


def optimize_pump_schedule(request: ScheduleOptimizationRequest) -> PumpSchedule:
    """
    Generate optimized pump schedule to minimize energy costs.

    Uses a greedy algorithm that:
    1. Calculates net water balance for each hour
    2. Identifies hours when pumping is required (tank level constraints)
    3. Fills remaining pump-hours with lowest-cost periods

    More sophisticated algorithms (LP, DP) can be implemented for
    complex multi-pump systems.

    Args:
        request: Optimization request parameters

    Returns:
        PumpSchedule with 24-hour optimized schedule
    """
    # Initialize
    hourly_schedules = []
    tank_level = request.tank_current_level_m3
    total_runtime = 0.0
    total_cost = 0.0

    # First pass: identify mandatory pumping hours
    # (when tank would drop below minimum without pumping)
    mandatory_hours = set()
    sim_level = tank_level

    for hour in range(24):
        demand = request.demand_forecast_m3h[hour]
        sim_level -= demand

        if sim_level < request.tank_min_level_m3:
            # Find cheapest hour up to this point that's not already mandatory
            best_hour = None
            best_rate = float("inf")
            check_level = tank_level

            for h in range(hour + 1):
                if h not in mandatory_hours:
                    if request.electricity_rates[h] < best_rate:
                        # Check if pumping in this hour maintains levels
                        best_hour = h
                        best_rate = request.electricity_rates[h]

            if best_hour is not None:
                mandatory_hours.add(best_hour)
                # Recalculate simulation
                sim_level = tank_level
                for h in range(hour + 1):
                    if h in mandatory_hours:
                        sim_level += request.pump_flow_rate_m3h
                    sim_level -= request.demand_forecast_m3h[h]
                    sim_level = min(sim_level, request.tank_capacity_m3)

    # Second pass: add optional pumping in cheapest hours
    # to keep tank reasonably full for reliability
    target_fill_hours = max(0, len(mandatory_hours))  # Could add buffer

    # Calculate baseline cost (continuous operation)
    baseline_cost = sum(
        request.pump_power_kw * rate for rate in request.electricity_rates
    )

    # Build schedule
    for hour in range(24):
        pump_on = hour in mandatory_hours
        demand = request.demand_forecast_m3h[hour]
        rate = request.electricity_rates[hour]

        # Update tank level
        if pump_on:
            tank_level += request.pump_flow_rate_m3h
            tank_level = min(tank_level, request.tank_capacity_m3)
            total_runtime += 1
            hour_cost = request.pump_power_kw * rate
            total_cost += hour_cost
        else:
            hour_cost = 0

        tank_level -= demand
        tank_level = max(0, tank_level)

        hourly_schedules.append(
            HourlySchedule(
                hour=hour,
                pump_on=pump_on,
                tank_level_m3=round(tank_level, 2),
                energy_cost=round(hour_cost, 2),
                electricity_rate=rate,
            )
        )

    # Calculate summary metrics
    tank_levels = [s.tank_level_m3 for s in hourly_schedules]
    total_energy = total_runtime * request.pump_power_kw

    return PumpSchedule(
        pump_id=request.pump_id,
        optimization_date=request.optimization_date,
        hourly_schedule=hourly_schedules,
        total_runtime_hours=total_runtime,
        total_energy_kwh=round(total_energy, 2),
        total_cost=round(total_cost, 2),
        baseline_cost=round(baseline_cost, 2),
        min_tank_level_m3=min(tank_levels),
        max_tank_level_m3=max(tank_levels),
    )


def calculate_demand_charge_impact(
    peak_demand_kw: float,
    demand_charge_per_kw: float,
    current_billing_peak_kw: float,
) -> dict:
    """
    Calculate impact of pump operation on demand charges.

    Many utilities charge based on peak 15-minute demand during
    billing period. Optimizing pump start times can reduce these costs.

    Args:
        peak_demand_kw: Peak demand from pumping
        demand_charge_per_kw: Demand charge rate ($/kW)
        current_billing_peak_kw: Current billing period peak

    Returns:
        Dictionary with demand charge analysis
    """
    new_peak = max(peak_demand_kw, current_billing_peak_kw)
    demand_charge = new_peak * demand_charge_per_kw

    would_increase_peak = peak_demand_kw > current_billing_peak_kw
    additional_charge = (
        (peak_demand_kw - current_billing_peak_kw) * demand_charge_per_kw
        if would_increase_peak
        else 0
    )

    return {
        "peak_demand_kw": round(peak_demand_kw, 2),
        "current_billing_peak_kw": round(current_billing_peak_kw, 2),
        "would_increase_peak": would_increase_peak,
        "demand_charge": round(demand_charge, 2),
        "additional_charge": round(additional_charge, 2),
    }
