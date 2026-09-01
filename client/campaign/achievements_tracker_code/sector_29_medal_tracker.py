"""
Sector 29 In-Game Milestone & Medal Validator.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class SectorMedalCriteria:
    medal_id: str
    name: str
    condition_description: str
    is_unlocked: bool

class Sector29MedalTracker:
    def __init__(self):
        self.sector_id: str = "sector_29"
        self.medals: List[SectorMedalCriteria] = [
            SectorMedalCriteria("IRON_DEFENDER_29", "Iron Sentinel", "Take zero base core damage", False),
            SectorMedalCriteria("ENERGY_MAGNATE_29", "Energy Tycoon", "Accumulate over 1000 excess energy", False),
            SectorMedalCriteria("EXTERMINATOR_29", "Swarm Purger", "Eliminate all hostiles in under 4 minutes", False)
        ]

    def evaluate_medals(self, dmg_taken: float, final_energy: float, clear_time_sec: float) -> List[str]:
        unlocked = []
        if dmg_taken <= 0.0:
            unlocked.append(self.medals[0].medal_id)
        if final_energy >= 1000.0:
            unlocked.append(self.medals[1].medal_id)
        if clear_time_sec <= 240.0:
            unlocked.append(self.medals[2].medal_id)
        return unlocked
