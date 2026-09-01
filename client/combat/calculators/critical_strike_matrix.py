from __future__ import annotations
from dataclasses import dataclass
from client.core.rng import DeterministicRNG

@dataclass
class CritRollResult:
    is_critical: bool
    is_super_critical: bool
    multiplier: float
    total_damage: float

class CriticalStrikeMatrix:
    @staticmethod
    def evaluate_strike(
        raw_damage: float,
        crit_chance: float,
        crit_multiplier: float = 2.0,
        rng: DeterministicRNG = None
    ) -> CritRollResult:
        if rng is None:
            rng = DeterministicRNG()

        roll = rng.next_float()
        if roll <= crit_chance:
            # Check for super critical strike if crit_chance > 1.0
            if crit_chance > 1.0 and (roll <= crit_chance - 1.0):
                return CritRollResult(
                    is_critical=True,
                    is_super_critical=True,
                    multiplier=crit_multiplier * 1.5,
                    total_damage=round(raw_damage * crit_multiplier * 1.5, 2)
                )
            return CritRollResult(
                is_critical=True,
                is_super_critical=False,
                multiplier=crit_multiplier,
                total_damage=round(raw_damage * crit_multiplier, 2)
            )

        return CritRollResult(
            is_critical=False,
            is_super_critical=False,
            multiplier=1.0,
            total_damage=round(raw_damage, 2)
        )
