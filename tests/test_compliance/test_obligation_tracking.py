"""Tests for compliance obligation tracking."""

from datetime import date, timedelta

import pytest

from src.compliance.obligation_tracking import (
    Obligation,
    ObligationStatus,
    get_obligations,
    update_obligation_status,
)


class TestObligationRetrieval:
    """Tests for retrieving obligations."""

    def test_get_all_obligations(self):
        """Test retrieving all obligations."""
        obligations = get_obligations()

        assert len(obligations) > 0
        assert all(isinstance(o, Obligation) for o in obligations)

    def test_filter_by_status(self):
        """Test filtering obligations by status."""
        pending = get_obligations(status=ObligationStatus.PENDING)

        assert all(o.status == ObligationStatus.PENDING for o in pending)

    def test_filter_by_due_date(self):
        """Test filtering by due date window."""
        obligations = get_obligations(due_within_days=30)
        cutoff = date.today() + timedelta(days=30)

        assert all(o.due_date <= cutoff for o in obligations)

    def test_obligations_sorted_by_due_date(self):
        """Test that obligations are sorted by due date."""
        obligations = get_obligations()

        if len(obligations) > 1:
            for i in range(len(obligations) - 1):
                assert obligations[i].due_date <= obligations[i + 1].due_date


class TestObligationUpdate:
    """Tests for updating obligation status."""

    def test_update_to_completed(self):
        """Test marking obligation as completed."""
        obligations = get_obligations()
        if obligations:
            obligation_id = obligations[0].id
            updated = update_obligation_status(
                obligation_id=obligation_id,
                status=ObligationStatus.COMPLETED,
                notes="Completed via test",
            )

            assert updated.status == ObligationStatus.COMPLETED
            assert updated.completion_date is not None

    def test_update_nonexistent_raises(self):
        """Test that updating nonexistent obligation raises error."""
        with pytest.raises(ValueError):
            update_obligation_status(
                obligation_id="NONEXISTENT-ID",
                status=ObligationStatus.COMPLETED,
            )


class TestObligationModel:
    """Tests for the Obligation model itself."""

    def test_is_overdue_property(self):
        """Test is_overdue computed property."""
        past_due = Obligation(
            id="TEST-001",
            title="Test Obligation",
            regulation="Test Reg",
            category="monitoring",
            frequency="Monthly",
            due_date=date.today() - timedelta(days=5),
            status=ObligationStatus.PENDING,
        )

        assert past_due.is_overdue is True

    def test_not_overdue_when_completed(self):
        """Test completed obligations are not overdue."""
        completed = Obligation(
            id="TEST-002",
            title="Test Obligation",
            regulation="Test Reg",
            category="monitoring",
            frequency="Monthly",
            due_date=date.today() - timedelta(days=5),
            status=ObligationStatus.COMPLETED,
        )

        assert completed.is_overdue is False

    def test_days_until_due(self):
        """Test days_until_due calculation."""
        future = Obligation(
            id="TEST-003",
            title="Test Obligation",
            regulation="Test Reg",
            category="monitoring",
            frequency="Monthly",
            due_date=date.today() + timedelta(days=10),
            status=ObligationStatus.PENDING,
        )

        assert future.days_until_due == 10
