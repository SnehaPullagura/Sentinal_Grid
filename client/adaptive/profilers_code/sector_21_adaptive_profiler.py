"""
Sector 21 Adaptive Defense Profiler & Counter-Wave Engine.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class DefensePostureProfile:
    kinetic_weight: float
    energy_weight: float
    control_weight: float
    recommended_threat_counter: str
    target_budget_mult: float

class Sector21AdaptiveProfiler:
    def __init__(self):
        self.sector_id: str = "sector_21"
        self.historical_postures: List[DefensePostureProfile] = []

    def evaluate_defense_posture(self, kinetic_dmg: float, energy_dmg: float, control_count: int) -> DefensePostureProfile:
        total = max(1.0, kinetic_dmg + energy_dmg)
        k_ratio = kinetic_dmg / total
        e_ratio = energy_dmg / total
        c_weight = min(1.0, control_count * 0.1)

        counter = "ARMORED_VANGUARD" if k_ratio > 0.6 else "PHASE_DISRUPTOR" if e_ratio > 0.6 else "AERO_SWARM"
        profile = DefensePostureProfile(
            kinetic_weight=round(k_ratio, 2),
            energy_weight=round(e_ratio, 2),
            control_weight=round(c_weight, 2),
            recommended_threat_counter=counter,
            target_budget_mult=1.15 if total > 2000.0 else 1.0
        )
        self.historical_postures.append(profile)
        return profile
