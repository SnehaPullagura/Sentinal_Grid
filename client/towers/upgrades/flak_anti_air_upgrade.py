"""
Upgrade Progression & Evolution Graph: FLAK_ANTI_AIR
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

class FlakAntiAirEvolutionGraph:
    def __init__(self):
        self.evolution_tiers: List[EvolutionTier] = self._build_evolution_paths()

    def _build_evolution_paths(self) -> List[EvolutionTier]:
        return [
            EvolutionTier(1, "Flak Anti Air Mk.I", 0, 0, 1.0, 1.0, 1.0, flavour_text="Base standard assembly"),
            EvolutionTier(2, "Flak Anti Air Mk.II", 100, 10, 1.35, 1.15, 1.10, flavour_text="Reinforced power conduits"),
            EvolutionTier(3, "Flak Anti Air Mk.III", 220, 25, 1.80, 1.30, 1.25, unlocked_ability="flak_anti_air_overdrive", flavour_text="Supercharged combat core"),
            EvolutionTier(4, "Flak Anti Air Mk.IV", 450, 50, 2.50, 1.50, 1.40, unlocked_ability="flak_anti_air_hypercharge", flavour_text="Experimental military grade"),
            EvolutionTier(5, "Flak Anti Air Prototype Omega", 850, 100, 3.80, 1.85, 1.65, unlocked_ability="flak_anti_air_apocalypse", flavour_text="Apex technological mastery")
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
