"""Leak Detection Analysis.

Provides analysis tools for identifying and prioritizing leak
detection activities based on available data.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, computed_field


class LeakPriority(str, Enum):
    """Leak detection priority levels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class LeakAnalysis(BaseModel):
    """Results of leak indicator analysis for a zone."""

    zone_id: str = Field(..., description="Distribution zone identifier")
    analysis_timestamp: datetime = Field(
        default_factory=datetime.now, description="When analysis was performed"
    )

    # MNF Metrics
    average_mnf_m3h: float = Field(..., description="Average MNF (m³/h)")
    mnf_trend: Literal["increasing", "stable", "decreasing"] = Field(
        ..., description="MNF trend direction"
    )
    mnf_trend_slope: float = Field(
        ..., description="MNF trend slope (m³/h per day)"
    )

    # Infrastructure metrics
    pipe_length_km: float = Field(..., description="Total pipe length (km)")
    service_connections: int = Field(..., description="Number of connections")
    leakage_rate_m3_km_day: float = Field(
        ..., description="Leakage rate (m³/km/day)"
    )

    # Risk assessment
    infrastructure_leakage_index: float = Field(
        ..., description="ILI value"
    )
    priority: LeakPriority = Field(..., description="Detection priority")
    risk_score: float = Field(
        ..., ge=0, le=100, description="Overall risk score (0-100)"
    )

    # Recommendations
    recommended_actions: list[str] = Field(
        default_factory=list, description="Recommended actions"
    )

    @computed_field
    @property
    def leakage_per_connection_lpd(self) -> float:
        """Leakage per connection (liters per connection per day)."""
        if self.service_connections == 0:
            return 0.0
        daily_leakage_liters = self.average_mnf_m3h * 24 * 1000
        return round(daily_leakage_liters / self.service_connections, 1)


def analyze_leak_indicators(
    zone_id: str,
    mnf_values: list[float],
    system_pressure: float,
    pipe_length_km: float,
    service_connections: int,
) -> LeakAnalysis:
    """
    Analyze leak indicators for a distribution zone.

    Combines multiple metrics to assess leakage levels and
    prioritize detection activities.

    Args:
        zone_id: Identifier for the distribution zone
        mnf_values: Recent MNF readings (m³/h), minimum 7 values
        system_pressure: Average system pressure (meters)
        pipe_length_km: Total pipe length in zone (km)
        service_connections: Number of service connections

    Returns:
        LeakAnalysis with metrics, priority, and recommendations
    """
    # Calculate MNF statistics
    average_mnf = sum(mnf_values) / len(mnf_values)

    # Calculate trend using simple linear regression
    n = len(mnf_values)
    x_mean = (n - 1) / 2
    y_mean = average_mnf

    numerator = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(mnf_values))
    denominator = sum((i - x_mean) ** 2 for i in range(n))

    slope = numerator / denominator if denominator != 0 else 0

    # Determine trend direction
    if slope > 0.01:
        trend = "increasing"
    elif slope < -0.01:
        trend = "decreasing"
    else:
        trend = "stable"

    # Calculate leakage rate per km
    daily_leakage_m3 = average_mnf * 24
    leakage_rate = daily_leakage_m3 / pipe_length_km if pipe_length_km > 0 else 0

    # Estimate ILI (simplified calculation)
    # UARL approximation for small systems
    uarl_lpd = (18 * pipe_length_km + 0.8 * service_connections) * system_pressure
    carl_lpd = average_mnf * 24 * 1000  # Convert m³/h to liters/day

    ili = carl_lpd / uarl_lpd if uarl_lpd > 0 else float("inf")

    # Calculate risk score (0-100)
    risk_score = min(100, calculate_risk_score(ili, trend, slope, leakage_rate))

    # Determine priority
    priority = determine_priority(risk_score, trend)

    # Generate recommendations
    recommendations = generate_recommendations(
        ili, trend, leakage_rate, risk_score
    )

    return LeakAnalysis(
        zone_id=zone_id,
        average_mnf_m3h=round(average_mnf, 3),
        mnf_trend=trend,
        mnf_trend_slope=round(slope, 4),
        pipe_length_km=pipe_length_km,
        service_connections=service_connections,
        leakage_rate_m3_km_day=round(leakage_rate, 2),
        infrastructure_leakage_index=round(ili, 2),
        priority=priority,
        risk_score=round(risk_score, 1),
        recommended_actions=recommendations,
    )


def calculate_risk_score(
    ili: float,
    trend: str,
    slope: float,
    leakage_rate: float,
) -> float:
    """
    Calculate overall risk score based on multiple factors.

    Weights:
    - ILI: 40%
    - Trend: 25%
    - Leakage rate: 35%
    """
    # ILI score (0-100)
    if ili < 2:
        ili_score = 10
    elif ili < 4:
        ili_score = 30
    elif ili < 8:
        ili_score = 60
    else:
        ili_score = min(100, 60 + (ili - 8) * 5)

    # Trend score (0-100)
    if trend == "decreasing":
        trend_score = 10
    elif trend == "stable":
        trend_score = 30
    else:
        # Increasing - score based on slope magnitude
        trend_score = min(100, 50 + abs(slope) * 500)

    # Leakage rate score (0-100)
    # Benchmark: 10 m³/km/day is acceptable, >30 is concerning
    if leakage_rate < 10:
        rate_score = 20
    elif leakage_rate < 20:
        rate_score = 40
    elif leakage_rate < 30:
        rate_score = 60
    else:
        rate_score = min(100, 60 + (leakage_rate - 30) * 2)

    # Weighted average
    return (ili_score * 0.40) + (trend_score * 0.25) + (rate_score * 0.35)


def determine_priority(risk_score: float, trend: str) -> LeakPriority:
    """Determine priority based on risk score and trend."""
    if risk_score >= 75 or (risk_score >= 60 and trend == "increasing"):
        return LeakPriority.CRITICAL
    elif risk_score >= 50:
        return LeakPriority.HIGH
    elif risk_score >= 30:
        return LeakPriority.MEDIUM
    else:
        return LeakPriority.LOW


def generate_recommendations(
    ili: float,
    trend: str,
    leakage_rate: float,
    risk_score: float,
) -> list[str]:
    """Generate actionable recommendations based on analysis."""
    recommendations = []

    if risk_score >= 75:
        recommendations.append(
            "URGENT: Schedule immediate leak detection survey"
        )

    if ili > 8:
        recommendations.append(
            "High ILI indicates significant unreported breaks - "
            "consider acoustic leak detection"
        )
    elif ili > 4:
        recommendations.append(
            "Moderate ILI - systematic leak survey recommended within 30 days"
        )

    if trend == "increasing":
        recommendations.append(
            "Increasing MNF trend suggests developing leaks - "
            "monitor closely and investigate"
        )

    if leakage_rate > 30:
        recommendations.append(
            f"Leakage rate of {leakage_rate:.1f} m³/km/day exceeds "
            "benchmark - prioritize this zone for detection"
        )

    if not recommendations:
        recommendations.append(
            "Continue routine monitoring - no immediate action required"
        )

    return recommendations

