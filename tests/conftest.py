"""Pytest configuration and shared fixtures."""

from datetime import date, datetime
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from api.auth import create_access_token
from api.main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Create a test client for the FastAPI application."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def auth_headers() -> dict[str, str]:
    """Create authentication headers with a valid JWT token."""
    token = create_access_token(subject="test-user-id")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def authenticated_client(
    client: TestClient, auth_headers: dict[str, str]
) -> TestClient:
    """Create a test client with authentication headers pre-set."""
    client.headers.update(auth_headers)
    return client


# Sample data fixtures


@pytest.fixture
def sample_water_balance_input() -> dict:
    """Sample water balance calculation input."""
    return {
        "system_input_volume": 10000.0,
        "billed_metered_consumption": 7500.0,
        "billed_unmetered_consumption": 200.0,
        "unbilled_metered_consumption": 100.0,
        "unbilled_unmetered_consumption": 50.0,
        "unauthorized_consumption": 100.0,
        "meter_inaccuracies": 150.0,
        "period_start": "2024-01-01",
        "period_end": "2024-01-31",
    }


@pytest.fixture
def sample_hourly_flows() -> list[float]:
    """Sample 24-hour flow data for MNF analysis."""
    # Typical diurnal pattern with MNF around 2-4 AM
    return [
        15.0,  # 00:00
        12.0,  # 01:00
        8.0,  # 02:00 - MNF window
        7.5,  # 03:00 - MNF window
        9.0,  # 04:00
        14.0,  # 05:00
        25.0,  # 06:00
        45.0,  # 07:00
        55.0,  # 08:00
        50.0,  # 09:00
        48.0,  # 10:00
        52.0,  # 11:00
        58.0,  # 12:00
        55.0,  # 13:00
        50.0,  # 14:00
        52.0,  # 15:00
        55.0,  # 16:00
        60.0,  # 17:00
        65.0,  # 18:00 - Evening peak
        58.0,  # 19:00
        45.0,  # 20:00
        35.0,  # 21:00
        25.0,  # 22:00
        18.0,  # 23:00
    ]


@pytest.fixture
def sample_pump_schedule_input() -> dict:
    """Sample pump schedule optimization input."""
    return {
        "pump_id": "PUMP-001",
        "tank_capacity_m3": 500.0,
        "tank_current_level_m3": 300.0,
        "tank_min_level_m3": 100.0,
        "pump_flow_rate_m3h": 50.0,
        "pump_power_kw": 22.0,
        "demand_forecast_m3h": [
            10,
            8,
            6,
            5,
            5,
            8,
            15,
            25,
            30,
            28,
            26,
            28,
            30,
            28,
            26,
            28,
            32,
            35,
            30,
            25,
            20,
            15,
            12,
            10,
        ],
        "electricity_rates": [
            0.08,
            0.08,
            0.08,
            0.08,
            0.08,
            0.08,  # Off-peak
            0.12,
            0.12,
            0.12,
            0.12,
            0.12,
            0.12,
            0.12,
            0.12,  # Mid-peak
            0.18,
            0.18,
            0.18,
            0.18,
            0.18,
            0.18,
            0.18,
            0.18,  # On-peak
            0.08,
            0.08,  # Off-peak
        ],
        "optimization_date": str(date.today()),
    }


@pytest.fixture
def sample_efficiency_input() -> dict:
    """Sample pump efficiency analysis input."""
    return {
        "pump_id": "PUMP-001",
        "flow_rate_m3h": 45.0,
        "discharge_pressure_m": 55.0,
        "suction_pressure_m": 5.0,
        "power_consumption_kw": 20.0,
        "rated_efficiency": 0.75,
    }
