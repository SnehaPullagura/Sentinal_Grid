"""
Sector 19 Challenge Scenario Evaluator & Modifier Matrix.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional

@dataclass
class ChallengeModifier:
    mod_id: str
    name: str
    enemy_speed_mult: float
    enemy_hp_mult: float
    tower_cost_mult: float
    energy_decay_rate: float

class Sector19ChallengeEvaluator:
    def __init__(self):
        self.sector_id: str = "sector_19"
        self.challenge_name: str = "IRON_MAN_CRUCIBLE_19"
        self.modifiers: List[ChallengeModifier] = [
            ChallengeModifier("SPEED_SURGE", "Kinetic Overdrive", 1.25, 0.90, 1.0, 0.0),
            ChallengeModifier("ARMORED_CONVOY", "Nanite Reinforced Plating", 0.85, 1.45, 1.10, 0.0),
            ChallengeModifier("ENERGY_DROUGHT", "Plasma Core Drain", 1.0, 1.0, 1.20, 0.05)
        ]

    def get_aggregate_difficulty(self) -> float:
        return round(1.0 + (19 * 0.08), 2)
