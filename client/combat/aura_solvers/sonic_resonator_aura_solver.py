"""
Commander Tactical Aura & Spatial Resonance Solver: SONIC_RESONATOR
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class AuraResonanceState:
    tower_id: str
    aura_radius: float
    efficiency_bonus_pct: float
    energy_regeneration_buff: float
    max_stacked_allies: int

class SonicResonatorAuraSolver:
    def __init__(self):
        self.tower_id: str = "sonic_resonator"
        self.base_radius: float = 180.0

    def compute_aura_effect(self, ally_count_in_range: int) -> AuraResonanceState:
        eff = min(35.0, ally_count_in_range * 3.5)
        return AuraResonanceState(
            tower_id=self.tower_id,
            aura_radius=self.base_radius,
            efficiency_bonus_pct=round(eff, 1),
            energy_regeneration_buff=round(ally_count_in_range * 0.4, 2),
            max_stacked_allies=8
        )
