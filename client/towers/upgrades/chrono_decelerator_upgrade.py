"""
Upgrade Progression & Evolution Graph: CHRONO_DECELERATOR
Provides branching skill paths for Level 1 to 5 enhancements,
overdrive stat modifiers, and specialized capability unlocks.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from client.towers.tower_definitions import TowerStats

@dataclass
class EvolutionTier:
    tier_level: int
    title: str
    credit_cost: int
    energy_cost: int
    damage_multiplier: float
    attack_rate_multiplier: float
    range_multiplier: float
    unlocked_ability: Optional[str] = None
    flavour_text: str = ""

class ChronoDeceleratorEvolutionGraph:
    def __init__(self):
        self.evolution_tiers: List[EvolutionTier] = self._build_evolution_paths()

    def _build_evolution_paths(self) -> List[EvolutionTier]:
        return [
            EvolutionTier(1, "Chrono Decelerator Mk.I", 0, 0, 1.0, 1.0, 1.0, flavour_text="Base standard assembly"),
            EvolutionTier(2, "Chrono Decelerator Mk.II", 100, 10, 1.35, 1.15, 1.10, flavour_text="Reinforced power conduits"),
            EvolutionTier(3, "Chrono Decelerator Mk.III", 220, 25, 1.80, 1.30, 1.25, unlocked_ability="chrono_decelerator_overdrive", flavour_text="Supercharged combat core"),
            EvolutionTier(4, "Chrono Decelerator Mk.IV", 450, 50, 2.50, 1.50, 1.40, unlocked_ability="chrono_decelerator_hypercharge", flavour_text="Experimental military grade"),
            EvolutionTier(5, "Chrono Decelerator Prototype Omega", 850, 100, 3.80, 1.85, 1.65, unlocked_ability="chrono_decelerator_apocalypse", flavour_text="Apex technological mastery")
        ]

    def upgrade_stats(self, current_stats: TowerStats, target_tier: int) -> bool:
        for t in self.evolution_tiers:
            if t.tier_level == target_tier:
                current_stats.attack.base_damage *= t.damage_multiplier
                current_stats.attack.attack_rate *= t.attack_rate_multiplier
                current_stats.attack.range_radius *= t.range_multiplier
                current_stats.level = target_tier
                return True
        return False
