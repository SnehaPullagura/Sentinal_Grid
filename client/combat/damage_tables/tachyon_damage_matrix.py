"""
Combat Damage Matrix Table: TACHYON
Defines effectiveness coefficients, damage mitigation formulas, and status procs
against all classified enemy defensive armor and shielding layers.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict

@dataclass
class TachyonDamageProfile:
    damage_type: str = "tachyon"
    base_armor_penetration: float = 0.15
    critical_multiplier_bonus: float = 0.25
    environmental_modifier: float = 1.0

    def get_effectiveness_against(self, armor_class: str) -> float:
        matrix: Dict[str, float] = {
            "unarmored": 1.25,
            "light_kevlar": 1.10,
            "heavy_plating": 0.75 if "tachyon" == "kinetic" else 1.20,
            "reactive_composite": 0.85,
            "energy_shield": 0.50 if "tachyon" == "kinetic" else 1.50,
            "phase_barrier": 0.60 if "tachyon" != "quantum" else 2.00,
            "nanite_mesh": 0.90,
            "dreadnought_hull": 0.70
        }
        return matrix.get(armor_class, 1.0) * self.environmental_modifier

    def calculate_mitigated_damage(self, incoming_damage: float, armor_rating: float, armor_class: str) -> float:
        eff = self.get_effectiveness_against(armor_class)
        adjusted_armor = max(0.0, armor_rating * (1.0 - self.base_armor_penetration))
        reduction = adjusted_armor / (100.0 + adjusted_armor) if adjusted_armor > 0 else 0.0
        return max(1.0, incoming_damage * eff * (1.0 - reduction))
