"""Compliance Management API endpoints."""

from datetime import date, datetime
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field

from api.auth import CurrentUser
from src.compliance.obligation_tracking import (
    Obligation,
    ObligationStatus,
    get_obligations,
    update_obligation_status,
)
from src.compliance.report_generation import (
    ComplianceReport,
    ReportType,
    generate_report,
)
from src.compliance.risk_scoring import (
    RiskAssessment,
    calculate_compliance_risk,
)

router = APIRouter()


# Request/Response Models
class ObligationCreateRequest(BaseModel):
    """Request model for creating a new obligation."""

    title: str = Field(..., min_length=1, max_length=200, description="Obligation title")
    description: str = Field(default="", description="Detailed description")
    regulation: str = Field(
        ..., description="Regulatory reference (e.g., 'EPA SDWA 40 CFR 141.21')"
    )
    category: str = Field(
        ..., description="Category (e.g., 'Monitoring', 'Reporting', 'Treatment')"
    )
    frequency: str = Field(
        ..., description="Frequency (e.g., 'Monthly', 'Quarterly', 'Annual')"
    )
    due_date: date = Field(..., description="Next due date")
    responsible_party: str = Field(default="", description="Responsible person/role")


class ObligationUpdateRequest(BaseModel):
    """Request model for updating an obligation."""

    status: ObligationStatus = Field(..., description="New status")
    completion_date: date | None = Field(default=None, description="Completion date")
    notes: str = Field(default="", description="Status notes")


class ReportGenerateRequest(BaseModel):
    """Request model for generating a compliance report."""

    report_type: ReportType = Field(..., description="Type of report to generate")
    period_start: date = Field(..., description="Report period start")
    period_end: date = Field(..., description="Report period end")
    include_supporting_data: bool = Field(
        default=True, description="Include supporting data tables"
    )


class RiskAssessmentRequest(BaseModel):
    """Request model for compliance risk assessment."""

    include_categories: list[str] = Field(
        default=[], description="Categories to include (empty = all)"
    )


# Endpoints
@router.get("/obligations", response_model=list[Obligation])
async def list_obligations(
    current_user: CurrentUser,
    status: Annotated[ObligationStatus | None, Query()] = None,
    category: Annotated[str | None, Query()] = None,
    due_within_days: Annotated[int | None, Query(ge=1, le=365)] = None,
) -> list[Obligation]:
    """
    List compliance obligations with optional filtering.

    Filter by status, category, or upcoming due dates to focus
    on the most pressing compliance requirements.
    """
    return get_obligations(
        status=status,
        category=category,
        due_within_days=due_within_days,
    )


@router.post("/obligations", response_model=Obligation)
async def create_obligation(
    request: ObligationCreateRequest,
    current_user: CurrentUser,
) -> Obligation:
    """
    Create a new compliance obligation.

    Track regulatory requirements with due dates, frequencies,
    and responsible parties.
    """
    # TODO: Implement database persistence
    return Obligation(
        id="OBL-" + datetime.now().strftime("%Y%m%d%H%M%S"),
        title=request.title,
        description=request.description,
        regulation=request.regulation,
        category=request.category,
        frequency=request.frequency,
        due_date=request.due_date,
        status=ObligationStatus.PENDING,
        responsible_party=request.responsible_party,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@router.patch("/obligations/{obligation_id}", response_model=Obligation)
async def update_obligation(
    obligation_id: str,
    request: ObligationUpdateRequest,
    current_user: CurrentUser,
) -> Obligation:
    """
    Update the status of a compliance obligation.

    Mark obligations as completed, in progress, or overdue
    with optional notes and completion dates.
    """
    return update_obligation_status(
        obligation_id=obligation_id,
        status=request.status,
        completion_date=request.completion_date,
        notes=request.notes,
    )


@router.post("/reports/generate", response_model=ComplianceReport)
async def generate_compliance_report(
    request: ReportGenerateRequest,
    current_user: CurrentUser,
) -> ComplianceReport:
    """
    Generate a compliance report for regulatory submission.

    Supports various EPA-required report types including CCR,
    monthly operating reports, and sampling summaries.
    """
    return generate_report(
        report_type=request.report_type,
        period_start=request.period_start,
        period_end=request.period_end,
        include_supporting_data=request.include_supporting_data,
    )


@router.get("/reports/types")
async def list_report_types(
    current_user: CurrentUser,
) -> list[dict]:
    """List available compliance report types."""
    return [
        {
            "type": "CCR",
            "name": "Consumer Confidence Report",
            "frequency": "Annual",
            "description": "Annual water quality report for customers",
        },
        {
            "type": "MOR",
            "name": "Monthly Operating Report",
            "frequency": "Monthly",
            "description": "Monthly system operation summary",
        },
        {
            "type": "SAMPLING",
            "name": "Sampling Summary",
            "frequency": "As needed",
            "description": "Water quality sampling results",
        },
        {
            "type": "VIOLATION",
            "name": "Violation Response",
            "frequency": "As needed",
            "description": "Response to compliance violations",
        },
    ]


@router.post("/risk-assessment", response_model=RiskAssessment)
async def assess_compliance_risk(
    request: RiskAssessmentRequest,
    current_user: CurrentUser,
) -> RiskAssessment:
    """
    Calculate overall compliance risk score.

    Analyzes pending obligations, historical compliance,
    and upcoming deadlines to identify risk areas.
    """
    return calculate_compliance_risk(
        include_categories=request.include_categories,
    )


@router.get("/summary")
async def get_compliance_summary(
    current_user: CurrentUser,
) -> dict:
    """
    Get compliance summary for the dashboard.

    Returns key metrics including obligation counts by status,
    upcoming deadlines, and overall compliance health score.
    """
    # TODO: Implement database queries
    return {
        "total_obligations": 24,
        "completed": 18,
        "pending": 4,
        "overdue": 2,
        "due_this_week": 1,
        "due_this_month": 3,
        "compliance_score": 85.0,
        "risk_level": "low",
        "last_violation_days_ago": 180,
    }


@router.get("/calendar")
async def get_compliance_calendar(
    current_user: CurrentUser,
    month: Annotated[int, Query(ge=1, le=12)],
    year: Annotated[int, Query(ge=2020, le=2100)],
) -> list[dict]:
    """
    Get compliance calendar for a specific month.

    Returns obligations and deadlines organized by date
    for calendar view display.
    """
    # TODO: Implement database queries
    return [
        {
            "date": f"{year}-{month:02d}-15",
            "obligations": [
                {
                    "id": "OBL-001",
                    "title": "Monthly Coliform Sampling",
                    "status": "pending",
                }
            ],
        },
        {
            "date": f"{year}-{month:02d}-28",
            "obligations": [
                {
                    "id": "OBL-002",
                    "title": "Monthly Operating Report",
                    "status": "pending",
                }
            ],
        },
    ]

