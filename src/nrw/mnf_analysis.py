"""Minimum Night Flow (MNF) Analysis.

MNF analysis identifies the period of lowest flow (typically 2-4 AM)
when legitimate consumption is minimal. The flow during this period
represents background leakage plus legitimate night use.

MNF Components:
- Background leakage (unreported breaks, joint leaks)
- Legitimate night use (estimated at 1-6 L/connection/hour)
- Exceptional night use (industry, etc.)
"""

from dataclasses import dataclass
from datetime import datetime, time
from typing import Optional

from pydantic import BaseModel, Field, computed_field


class MNFResult(BaseModel):
    """Results of Minimum Night Flow analysis."""

    # MNF values
    minimum_flow_m3h: float = Field(..., description="Minimum flow rate (m³/h)")
    mnf_hour: int = Field(..., ge=0, le=23, description="Hour of minimum flow (0-23)")
    average_night_flow_m3h: float = Field(
        ..., description="Average flow during night window (m³/h)"
    )

    # Leakage estimates
    estimated_legitimate_night_use_m3h: float = Field(
        ..., description="Estimated legitimate night use (m³/h)"
    )
    estimated_background_leakage_m3h: float = Field(
        ..., description="Estimated background leakage (m³/h)"
    )

    # Daily extrapolation
    estimated_daily_leakage_m3: float = Field(
        ..., description="Estimated daily leakage volume (m³)"
    )

    # Context
    service_connections: int = Field(..., description="Number of service connections")
    average_pressure_m: float = Field(..., description="Average system pressure (m)")

    # Quality indicators
    night_day_ratio: float = Field(..., description="Ratio of night flow to day flow")
    confidence: str = Field(..., description="Confidence level of estimate")

    @computed_field
    @property
    def leakage_per_connection_lph(self) -> float:
        """Leakage per connection (liters per hour)."""
        if self.service_connections == 0:
            return 0.0
        return round(
            (self.estimated_background_leakage_m3h * 1000) / self.service_connections,
            2,
        )

    @computed_field
    @property
    def annual_leakage_estimate_m3(self) -> float:
        """Estimated annual leakage volume (m³)."""
        return round(self.estimated_daily_leakage_m3 * 365, 0)


# Night window constants
NIGHT_START_HOUR = 1  # 1 AM
NIGHT_END_HOUR = 5  # 5 AM (exclusive)
MNF_WINDOW_START = 2  # 2 AM
MNF_WINDOW_END = 4  # 4 AM

# Legitimate night use estimates (liters/connection/hour)
LEGITIMATE_NIGHT_USE_MIN = 1.0
LEGITIMATE_NIGHT_USE_MAX = 6.0
LEGITIMATE_NIGHT_USE_DEFAULT = 3.0


def analyze_minimum_night_flow(
    hourly_flows: list[float],
    service_connections: int,
    average_pressure: float = 40.0,
    legitimate_night_use_lph: float = LEGITIMATE_NIGHT_USE_DEFAULT,
) -> MNFResult:
    """
    Analyze hourly flow data to estimate background leakage.

    The analysis:
    1. Identifies the minimum flow period (typically 2-4 AM)
    2. Estimates legitimate night use
    3. Calculates background leakage as MNF minus legitimate use
    4. Extrapolates to daily/annual volumes

    Args:
        hourly_flows: Hourly flow readings (m³/h), 24+ values
                     Index 0 = midnight, Index 1 = 1 AM, etc.
        service_connections: Number of service connections
        average_pressure: Average system pressure (meters)
        legitimate_night_use_lph: Estimated legitimate use per connection (L/h)

    Returns:
        MNFResult with leakage estimates and confidence indicators
    """
    # Ensure we have at least 24 hours of data
    if len(hourly_flows) < 24:
        raise ValueError("At least 24 hourly flow readings required")

    # Use first 24 hours if more data provided (could enhance to use multiple days)
    flows = hourly_flows[:24]

    # Find MNF in the typical window (2-4 AM)
    mnf_window_flows = flows[MNF_WINDOW_START:MNF_WINDOW_END]
    minimum_flow = min(mnf_window_flows)
    mnf_hour = MNF_WINDOW_START + mnf_window_flows.index(minimum_flow)

    # Calculate average night flow (1-5 AM)
    night_flows = flows[NIGHT_START_HOUR:NIGHT_END_HOUR]
    average_night_flow = sum(night_flows) / len(night_flows)

    # Calculate average day flow for comparison
    day_flows = flows[6:22]  # 6 AM to 10 PM
    average_day_flow = sum(day_flows) / len(day_flows)
    night_day_ratio = (
        average_night_flow / average_day_flow if average_day_flow > 0 else 1.0
    )

    # Estimate legitimate night use
    # Convert from L/h to m³/h per connection, then multiply by connections
    legitimate_use_m3h = legitimate_night_use_lph * service_connections / 1000

    # Background leakage = MNF - legitimate use
    background_leakage = max(0, minimum_flow - legitimate_use_m3h)

    # Night-day factor for extrapolation
    # Leakage varies with pressure, which typically varies throughout day
    # Simple approach: assume night leakage represents ~80% of average daily rate
    night_day_factor = 1.25  # Adjust based on pressure profile if available

    # Daily leakage estimate
    daily_leakage = background_leakage * 24 * night_day_factor

    # Determine confidence level
    confidence = assess_confidence(
        minimum_flow,
        average_night_flow,
        night_day_ratio,
        service_connections,
    )

    return MNFResult(
        minimum_flow_m3h=round(minimum_flow, 3),
        mnf_hour=mnf_hour,
        average_night_flow_m3h=round(average_night_flow, 3),
        estimated_legitimate_night_use_m3h=round(legitimate_use_m3h, 3),
        estimated_background_leakage_m3h=round(background_leakage, 3),
        estimated_daily_leakage_m3=round(daily_leakage, 2),
        service_connections=service_connections,
        average_pressure_m=average_pressure,
        night_day_ratio=round(night_day_ratio, 3),
        confidence=confidence,
    )


def assess_confidence(
    minimum_flow: float,
    average_night_flow: float,
    night_day_ratio: float,
    service_connections: int,
) -> str:
    """
    Assess confidence in MNF analysis results.

    Factors that reduce confidence:
    - Very small systems (fewer samples/connections)
    - High night/day ratio (possible night consumers)
    - Large variance between MNF and average night flow
    """
    # Start with high confidence
    score = 100

    # Small systems have less reliable MNF
    if service_connections < 200:
        score -= 15
    elif service_connections < 500:
        score -= 5

    # High night/day ratio suggests industrial/commercial night use
    if night_day_ratio > 0.4:
        score -= 20
    elif night_day_ratio > 0.3:
        score -= 10

    # Large difference between MNF and average night flow
    # suggests unusual activity or meter issues
    variance = (
        abs(average_night_flow - minimum_flow) / minimum_flow if minimum_flow > 0 else 0
    )
    if variance > 0.3:
        score -= 15
    elif variance > 0.2:
        score -= 5

    # Convert score to confidence level
    if score >= 80:
        return "high"
    elif score >= 60:
        return "medium"
    else:
        return "low"


def calculate_component_analysis(
    mnf_m3h: float,
    service_connections: int,
    known_night_users: list[dict] | None = None,
) -> dict:
    """
    Detailed component analysis of night flow.

    Breaks down MNF into:
    - Domestic night use
    - Known exceptional users
    - Background leakage
    - Unreported breaks estimate

    Args:
        mnf_m3h: Measured minimum night flow (m³/h)
        service_connections: Total service connections
        known_night_users: List of known night users with estimated flow

    Returns:
        Dictionary with component breakdown
    """
    # Domestic night use estimate
    domestic_use_m3h = service_connections * LEGITIMATE_NIGHT_USE_DEFAULT / 1000

    # Known exceptional users
    exceptional_use_m3h = 0.0
    if known_night_users:
        exceptional_use_m3h = sum(
            user.get("estimated_flow_m3h", 0) for user in known_night_users
        )

    # Background leakage (remainder)
    background_leakage_m3h = max(0, mnf_m3h - domestic_use_m3h - exceptional_use_m3h)

    return {
        "mnf_m3h": round(mnf_m3h, 3),
        "components": {
            "domestic_night_use_m3h": round(domestic_use_m3h, 3),
            "exceptional_users_m3h": round(exceptional_use_m3h, 3),
            "background_leakage_m3h": round(background_leakage_m3h, 3),
        },
        "percentages": {
            "domestic": (
                round(domestic_use_m3h / mnf_m3h * 100, 1) if mnf_m3h > 0 else 0
            ),
            "exceptional": (
                round(exceptional_use_m3h / mnf_m3h * 100, 1) if mnf_m3h > 0 else 0
            ),
            "leakage": (
                round(background_leakage_m3h / mnf_m3h * 100, 1) if mnf_m3h > 0 else 0
            ),
        },
    }
