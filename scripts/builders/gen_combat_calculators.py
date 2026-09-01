import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate_combat_calculators():
    print("--> Generating Advanced Combat Calculators...")
    
    # 1. armor_penetration_calculator.py
    write_file("client/combat/calculators/armor_penetration_calculator.py", """from __future__ import annotations
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
""")

    # 2. elemental_reaction_engine.py
    write_file("client/combat/calculators/elemental_reaction_engine.py", """from __future__ import annotations
from enum import Enum, auto
from typing import Dict, Optional, Tuple
from dataclasses import dataclass

class DamageType(Enum):
    KINETIC = auto()
    ENERGY = auto()
    CRYO = auto()
    PLASMA = auto()
    EMP = auto()
    EXPLOSIVE = auto()
    CORROSIVE = auto()

class ElementalReaction(Enum):
    NONE = auto()
    THERMAL_SHOCK = auto()     # Cryo + Plasma: massive true damage shatter
    OVERLOAD_SURGE = auto()    # Energy + EMP: huge AoE stun & shield wipe
    SUNDER_ARMOR = auto()      # Kinetic + Corrosive: 80% permanent armor shred
    SUPERCONDUCTOR = auto()   # Cryo + EMP: chain lightning slows 5 targets

@dataclass
class ReactionResult:
    reaction: ElementalReaction
    bonus_damage: float
    aoe_radius: float
    applied_status: Optional[str]
    description: str

class ElementalReactionEngine:
    @staticmethod
    def evaluate_reaction(
        primary_type: DamageType,
        applied_type: DamageType,
        base_damage: float
    ) -> ReactionResult:
        # Cryo + Plasma -> Thermal Shock
        if (primary_type == DamageType.CRYO and applied_type == DamageType.PLASMA) or \
           (primary_type == DamageType.PLASMA and applied_type == DamageType.CRYO):
            return ReactionResult(
                reaction=ElementalReaction.THERMAL_SHOCK,
                bonus_damage=base_damage * 1.75,
                aoe_radius=60.0,
                applied_status="SHATTERED",
                description="Thermal shock vaporized target molecular integrity!"
            )

        # Energy + EMP -> Overload Surge
        if (primary_type == DamageType.ENERGY and applied_type == DamageType.EMP) or \
           (primary_type == DamageType.EMP and applied_type == DamageType.ENERGY):
            return ReactionResult(
                reaction=ElementalReaction.OVERLOAD_SURGE,
                bonus_damage=base_damage * 1.40,
                aoe_radius=80.0,
                applied_status="STUNNED",
                description="EMP overload triggered cascading electronic circuit surge!"
            )

        # Kinetic + Corrosive -> Sunder Armor
        if (primary_type == DamageType.KINETIC and applied_type == DamageType.CORROSIVE) or \
           (primary_type == DamageType.CORROSIVE and applied_type == DamageType.KINETIC):
            return ReactionResult(
                reaction=ElementalReaction.SUNDER_ARMOR,
                bonus_damage=base_damage * 1.20,
                aoe_radius=0.0,
                applied_status="SUNDERED",
                description="Acidic kinetic impact crushed armor plates!"
            )

        return ReactionResult(
            reaction=ElementalReaction.NONE,
            bonus_damage=0.0,
            aoe_radius=0.0,
            applied_status=None,
            description="Standard hit"
        )
""")

    # 3. damage_falloff_model.py
    write_file("client/combat/calculators/damage_falloff_model.py", """from __future__ import annotations
import math

class DamageFalloffModel:
    @staticmethod
    def calculate_ballistic_damage(
        base_damage: float,
        distance: float,
        optimal_range: float,
        max_range: float,
        falloff_exponent: float = 1.5
    ) -> float:
        if distance <= optimal_range:
            return base_damage
        if distance >= max_range:
            return base_damage * 0.25  # Minimum glancing damage

        t = (distance - optimal_range) / max(1.0, max_range - optimal_range)
        decay = (1.0 - t) ** falloff_exponent
        return max(base_damage * 0.25, base_damage * (0.25 + 0.75 * decay))

    @staticmethod
    def calculate_splash_damage(
        center_damage: float,
        impact_dist: float,
        splash_radius: float,
        min_splash_ratio: float = 0.20
    ) -> float:
        if impact_dist >= splash_radius:
            return 0.0
        ratio = max(0.0, min(1.0, 1.0 - (impact_dist / splash_radius)))
        return center_damage * (min_splash_ratio + (1.0 - min_splash_ratio) * ratio)
""")

if __name__ == "__main__":
    generate_combat_calculators()
