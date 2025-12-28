# RWA API Reference

Complete API documentation for the RWA platform.

## Base URL

```
Development: http://localhost:8000/api/v1
Production: https://api.yourserver.com/api/v1
```

## Authentication

All endpoints (except health check) require JWT authentication.

### Obtain Token

```http
POST /auth/login
Content-Type: application/json

{
  "email": "operator@example.com",
  "password": "your-password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Using the Token

Include in all requests:
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### Refresh Token

```http
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

---

## Health Check

### GET /health

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "app": "RWA",
  "version": "0.1.0",
  "environment": "development"
}
```

---

## Non-Revenue Water (NRW)

### POST /nrw/water-balance

Calculate IWA-standard water balance.

**Request:**
```json
{
  "system_input_volume": 10000.0,
  "billed_metered_consumption": 7500.0,
  "billed_unmetered_consumption": 200.0,
  "unbilled_metered_consumption": 100.0,
  "unbilled_unmetered_consumption": 50.0,
  "unauthorized_consumption": 100.0,
  "meter_inaccuracies": 150.0,
  "period_start": "2024-01-01",
  "period_end": "2024-01-31"
}
```

**Response:**
```json
{
  "system_input_volume": 10000.0,
  "billed_authorized_consumption": 7700.0,
  "unbilled_authorized_consumption": 150.0,
  "authorized_consumption": 7850.0,
  "apparent_losses": 250.0,
  "real_losses": 1900.0,
  "water_losses": 2150.0,
  "revenue_water": 7700.0,
  "non_revenue_water": 2300.0,
  "nrw_percentage": 23.0,
  "real_losses_percentage": 19.0,
  "apparent_losses_percentage": 2.5,
  "period_start": "2024-01-01",
  "period_end": "2024-01-31",
  "period_days": 31
}
```

### POST /nrw/mnf-analysis

Analyze Minimum Night Flow for leakage estimation.

**Request:**
```json
{
  "hourly_flows": [15.0, 12.0, 8.0, 7.5, 9.0, ...],
  "service_connections": 850,
  "average_pressure": 40.0
}
```

**Response:**
```json
{
  "minimum_flow_m3h": 7.5,
  "mnf_hour": 3,
  "average_night_flow_m3h": 9.125,
  "estimated_legitimate_night_use_m3h": 2.55,
  "estimated_background_leakage_m3h": 4.95,
  "estimated_daily_leakage_m3": 148.5,
  "service_connections": 850,
  "average_pressure_m": 40.0,
  "night_day_ratio": 0.185,
  "confidence": "high",
  "leakage_per_connection_lph": 5.82,
  "annual_leakage_estimate_m3": 54203.0
}
```

### POST /nrw/leak-indicators

Analyze leak indicators for a distribution zone.

**Request:**
```json
{
  "zone_id": "ZONE-A",
  "mnf_values": [8.2, 8.5, 8.3, 8.8, 9.1, 9.5, 9.8],
  "system_pressure": 42.0,
  "pipe_length_km": 12.5,
  "service_connections": 350
}
```

**Response:**
```json
{
  "zone_id": "ZONE-A",
  "analysis_timestamp": "2024-01-15T10:30:00Z",
  "average_mnf_m3h": 8.886,
  "mnf_trend": "increasing",
  "mnf_trend_slope": 0.2571,
  "pipe_length_km": 12.5,
  "service_connections": 350,
  "leakage_rate_m3_km_day": 17.06,
  "infrastructure_leakage_index": 3.45,
  "priority": "medium",
  "risk_score": 42.5,
  "leakage_per_connection_lpd": 609.4,
  "recommended_actions": [
    "Increasing MNF trend suggests developing leaks - monitor closely"
  ]
}
```

### GET /nrw/summary

Get NRW dashboard summary.

**Query Parameters:**
- `period_days` (int, 7-365, default: 30)

**Response:**
```json
{
  "period_days": 30,
  "nrw_percentage": 22.5,
  "nrw_volume_m3": 4500.0,
  "real_losses_m3": 3200.0,
  "apparent_losses_m3": 1300.0,
  "infrastructure_leakage_index": 2.8,
  "trend": "improving",
  "trend_percentage": -3.2
}
```

---

## Energy Management

### POST /energy/optimize-schedule

Generate optimized pump schedule.

**Request:**
```json
{
  "pump_id": "PUMP-001",
  "tank_capacity_m3": 500.0,
  "tank_current_level_m3": 300.0,
  "tank_min_level_m3": 100.0,
  "pump_flow_rate_m3h": 50.0,
  "pump_power_kw": 22.0,
  "demand_forecast_m3h": [10, 8, 6, 5, 5, 8, ...],
  "electricity_rates": [0.08, 0.08, 0.08, 0.08, ...],
  "optimization_date": "2024-01-15"
}
```

**Response:**
```json
{
  "pump_id": "PUMP-001",
  "optimization_date": "2024-01-15",
  "generated_at": "2024-01-14T22:00:00Z",
  "hourly_schedule": [
    {
      "hour": 0,
      "pump_on": true,
      "tank_level_m3": 340.0,
      "energy_cost": 1.76,
      "electricity_rate": 0.08
    },
    ...
  ],
  "total_runtime_hours": 8.0,
  "total_energy_kwh": 176.0,
  "total_cost": 18.48,
  "baseline_cost": 52.80,
  "savings_amount": 34.32,
  "savings_percentage": 65.0,
  "min_tank_level_m3": 105.0,
  "max_tank_level_m3": 450.0
}
```

### POST /energy/efficiency-analysis

Analyze pump operating efficiency.

**Request:**
```json
{
  "pump_id": "PUMP-001",
  "flow_rate_m3h": 45.0,
  "discharge_pressure_m": 55.0,
  "suction_pressure_m": 5.0,
  "power_consumption_kw": 20.0,
  "rated_efficiency": 0.75
}
```

**Response:**
```json
{
  "pump_id": "PUMP-001",
  "analysis_timestamp": "2024-01-15T10:30:00Z",
  "flow_rate_m3h": 45.0,
  "total_head_m": 50.0,
  "power_consumption_kw": 20.0,
  "hydraulic_power_kw": 6.13,
  "wire_to_water_efficiency": 0.307,
  "rated_efficiency": 0.75,
  "efficiency_percentage": 30.7,
  "efficiency_ratio": 0.409,
  "specific_energy_kwh_m3": 0.444,
  "efficiency_rating": "poor",
  "degradation_percentage": 59.1,
  "maintenance_recommended": true,
  "recommendations": [
    "CRITICAL: Efficiency below 70% of rated - pump rebuild or replacement should be evaluated"
  ]
}
```

### GET /energy/summary

Get energy management dashboard summary.

**Response:**
```json
{
  "period_days": 30,
  "total_energy_kwh": 45000.0,
  "total_cost_usd": 5400.0,
  "average_efficiency": 0.68,
  "peak_demand_kw": 125.0,
  "off_peak_usage_percentage": 42.0,
  "potential_savings_usd": 810.0,
  "savings_percentage": 15.0
}
```

### GET /energy/pumps

List all pumps in the system.

**Response:**
```json
[
  {
    "pump_id": "PUMP-001",
    "name": "Main Well Pump",
    "status": "running",
    "current_efficiency": 0.72,
    "runtime_hours_today": 8.5
  },
  ...
]
```

---

## Compliance

### GET /compliance/obligations

List compliance obligations.

**Query Parameters:**
- `status` (string): Filter by status (pending, completed, overdue)
- `category` (string): Filter by category
- `due_within_days` (int): Filter by due date

**Response:**
```json
[
  {
    "id": "OBL-001",
    "title": "Monthly Coliform Sampling",
    "description": "Collect and submit total coliform samples",
    "regulation": "EPA SDWA 40 CFR 141.21",
    "category": "monitoring",
    "frequency": "Monthly",
    "due_date": "2024-01-15",
    "status": "pending",
    "responsible_party": "Operator"
  },
  ...
]
```

### POST /compliance/obligations

Create a new obligation.

**Request:**
```json
{
  "title": "Quarterly DBP Sampling",
  "description": "Disinfection byproduct monitoring",
  "regulation": "EPA SDWA 40 CFR 141.132",
  "category": "monitoring",
  "frequency": "Quarterly",
  "due_date": "2024-03-31",
  "responsible_party": "Operator"
}
```

### PATCH /compliance/obligations/{obligation_id}

Update obligation status.

**Request:**
```json
{
  "status": "completed",
  "completion_date": "2024-01-14",
  "notes": "Samples submitted to lab"
}
```

### POST /compliance/reports/generate

Generate a compliance report.

**Request:**
```json
{
  "report_type": "CCR",
  "period_start": "2023-01-01",
  "period_end": "2023-12-31",
  "include_supporting_data": true
}
```

**Response:**
```json
{
  "report_id": "CCR-20240115103000",
  "report_type": "CCR",
  "title": "Consumer Confidence Report 2023",
  "period_start": "2023-01-01",
  "period_end": "2023-12-31",
  "generated_at": "2024-01-15T10:30:00Z",
  "sections": [...],
  "compliance_status": "compliant",
  "violations_count": 0,
  "format": "pdf"
}
```

### POST /compliance/risk-assessment

Calculate compliance risk score.

**Response:**
```json
{
  "assessment_date": "2024-01-15T10:30:00Z",
  "overall_risk_score": 35.5,
  "overall_risk_level": "medium",
  "category_risks": [...],
  "total_obligations": 24,
  "completed_obligations": 18,
  "pending_obligations": 4,
  "overdue_obligations": 2,
  "compliance_percentage": 91.7,
  "recommendations": [
    "2 overdue obligations require immediate attention"
  ]
}
```

### GET /compliance/summary

Get compliance dashboard summary.

**Response:**
```json
{
  "total_obligations": 24,
  "completed": 18,
  "pending": 4,
  "overdue": 2,
  "due_this_week": 1,
  "due_this_month": 3,
  "compliance_score": 85.0,
  "risk_level": "low",
  "last_violation_days_ago": 180
}
```

---

## Data Ingestion

### POST /data/manual-reading

Submit a single manual meter reading.

**Request:**
```json
{
  "meter_id": "PROD-001",
  "reading_value": 175250.0,
  "reading_date": "2024-01-15T08:00:00Z",
  "reading_type": "production",
  "notes": "Monthly read"
}
```

### POST /data/manual-readings/batch

Submit multiple readings at once.

**Request:**
```json
{
  "readings": [
    {
      "meter_id": "PROD-001",
      "reading_value": 175250.0,
      "reading_date": "2024-01-15T08:00:00Z",
      "reading_type": "production"
    },
    ...
  ],
  "source": "manual_entry"
}
```

### POST /data/upload/csv

Upload CSV file with meter readings.

**Request:**
- Content-Type: multipart/form-data
- File: CSV file
- Query param: `data_type` (meter_readings, production, billing)

### GET /data/sources

List configured data sources.

**Response:**
```json
[
  {
    "id": "SRC-001",
    "type": "manual",
    "name": "Manual Entry",
    "enabled": true,
    "status": "active",
    "last_data": "2024-01-15T10:30:00Z"
  },
  ...
]
```

### GET /data/status

Get data ingestion status.

**Response:**
```json
{
  "status": "healthy",
  "active_sources": 2,
  "records_today": 1450,
  "last_ingestion": "2024-01-15T10:30:00Z",
  "errors_last_24h": 0,
  "data_freshness": {
    "production_meters": "5 minutes ago",
    "customer_meters": "Monthly - due in 15 days"
  }
}
```

---

## Error Responses

All endpoints return errors in a consistent format:

```json
{
  "detail": "Error message describing what went wrong",
  "type": "ValidationError"
}
```

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Missing or invalid token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 422 | Validation Error - Input validation failed |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |

---

## Rate Limiting

- Default: 60 requests per minute
- Burst: 10 requests
- Headers returned:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

