"""
Sector 10 In-Game Milestone & Medal Validator.
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

class Sector10MedalTracker:
    def __init__(self):
        self.sector_id: str = "sector_10"
        self.medals: List[SectorMedalCriteria] = [
            SectorMedalCriteria("IRON_DEFENDER_10", "Iron Sentinel", "Take zero base core damage", False),
            SectorMedalCriteria("ENERGY_MAGNATE_10", "Energy Tycoon", "Accumulate over 1000 excess energy", False),
            SectorMedalCriteria("EXTERMINATOR_10", "Swarm Purger", "Eliminate all hostiles in under 4 minutes", False)
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
