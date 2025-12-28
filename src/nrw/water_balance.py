"""IWA Water Balance Calculations.

Implements the International Water Association (IWA) standard water balance
methodology for quantifying Non-Revenue Water (NRW) and its components.

Reference: IWA Water Loss Task Force methodology
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, computed_field


class WaterBalanceInput(BaseModel):
    """Input parameters for water balance calculation."""

    # System Input Volume
    system_input_volume: float = Field(
        ..., gt=0, description="Total volume entering the system (m³)"
    )

    # Authorized Consumption - Billed
    billed_metered_consumption: float = Field(
        ..., ge=0, description="Billed metered consumption (m³)"
    )
    billed_unmetered_consumption: float = Field(
        default=0, ge=0, description="Billed unmetered consumption (m³)"
    )

    # Authorized Consumption - Unbilled
    unbilled_metered_consumption: float = Field(
        default=0, ge=0, description="Unbilled metered consumption (m³)"
    )
    unbilled_unmetered_consumption: float = Field(
        default=0, ge=0, description="Unbilled unmetered consumption (m³)"
    )

    # Apparent Losses (estimates)
    unauthorized_consumption: float = Field(
        default=0, ge=0, description="Estimated unauthorized consumption/theft (m³)"
    )
    meter_inaccuracies: float = Field(
        default=0, ge=0, description="Estimated meter under-registration (m³)"
    )

    # Period
    period_start: date = Field(..., description="Balance period start date")
    period_end: date = Field(..., description="Balance period end date")


class WaterBalance(BaseModel):
    """IWA-standard water balance result."""

    # Input
    system_input_volume: float = Field(
        ..., description="Total system input volume (m³)"
    )

    # Authorized Consumption
    billed_authorized_consumption: float = Field(
        ..., description="Total billed authorized consumption (m³)"
    )
    unbilled_authorized_consumption: float = Field(
        ..., description="Total unbilled authorized consumption (m³)"
    )

    @computed_field
    @property
    def authorized_consumption(self) -> float:
        """Total authorized consumption (m³)."""
        return self.billed_authorized_consumption + self.unbilled_authorized_consumption

    # Water Losses
    apparent_losses: float = Field(
        ..., description="Total apparent losses (m³)"
    )
    real_losses: float = Field(
        ..., description="Total real losses (m³)"
    )

    @computed_field
    @property
    def water_losses(self) -> float:
        """Total water losses (m³)."""
        return self.apparent_losses + self.real_losses

    # Revenue Water
    @computed_field
    @property
    def revenue_water(self) -> float:
        """Revenue water = billed authorized consumption (m³)."""
        return self.billed_authorized_consumption

    # Non-Revenue Water
    @computed_field
    @property
    def non_revenue_water(self) -> float:
        """Non-revenue water (m³)."""
        return self.system_input_volume - self.revenue_water

    # Percentages
    @computed_field
    @property
    def nrw_percentage(self) -> float:
        """NRW as percentage of system input."""
        if self.system_input_volume == 0:
            return 0.0
        return round((self.non_revenue_water / self.system_input_volume) * 100, 2)

    @computed_field
    @property
    def real_losses_percentage(self) -> float:
        """Real losses as percentage of system input."""
        if self.system_input_volume == 0:
            return 0.0
        return round((self.real_losses / self.system_input_volume) * 100, 2)

    @computed_field
    @property
    def apparent_losses_percentage(self) -> float:
        """Apparent losses as percentage of system input."""
        if self.system_input_volume == 0:
            return 0.0
        return round((self.apparent_losses / self.system_input_volume) * 100, 2)

    # Period
    period_start: date
    period_end: date
    period_days: int


def calculate_water_balance(input_data: WaterBalanceInput) -> WaterBalance:
    """
    Calculate IWA-standard water balance.

    The water balance follows this hierarchy:
    
    System Input Volume
    ├── Authorized Consumption
    │   ├── Billed Authorized Consumption (Revenue Water)
    │   │   ├── Billed Metered Consumption
    │   │   └── Billed Unmetered Consumption
    │   └── Unbilled Authorized Consumption
    │       ├── Unbilled Metered Consumption
    │       └── Unbilled Unmetered Consumption
    └── Water Losses (Non-Revenue Water - Unbilled Auth. Consumption)
        ├── Apparent Losses
        │   ├── Unauthorized Consumption
        │   └── Meter Inaccuracies
        └── Real Losses (calculated as remainder)

    Args:
        input_data: Water balance input parameters

    Returns:
        WaterBalance with all calculated components
    """
    # Calculate authorized consumption components
    billed_authorized = (
        input_data.billed_metered_consumption
        + input_data.billed_unmetered_consumption
    )
    unbilled_authorized = (
        input_data.unbilled_metered_consumption
        + input_data.unbilled_unmetered_consumption
    )

    # Calculate apparent losses
    apparent_losses = (
        input_data.unauthorized_consumption + input_data.meter_inaccuracies
    )

    # Calculate real losses as the remainder
    # Real Losses = System Input - Authorized Consumption - Apparent Losses
    total_authorized = billed_authorized + unbilled_authorized
    real_losses = max(
        0, input_data.system_input_volume - total_authorized - apparent_losses
    )

    # Calculate period days
    period_days = (input_data.period_end - input_data.period_start).days + 1

    return WaterBalance(
        system_input_volume=input_data.system_input_volume,
        billed_authorized_consumption=billed_authorized,
        unbilled_authorized_consumption=unbilled_authorized,
        apparent_losses=apparent_losses,
        real_losses=real_losses,
        period_start=input_data.period_start,
        period_end=input_data.period_end,
        period_days=period_days,
    )


@dataclass
class InfrastructureLeakageIndex:
    """
    Infrastructure Leakage Index (ILI) calculation.

    ILI = Current Annual Real Losses (CARL) / Unavoidable Annual Real Losses (UARL)

    ILI benchmarks:
    - < 2.0: Excellent (world-class)
    - 2.0 - 4.0: Good
    - 4.0 - 8.0: Average
    - > 8.0: Poor
    """

    current_annual_real_losses: float  # m³/year
    unavoidable_annual_real_losses: float  # m³/year

    @property
    def ili(self) -> float:
        """Calculate ILI value."""
        if self.unavoidable_annual_real_losses == 0:
            return float("inf")
        return self.current_annual_real_losses / self.unavoidable_annual_real_losses

    @property
    def rating(self) -> str:
        """Get ILI performance rating."""
        ili = self.ili
        if ili < 2.0:
            return "excellent"
        elif ili < 4.0:
            return "good"
        elif ili < 8.0:
            return "average"
        else:
            return "poor"


def calculate_uarl(
    mains_length_km: float,
    service_connections: int,
    service_connection_length_m: float,
    average_pressure_m: float,
) -> float:
    """
    Calculate Unavoidable Annual Real Losses (UARL).

    UARL = (18 × Lm + 0.8 × Nc + 25 × Lp) × P

    Where:
    - Lm = mains length in km
    - Nc = number of service connections
    - Lp = total length of service connections in km
    - P = average operating pressure in meters

    Args:
        mains_length_km: Length of distribution mains (km)
        service_connections: Number of service connections
        service_connection_length_m: Average length of service connection (m)
        average_pressure_m: Average operating pressure (m)

    Returns:
        UARL in liters per day
    """
    # Convert service connection length to km
    total_service_length_km = (
        service_connections * service_connection_length_m / 1000
    )

    # UARL formula (liters/day)
    uarl = (
        (18 * mains_length_km)
        + (0.8 * service_connections)
        + (25 * total_service_length_km)
    ) * average_pressure_m

    return uarl

