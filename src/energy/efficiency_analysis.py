"""Pump Efficiency Analysis.

Monitors and analyzes pump operating efficiency to identify
degradation, maintenance needs, and optimization opportunities.

Key metrics:
- Wire-to-water efficiency
- Specific energy consumption
- Efficiency degradation trends
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, computed_field

# Physical constants
WATER_DENSITY = 1000  # kg/m³
GRAVITY = 9.81  # m/s²


class PumpEfficiencyInput(BaseModel):
    """Input parameters for pump efficiency calculation."""

    pump_id: str = Field(..., description="Pump identifier")
    flow_rate_m3h: float = Field(..., gt=0, description="Flow rate (m³/h)")
    discharge_pressure_m: float = Field(
        ..., gt=0, description="Discharge pressure head (m)"
    )
    suction_pressure_m: float = Field(
        ..., ge=0, description="Suction pressure head (m)"
    )
    power_consumption_kw: float = Field(
        ..., gt=0, description="Electrical power consumption (kW)"
    )
    rated_efficiency: float = Field(
        default=0.75, gt=0, le=1, description="Manufacturer rated efficiency"
    )


class EfficiencyReport(BaseModel):
    """Pump efficiency analysis report."""

    pump_id: str = Field(..., description="Pump identifier")
    analysis_timestamp: datetime = Field(
        default_factory=datetime.now, description="Analysis timestamp"
    )

    # Operating conditions
    flow_rate_m3h: float = Field(..., description="Flow rate (m³/h)")
    total_head_m: float = Field(..., description="Total dynamic head (m)")
    power_consumption_kw: float = Field(..., description="Power consumption (kW)")

    # Efficiency metrics
    hydraulic_power_kw: float = Field(..., description="Hydraulic (water) power (kW)")
    wire_to_water_efficiency: float = Field(
        ..., description="Overall wire-to-water efficiency (0-1)"
    )
    rated_efficiency: float = Field(..., description="Rated efficiency (0-1)")

    @computed_field
    @property
    def efficiency_percentage(self) -> float:
        """Wire-to-water efficiency as percentage."""
        return round(self.wire_to_water_efficiency * 100, 1)

    @computed_field
    @property
    def efficiency_ratio(self) -> float:
        """Ratio of actual to rated efficiency."""
        if self.rated_efficiency == 0:
            return 0.0
        return round(self.wire_to_water_efficiency / self.rated_efficiency, 3)

    # Specific energy
    specific_energy_kwh_m3: float = Field(..., description="Specific energy (kWh/m³)")

    # Assessment
    efficiency_rating: Literal["excellent", "good", "fair", "poor"] = Field(
        ..., description="Efficiency rating"
    )
    degradation_percentage: float = Field(
        ..., description="Efficiency degradation from rated (%)"
    )

    # Recommendations
    maintenance_recommended: bool = Field(
        ..., description="Whether maintenance is recommended"
    )
    recommendations: list[str] = Field(
        default_factory=list, description="Specific recommendations"
    )


def analyze_pump_efficiency(input_data: PumpEfficiencyInput) -> EfficiencyReport:
    """
    Analyze pump operating efficiency.

    Wire-to-water efficiency is calculated as:
    η = (ρ × g × Q × H) / (P × 1000)

    Where:
    - ρ = water density (kg/m³)
    - g = gravitational acceleration (m/s²)
    - Q = flow rate (m³/s)
    - H = total head (m)
    - P = electrical power (kW)

    Args:
        input_data: Pump operating parameters

    Returns:
        EfficiencyReport with analysis and recommendations
    """
    # Calculate total dynamic head
    total_head = input_data.discharge_pressure_m - input_data.suction_pressure_m

    # Convert flow rate to m³/s
    flow_rate_m3s = input_data.flow_rate_m3h / 3600

    # Calculate hydraulic (water) power
    # P_hydraulic = ρ × g × Q × H (in Watts)
    hydraulic_power_w = WATER_DENSITY * GRAVITY * flow_rate_m3s * total_head
    hydraulic_power_kw = hydraulic_power_w / 1000

    # Calculate wire-to-water efficiency
    wire_to_water = hydraulic_power_kw / input_data.power_consumption_kw

    # Calculate specific energy (kWh/m³)
    specific_energy = input_data.power_consumption_kw / input_data.flow_rate_m3h

    # Calculate degradation from rated
    degradation = (
        (input_data.rated_efficiency - wire_to_water) / input_data.rated_efficiency
    ) * 100

    # Determine efficiency rating
    efficiency_ratio = wire_to_water / input_data.rated_efficiency
    if efficiency_ratio >= 0.95:
        rating = "excellent"
    elif efficiency_ratio >= 0.85:
        rating = "good"
    elif efficiency_ratio >= 0.70:
        rating = "fair"
    else:
        rating = "poor"

    # Determine if maintenance is needed
    maintenance_needed = efficiency_ratio < 0.80 or degradation > 15

    # Generate recommendations
    recommendations = generate_efficiency_recommendations(
        wire_to_water,
        input_data.rated_efficiency,
        efficiency_ratio,
        degradation,
        specific_energy,
    )

    return EfficiencyReport(
        pump_id=input_data.pump_id,
        flow_rate_m3h=input_data.flow_rate_m3h,
        total_head_m=round(total_head, 2),
        power_consumption_kw=input_data.power_consumption_kw,
        hydraulic_power_kw=round(hydraulic_power_kw, 2),
        wire_to_water_efficiency=round(wire_to_water, 3),
        rated_efficiency=input_data.rated_efficiency,
        specific_energy_kwh_m3=round(specific_energy, 3),
        efficiency_rating=rating,
        degradation_percentage=round(degradation, 1),
        maintenance_recommended=maintenance_needed,
        recommendations=recommendations,
    )


def generate_efficiency_recommendations(
    actual_efficiency: float,
    rated_efficiency: float,
    efficiency_ratio: float,
    degradation: float,
    specific_energy: float,
) -> list[str]:
    """Generate specific recommendations based on efficiency analysis."""
    recommendations = []

    if efficiency_ratio < 0.70:
        recommendations.append(
            "CRITICAL: Efficiency below 70% of rated - pump rebuild or "
            "replacement should be evaluated"
        )
    elif efficiency_ratio < 0.80:
        recommendations.append(
            "Significant efficiency loss detected - schedule maintenance "
            "inspection within 30 days"
        )
    elif efficiency_ratio < 0.90:
        recommendations.append(
            "Minor efficiency degradation - monitor trend and include in "
            "next scheduled maintenance"
        )

    if degradation > 20:
        recommendations.append(
            "Check for worn impeller, excessive clearances, or "
            "mechanical seal issues"
        )

    if specific_energy > 0.5:
        recommendations.append(
            f"Specific energy of {specific_energy:.3f} kWh/m³ is high - "
            "verify pump is properly sized for current operating conditions"
        )

    if actual_efficiency < 0.5:
        recommendations.append(
            "Operating efficiency below 50% - consider VFD installation "
            "or pump resizing"
        )

    if not recommendations:
        recommendations.append(
            "Pump operating within acceptable parameters - continue "
            "routine monitoring"
        )

    return recommendations


def calculate_energy_savings_potential(
    current_efficiency: float,
    target_efficiency: float,
    annual_energy_kwh: float,
    electricity_rate: float,
) -> dict:
    """
    Calculate potential energy and cost savings from efficiency improvement.

    Args:
        current_efficiency: Current wire-to-water efficiency
        target_efficiency: Target efficiency after improvement
        annual_energy_kwh: Current annual energy consumption
        electricity_rate: Average electricity rate ($/kWh)

    Returns:
        Dictionary with savings analysis
    """
    if current_efficiency >= target_efficiency:
        return {
            "current_efficiency": current_efficiency,
            "target_efficiency": target_efficiency,
            "energy_savings_kwh": 0,
            "cost_savings_annual": 0,
            "message": "Current efficiency meets or exceeds target",
        }

    # Energy savings = current_energy × (1 - current/target)
    efficiency_improvement_factor = 1 - (current_efficiency / target_efficiency)
    energy_savings = annual_energy_kwh * efficiency_improvement_factor
    cost_savings = energy_savings * electricity_rate

    return {
        "current_efficiency": round(current_efficiency, 3),
        "target_efficiency": round(target_efficiency, 3),
        "efficiency_improvement": round(
            (target_efficiency - current_efficiency) * 100, 1
        ),
        "energy_savings_kwh": round(energy_savings, 0),
        "cost_savings_annual": round(cost_savings, 2),
        "payback_note": "Compare savings against maintenance/upgrade cost for payback",
    }
