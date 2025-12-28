"""Tests for water balance calculations."""

from datetime import date

import pytest

from src.nrw.water_balance import (
    WaterBalance,
    WaterBalanceInput,
    calculate_uarl,
    calculate_water_balance,
)


class TestWaterBalanceCalculation:
    """Tests for the water balance calculation function."""

    def test_basic_water_balance(self):
        """Test basic water balance calculation."""
        input_data = WaterBalanceInput(
            system_input_volume=1000.0,
            billed_metered_consumption=800.0,
            billed_unmetered_consumption=0.0,
            unbilled_metered_consumption=0.0,
            unbilled_unmetered_consumption=0.0,
            unauthorized_consumption=50.0,
            meter_inaccuracies=0.0,
            period_start=date(2024, 1, 1),
            period_end=date(2024, 1, 31),
        )

        result = calculate_water_balance(input_data)

        assert result.system_input_volume == 1000.0
        assert result.billed_authorized_consumption == 800.0
        assert result.apparent_losses == 50.0
        assert result.real_losses == 150.0  # 1000 - 800 - 50
        assert result.non_revenue_water == 200.0  # 1000 - 800

    def test_nrw_percentage_calculation(self):
        """Test NRW percentage is calculated correctly."""
        input_data = WaterBalanceInput(
            system_input_volume=1000.0,
            billed_metered_consumption=750.0,
            period_start=date(2024, 1, 1),
            period_end=date(2024, 1, 31),
        )

        result = calculate_water_balance(input_data)

        assert result.nrw_percentage == 25.0

    def test_zero_system_input(self):
        """Test handling of zero system input."""
        input_data = WaterBalanceInput(
            system_input_volume=0.001,  # Near zero (can't be exactly 0)
            billed_metered_consumption=0.0,
            period_start=date(2024, 1, 1),
            period_end=date(2024, 1, 31),
        )

        result = calculate_water_balance(input_data)

        # Should not raise an error
        assert result.system_input_volume == 0.001

    def test_all_consumption_components(self):
        """Test with all consumption components populated."""
        input_data = WaterBalanceInput(
            system_input_volume=10000.0,
            billed_metered_consumption=7000.0,
            billed_unmetered_consumption=500.0,
            unbilled_metered_consumption=200.0,
            unbilled_unmetered_consumption=100.0,
            unauthorized_consumption=300.0,
            meter_inaccuracies=400.0,
            period_start=date(2024, 1, 1),
            period_end=date(2024, 12, 31),
        )

        result = calculate_water_balance(input_data)

        # Verify authorized consumption
        assert result.billed_authorized_consumption == 7500.0
        assert result.unbilled_authorized_consumption == 300.0
        assert result.authorized_consumption == 7800.0

        # Verify losses
        assert result.apparent_losses == 700.0
        assert result.real_losses == 1500.0  # 10000 - 7800 - 700
        assert result.water_losses == 2200.0

        # Verify revenue water
        assert result.revenue_water == 7500.0
        assert result.non_revenue_water == 2500.0

    def test_period_days_calculation(self):
        """Test period days is calculated correctly."""
        input_data = WaterBalanceInput(
            system_input_volume=1000.0,
            billed_metered_consumption=800.0,
            period_start=date(2024, 1, 1),
            period_end=date(2024, 1, 31),
        )

        result = calculate_water_balance(input_data)

        assert result.period_days == 31


class TestUARLCalculation:
    """Tests for UARL (Unavoidable Annual Real Losses) calculation."""

    def test_basic_uarl(self):
        """Test basic UARL calculation."""
        uarl = calculate_uarl(
            mains_length_km=10.0,
            service_connections=500,
            service_connection_length_m=15.0,
            average_pressure_m=40.0,
        )

        # UARL = (18 × 10 + 0.8 × 500 + 25 × 7.5) × 40
        # UARL = (180 + 400 + 187.5) × 40
        # UARL = 767.5 × 40 = 30,700 L/day
        expected = (18 * 10 + 0.8 * 500 + 25 * 7.5) * 40
        assert abs(uarl - expected) < 0.1

    def test_uarl_small_system(self):
        """Test UARL for a small rural system."""
        uarl = calculate_uarl(
            mains_length_km=5.0,
            service_connections=200,
            service_connection_length_m=10.0,
            average_pressure_m=35.0,
        )

        assert uarl > 0
        # Small system should have lower UARL
        assert uarl < 20000  # Reasonable upper bound for small system
