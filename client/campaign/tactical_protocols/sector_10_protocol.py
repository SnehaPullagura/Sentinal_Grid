"""
Sector 10 Planetary Defense Tactical Protocol Engine.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class DefenseProtocolDirective:
    code: str
    priority_level: int
    reinforcement_threshold_hp: float
    tactical_behavior: str

class Sector10DefenseProtocol:
    def __init__(self):
        self.sector_id: str = "sector_10"
        self.directives: List[DefenseProtocolDirective] = [
            DefenseProtocolDirective("ALPHA_LOCKDOWN", 1, 0.25, "CONVERGE_DEFENSIVE_FIRE"),
            DefenseProtocolDirective("BETA_OVERDRIVE", 2, 0.50, "ACTIVATE_SURGE_BATTERIES"),
            DefenseProtocolDirective("GAMMA_EVAC", 3, 0.10, "PRIORITIZE_CORE_SURVIVAL")
        ]

    def get_directive_for_integrity(self, hp_ratio: float) -> DefenseProtocolDirective:
        for d in sorted(self.directives, key=lambda x: x.reinforcement_threshold_hp):
            if hp_ratio <= d.reinforcement_threshold_hp:
                return d
        return self.directives[1]
