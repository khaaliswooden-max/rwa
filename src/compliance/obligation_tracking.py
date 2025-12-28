"""Compliance Obligation Tracking.

Tracks regulatory obligations including monitoring requirements,
reporting deadlines, and operational compliance items.

Supports EPA SDWA requirements and state-specific regulations.
"""

from datetime import date, datetime, timedelta
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ObligationStatus(str, Enum):
    """Status of a compliance obligation."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    OVERDUE = "overdue"
    WAIVED = "waived"


class ObligationCategory(str, Enum):
    """Category of compliance obligation."""

    MONITORING = "monitoring"
    REPORTING = "reporting"
    TREATMENT = "treatment"
    OPERATIONAL = "operational"
    ADMINISTRATIVE = "administrative"
    INFRASTRUCTURE = "infrastructure"


class Obligation(BaseModel):
    """A compliance obligation to be tracked."""

    id: str = Field(..., description="Unique identifier")
    title: str = Field(..., description="Obligation title")
    description: str = Field(default="", description="Detailed description")

    # Regulatory reference
    regulation: str = Field(
        ..., description="Regulatory reference (e.g., 'EPA SDWA 40 CFR 141.21')"
    )
    category: str = Field(..., description="Obligation category")

    # Timing
    frequency: str = Field(
        ..., description="Frequency (e.g., 'Monthly', 'Quarterly', 'Annual')"
    )
    due_date: date = Field(..., description="Next due date")

    # Status
    status: ObligationStatus = Field(
        default=ObligationStatus.PENDING, description="Current status"
    )
    completion_date: date | None = Field(
        default=None, description="Date completed"
    )
    notes: str = Field(default="", description="Status notes")

    # Assignment
    responsible_party: str = Field(default="", description="Responsible person/role")

    # Metadata
    created_at: datetime = Field(
        default_factory=datetime.now, description="When created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="When last updated"
    )

    @property
    def is_overdue(self) -> bool:
        """Check if obligation is overdue."""
        return (
            self.status not in [ObligationStatus.COMPLETED, ObligationStatus.WAIVED]
            and self.due_date < date.today()
        )

    @property
    def days_until_due(self) -> int:
        """Days until due (negative if overdue)."""
        return (self.due_date - date.today()).days


# In-memory storage for demo (would be database in production)
_obligations_db: dict[str, Obligation] = {}


def get_obligations(
    status: ObligationStatus | None = None,
    category: str | None = None,
    due_within_days: int | None = None,
) -> list[Obligation]:
    """
    Retrieve obligations with optional filtering.

    Args:
        status: Filter by status
        category: Filter by category
        due_within_days: Filter for obligations due within N days

    Returns:
        List of matching obligations
    """
    # Return sample data for demo
    sample_obligations = _get_sample_obligations()

    results = list(sample_obligations.values())

    if status:
        results = [o for o in results if o.status == status]

    if category:
        results = [o for o in results if o.category == category]

    if due_within_days:
        cutoff = date.today() + timedelta(days=due_within_days)
        results = [o for o in results if o.due_date <= cutoff]

    # Sort by due date
    results.sort(key=lambda o: o.due_date)

    return results


def update_obligation_status(
    obligation_id: str,
    status: ObligationStatus,
    completion_date: date | None = None,
    notes: str = "",
) -> Obligation:
    """
    Update the status of an obligation.

    Args:
        obligation_id: ID of obligation to update
        status: New status
        completion_date: Date completed (if applicable)
        notes: Status notes

    Returns:
        Updated obligation
    """
    obligations = _get_sample_obligations()

    if obligation_id not in obligations:
        raise ValueError(f"Obligation {obligation_id} not found")

    obligation = obligations[obligation_id]
    obligation.status = status
    obligation.notes = notes
    obligation.updated_at = datetime.now()

    if status == ObligationStatus.COMPLETED:
        obligation.completion_date = completion_date or date.today()

    return obligation


def _get_sample_obligations() -> dict[str, Obligation]:
    """Get sample obligations for demo."""
    today = date.today()

    return {
        "OBL-001": Obligation(
            id="OBL-001",
            title="Monthly Coliform Sampling",
            description="Collect and submit total coliform samples per monitoring plan",
            regulation="EPA SDWA 40 CFR 141.21",
            category="monitoring",
            frequency="Monthly",
            due_date=today + timedelta(days=15),
            status=ObligationStatus.PENDING,
            responsible_party="Operator",
        ),
        "OBL-002": Obligation(
            id="OBL-002",
            title="Monthly Operating Report",
            description="Submit monthly operating report to state agency",
            regulation="State Regulation",
            category="reporting",
            frequency="Monthly",
            due_date=today + timedelta(days=28),
            status=ObligationStatus.PENDING,
            responsible_party="Operator",
        ),
        "OBL-003": Obligation(
            id="OBL-003",
            title="Quarterly DBP Sampling",
            description="Disinfection byproduct (DBP) monitoring",
            regulation="EPA SDWA 40 CFR 141.132",
            category="monitoring",
            frequency="Quarterly",
            due_date=today + timedelta(days=45),
            status=ObligationStatus.PENDING,
            responsible_party="Operator",
        ),
        "OBL-004": Obligation(
            id="OBL-004",
            title="Annual Consumer Confidence Report",
            description="Prepare and distribute CCR to customers",
            regulation="EPA SDWA 40 CFR 141.151",
            category="reporting",
            frequency="Annual",
            due_date=date(today.year, 7, 1),
            status=ObligationStatus.PENDING,
            responsible_party="Manager",
        ),
        "OBL-005": Obligation(
            id="OBL-005",
            title="Chlorine Residual Monitoring",
            description="Daily chlorine residual checks",
            regulation="EPA SDWA 40 CFR 141.72",
            category="monitoring",
            frequency="Daily",
            due_date=today,
            status=ObligationStatus.IN_PROGRESS,
            responsible_party="Operator",
        ),
    }


# Pre-defined EPA SDWA obligations template
EPA_SDWA_OBLIGATIONS = [
    {
        "title": "Total Coliform Rule Sampling",
        "regulation": "40 CFR 141.21",
        "category": "monitoring",
        "frequency": "Monthly",
        "description": "Routine coliform sampling per approved monitoring plan",
    },
    {
        "title": "Lead and Copper Rule Sampling",
        "regulation": "40 CFR 141.86",
        "category": "monitoring",
        "frequency": "Per Schedule",
        "description": "Lead and copper tap sampling per LCR schedule",
    },
    {
        "title": "Disinfection Byproducts Monitoring",
        "regulation": "40 CFR 141.132",
        "category": "monitoring",
        "frequency": "Quarterly/Annual",
        "description": "TTHM and HAA5 sampling per Stage 2 DBP Rule",
    },
    {
        "title": "Consumer Confidence Report",
        "regulation": "40 CFR 141.151",
        "category": "reporting",
        "frequency": "Annual",
        "description": "Annual water quality report to customers by July 1",
    },
    {
        "title": "Sanitary Survey",
        "regulation": "40 CFR 141.723",
        "category": "operational",
        "frequency": "3-5 Years",
        "description": "Comprehensive system evaluation by primacy agency",
    },
]

