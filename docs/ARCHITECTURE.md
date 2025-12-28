# RWA Architecture

This document describes the system architecture of the Rural Water Association (RWA) Digital Transformation Platform.

## Overview

RWA follows a **modular monolith** architecture, optimized for small-team maintenance while providing clear module boundaries for potential future decomposition.

```
┌─────────────────────────────────────────────────────────────────┐
│                       React Frontend                            │
│              (Dashboard, Reports, Configuration)                │
└──────────────────────────┬──────────────────────────────────────┘
                           │ REST API (JSON)
┌──────────────────────────▼──────────────────────────────────────┐
│                       API Gateway                               │
│         (FastAPI, Authentication, Rate Limiting, CORS)          │
└───────┬──────────────────┬──────────────────┬───────────────────┘
        │                  │                  │
┌───────▼───────┐  ┌───────▼───────┐  ┌───────▼───────┐
│  NRW Module   │  │ Energy Module │  │  Compliance   │
│               │  │               │  │    Module     │
│ • Water       │  │ • Pump        │  │ • Obligation  │
│   Balance     │  │   Scheduling  │  │   Tracking    │
│ • Leak        │  │ • Efficiency  │  │ • Report      │
│   Detection   │  │   Analysis    │  │   Generation  │
│ • MNF         │  │ • Cost        │  │ • Risk        │
│   Analysis    │  │   Optimization│  │   Scoring     │
└───────┬───────┘  └───────┬───────┘  └───────┬───────┘
        │                  │                  │
┌───────▼──────────────────▼──────────────────▼───────────────────┐
│                    Data Ingestion Layer                         │
│          (SCADA Connectors, AMI Import, Manual Entry)           │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                        Data Store                               │
│        PostgreSQL (Relational) + TimescaleDB (Time-Series)      │
└─────────────────────────────────────────────────────────────────┘
```

## Design Principles

### 1. MVRI-First Design

**Minimum Viable RWA Infrastructure (MVRI)** targets systems with:
- 500–2,000 service connections
- 1–2 operators
- Limited or no SCADA
- Monthly manual meter reads

Every feature must work with minimal data and degrade gracefully as data availability decreases.

### 2. Graceful Data Degradation

| Data Level | Available Features |
|------------|-------------------|
| **Full SCADA/AMI** | Real-time leak detection, hourly optimization, predictive maintenance |
| **Daily Reads** | Daily water balance, basic leak indicators, daily pump scheduling |
| **Monthly Reads** | Monthly water balance, trend analysis, compliance tracking |
| **Manual Only** | Basic water balance, obligation tracking, manual entry |

### 3. First-Principles Models

All calculations use transparent, physics-based models rather than black-box ML:
- IWA water balance methodology
- Pump affinity laws
- Hydraulic calculations

Benefits:
- Explainable results
- Works with limited data
- Auditable for compliance
- No training data required

### 4. Offline Capability

Core functions work without constant connectivity:
- Local data caching
- Queued synchronization
- Offline-first PWA design

## Technology Stack

### Backend

| Component | Technology | Purpose |
|-----------|------------|---------|
| Framework | FastAPI | High-performance async Python web framework |
| Database | PostgreSQL 15+ | Primary relational database |
| Time-Series | TimescaleDB | Efficient time-series data storage |
| Authentication | JWT (python-jose) | Stateless authentication tokens |
| ORM | SQLAlchemy 2.0 | Database abstraction |
| Validation | Pydantic v2 | Data validation and serialization |
| Task Queue | APScheduler | Background job scheduling |

### Frontend

| Component | Technology | Purpose |
|-----------|------------|---------|
| Framework | React 18 | UI component library |
| Language | TypeScript | Type-safe JavaScript |
| Build Tool | Vite | Fast development and builds |
| Styling | Tailwind CSS | Utility-first CSS |
| Charts | Recharts | Data visualization |
| State | React Query | Server state management |
| Forms | React Hook Form | Form handling |

### Infrastructure

| Component | Technology | Purpose |
|-----------|------------|---------|
| Containerization | Docker | Consistent deployment |
| Orchestration | Docker Compose | Local development |
| CI/CD | GitHub Actions | Automated testing and deployment |
| Monitoring | Structured logging | Application observability |

## Module Details

### NRW (Non-Revenue Water) Module

**Purpose**: Reduce water losses through systematic identification and quantification.

**Key Components**:
- `water_balance.py`: IWA-standard water balance calculations
- `leak_detection.py`: Leak indicator analysis and prioritization
- `mnf_analysis.py`: Minimum Night Flow leakage estimation

**Data Flow**:
```
Meter Readings → Water Balance → Loss Analysis → Recommendations
                      ↓
              ILI Calculation → Benchmarking
```

### Energy Module

**Purpose**: Optimize pump operations for energy cost reduction.

**Key Components**:
- `pump_scheduling.py`: Time-of-use rate optimization
- `efficiency_analysis.py`: Wire-to-water efficiency monitoring
- `cost_optimization.py`: Demand charge and rate analysis

**Data Flow**:
```
SCADA/Meter Data → Pump Status → Efficiency Analysis → Recommendations
        ↓
Rate Schedule → Demand Forecast → Schedule Optimization → Control Output
```

### Compliance Module

**Purpose**: Track regulatory obligations and automate reporting.

**Key Components**:
- `obligation_tracking.py`: Deadline and requirement management
- `report_generation.py`: Automated regulatory reports
- `risk_scoring.py`: Proactive compliance risk assessment

**Data Flow**:
```
Regulatory Requirements → Obligation Database → Calendar/Alerts
        ↓
Operational Data → Report Generation → Regulatory Submission
```

## Data Model

### Core Entities

```
WaterSystem (1) ─── (N) User
     │
     ├── (N) MeterReading    [TimescaleDB hypertable]
     ├── (N) SCADAData       [TimescaleDB hypertable]
     ├── (N) Pump
     ├── (N) Obligation
     └── (N) EnergyUsage
```

### Time-Series Storage

TimescaleDB hypertables are used for:
- `meter_readings`: Production and distribution meter data
- `scada_data`: SCADA telemetry points

Benefits:
- Automatic partitioning by time
- Efficient time-range queries
- Built-in compression
- Continuous aggregates

## API Design

### REST Conventions

- Base URL: `/api/v1`
- Resource-based URLs: `/api/v1/nrw/water-balance`
- HTTP methods: GET (read), POST (create/calculate), PATCH (update), DELETE (remove)
- JSON request/response bodies
- JWT Bearer authentication

### Authentication Flow

```
1. POST /api/v1/auth/login (email, password)
      ↓
2. Receive {access_token, refresh_token}
      ↓
3. Include "Authorization: Bearer {access_token}" in requests
      ↓
4. POST /api/v1/auth/refresh when access token expires
```

### Rate Limiting

- Default: 60 requests/minute
- Burst: 10 requests
- Per-user tracking

## Security

### Authentication
- JWT tokens with configurable expiration
- bcrypt password hashing
- Refresh token rotation

### Authorization
- Role-based access control (RBAC)
- Roles: admin, manager, operator
- Resource-level permissions

### Data Protection
- HTTPS required in production
- Parameterized database queries
- Input validation on all endpoints
- CORS restricted to frontend origin

## Deployment

### Development
```bash
# Backend
python -m uvicorn api.main:app --reload

# Frontend  
cd frontend && npm run dev
```

### Production
- Docker containers
- PostgreSQL with TimescaleDB
- Reverse proxy (nginx/Caddy)
- HTTPS with valid certificates
- Environment-based configuration

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## Future Considerations

### Potential Enhancements
- GraphQL API for complex queries
- WebSocket for real-time updates
- Mobile app (React Native)
- Multi-tenant SaaS mode

### Scalability Path
- Module extraction to microservices
- Message queue for async processing
- Read replicas for reporting
- CDN for static assets

