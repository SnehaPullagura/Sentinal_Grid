"""
Sector 21 Victory Condition & Star Rating Engine.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class SectorStarRating:
    stars_awarded: int
    flawless_victory: bool
    under_budget_bonus: bool
    speedrun_bonus: bool

class Sector21VictoryEvaluator:
    def __init__(self):
        self.sector_id: str = "sector_21"
        self.flawless_hp_threshold: float = 94.0

    def evaluate_victory(self, hp_pct: float, time_sec: float, spent_credits: int) -> SectorStarRating:
        is_flawless = hp_pct >= self.flawless_hp_threshold
        is_speed = time_sec <= (300.0 + 210)
        is_budget = spent_credits <= (2500 + 3150)

        stars = 1
        if is_flawless:
            stars += 1
        if is_speed and is_budget:
            stars += 1

        return SectorStarRating(
            stars_awarded=min(3, stars),
            flawless_victory=is_flawless,
            under_budget_bonus=is_budget,
            speedrun_bonus=is_speed
        )
