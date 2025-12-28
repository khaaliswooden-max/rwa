"""Tests for main API endpoints."""

import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_check(self, client: TestClient):
        """Test health check returns healthy status."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data

    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint returns API info."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "RWA" in data["message"]


class TestNRWEndpoints:
    """Tests for NRW API endpoints."""

    def test_water_balance_requires_auth(self, client: TestClient):
        """Test water balance endpoint requires authentication."""
        response = client.post("/api/v1/nrw/water-balance", json={})

        assert response.status_code == 401

    def test_water_balance_calculation(
        self,
        authenticated_client: TestClient,
        sample_water_balance_input: dict,
    ):
        """Test water balance calculation endpoint."""
        response = authenticated_client.post(
            "/api/v1/nrw/water-balance",
            json=sample_water_balance_input,
        )

        assert response.status_code == 200
        data = response.json()
        assert "system_input_volume" in data
        assert "non_revenue_water" in data
        assert "nrw_percentage" in data

    def test_nrw_summary(self, authenticated_client: TestClient):
        """Test NRW summary endpoint."""
        response = authenticated_client.get("/api/v1/nrw/summary")

        assert response.status_code == 200
        data = response.json()
        assert "nrw_percentage" in data


class TestEnergyEndpoints:
    """Tests for Energy API endpoints."""

    def test_pump_schedule_requires_auth(self, client: TestClient):
        """Test pump schedule endpoint requires authentication."""
        response = client.post("/api/v1/energy/optimize-schedule", json={})

        assert response.status_code == 401

    def test_energy_summary(self, authenticated_client: TestClient):
        """Test energy summary endpoint."""
        response = authenticated_client.get("/api/v1/energy/summary")

        assert response.status_code == 200
        data = response.json()
        assert "total_energy_kwh" in data
        assert "total_cost_usd" in data

    def test_list_pumps(self, authenticated_client: TestClient):
        """Test list pumps endpoint."""
        response = authenticated_client.get("/api/v1/energy/pumps")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestComplianceEndpoints:
    """Tests for Compliance API endpoints."""

    def test_obligations_requires_auth(self, client: TestClient):
        """Test obligations endpoint requires authentication."""
        response = client.get("/api/v1/compliance/obligations")

        assert response.status_code == 401

    def test_list_obligations(self, authenticated_client: TestClient):
        """Test list obligations endpoint."""
        response = authenticated_client.get("/api/v1/compliance/obligations")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_compliance_summary(self, authenticated_client: TestClient):
        """Test compliance summary endpoint."""
        response = authenticated_client.get("/api/v1/compliance/summary")

        assert response.status_code == 200
        data = response.json()
        assert "total_obligations" in data
        assert "compliance_score" in data

    def test_report_types(self, authenticated_client: TestClient):
        """Test list report types endpoint."""
        response = authenticated_client.get("/api/v1/compliance/reports/types")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0


class TestDataIngestionEndpoints:
    """Tests for Data Ingestion API endpoints."""

    def test_ingestion_status(self, authenticated_client: TestClient):
        """Test data ingestion status endpoint."""
        response = authenticated_client.get("/api/v1/data/status")

        assert response.status_code == 200
        data = response.json()
        assert "status" in data

    def test_list_data_sources(self, authenticated_client: TestClient):
        """Test list data sources endpoint."""
        response = authenticated_client.get("/api/v1/data/sources")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

