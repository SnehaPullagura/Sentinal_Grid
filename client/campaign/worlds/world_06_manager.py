"""
Campaign World 06 Environmental Manager & Narrative Arc.
Regulates global atmospheric modifiers, radiation storms, orbital jamming,
and strategic unlocked tech nodes for World 06.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class EnvironmentalModifier:
    name: str
    description: str
    energy_recharge_multiplier: float = 1.0
    speed_multiplier: float = 1.0
    hazard_damage_per_sec: float = 0.0

class World06Manager:
    def __init__(self):
        self.world_id: str = "world_06"
        self.name: str = "Sector World 06 - Core Frontier"
        self.environment: EnvironmentalModifier = EnvironmentalModifier(
            name="Atmospheric Ionization",
            description="High radiation speeds up shield recharge by 20%",
            energy_recharge_multiplier=1.20
        )
        self.levels: List[str] = [f"mission_{(w-1)*5 + l:02d}" for l in range(1, 6)]

    def get_world_status(self) -> dict:
        return {
            "world_id": self.world_id,
            "name": self.name,
            "total_levels": len(self.levels),
            "environment": self.environment.name
        }
