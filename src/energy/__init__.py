"""Energy Management Module.

This module provides tools for optimizing energy consumption
in water system operations, with focus on pump scheduling
and efficiency monitoring.

Key components:
- Pump Scheduling: Time-of-use rate optimization
- Efficiency Analysis: Wire-to-water efficiency monitoring
- Cost Optimization: Demand charge and rate structure analysis
"""

from src.energy.cost_optimization import CostAnalysis, EnergyCostInput, analyze_energy_costs
from src.energy.efficiency_analysis import (
    EfficiencyReport,
    PumpEfficiencyInput,
    analyze_pump_efficiency,
)
from src.energy.pump_scheduling import (
    PumpSchedule,
    ScheduleOptimizationRequest,
    optimize_pump_schedule,
)

__all__ = [
    "PumpSchedule",
    "ScheduleOptimizationRequest",
    "optimize_pump_schedule",
    "EfficiencyReport",
    "PumpEfficiencyInput",
    "analyze_pump_efficiency",
    "CostAnalysis",
    "EnergyCostInput",
    "analyze_energy_costs",
]

