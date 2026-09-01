"""
Sector 11 Campaign Epilogue & Victory Aftermath Model.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class SectorAftermathSummary:
    sector_id: str
    grid_integrity_pct: float
    civilian_casualties_prevented: int
    unlocked_research_credits: int
    commander_commendation: str

class Sector11EpilogueEngine:
    def __init__(self):
        self.sector_id: str = "sector_11"

    def compile_aftermath(self, base_hp_remaining: float, max_hp: float, total_kills: int) -> SectorAftermathSummary:
        integrity = max(0.0, min(100.0, (base_hp_remaining / max(1.0, max_hp)) * 100.0))
        saved = total_kills * 21
        credits = int(integrity * 26)
        grade = "ADMIRAL_HONOR" if integrity > 90.0 else "TACTICAL_MERIT" if integrity > 50.0 else "SURVIVAL_MEDAL"

        return SectorAftermathSummary(
            sector_id=self.sector_id,
            grid_integrity_pct=round(integrity, 2),
            civilian_casualties_prevented=saved,
            unlocked_research_credits=credits,
            commander_commendation=grade
        )
