"""
High-Energy Optics Research Branch.
Continuous beam lasers, plasma mortars, tachyon emitters and solar lances
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

class EnergyResearchTree:
    def __init__(self):
        self.branch_id: str = "energy"
        self.name: str = "High-Energy Optics Research"
        self.description: str = "Continuous beam lasers, plasma mortars, tachyon emitters and solar lances"
        self.tiers: List[ResearchTier] = self._build_tiers()

    def _build_tiers(self) -> List[ResearchTier]:
        tiers = []
        for t in range(1, 11):
            tiers.append(ResearchTier(
                tier=t,
                name=f"High-Energy Optics Research Tier {t}",
                token_cost=15 * t,
                damage_bonus_pct=round(0.08 * t, 3),
                range_bonus_pct=round(0.05 * t, 3),
                special_perk=f"Empowers tier {t} energy weapon signatures with +{t * 10}% overload chance"
            ))
        return tiers

    def get_tier(self, tier_number: int) -> Optional[ResearchTier]:
        for t in self.tiers:
            if t.tier == tier_number:
                return t
        return None
