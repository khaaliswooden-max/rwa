"""Data Ingestion API endpoints."""

from datetime import datetime
from typing import Annotated, Literal

from fastapi import APIRouter, File, Query, UploadFile
from pydantic import BaseModel, Field

from api.auth import CurrentUser

router = APIRouter()


# Models
class ManualReadingInput(BaseModel):
    """Manual meter reading input."""

    meter_id: str = Field(..., description="Meter identifier")
    reading_value: float = Field(..., ge=0, description="Meter reading value")
    reading_date: datetime = Field(..., description="Date/time of reading")
    reading_type: Literal["production", "distribution", "customer"] = Field(
        ..., description="Type of meter"
    )
    notes: str = Field(default="", description="Optional notes")


class ManualReadingBatch(BaseModel):
    """Batch of manual readings."""

    readings: list[ManualReadingInput] = Field(
        ..., min_length=1, description="List of readings"
    )
    source: str = Field(default="manual_entry", description="Data source identifier")


class DataSourceConfig(BaseModel):
    """Data source configuration."""

    source_type: Literal["scada", "ami", "manual", "csv"] = Field(
        ..., description="Type of data source"
    )
    name: str = Field(..., description="Source name")
    enabled: bool = Field(default=True, description="Is source active")
    connection_string: str | None = Field(
        default=None, description="Connection details"
    )
    polling_interval_minutes: int = Field(
        default=15, ge=1, le=1440, description="Polling interval"
    )


class IngestionResult(BaseModel):
    """Result of data ingestion operation."""

    success: bool
    records_processed: int
    records_failed: int
    errors: list[str]
    timestamp: datetime


# Endpoints
@router.post("/manual-reading", response_model=IngestionResult)
async def submit_manual_reading(
    reading: ManualReadingInput,
    current_user: CurrentUser,
) -> IngestionResult:
    """
    Submit a single manual meter reading.

    For operators entering individual readings from field visits
    or meter checks.
    """
    # TODO: Implement database persistence
    return IngestionResult(
        success=True,
        records_processed=1,
        records_failed=0,
        errors=[],
        timestamp=datetime.now(),
    )


@router.post("/manual-readings/batch", response_model=IngestionResult)
async def submit_manual_readings_batch(
    batch: ManualReadingBatch,
    current_user: CurrentUser,
) -> IngestionResult:
    """
    Submit multiple manual meter readings at once.

    For batch entry of readings collected during meter
    reading routes.
    """
    # TODO: Implement database persistence
    return IngestionResult(
        success=True,
        records_processed=len(batch.readings),
        records_failed=0,
        errors=[],
        timestamp=datetime.now(),
    )


@router.post("/upload/csv", response_model=IngestionResult)
async def upload_csv_data(
    current_user: CurrentUser,
    file: UploadFile = File(..., description="CSV file with meter readings"),
    data_type: Annotated[
        Literal["meter_readings", "production", "billing"],
        Query(description="Type of data in the CSV"),
    ] = "meter_readings",
) -> IngestionResult:
    """
    Upload CSV file with meter readings or other data.

    Supports standard CSV formats for meter readings,
    production data, and billing exports.
    """
    if not file.filename or not file.filename.endswith(".csv"):
        return IngestionResult(
            success=False,
            records_processed=0,
            records_failed=0,
            errors=["File must be a CSV"],
            timestamp=datetime.now(),
        )

    # TODO: Implement CSV parsing and database persistence
    return IngestionResult(
        success=True,
        records_processed=0,  # Would be actual count
        records_failed=0,
        errors=[],
        timestamp=datetime.now(),
    )


@router.get("/sources")
async def list_data_sources(
    current_user: CurrentUser,
) -> list[dict]:
    """
    List configured data sources and their status.

    Shows all connected SCADA systems, AMI integrations,
    and manual entry configurations.
    """
    # TODO: Implement database queries
    return [
        {
            "id": "SRC-001",
            "type": "manual",
            "name": "Manual Entry",
            "enabled": True,
            "status": "active",
            "last_data": datetime.now().isoformat(),
        },
        {
            "id": "SRC-002",
            "type": "scada",
            "name": "Well House SCADA",
            "enabled": True,
            "status": "connected",
            "last_data": datetime.now().isoformat(),
        },
    ]


@router.post("/sources", response_model=dict)
async def configure_data_source(
    config: DataSourceConfig,
    current_user: CurrentUser,
) -> dict:
    """
    Configure a new data source.

    Set up connections to SCADA systems, AMI providers,
    or other data sources.
    """
    # TODO: Implement configuration persistence
    return {
        "id": "SRC-" + datetime.now().strftime("%Y%m%d%H%M%S"),
        "type": config.source_type,
        "name": config.name,
        "enabled": config.enabled,
        "status": "configured",
        "created_at": datetime.now().isoformat(),
    }


@router.get("/status")
async def get_ingestion_status(
    current_user: CurrentUser,
) -> dict:
    """
    Get overall data ingestion status.

    Shows recent ingestion activity, any errors, and
    data freshness metrics.
    """
    return {
        "status": "healthy",
        "active_sources": 2,
        "records_today": 1450,
        "last_ingestion": datetime.now().isoformat(),
        "errors_last_24h": 0,
        "data_freshness": {
            "production_meters": "5 minutes ago",
            "customer_meters": "Monthly - due in 15 days",
            "scada": "Real-time",
        },
    }


@router.get("/history")
async def get_ingestion_history(
    current_user: CurrentUser,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    source_type: Annotated[str | None, Query()] = None,
) -> list[dict]:
    """
    Get recent data ingestion history.

    Shows log of recent data imports with status and
    record counts.
    """
    # TODO: Implement database queries
    return [
        {
            "id": "ING-001",
            "source": "SCADA",
            "timestamp": datetime.now().isoformat(),
            "records": 48,
            "status": "success",
        },
        {
            "id": "ING-002",
            "source": "Manual Entry",
            "timestamp": datetime.now().isoformat(),
            "records": 1,
            "status": "success",
        },
    ]
