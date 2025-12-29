"""Energy Cost Optimization.

Analyzes energy costs and identifies optimization opportunities
through rate structure analysis, demand management, and
operational adjustments.

Key features:
- Time-of-use rate analysis
- Demand charge optimization
- Power factor correction assessment
- Cost trend tracking
"""

from datetime import date, datetime

from pydantic import BaseModel, Field, computed_field


class EnergyCostInput(BaseModel):
    """Input parameters for energy cost analysis."""

    period_start: date = Field(..., description="Analysis period start")
    period_end: date = Field(..., description="Analysis period end")
    pump_ids: list[str] = Field(
        default_factory=list, description="Pumps to analyze (empty = all)"
    )


class RatePeriodAnalysis(BaseModel):
    """Analysis for a specific rate period."""

    period_name: str = Field(..., description="Rate period name")
    hours_start: int = Field(..., description="Period start hour")
    hours_end: int = Field(..., description="Period end hour")
    rate_per_kwh: float = Field(..., description="Rate ($/kWh)")
    energy_kwh: float = Field(..., description="Energy used in period (kWh)")
    cost: float = Field(..., description="Cost for period ($)")
    percentage_of_total: float = Field(..., description="% of total energy")


class CostAnalysis(BaseModel):
    """Energy cost analysis result."""

    period_start: date = Field(..., description="Analysis period start")
    period_end: date = Field(..., description="Analysis period end")
    analysis_timestamp: datetime = Field(
        default_factory=datetime.now, description="When analysis was performed"
    )

    # Energy summary
    total_energy_kwh: float = Field(..., description="Total energy (kWh)")
    total_cost: float = Field(..., description="Total cost ($)")
    average_rate: float = Field(..., description="Blended average rate ($/kWh)")

    # Time-of-use breakdown
    rate_period_analysis: list[RatePeriodAnalysis] = Field(
        ..., description="Analysis by rate period"
    )

    # Demand charges
    peak_demand_kw: float = Field(..., description="Peak demand (kW)")
    demand_charge: float = Field(..., description="Demand charge ($)")

    # Optimization potential
    optimal_cost_estimate: float = Field(..., description="Estimated optimal cost ($)")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def savings_potential(self) -> float:
        """Potential savings through optimization ($)."""
        return round(self.total_cost - self.optimal_cost_estimate, 2)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def savings_potential_percentage(self) -> float:
        """Potential savings as percentage."""
        if self.total_cost == 0:
            return 0.0
        return round((self.savings_potential / self.total_cost) * 100, 1)

    # Recommendations
    recommendations: list[str] = Field(
        default_factory=list, description="Optimization recommendations"
    )


def analyze_energy_costs(input_data: EnergyCostInput) -> CostAnalysis:
    """
    Analyze energy costs and identify optimization opportunities.

    This is a simplified implementation. In production, this would
    query actual meter data and utility rate schedules.

    Args:
        input_data: Analysis parameters

    Returns:
        CostAnalysis with breakdown and recommendations
    """
    # Calculate period days
    period_days = (input_data.period_end - input_data.period_start).days + 1

    # Simulated data - would come from database in production
    # Typical small water system: 1,000-2,000 kWh/day
    daily_energy = 1500.0
    total_energy = daily_energy * period_days

    # Simulated rate structure (3-tier TOU)
    rate_periods = [
        RatePeriodAnalysis(
            period_name="Off-Peak",
            hours_start=22,
            hours_end=6,
            rate_per_kwh=0.08,
            energy_kwh=total_energy * 0.35,  # 35% during off-peak
            cost=total_energy * 0.35 * 0.08,
            percentage_of_total=35.0,
        ),
        RatePeriodAnalysis(
            period_name="Mid-Peak",
            hours_start=6,
            hours_end=14,
            rate_per_kwh=0.12,
            energy_kwh=total_energy * 0.40,  # 40% during mid-peak
            cost=total_energy * 0.40 * 0.12,
            percentage_of_total=40.0,
        ),
        RatePeriodAnalysis(
            period_name="On-Peak",
            hours_start=14,
            hours_end=22,
            rate_per_kwh=0.18,
            energy_kwh=total_energy * 0.25,  # 25% during on-peak
            cost=total_energy * 0.25 * 0.18,
            percentage_of_total=25.0,
        ),
    ]

    # Calculate totals
    total_cost = sum(rp.cost for rp in rate_periods)
    average_rate = total_cost / total_energy if total_energy > 0 else 0

    # Demand charge simulation
    peak_demand = 75.0  # kW
    demand_charge_rate = 12.0  # $/kW
    demand_charge = peak_demand * demand_charge_rate

    total_cost += demand_charge

    # Calculate optimal cost (shift to off-peak)
    # Assume 60% could run off-peak with good scheduling
    optimal_rate_periods = [
        total_energy * 0.60 * 0.08,  # 60% off-peak
        total_energy * 0.30 * 0.12,  # 30% mid-peak
        total_energy * 0.10 * 0.18,  # 10% on-peak
    ]
    optimal_energy_cost = sum(optimal_rate_periods)

    # Reduced demand charge with better scheduling
    optimal_demand_charge = peak_demand * 0.85 * demand_charge_rate
    optimal_cost = optimal_energy_cost + optimal_demand_charge

    # Generate recommendations
    recommendations = generate_cost_recommendations(
        rate_periods, peak_demand, demand_charge, total_cost - optimal_cost
    )

    return CostAnalysis(
        period_start=input_data.period_start,
        period_end=input_data.period_end,
        total_energy_kwh=round(total_energy, 0),
        total_cost=round(total_cost, 2),
        average_rate=round(average_rate, 4),
        rate_period_analysis=rate_periods,
        peak_demand_kw=peak_demand,
        demand_charge=round(demand_charge, 2),
        optimal_cost_estimate=round(optimal_cost, 2),
        recommendations=recommendations,
    )


def generate_cost_recommendations(
    rate_periods: list[RatePeriodAnalysis],
    peak_demand: float,
    demand_charge: float,
    potential_savings: float,
) -> list[str]:
    """Generate cost optimization recommendations."""
    recommendations = []

    # Analyze TOU distribution
    on_peak_usage = next(
        (rp.percentage_of_total for rp in rate_periods if rp.period_name == "On-Peak"),
        0,
    )
    off_peak_usage = next(
        (rp.percentage_of_total for rp in rate_periods if rp.period_name == "Off-Peak"),
        0,
    )

    if on_peak_usage > 20:
        recommendations.append(
            f"On-peak usage is {on_peak_usage:.0f}% - shift pumping to "
            "off-peak hours (10pm-6am) where possible"
        )

    if off_peak_usage < 50:
        recommendations.append(
            "Increase off-peak pumping by pre-filling storage tanks "
            "during low-rate periods"
        )

    # Demand charge analysis
    if demand_charge > 500:
        recommendations.append(
            f"Demand charges of ${demand_charge:.0f}/month are significant - "
            "consider soft-start equipment or staggered pump starts"
        )

    # Savings potential
    if potential_savings > 100:
        recommendations.append(
            f"Potential monthly savings of ${potential_savings:.0f} through "
            "schedule optimization"
        )

    if not recommendations:
        recommendations.append(
            "Energy usage patterns are reasonably optimized - "
            "continue monitoring for opportunities"
        )

    return recommendations


def calculate_power_factor_impact(
    measured_power_factor: float,
    target_power_factor: float,
    monthly_kwh: float,
    pf_penalty_threshold: float = 0.85,
    pf_penalty_rate: float = 0.01,
) -> dict:
    """
    Calculate impact of power factor on energy costs.

    Many utilities penalize low power factor (typically < 0.85).

    Args:
        measured_power_factor: Current power factor
        target_power_factor: Target after correction
        monthly_kwh: Monthly energy usage
        pf_penalty_threshold: PF below which penalties apply
        pf_penalty_rate: Penalty rate per 0.01 below threshold

    Returns:
        Dictionary with power factor analysis
    """
    current_penalty: float = 0.0
    if measured_power_factor < pf_penalty_threshold:
        pf_shortfall = int((pf_penalty_threshold - measured_power_factor) * 100)
        current_penalty = monthly_kwh * pf_penalty_rate * pf_shortfall

    potential_penalty: float = 0.0
    if target_power_factor < pf_penalty_threshold:
        pf_shortfall = int((pf_penalty_threshold - target_power_factor) * 100)
        potential_penalty = monthly_kwh * pf_penalty_rate * pf_shortfall

    savings = current_penalty - potential_penalty

    return {
        "measured_power_factor": measured_power_factor,
        "target_power_factor": target_power_factor,
        "current_monthly_penalty": round(current_penalty, 2),
        "potential_monthly_penalty": round(potential_penalty, 2),
        "monthly_savings": round(savings, 2),
        "annual_savings": round(savings * 12, 2),
        "correction_needed": measured_power_factor < pf_penalty_threshold,
    }
