# Mathematical Models

This document describes the mathematical models and algorithms used in the RWA platform.

## Non-Revenue Water (NRW) Models

### IWA Water Balance

The International Water Association (IWA) water balance is the foundation for NRW analysis.

#### Water Balance Hierarchy

```
System Input Volume (SIV)
├── Authorized Consumption (AC)
│   ├── Billed Authorized Consumption (Revenue Water)
│   │   ├── Billed Metered Consumption
│   │   └── Billed Unmetered Consumption
│   └── Unbilled Authorized Consumption
│       ├── Unbilled Metered Consumption
│       └── Unbilled Unmetered Consumption
└── Water Losses
    ├── Apparent Losses
    │   ├── Unauthorized Consumption
    │   └── Metering Inaccuracies
    └── Real Losses
        ├── Leakage on Transmission/Distribution Mains
        ├── Leakage and Overflows at Storage
        └── Leakage on Service Connections
```

#### Equations

**Non-Revenue Water (NRW):**
$$NRW = SIV - Billed\ Authorized\ Consumption$$

**NRW Percentage:**
$$NRW\% = \frac{NRW}{SIV} \times 100$$

**Water Losses:**
$$Water\ Losses = SIV - Authorized\ Consumption$$

**Real Losses:**
$$Real\ Losses = Water\ Losses - Apparent\ Losses$$

---

### Infrastructure Leakage Index (ILI)

ILI provides a performance benchmark independent of system characteristics.

$$ILI = \frac{CARL}{UARL}$$

Where:
- **CARL** = Current Annual Real Losses (L/day or m³/year)
- **UARL** = Unavoidable Annual Real Losses (L/day)

#### UARL Formula

$$UARL = (18 \times L_m + 0.8 \times N_c + 25 \times L_p) \times P$$

Where:
- $L_m$ = Length of mains (km)
- $N_c$ = Number of service connections
- $L_p$ = Total length of service connections (km)
- $P$ = Average operating pressure (m)

#### ILI Performance Bands

| ILI Range | Performance | Description |
|-----------|-------------|-------------|
| < 2.0 | Excellent | World-class performance |
| 2.0 - 4.0 | Good | Well-managed system |
| 4.0 - 8.0 | Average | Typical performance |
| > 8.0 | Poor | Significant improvement potential |

---

### Minimum Night Flow (MNF) Analysis

MNF identifies background leakage during low-consumption periods.

#### MNF Calculation

$$MNF = min(Q_{night})$$

Typically analyzed during the night window (2:00 AM - 4:00 AM).

#### Background Leakage Estimation

$$Background\ Leakage = MNF - Legitimate\ Night\ Use$$

**Legitimate Night Use:**
$$LNU = N_c \times q_{night}$$

Where:
- $N_c$ = Number of service connections
- $q_{night}$ = Estimated night use per connection (typically 1-6 L/h)

#### Night-Day Factor

For daily leakage extrapolation:
$$Daily\ Leakage \approx Background\ Leakage \times 24 \times NDF$$

Where NDF (Night-Day Factor) accounts for pressure variation, typically 1.1-1.3.

---

### Leak Detection Indicators

#### Leakage Rate per Kilometer

$$Leakage\ Rate = \frac{Daily\ Leakage\ (m³)}{Pipe\ Length\ (km)}$$

**Benchmark:** < 10 m³/km/day is generally acceptable.

#### Leakage per Connection

$$L_{pc} = \frac{Annual\ Real\ Losses}{N_c \times 365}$$

Units: L/connection/day

---

## Energy Management Models

### Pump Hydraulics

#### Hydraulic Power (Water Power)

$$P_{hydraulic} = \rho \times g \times Q \times H$$

Where:
- $\rho$ = Water density (1000 kg/m³)
- $g$ = Gravitational acceleration (9.81 m/s²)
- $Q$ = Flow rate (m³/s)
- $H$ = Total head (m)

In practical units:
$$P_{hydraulic} (kW) = \frac{Q (m³/h) \times H (m)}{367.2}$$

#### Wire-to-Water Efficiency

$$\eta_{w2w} = \frac{P_{hydraulic}}{P_{electrical}}$$

Where $P_{electrical}$ is the electrical power input (kW).

#### Total Dynamic Head

$$TDH = H_{discharge} - H_{suction} + h_f$$

Where:
- $H_{discharge}$ = Discharge pressure head (m)
- $H_{suction}$ = Suction pressure head (m)
- $h_f$ = Friction losses (m)

---

### Pump Affinity Laws

For variable speed pumps:

$$\frac{Q_2}{Q_1} = \frac{N_2}{N_1}$$

$$\frac{H_2}{H_1} = \left(\frac{N_2}{N_1}\right)^2$$

$$\frac{P_2}{P_1} = \left(\frac{N_2}{N_1}\right)^3$$

Where:
- $Q$ = Flow rate
- $H$ = Head
- $P$ = Power
- $N$ = Rotational speed (RPM)

---

### Specific Energy

Energy per unit volume of water pumped:

$$SE = \frac{Energy\ (kWh)}{Volume\ (m³)}$$

Or from operating parameters:
$$SE = \frac{P_{electrical}}{Q} = \frac{H}{367.2 \times \eta_{w2w}}$$

**Typical ranges:**
- Groundwater: 0.2 - 0.6 kWh/m³
- Distribution boosting: 0.1 - 0.3 kWh/m³

---

### Pump Schedule Optimization

#### Objective Function

Minimize total energy cost:
$$\min \sum_{t=1}^{24} C_t \times P \times x_t$$

Where:
- $C_t$ = Electricity rate at hour $t$ ($/kWh)
- $P$ = Pump power (kW)
- $x_t$ = Binary decision (0 or 1) for pump operation at hour $t$

#### Constraints

**Tank level constraint:**
$$V_{min} \leq V_t \leq V_{max}\ \ \forall t$$

**Tank continuity:**
$$V_{t+1} = V_t + Q_p \times x_t - D_t$$

Where:
- $V_t$ = Tank volume at hour $t$
- $Q_p$ = Pump flow rate (m³/h)
- $D_t$ = Demand at hour $t$ (m³/h)

**Minimum runtime (optional):**
$$\sum_{t=1}^{24} x_t \geq T_{min}$$

---

### Demand Charge Optimization

Monthly demand charge:
$$DC = P_{peak} \times R_D$$

Where:
- $P_{peak}$ = Peak 15-minute demand (kW)
- $R_D$ = Demand rate ($/kW)

Optimization target: Schedule pump starts to avoid coinciding with system peaks.

---

## Compliance Models

### Risk Scoring

#### Category Risk Score

$$R_{cat} = w_o \times \frac{N_{overdue}}{N_{total}} + w_p \times \frac{N_{pending}}{N_{total}} + w_c \times (1 - \frac{N_{completed}}{N_{total}})$$

Where:
- $w_o$ = Overdue weight (e.g., 0.5)
- $w_p$ = Pending weight (e.g., 0.3)
- $w_c$ = Completion weight (e.g., 0.2)

#### Overall Risk Score

$$R_{overall} = \sum_{i} w_i \times R_{cat,i} + penalty_{critical}$$

Where:
- $w_i$ = Category importance weight
- $penalty_{critical}$ = Additional score for critical-risk categories

#### Risk Level Mapping

| Score Range | Level |
|-------------|-------|
| 0 - 25 | Low |
| 25 - 50 | Medium |
| 50 - 75 | High |
| 75 - 100 | Critical |

---

## Statistical Methods

### Trend Analysis

#### Simple Linear Regression

For MNF trend detection:
$$y = mx + b$$

Where:
$$m = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2}$$
$$b = \bar{y} - m\bar{x}$$

**Interpretation:**
- $m > 0.01$: Increasing trend (potential developing leak)
- $|m| < 0.01$: Stable
- $m < -0.01$: Decreasing trend (improving)

### Anomaly Detection

#### Z-Score Method

$$z = \frac{x - \mu}{\sigma}$$

**Alert threshold:** $|z| > 2$ (95% confidence) or $|z| > 3$ (99% confidence)

#### Moving Average

$$MA_n = \frac{1}{n} \sum_{i=0}^{n-1} x_{t-i}$$

Anomaly when: $|x_t - MA_n| > k \times \sigma_{MA}$

---

## Unit Conversions

### Volume

| From | To | Multiply by |
|------|-----|-------------|
| m³ | gallons | 264.172 |
| gallons | m³ | 0.003785 |
| MGD | m³/day | 3,785.41 |
| m³/h | GPM | 4.403 |

### Pressure

| From | To | Multiply by |
|------|-----|-------------|
| meters | psi | 1.422 |
| psi | meters | 0.703 |
| bar | meters | 10.197 |

### Power

| From | To | Multiply by |
|------|-----|-------------|
| kW | HP | 1.341 |
| HP | kW | 0.746 |

---

## References

1. IWA Water Loss Task Force. "Assessing Non-Revenue Water and Its Components."
2. AWWA M36. "Water Audits and Loss Control Programs."
3. Hydraulic Institute. "Pump Standards."
4. EPA. "Energy Use in Water and Wastewater Utilities."

