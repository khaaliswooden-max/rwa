"""Energy Management API endpoints."""

from datetime import date, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field

from api.auth import CurrentUser
from src.energy.pump_scheduling import (
    PumpSchedule,
    ScheduleOptimizationRequest,
    optimize_pump_schedule,
)
from src.energy.efficiency_analysis import (
    EfficiencyReport,
    PumpEfficiencyInput,
    analyze_pump_efficiency,
)
from src.energy.cost_optimization import (
    CostAnalysis,
    EnergyCostInput,
    analyze_energy_costs,
)

router = APIRouter()


# Request Models
class PumpScheduleRequest(BaseModel):
    """Request model for pump schedule optimization."""

    pump_id: str = Field(..., description="Pump identifier")
    tank_capacity_m3: float = Field(..., gt=0, description="Storage tank capacity (m³)")
    tank_current_level_m3: float = Field(
        ..., ge=0, description="Current tank level (m³)"
    )
    tank_min_level_m3: float = Field(
        ..., ge=0, description="Minimum tank level (m³)"
    )
    pump_flow_rate_m3h: float = Field(
        ..., gt=0, description="Pump flow rate (m³/h)"
    )
    pump_power_kw: float = Field(..., gt=0, description="Pump power (kW)")
    demand_forecast_m3h: list[float] = Field(
        ..., min_length=24, max_length=24, description="24-hour demand forecast (m³/h)"
    )
    electricity_rates: list[float] = Field(
        ..., min_length=24, max_length=24, description="24-hour electricity rates ($/kWh)"
    )
    optimization_date: date = Field(..., description="Date for optimization")


class EfficiencyAnalysisRequest(BaseModel):
    """Request model for pump efficiency analysis."""

    pump_id: str = Field(..., description="Pump identifier")
    flow_rate_m3h: float = Field(..., gt=0, description="Current flow rate (m³/h)")
    discharge_pressure_m: float = Field(
        ..., gt=0, description="Discharge pressure (meters)"
    )
    suction_pressure_m: float = Field(
        ..., ge=0, description="Suction pressure (meters)"
    )
    power_consumption_kw: float = Field(
        ..., gt=0, description="Power consumption (kW)"
    )
    rated_efficiency: float = Field(
        default=0.75, gt=0, le=1, description="Rated pump efficiency"
    )


class CostAnalysisRequest(BaseModel):
    """Request model for energy cost analysis."""

    period_start: date = Field(..., description="Analysis period start")
    period_end: date = Field(..., description="Analysis period end")
    pump_ids: list[str] = Field(
        default=[], description="Specific pumps to analyze (empty = all)"
    )


# Endpoints
@router.post("/optimize-schedule", response_model=PumpSchedule)
async def optimize_pump_schedule_endpoint(
    request: PumpScheduleRequest,
    current_user: CurrentUser,
) -> PumpSchedule:
    """
    Optimize pump scheduling for minimum energy cost.

    Uses time-of-use electricity rates and demand forecasts to
    minimize pumping costs while maintaining adequate storage levels.
    Target: 15-30% energy cost reduction.
    """
    optimization_request = ScheduleOptimizationRequest(
        pump_id=request.pump_id,
        tank_capacity_m3=request.tank_capacity_m3,
        tank_current_level_m3=request.tank_current_level_m3,
        tank_min_level_m3=request.tank_min_level_m3,
        pump_flow_rate_m3h=request.pump_flow_rate_m3h,
        pump_power_kw=request.pump_power_kw,
        demand_forecast_m3h=request.demand_forecast_m3h,
        electricity_rates=request.electricity_rates,
        optimization_date=request.optimization_date,
    )
    return optimize_pump_schedule(optimization_request)


@router.post("/efficiency-analysis", response_model=EfficiencyReport)
async def analyze_efficiency_endpoint(
    request: EfficiencyAnalysisRequest,
    current_user: CurrentUser,
) -> EfficiencyReport:
    """
    Analyze pump operating efficiency.

    Compares current wire-to-water efficiency against rated
    efficiency to identify degradation and maintenance needs.
    """
    input_data = PumpEfficiencyInput(
        pump_id=request.pump_id,
        flow_rate_m3h=request.flow_rate_m3h,
        discharge_pressure_m=request.discharge_pressure_m,
        suction_pressure_m=request.suction_pressure_m,
        power_consumption_kw=request.power_consumption_kw,
        rated_efficiency=request.rated_efficiency,
    )
    return analyze_pump_efficiency(input_data)


@router.post("/cost-analysis", response_model=CostAnalysis)
async def analyze_costs_endpoint(
    request: CostAnalysisRequest,
    current_user: CurrentUser,
) -> CostAnalysis:
    """
    Analyze energy costs for pumping operations.

    Breaks down costs by time-of-use periods, identifies
    optimization opportunities, and tracks cost trends.
    """
    input_data = EnergyCostInput(
        period_start=request.period_start,
        period_end=request.period_end,
        pump_ids=request.pump_ids,
    )
    return analyze_energy_costs(input_data)


@router.get("/summary")
async def get_energy_summary(
    current_user: CurrentUser,
    period_days: Annotated[int, Query(ge=7, le=365)] = 30,
) -> dict:
    """
    Get energy management summary for the dashboard.

    Returns key metrics including total costs, efficiency ratings,
    and optimization opportunities.
    """
    # TODO: Implement database queries for historical data
    return {
        "period_days": period_days,
        "total_energy_kwh": 45000.0,
        "total_cost_usd": 5400.0,
        "average_efficiency": 0.68,
        "peak_demand_kw": 125.0,
        "off_peak_usage_percentage": 42.0,
        "potential_savings_usd": 810.0,
        "savings_percentage": 15.0,
    }


@router.get("/pumps")
async def list_pumps(
    current_user: CurrentUser,
) -> list[dict]:
    """List all pumps in the system with current status."""
    # TODO: Implement database queries
    return [
        {
            "pump_id": "PUMP-001",
            "name": "Main Well Pump",
            "status": "running",
            "current_efficiency": 0.72,
            "runtime_hours_today": 8.5,
        },
        {
            "pump_id": "PUMP-002",
            "name": "Booster Station A",
            "status": "idle",
            "current_efficiency": 0.65,
            "runtime_hours_today": 3.2,
        },
    ]

