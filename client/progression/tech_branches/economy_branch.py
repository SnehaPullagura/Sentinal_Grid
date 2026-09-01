"""
Quantum Matter Economics Branch.
Resource extraction spires, interest compounds, kill reward bounties
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

class EconomyResearchTree:
    def __init__(self):
        self.branch_id: str = "economy"
        self.name: str = "Quantum Matter Economics"
        self.description: str = "Resource extraction spires, interest compounds, kill reward bounties"
        self.tiers: List[ResearchTier] = self._build_tiers()

    def _build_tiers(self) -> List[ResearchTier]:
        tiers = []
        for t in range(1, 11):
            tiers.append(ResearchTier(
                tier=t,
                name=f"Quantum Matter Economics Tier {t}",
                token_cost=15 * t,
                damage_bonus_pct=round(0.08 * t, 3),
                range_bonus_pct=round(0.05 * t, 3),
                special_perk=f"Empowers tier {t} economy weapon signatures with +{t * 10}% overload chance"
            ))
        return tiers

    def get_tier(self, tier_number: int) -> Optional[ResearchTier]:
        for t in self.tiers:
            if t.tier == tier_number:
                return t
        return None
