"""
Tower Combo Synergy Solver: ARC_DISCHARGER
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class SynergyProcOutcome:
    combo_name: str
    bonus_damage_multiplier: float
    chain_reaction_triggered: bool

class ArcDischargerSynergySolver:
    def __init__(self):
        self.primary_tower: str = "arc_discharger"

    def evaluate_combo_with(self, partner_tower_id: str) -> SynergyProcOutcome:
        if partner_tower_id in ("frostbite_cryo", "singularity_trap", "arc_discharger"):
            return SynergyProcOutcome(f"ARC_DISCHARGER_ELEMENTAL_CONVERGENCE", 1.45, True)
        return SynergyProcOutcome(f"ARC_DISCHARGER_REINFORCED_FIRE", 1.10, False)
