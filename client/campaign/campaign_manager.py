from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class LevelProgress:
    level_id: str
    is_unlocked: bool = False
    is_completed: bool = False
    stars_earned: int = 0
    high_score: int = 0

@dataclass
class CampaignWorld:
    world_id: str
    name: str
    description: str
    levels: List[str] = field(default_factory=list)

class CampaignManager:
    def __init__(self):
        self.worlds: List[CampaignWorld] = [
            CampaignWorld("world_1", "Iron Frontier", "Outer colonies under rogue AI siege", ["level_1_1", "level_1_2", "level_1_3", "boss_1"]),
            CampaignWorld("world_2", "Neon Grid", "Cybernetic metropolis core defense", ["level_2_1", "level_2_2", "level_2_3", "boss_2"]),
            CampaignWorld("world_3", "Void Abyss", "Final stronghold against the swarm", ["level_3_1", "level_3_2", "level_3_3", "boss_3"])
        ]
        self.progress: Dict[str, LevelProgress] = {
            "level_1_1": LevelProgress("level_1_1", is_unlocked=True),
            "level_1_2": LevelProgress("level_1_2"),
            "level_1_3": LevelProgress("level_1_3"),
            "boss_1": LevelProgress("boss_1")
        }

    def complete_level(self, level_id: str, stars: int, score: int) -> None:
        if level_id in self.progress:
            lp = self.progress[level_id]
            lp.is_completed = True
            lp.stars_earned = max(lp.stars_earned, stars)
            lp.high_score = max(lp.high_score, score)

        # Unlock next level
        keys = list(self.progress.keys())
        if level_id in keys:
            idx = keys.index(level_id)
            if idx + 1 < len(keys):
                self.progress[keys[idx + 1]].is_unlocked = True
