"""
Commander Active Operations Branch.
Orbital strikes, grid overclocking, nanite emergency repairs
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

class CommanderResearchTree:
    def __init__(self):
        self.branch_id: str = "commander"
        self.name: str = "Commander Active Operations"
        self.description: str = "Orbital strikes, grid overclocking, nanite emergency repairs"
        self.tiers: List[ResearchTier] = self._build_tiers()

    def _build_tiers(self) -> List[ResearchTier]:
        tiers = []
        for t in range(1, 11):
            tiers.append(ResearchTier(
                tier=t,
                name=f"Commander Active Operations Tier {t}",
                token_cost=15 * t,
                damage_bonus_pct=round(0.08 * t, 3),
                range_bonus_pct=round(0.05 * t, 3),
                special_perk=f"Empowers tier {t} commander weapon signatures with +{t * 10}% overload chance"
            ))
        return tiers

    def get_tier(self, tier_number: int) -> Optional[ResearchTier]:
        for t in self.tiers:
            if t.tier == tier_number:
                return t
        return None
