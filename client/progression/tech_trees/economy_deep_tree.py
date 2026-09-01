"""
Deep Tech Tree Progression Engine: ECONOMY
Handles multi-branch dependency graphs, point costs, statistical scaling,
and active tactical perks for all 20 tiers of economy research.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

@dataclass
class DeepTechTier:
    tier: int
    name: str
    token_cost: int
    damage_bonus: float
    range_bonus: float
    rate_bonus: float
    special_perk_id: str
    prerequisites: List[int] = field(default_factory=list)
    unlocked: bool = False

class EconomyDeepResearchEngine:
    def __init__(self):
        self.branch_name: str = "economy"
        self.unlocked_tiers: Set[int] = set()
        self.tiers: Dict[int, DeepTechTier] = self._build_20_tiers()

    def _build_20_tiers(self) -> Dict[int, DeepTechTier]:
        tree = {}
        for t in range(1, 21):
            tree[t] = DeepTechTier(
                tier=t,
                name=f"Economy Mastery Tier {t}",
                token_cost=10 * t + 5,
                damage_bonus=round(0.05 * t, 3),
                range_bonus=round(0.03 * t, 3),
                rate_bonus=round(0.04 * t, 3),
                special_perk_id=f"economy_perk_tier_{t}",
                prerequisites=[t - 1] if t > 1 else []
            )
        return tree

    def can_research(self, tier: int, available_tokens: int) -> bool:
        node = self.tiers.get(tier)
        if not node or node.unlocked or available_tokens < node.token_cost:
            return False
        return all(p in self.unlocked_tiers for p in node.prerequisites)

    def research_tier(self, tier: int, available_tokens: int) -> Optional[int]:
        if not self.can_research(tier, available_tokens):
            return None
        self.tiers[tier].unlocked = True
        self.unlocked_tiers.add(tier)
        return available_tokens - self.tiers[tier].token_cost

    def get_aggregate_modifiers(self) -> dict:
        total_dmg = sum(self.tiers[t].damage_bonus for t in self.unlocked_tiers)
        total_rng = sum(self.tiers[t].range_bonus for t in self.unlocked_tiers)
        total_rate = sum(self.tiers[t].rate_bonus for t in self.unlocked_tiers)
        return {
            "damage_multiplier": 1.0 + total_dmg,
            "range_multiplier": 1.0 + total_rng,
            "rate_multiplier": 1.0 + total_rate,
            "unlocked_count": len(self.unlocked_tiers)
        }
