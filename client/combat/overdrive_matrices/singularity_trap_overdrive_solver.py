"""
Overdrive Supercharge Solver: SINGULARITY_TRAP
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class OverdriveDischargeState:
    is_overdriven: bool
    damage_boost_mult: float
    firerate_boost_mult: float
    energy_consumption_per_sec: float
    heat_dissipation_factor: float

class SingularityTrapOverdriveSolver:
    def __init__(self):
        self.tower_id: str = "singularity_trap"
        self.nominal_power_mw: float = 15.299999999999999

    def activate_overdrive(self, current_energy: float) -> OverdriveDischargeState:
        can_boost = current_energy >= 25.0
        return OverdriveDischargeState(
            is_overdriven=can_boost,
            damage_boost_mult=1.65 if can_boost else 1.0,
            firerate_boost_mult=1.40 if can_boost else 1.0,
            energy_consumption_per_sec=5.0 if can_boost else 0.0,
            heat_dissipation_factor=0.85
        )
