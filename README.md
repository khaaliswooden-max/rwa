# RWA — Rural Water Association Digital Transformation Platform

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![CI](https://github.com/khaaliswooden-max/rwa/workflows/CI/badge.svg)](https://github.com/khaaliswooden-max/rwa/actions)
[![codecov](https://codecov.io/gh/khaaliswooden-max/rwa/branch/main/graph/badge.svg)](https://codecov.io/gh/khaaliswooden-max/rwa)

> Empowering small rural water systems with data-driven operations through Non-Revenue Water optimization, Energy management, and Compliance automation.

---

## Problem Statement

America's 50,000+ small rural water systems face a perfect storm of challenges:

- **Aging infrastructure** with limited capital for replacement
- **Staffing constraints** — most operate with fewer than 2 full-time employees
- **Data scarcity** — minimal SCADA, sporadic meter readings, paper-based records
- **Regulatory pressure** — EPA Safe Drinking Water Act compliance with enterprise-level expectations
- **Financial stress** — operating budgets of $100-200K must cover everything

Large utilities have sophisticated asset management, real-time analytics, and dedicated compliance teams. Rural systems have spreadsheets, intuition, and overworked operators juggling treatment, distribution, billing, and regulatory reporting.

**RWA bridges this gap** with purpose-built tools designed for the constraints of small systems.

---

## Solution Overview

RWA delivers three integrated domains targeting the highest-impact operational challenges:

### 🚰 Non-Revenue Water (NRW) Optimization
Reduce water losses through systematic identification of real losses (leaks, breaks) and apparent losses (meter inaccuracies, theft). Uses IWA water balance methodology adapted for limited instrumentation.

### ⚡ Energy Management
Optimize pump scheduling around time-of-use rates and demand charges. Model pump efficiency degradation. Target 15-30% energy cost reduction without capital investment.

### 📋 Compliance Automation
Track regulatory obligations, automate report generation, and provide early warning on compliance risks. Transform reactive scrambling into proactive management.

---

## Key Features

- **MVRI-First Design** — Built for Minimum Viable RWA Infrastructure (500-2,000 connections)
- **Graceful Data Degradation** — Works with monthly manual reads, improves with AMI/SCADA
- **First-Principles Models** — Transparent physics-based calculations, not black-box ML
- **Regulatory Mapping** — EPA SDWA obligations pre-loaded with state-specific variants
- **Offline Capability** — Core functions work without constant connectivity
- **Progressive Enhancement** — Start simple, add complexity as capacity grows
- **Open Architecture** — Standard APIs, no vendor lock-in
- **Operator-Centric UX** — Designed for non-technical staff with limited time

---

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL 15+ with TimescaleDB extension

### Installation

```bash
# Clone the repository
git clone https://github.com/khaaliswooden-max/rwa.git
cd rwa

# Set up Python environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Set up frontend
cd frontend
npm install
cd ..

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Initialize database
python scripts/init_db.py

# Run development servers
python -m uvicorn api.main:app --reload  # Backend on :8000
cd frontend && npm run dev               # Frontend on :3000
```

---

## Architecture Overview

RWA follows a modular monolith architecture optimized for small-team maintenance:

```
┌─────────────────────────────────────────────────────────────┐
│                      React Frontend                         │
│              (Dashboard, Reports, Configuration)            │
└─────────────────────────┬───────────────────────────────────┘
                          │ REST API
┌─────────────────────────▼───────────────────────────────────┐
│                     API Gateway                             │
│              (FastAPI, Authentication, Rate Limiting)       │
└──────┬──────────────────┬──────────────────┬────────────────┘
       │                  │                  │
┌──────▼──────┐   ┌───────▼───────┐   ┌──────▼──────┐
│ NRW Module  │   │ Energy Module │   │ Compliance  │
│             │   │               │   │   Module    │
│ - Water     │   │ - Pump        │   │ - Obligation│
│   Balance   │   │   Scheduling  │   │   Tracking  │
│ - Leak      │   │ - Efficiency  │   │ - Report    │
│   Detection │   │   Analysis    │   │   Generation│
│ - MNF       │   │ - Cost        │   │ - Risk      │
│   Analysis  │   │   Optimization│   │   Scoring   │
└──────┬──────┘   └───────┬───────┘   └──────┬──────┘
       │                  │                  │
┌──────▼──────────────────▼──────────────────▼────────────────┐
│                    Data Ingestion Layer                     │
│         (SCADA Connectors, AMI Import, Manual Entry)        │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                      Data Store                             │
│     PostgreSQL (Relational) + TimescaleDB (Time-Series)     │
└─────────────────────────────────────────────────────────────┘
```

For detailed architecture documentation, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## Documentation

| Document | Description |
|----------|-------------|
| [Architecture](docs/ARCHITECTURE.md) | System design, components, data flow |
| [Deployment](docs/DEPLOYMENT.md) | Installation, configuration, production setup |
| [API Reference](docs/API.md) | REST endpoints, authentication, examples |
| [MVRI Specification](docs/MVRI-SPECIFICATION.md) | Minimum Viable RWA Infrastructure definition |
| [Mathematical Models](docs/MATHEMATICAL-MODELS.md) | Domain equations and algorithms |

---

## Contributing

We welcome contributions! Please read our [Contributing Guide](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) before submitting issues or pull requests.

### Development Priorities

1. **Core domain logic** — NRW, Energy, Compliance calculations
2. **Data connectors** — SCADA/AMI integrations for common systems
3. **Compliance templates** — State-specific regulatory mappings
4. **Documentation** — Operator guides, case studies

---

## License

This project is licensed under the Apache License 2.0 — see the [LICENSE](LICENSE) file for details.

Copyright 2025 Visionblox LLC / Zuup Innovation Labs

---

## Acknowledgments

- International Water Association (IWA) for water loss methodology frameworks
- EPA Office of Water for regulatory guidance
- Rural water operators who shared their challenges and validated our approach

---

## Contact

- **Project Lead:** [khaaliswooden-max](https://github.com/khaaliswooden-max)
- **Organization:** [Visionblox LLC](https://visionblox.io)
- **Security Issues:** security@visionblox.io
- **General Inquiries:** hello@visionblox.io

