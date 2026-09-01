from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple

@dataclass
class ArmorPenetrationResult:
    effective_armor: float
    damage_mitigated: float
    final_damage: float
    armor_shred_applied: float

class ArmorPenetrationCalculator:
    @staticmethod
    def calculate(
        raw_damage: float,
        target_armor: float,
        flat_penetration: float = 0.0,
        percent_penetration: float = 0.0,
        armor_shred_percent: float = 0.0
    ) -> ArmorPenetrationResult:
        # Step 1: Apply armor shred
        shredded_armor = max(0.0, target_armor * (1.0 - min(0.85, armor_shred_percent)))
        # Step 2: Apply penetration
        effective_armor = max(0.0, (shredded_armor - flat_penetration) * (1.0 - min(0.9, percent_penetration)))
        # Step 3: Damage reduction formula (100 / (100 + armor))
        damage_reduction = effective_armor / (100.0 + effective_armor) if effective_armor > 0 else 0.0
        mitigated = raw_damage * damage_reduction
        final_dmg = max(1.0, raw_damage - mitigated)

        return ArmorPenetrationResult(
            effective_armor=round(effective_armor, 2),
            damage_mitigated=round(mitigated, 2),
            final_damage=round(final_dmg, 2),
            armor_shred_applied=round(target_armor - shredded_armor, 2)
        )
