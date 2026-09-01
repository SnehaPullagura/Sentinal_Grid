"""
Damage Physics & Molecular Mitigation Model: FLAK_SHRAPNEL_BURST
Defines velocity drag, armor shredding formulas, kinetic dispersion,
and status effect propagation against all defensive material classes.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass
class PhysicsCalculationResult:
    applied_damage: float
    armor_mitigated: float
    shield_absorbed: float
    critical_strike_proc: bool
    status_applied: str

class FlakShrapnelBurstPhysicsModel:
    def __init__(self):
        self.damage_type: str = "flak_shrapnel_burst"
        self.base_velocity: float = 400.0
        self.penetration_index: float = 0.35
        self.dispersion_angle_rad: float = 0.05

    def compute_impact(
        self,
        raw_damage: float,
        target_armor: float,
        target_shield: float,
        impact_distance: float,
        is_crit: bool = False
    ) -> PhysicsCalculationResult:
        # Distance air resistance dissipation
        attenuation = max(0.4, 1.0 - (impact_distance / 600.0) * 0.3)
        dmg = raw_damage * attenuation * (1.5 if is_crit else 1.0)

        # Shield absorption
        absorbed = min(target_shield, dmg * 0.8)
        remaining_dmg = dmg - absorbed

        # Armor mitigation
        eff_armor = max(0.0, target_armor * (1.0 - self.penetration_index))
        reduction = eff_armor / (100.0 + eff_armor) if eff_armor > 0 else 0.0
        mitigated = remaining_dmg * reduction
        final_dmg = max(1.0, remaining_dmg - mitigated)

        return PhysicsCalculationResult(
            applied_damage=round(final_dmg, 2),
            armor_mitigated=round(mitigated, 2),
            shield_absorbed=round(absorbed, 2),
            critical_strike_proc=is_crit,
            status_applied="FLAK_PROC"
        )
