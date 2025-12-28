"""Compliance Management Module.

This module provides tools for tracking and managing regulatory
compliance obligations for water systems under EPA Safe Drinking
Water Act and state regulations.

Key components:
- Obligation Tracking: Monitor and manage compliance deadlines
- Report Generation: Automated regulatory report creation
- Risk Scoring: Proactive compliance risk assessment
"""

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
from src.compliance.risk_scoring import RiskAssessment, calculate_compliance_risk

__all__ = [
    "Obligation",
    "ObligationStatus",
    "get_obligations",
    "update_obligation_status",
    "ComplianceReport",
    "ReportType",
    "generate_report",
    "RiskAssessment",
    "calculate_compliance_risk",
]
