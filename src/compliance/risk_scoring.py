"""Compliance Risk Scoring.

Calculates compliance risk scores based on obligation status,
historical performance, and upcoming deadlines.

Helps prioritize compliance activities and identify areas
requiring immediate attention.
"""

from datetime import date, datetime, timedelta
from typing import Literal

from pydantic import BaseModel, Field, computed_field


class CategoryRisk(BaseModel):
    """Risk assessment for a specific category."""

    category: str = Field(..., description="Category name")
    total_obligations: int = Field(..., description="Total obligations")
    completed: int = Field(..., description="Completed count")
    pending: int = Field(..., description="Pending count")
    overdue: int = Field(..., description="Overdue count")
    risk_score: float = Field(..., ge=0, le=100, description="Category risk score")
    risk_level: Literal["low", "medium", "high", "critical"] = Field(
        ..., description="Risk level"
    )


class RiskAssessment(BaseModel):
    """Overall compliance risk assessment."""

    assessment_date: datetime = Field(
        default_factory=datetime.now, description="Assessment timestamp"
    )

    # Overall metrics
    overall_risk_score: float = Field(
        ..., ge=0, le=100, description="Overall risk score (0-100)"
    )
    overall_risk_level: Literal["low", "medium", "high", "critical"] = Field(
        ..., description="Overall risk level"
    )

    # Category breakdown
    category_risks: list[CategoryRisk] = Field(..., description="Risk by category")

    # Summary statistics
    total_obligations: int = Field(..., description="Total obligations")
    completed_obligations: int = Field(..., description="Completed count")
    pending_obligations: int = Field(..., description="Pending count")
    overdue_obligations: int = Field(..., description="Overdue count")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def compliance_percentage(self) -> float:
        """Percentage of obligations completed or on track."""
        if self.total_obligations == 0:
            return 100.0
        on_track = self.completed_obligations + self.pending_obligations
        return round((on_track / self.total_obligations) * 100, 1)

    # Upcoming deadlines
    upcoming_deadlines: list[dict] = Field(
        default_factory=list, description="Upcoming deadlines (next 30 days)"
    )

    # Recommendations
    recommendations: list[str] = Field(
        default_factory=list, description="Risk mitigation recommendations"
    )


def calculate_compliance_risk(
    include_categories: list[str] | None = None,
) -> RiskAssessment:
    """
    Calculate overall compliance risk assessment.

    Risk scoring factors:
    - Overdue obligations (highest weight)
    - Obligations due within 7 days
    - Historical violation rate
    - Category-specific risk weights

    Args:
        include_categories: Limit to specific categories (None = all)

    Returns:
        RiskAssessment with scores and recommendations
    """
    # Get sample data (would query database in production)
    obligations = _get_sample_obligation_data()

    # Filter by category if specified
    if include_categories:
        obligations = [o for o in obligations if o["category"] in include_categories]

    # Calculate by category
    categories = set(o["category"] for o in obligations)
    category_risks = []

    for category in categories:
        cat_obligations = [o for o in obligations if o["category"] == category]
        total = len(cat_obligations)
        completed = sum(1 for o in cat_obligations if o["status"] == "completed")
        overdue = sum(1 for o in cat_obligations if o["status"] == "overdue")
        pending = total - completed - overdue

        # Calculate category risk score
        cat_risk_score = _calculate_category_risk(total, completed, overdue, pending)
        risk_level = _score_to_level(cat_risk_score)

        category_risks.append(
            CategoryRisk(
                category=category,
                total_obligations=total,
                completed=completed,
                pending=pending,
                overdue=overdue,
                risk_score=cat_risk_score,
                risk_level=risk_level,
            )
        )

    # Calculate overall metrics
    total_obligations = len(obligations)
    completed = sum(1 for o in obligations if o["status"] == "completed")
    overdue = sum(1 for o in obligations if o["status"] == "overdue")
    pending = total_obligations - completed - overdue

    # Calculate overall risk score (weighted average of category scores)
    if category_risks:
        overall_score = sum(cr.risk_score for cr in category_risks) / len(
            category_risks
        )
        # Boost score if any critical categories
        critical_count = sum(1 for cr in category_risks if cr.risk_level == "critical")
        overall_score = min(100, overall_score + (critical_count * 10))
    else:
        overall_score = 0

    overall_level = _score_to_level(overall_score)

    # Get upcoming deadlines
    upcoming = _get_upcoming_deadlines(obligations)

    # Generate recommendations
    recommendations = _generate_risk_recommendations(
        category_risks, overdue, overall_score
    )

    return RiskAssessment(
        overall_risk_score=round(overall_score, 1),
        overall_risk_level=overall_level,
        category_risks=category_risks,
        total_obligations=total_obligations,
        completed_obligations=completed,
        pending_obligations=pending,
        overdue_obligations=overdue,
        upcoming_deadlines=upcoming,
        recommendations=recommendations,
    )


def _calculate_category_risk(
    total: int, completed: int, overdue: int, pending: int
) -> float:
    """Calculate risk score for a category."""
    if total == 0:
        return 0.0

    # Base score from completion rate
    completion_rate = completed / total
    base_score = (1 - completion_rate) * 50

    # Overdue penalty (high weight)
    overdue_penalty = (overdue / total) * 40

    # Pending consideration (moderate weight)
    pending_factor = (pending / total) * 10

    return min(100, base_score + overdue_penalty + pending_factor)


def _score_to_level(score: float) -> Literal["low", "medium", "high", "critical"]:
    """Convert numeric score to risk level."""
    if score >= 75:
        return "critical"
    elif score >= 50:
        return "high"
    elif score >= 25:
        return "medium"
    else:
        return "low"


def _get_upcoming_deadlines(obligations: list[dict]) -> list[dict]:
    """Get obligations due in next 30 days."""
    today = date.today()
    cutoff = today + timedelta(days=30)

    upcoming = []
    for o in obligations:
        if o["status"] not in ["completed", "waived"]:
            due = o.get("due_date", today)
            if isinstance(due, str):
                due = date.fromisoformat(due)
            if today <= due <= cutoff:
                upcoming.append(
                    {
                        "title": o["title"],
                        "due_date": due.isoformat(),
                        "days_until_due": (due - today).days,
                        "category": o["category"],
                    }
                )

    # Sort by due date
    upcoming.sort(key=lambda x: x["due_date"])
    return upcoming[:10]  # Return top 10


def _generate_risk_recommendations(
    category_risks: list[CategoryRisk],
    total_overdue: int,
    overall_score: float,
) -> list[str]:
    """Generate risk mitigation recommendations."""
    recommendations = []

    if total_overdue > 0:
        recommendations.append(
            f"URGENT: {total_overdue} overdue obligation(s) require immediate attention"
        )

    # Find highest risk categories
    critical_cats = [cr for cr in category_risks if cr.risk_level == "critical"]
    for cat in critical_cats:
        recommendations.append(
            f"Critical risk in {cat.category}: {cat.overdue} overdue, "
            f"{cat.pending} pending out of {cat.total_obligations} total"
        )

    if overall_score >= 50:
        recommendations.append(
            "Consider allocating additional resources to compliance activities"
        )

    if overall_score >= 25:
        recommendations.append(
            "Review upcoming deadlines and prioritize based on regulatory impact"
        )

    if not recommendations:
        recommendations.append(
            "Compliance program is on track - continue routine monitoring"
        )

    return recommendations


def _get_sample_obligation_data() -> list[dict]:
    """Get sample obligation data for demo."""
    today = date.today()

    return [
        {
            "id": "1",
            "title": "Monthly Coliform Sampling",
            "category": "monitoring",
            "status": "completed",
            "due_date": today - timedelta(days=5),
        },
        {
            "id": "2",
            "title": "Monthly Operating Report",
            "category": "reporting",
            "status": "pending",
            "due_date": today + timedelta(days=10),
        },
        {
            "id": "3",
            "title": "Quarterly DBP Sampling",
            "category": "monitoring",
            "status": "pending",
            "due_date": today + timedelta(days=25),
        },
        {
            "id": "4",
            "title": "Daily Chlorine Checks",
            "category": "monitoring",
            "status": "completed",
            "due_date": today,
        },
        {
            "id": "5",
            "title": "Backflow Prevention Testing",
            "category": "operational",
            "status": "overdue",
            "due_date": today - timedelta(days=15),
        },
    ]
