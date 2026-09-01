from __future__ import annotations
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
        if (primary_type == DamageType.CRYO and applied_type == DamageType.PLASMA) or            (primary_type == DamageType.PLASMA and applied_type == DamageType.CRYO):
            return ReactionResult(
                reaction=ElementalReaction.THERMAL_SHOCK,
                bonus_damage=base_damage * 1.75,
                aoe_radius=60.0,
                applied_status="SHATTERED",
                description="Thermal shock vaporized target molecular integrity!"
            )

        # Energy + EMP -> Overload Surge
        if (primary_type == DamageType.ENERGY and applied_type == DamageType.EMP) or            (primary_type == DamageType.EMP and applied_type == DamageType.ENERGY):
            return ReactionResult(
                reaction=ElementalReaction.OVERLOAD_SURGE,
                bonus_damage=base_damage * 1.40,
                aoe_radius=80.0,
                applied_status="STUNNED",
                description="EMP overload triggered cascading electronic circuit surge!"
            )

        # Kinetic + Corrosive -> Sunder Armor
        if (primary_type == DamageType.KINETIC and applied_type == DamageType.CORROSIVE) or            (primary_type == DamageType.CORROSIVE and applied_type == DamageType.KINETIC):
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
