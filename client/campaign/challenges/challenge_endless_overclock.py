"""
Sentinel Grid Challenge Rule: Overclocked Surge
Both player towers and enemies have 100% higher speed
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ChallengeModifiers:
    challenge_id: str = "challenge_endless_overclock"
    title: str = "Overclocked Surge"
    description: str = "Both player towers and enemies have 100% higher speed"
    credit_multiplier: float = 1.0
    energy_multiplier: float = 1.0
    enemy_speed_multiplier: float = 1.0
    tower_range_multiplier: float = 1.0
    tower_damage_multiplier: float = 1.0
    base_hp_override: float = 100.0
    allowed_archetypes: list = None

    def apply_to_simulation(self, kernel_config: Dict[str, Any]) -> Dict[str, Any]:
        cfg = dict(kernel_config)
        cfg["credit_mult"] = self.credit_multiplier
        cfg["energy_mult"] = self.energy_multiplier
        cfg["enemy_speed_mult"] = self.enemy_speed_multiplier
        cfg["damage_mult"] = self.tower_damage_multiplier
        return cfg
