# MVRI Specification

**Minimum Viable RWA Infrastructure (MVRI)**

This document defines the minimum infrastructure requirements for effective RWA platform deployment and the expected functionality at each data availability tier.

## Overview

MVRI represents the baseline infrastructure that a rural water system needs to benefit from RWA. The platform is designed to provide value even with minimal data, while unlocking additional capabilities as data richness increases.

## Target System Profile

### Primary Target: Small Community Water Systems

| Characteristic | MVRI Range |
|---------------|------------|
| Service Connections | 500 – 2,000 |
| Population Served | 1,500 – 6,000 |
| Staff | 1 – 2 full-time operators |
| Annual Operating Budget | $100,000 – $300,000 |
| System Type | Community Water System |

### Infrastructure Baseline

| Component | Minimum Requirement |
|-----------|-------------------|
| Production Meters | 1 per source |
| Distribution Meters | Optional (master meter) |
| Customer Meters | 80%+ metered |
| Storage Monitoring | Manual level checks |
| Pressure Monitoring | Optional |
| SCADA | Not required |
| AMI | Not required |
| Internet Connectivity | Periodic (daily minimum) |

---

## Data Availability Tiers

### Tier 1: Manual Only (MVRI Baseline)

**Data Sources:**
- Monthly manual meter reads
- Manual tank level checks
- Paper-based operational logs
- Utility bills for energy data

**Available Functionality:**

| Module | Features |
|--------|----------|
| **NRW** | Monthly water balance, annual trend analysis |
| **Energy** | Monthly cost tracking, basic optimization recommendations |
| **Compliance** | Full obligation tracking, manual report generation |

**Limitations:**
- No leak detection capability
- No pump scheduling optimization
- Monthly data granularity only

---

### Tier 2: Daily Data

**Data Sources:**
- Daily meter reads (manual or AMR drive-by)
- Daily operational logs
- Daily tank level recordings

**Additional Functionality:**

| Module | Enhanced Features |
|--------|-------------------|
| **NRW** | Daily water balance, basic MNF approximation |
| **Energy** | Daily consumption tracking, TOU analysis |
| **Compliance** | Daily parameter tracking |

**Improvements:**
- 30x granularity improvement
- Faster trend detection
- Better anomaly identification

---

### Tier 3: Hourly Data (SCADA/AMI)

**Data Sources:**
- Hourly or sub-hourly SCADA data
- AMI customer meter data
- Real-time tank levels
- Pump run-time monitoring

**Additional Functionality:**

| Module | Enhanced Features |
|--------|-------------------|
| **NRW** | True MNF analysis, zone-level water balance, real-time leak alerts |
| **Energy** | Hourly pump scheduling, demand charge optimization, efficiency trending |
| **Compliance** | Real-time parameter monitoring |

**Improvements:**
- Near real-time operations
- Proactive leak detection
- Optimal pump scheduling
- 15-30% energy savings potential

---

### Tier 4: Full Instrumentation

**Data Sources:**
- Real-time flow at DMAs
- Pressure monitoring network
- Customer-level AMI with hourly reads
- Full SCADA integration

**Additional Functionality:**

| Module | Enhanced Features |
|--------|-------------------|
| **NRW** | District Metered Area analysis, pressure-based leak detection, customer-level leak alerts |
| **Energy** | Predictive pump maintenance, real-time optimization, demand response |
| **Compliance** | Automated sampling reminders, predictive compliance |

---

## Feature Availability Matrix

| Feature | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---------|--------|--------|--------|--------|
| Water Balance Calculation | ✓ Monthly | ✓ Daily | ✓ Hourly | ✓ Real-time |
| NRW Percentage | ✓ | ✓ | ✓ | ✓ |
| ILI Calculation | ✓ Est. | ✓ Est. | ✓ Accurate | ✓ Precise |
| MNF Analysis | ✗ | ◐ Approx | ✓ | ✓ |
| Leak Detection | ✗ | ◐ Basic | ✓ | ✓ DMA-level |
| Real-time Alerts | ✗ | ✗ | ✓ | ✓ |
| Energy Cost Tracking | ✓ Monthly | ✓ Daily | ✓ Hourly | ✓ Real-time |
| Pump Scheduling | ✗ | ◐ Manual | ✓ Optimized | ✓ Automated |
| Efficiency Monitoring | ✗ | ◐ Monthly | ✓ Trending | ✓ Real-time |
| Compliance Tracking | ✓ | ✓ | ✓ | ✓ |
| Automated Reports | ✓ | ✓ | ✓ | ✓ |
| Risk Scoring | ✓ | ✓ | ✓ | ✓ |
| Offline Mode | ✓ | ✓ | ✓ | ◐ |

Legend: ✓ Full | ◐ Partial | ✗ Not Available

---

## MVRI Data Requirements

### Minimum Data for NRW Module

| Data Point | Frequency | Source |
|------------|-----------|--------|
| Total Production | Monthly | Production meter(s) |
| Billed Consumption | Monthly | Billing system |
| Service Connections | Annual | System records |
| Pipe Length | One-time | System mapping |

### Minimum Data for Energy Module

| Data Point | Frequency | Source |
|------------|-----------|--------|
| Energy Consumption | Monthly | Utility bill |
| Pump Inventory | One-time | Asset records |
| Electricity Rates | Annual | Utility rate schedule |

### Minimum Data for Compliance Module

| Data Point | Frequency | Source |
|------------|-----------|--------|
| Regulatory Requirements | One-time | Primacy agency |
| System Classification | One-time | PWSID lookup |
| Monitoring Schedule | Annual | Primacy agency |

---

## Upgrade Path

### Tier 1 → Tier 2

**Investment:** ~$5,000 - $15,000
- Install data logging on production meters
- Implement daily operational log routine
- Configure daily data upload

**ROI Indicators:**
- Faster leak detection (days vs. months)
- More accurate water balance
- Better trend visibility

### Tier 2 → Tier 3

**Investment:** ~$50,000 - $150,000
- SCADA system installation
- AMI meter deployment (gradual)
- Real-time communication infrastructure

**ROI Indicators:**
- 15-30% energy cost reduction
- Proactive leak detection
- Reduced overtime for monitoring

### Tier 3 → Tier 4

**Investment:** ~$100,000 - $500,000+
- District Metered Area establishment
- Pressure monitoring network
- Full AMI deployment
- Advanced analytics

**ROI Indicators:**
- Sub-zone leak localization
- Predictive maintenance
- Customer engagement features

---

## Implementation Recommendations

### Getting Started (Tier 1)

1. **Week 1-2:** Deploy RWA platform
2. **Week 2-3:** Configure system parameters
3. **Week 3-4:** Input historical data
4. **Month 2:** First water balance analysis
5. **Ongoing:** Monthly data entry routine

### Building Foundation (Tier 2)

1. **Month 1:** Install data loggers
2. **Month 2:** Establish daily routine
3. **Month 3:** Baseline daily water balance
4. **Month 4+:** Trend analysis and optimization

### Advanced Operations (Tier 3+)

1. **Planning:** SCADA/AMI vendor selection
2. **Deployment:** Phased installation
3. **Integration:** RWA platform connection
4. **Optimization:** Enable advanced features

---

## Success Metrics by Tier

### Tier 1 Success

- [ ] Monthly water balance calculated
- [ ] NRW percentage tracked
- [ ] All compliance obligations logged
- [ ] Basic energy costs monitored

### Tier 2 Success

- [ ] Daily water balance automated
- [ ] Leak indicators monitored weekly
- [ ] Energy patterns understood
- [ ] Compliance deadlines never missed

### Tier 3 Success

- [ ] MNF < industry benchmark
- [ ] Pump schedule optimized
- [ ] 15%+ energy savings achieved
- [ ] Real-time operational visibility

### Tier 4 Success

- [ ] ILI < 2.0 (world-class)
- [ ] Zero undetected main breaks
- [ ] Predictive maintenance operational
- [ ] Customer-level analytics enabled

---

## Support Resources

- Implementation guide: [DEPLOYMENT.md](DEPLOYMENT.md)
- Technical architecture: [ARCHITECTURE.md](ARCHITECTURE.md)
- API documentation: [API.md](API.md)
- Community support: GitHub Discussions

