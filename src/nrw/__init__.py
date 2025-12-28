"""Non-Revenue Water (NRW) Module.

This module implements IWA water balance methodology for identifying
and quantifying water losses in distribution systems.

Key components:
- Water Balance: IWA-standard water balance calculations
- Leak Detection: Analysis of leak indicators and prioritization
- MNF Analysis: Minimum Night Flow analysis for background leakage estimation
"""

from src.nrw.leak_detection import LeakAnalysis, analyze_leak_indicators
from src.nrw.mnf_analysis import MNFResult, analyze_minimum_night_flow
from src.nrw.water_balance import WaterBalance, WaterBalanceInput, calculate_water_balance

__all__ = [
    "WaterBalance",
    "WaterBalanceInput",
    "calculate_water_balance",
    "LeakAnalysis",
    "analyze_leak_indicators",
    "MNFResult",
    "analyze_minimum_night_flow",
]

