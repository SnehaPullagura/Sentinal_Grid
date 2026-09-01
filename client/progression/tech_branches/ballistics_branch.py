"""
Ballistic Kinetic Research Branch.
Kinetic cannons, railguns, flak artillery and armor piercing munitions
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class ResearchTier:
    tier: int
    name: str
    token_cost: int
    damage_bonus_pct: float
    range_bonus_pct: float
    special_perk: str
    unlocked: bool = False

class BallisticsResearchTree:
    def __init__(self):
        self.branch_id: str = "ballistics"
        self.name: str = "Ballistic Kinetic Research"
        self.description: str = "Kinetic cannons, railguns, flak artillery and armor piercing munitions"
        self.tiers: List[ResearchTier] = self._build_tiers()

    def _build_tiers(self) -> List[ResearchTier]:
        tiers = []
        for t in range(1, 11):
            tiers.append(ResearchTier(
                tier=t,
                name=f"Ballistic Kinetic Research Tier {t}",
                token_cost=15 * t,
                damage_bonus_pct=round(0.08 * t, 3),
                range_bonus_pct=round(0.05 * t, 3),
                special_perk=f"Empowers tier {t} ballistics weapon signatures with +{t * 10}% overload chance"
            ))
        return tiers

    def get_tier(self, tier_number: int) -> Optional[ResearchTier]:
        for t in self.tiers:
            if t.tier == tier_number:
                return t
        return None
