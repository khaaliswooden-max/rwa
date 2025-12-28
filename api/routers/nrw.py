"""Non-Revenue Water (NRW) API endpoints."""

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field

from api.auth import CurrentUser
from src.nrw.water_balance import WaterBalance, WaterBalanceInput, calculate_water_balance
from src.nrw.leak_detection import LeakAnalysis, analyze_leak_indicators
from src.nrw.mnf_analysis import MNFResult, analyze_minimum_night_flow

router = APIRouter()


# Request/Response Models
class WaterBalanceRequest(BaseModel):
    """Request model for water balance calculation."""

    system_input_volume: float = Field(
        ..., gt=0, description="Total system input volume (cubic meters)"
    )
    billed_metered_consumption: float = Field(
        ..., ge=0, description="Billed metered consumption (cubic meters)"
    )
    billed_unmetered_consumption: float = Field(
        default=0, ge=0, description="Billed unmetered consumption (cubic meters)"
    )
    unbilled_metered_consumption: float = Field(
        default=0, ge=0, description="Unbilled metered consumption (cubic meters)"
    )
    unbilled_unmetered_consumption: float = Field(
        default=0, ge=0, description="Unbilled unmetered consumption (cubic meters)"
    )
    unauthorized_consumption: float = Field(
        default=0, ge=0, description="Estimated unauthorized consumption (cubic meters)"
    )
    meter_inaccuracies: float = Field(
        default=0, ge=0, description="Estimated meter inaccuracies (cubic meters)"
    )
    period_start: date = Field(..., description="Period start date")
    period_end: date = Field(..., description="Period end date")


class MNFRequest(BaseModel):
    """Request model for MNF analysis."""

    hourly_flows: list[float] = Field(
        ..., min_length=24, max_length=168, description="Hourly flow readings (m³/h)"
    )
    service_connections: int = Field(..., gt=0, description="Number of service connections")
    average_pressure: float = Field(
        default=40.0, ge=0, description="Average system pressure (meters)"
    )


class LeakIndicatorRequest(BaseModel):
    """Request model for leak detection analysis."""

    zone_id: str = Field(..., description="Distribution zone identifier")
    mnf_values: list[float] = Field(
        ..., min_length=7, description="Recent MNF values (m³/h)"
    )
    system_pressure: float = Field(..., ge=0, description="System pressure (meters)")
    pipe_length_km: float = Field(..., gt=0, description="Total pipe length in km")
    service_connections: int = Field(..., gt=0, description="Number of connections")


# Endpoints
@router.post("/water-balance", response_model=WaterBalance)
async def calculate_water_balance_endpoint(
    request: WaterBalanceRequest,
    current_user: CurrentUser,
) -> WaterBalance:
    """
    Calculate IWA-standard water balance for a given period.

    The water balance follows the International Water Association (IWA)
    methodology, breaking down system input into authorized consumption,
    apparent losses, and real losses.
    """
    input_data = WaterBalanceInput(
        system_input_volume=request.system_input_volume,
        billed_metered_consumption=request.billed_metered_consumption,
        billed_unmetered_consumption=request.billed_unmetered_consumption,
        unbilled_metered_consumption=request.unbilled_metered_consumption,
        unbilled_unmetered_consumption=request.unbilled_unmetered_consumption,
        unauthorized_consumption=request.unauthorized_consumption,
        meter_inaccuracies=request.meter_inaccuracies,
        period_start=request.period_start,
        period_end=request.period_end,
    )
    return calculate_water_balance(input_data)


@router.post("/mnf-analysis", response_model=MNFResult)
async def analyze_mnf_endpoint(
    request: MNFRequest,
    current_user: CurrentUser,
) -> MNFResult:
    """
    Analyze Minimum Night Flow (MNF) to estimate background leakage.

    MNF analysis identifies the lowest flow period (typically 2-4 AM)
    when legitimate consumption is minimal, providing an estimate of
    continuous background leakage.
    """
    return analyze_minimum_night_flow(
        hourly_flows=request.hourly_flows,
        service_connections=request.service_connections,
        average_pressure=request.average_pressure,
    )


@router.post("/leak-indicators", response_model=LeakAnalysis)
async def analyze_leak_indicators_endpoint(
    request: LeakIndicatorRequest,
    current_user: CurrentUser,
) -> LeakAnalysis:
    """
    Analyze leak indicators for a distribution zone.

    Combines MNF trends, Infrastructure Leakage Index (ILI), and
    other metrics to identify zones with high leakage probability.
    """
    return analyze_leak_indicators(
        zone_id=request.zone_id,
        mnf_values=request.mnf_values,
        system_pressure=request.system_pressure,
        pipe_length_km=request.pipe_length_km,
        service_connections=request.service_connections,
    )


@router.get("/summary")
async def get_nrw_summary(
    current_user: CurrentUser,
    period_days: Annotated[int, Query(ge=7, le=365)] = 30,
) -> dict:
    """
    Get NRW summary statistics for the dashboard.

    Returns key performance indicators including NRW percentage,
    Infrastructure Leakage Index (ILI), and trend information.
    """
    # TODO: Implement database queries for historical data
    return {
        "period_days": period_days,
        "nrw_percentage": 22.5,
        "nrw_volume_m3": 4500.0,
        "real_losses_m3": 3200.0,
        "apparent_losses_m3": 1300.0,
        "infrastructure_leakage_index": 2.8,
        "trend": "improving",
        "trend_percentage": -3.2,
    }

