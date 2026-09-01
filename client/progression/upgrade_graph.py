from __future__ import annotations
from enum import Enum, auto
from typing import Dict, List, Optional
from dataclasses import dataclass
from client.towers.tower_definitions import TowerStats

class UpgradeBranch(Enum):
    OFFENSIVE = auto()
    RANGE = auto()
    SPECIALIZATION = auto()

@dataclass
class UpgradeNode:
    node_id: str
    branch: UpgradeBranch
    tier: int
    name: str
    description: str
    cost_credits: int
    damage_multiplier: float = 1.0
    rate_multiplier: float = 1.0
    range_multiplier: float = 1.0
    new_status_effect: Optional[Any] = None

class UpgradeGraph:
    def __init__(self):
        self.branches: Dict[UpgradeBranch, List[UpgradeNode]] = {
            UpgradeBranch.OFFENSIVE: [
                UpgradeNode("off_1", UpgradeBranch.OFFENSIVE, 1, "Hyper Velocity", "Increases damage by 30%", 80, damage_multiplier=1.3),
                UpgradeNode("off_2", UpgradeBranch.OFFENSIVE, 2, "Plasma Overcharge", "Increases damage by 60% and attack rate by 20%", 160, damage_multiplier=1.6, rate_multiplier=1.2)
            ],
            UpgradeBranch.RANGE: [
                UpgradeNode("rng_1", UpgradeBranch.RANGE, 1, "Optic Focusing", "Extends range by 25%", 60, range_multiplier=1.25),
                UpgradeNode("rng_2", UpgradeBranch.RANGE, 2, "Orbital Radar", "Extends range by 50%", 130, range_multiplier=1.5)
            ],
            UpgradeBranch.SPECIALIZATION: [
                UpgradeNode("spec_1", UpgradeBranch.SPECIALIZATION, 1, "Armor Piercing", "Shreds heavy armor", 150),
                UpgradeNode("spec_2", UpgradeBranch.SPECIALIZATION, 2, "Overclock Reactor", "Double firing rate for 5s", 250)
            ]
        }

    def apply_upgrade(self, tower_stats: TowerStats, branch: UpgradeBranch, tier: int) -> bool:
        nodes = self.branches.get(branch, [])
        for node in nodes:
            if node.tier == tier:
                tower_stats.attack.base_damage *= node.damage_multiplier
                tower_stats.attack.attack_rate *= node.rate_multiplier
                tower_stats.attack.range_radius *= node.range_multiplier
                tower_stats.level += 1
                return True
        return False
from typing import Any
