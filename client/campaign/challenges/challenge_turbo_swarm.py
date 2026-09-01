"""
Sentinel Grid Challenge Rule: Hyperspeed Swarm
All enemies move 75% faster
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ChallengeModifiers:
    challenge_id: str = "challenge_turbo_swarm"
    title: str = "Hyperspeed Swarm"
    description: str = "All enemies move 75% faster"
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
