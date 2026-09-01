import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate():
    print("Generating Part 6: Economy, Upgrades, Active Abilities & Campaign...")

    # 1. client/economy/economy_service.py
    write_file("client/economy/economy_service.py", """from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional
from client.events.event_bus import EventBus, GameEventType

@dataclass
class Wallet:
    credits: int = 400
    energy: int = 100
    strategic_tokens: int = 0

class EconomyService:
    def __init__(self, event_bus: EventBus, starting_credits: int = 400, starting_energy: int = 100):
        self.event_bus: EventBus = event_bus
        self.wallet: Wallet = Wallet(credits=starting_credits, energy=starting_energy)
        self.total_earned: int = 0
        self.total_spent: int = 0

    def can_afford(self, credits: int = 0, energy: int = 0, tokens: int = 0) -> bool:
        return (self.wallet.credits >= credits and
                self.wallet.energy >= energy and
                self.wallet.strategic_tokens >= tokens)

    def spend(self, credits: int = 0, energy: int = 0, tokens: int = 0, reason: str = "general") -> bool:
        if not self.can_afford(credits, energy, tokens):
            return False
        self.wallet.credits -= credits
        self.wallet.energy -= energy
        self.wallet.strategic_tokens -= tokens
        self.total_spent += credits
        self.event_bus.emit(GameEventType.CREDITS_CHANGED, delta=-credits, total=self.wallet.credits, reason=reason)
        return True

    def earn(self, credits: int = 0, energy: int = 0, tokens: int = 0, reason: str = "reward") -> None:
        self.wallet.credits += credits
        self.wallet.energy += energy
        self.wallet.strategic_tokens += tokens
        self.total_earned += credits
        self.event_bus.emit(GameEventType.CREDITS_CHANGED, delta=credits, total=self.wallet.credits, reason=reason)

    def refund_tower(self, original_cost: int, sell_ratio: float = 0.75) -> int:
        refund_amount = int(original_cost * sell_ratio)
        self.earn(credits=refund_amount, reason="tower_sold")
        return refund_amount
""")

    # 2. client/progression/upgrade_graph.py
    write_file("client/progression/upgrade_graph.py", """from __future__ import annotations
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
""")

    # 3. client/abilities/ability_system.py
    write_file("client/abilities/ability_system.py", """from __future__ import annotations
from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, List, Optional, Callable
from client.math.vector2d import Vector2D
from client.events.event_bus import EventBus, GameEventType
from client.economy.economy_service import EconomyService

@dataclass
class CommanderAbility:
    ability_id: str
    name: str
    energy_cost: int
    cooldown_seconds: float
    current_cooldown: float = 0.0
    radius: float = 80.0
    description: str = ""

class AbilityManager:
    def __init__(self, event_bus: EventBus, economy: EconomyService):
        self.event_bus: EventBus = event_bus
        self.economy: EconomyService = economy
        self.abilities: Dict[str, CommanderAbility] = {
            "orbital_strike": CommanderAbility("orbital_strike", "Orbital Kinetic Strike", 40, 30.0, radius=90.0, description="Massive area damage blast"),
            "cryo_surge": CommanderAbility("cryo_surge", "Cryo Flash Freeze", 25, 20.0, radius=120.0, description="Freezes all enemies in area for 4s"),
            "nano_repair": CommanderAbility("nano_repair", "Nanite Base Repair", 35, 45.0, description="Restores 25 Base HP"),
            "overclock": CommanderAbility("overclock", "Grid Overclock", 30, 25.0, description="Boosts all tower attack speeds by 50% for 8s")
        }

    def update_cooldowns(self, delta_time: float) -> None:
        for ab in self.abilities.values():
            if ab.current_cooldown > 0.0:
                ab.current_cooldown = max(0.0, ab.current_cooldown - delta_time)

    def trigger_ability(self, ability_id: str, target_pos: Optional[Vector2D] = None) -> bool:
        ab = self.abilities.get(ability_id)
        if not ab or ab.current_cooldown > 0.0:
            return False

        if not self.economy.spend(energy=ab.energy_cost, reason=f"ability_{ability_id}"):
            return False

        ab.current_cooldown = ab.cooldown_seconds
        self.event_bus.emit(
            GameEventType.ABILITY_TRIGGERED,
            ability_id=ability_id,
            target_pos=target_pos.to_tuple() if target_pos else None
        )
        return True
""")

    # 4. client/maps/map_definition.py
    write_file("client/maps/map_definition.py", """from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from client.math.vector2d import Vector2D

@dataclass
class MapDefinition:
    map_id: str
    name: str
    width: int = 32
    height: int = 24
    cell_size: float = 32.0
    spawn_points: List[Vector2D] = field(default_factory=list)
    base_objective_pos: Vector2D = field(default_factory=Vector2D.zero)
    blocked_cells: List[Tuple[int, int]] = field(default_factory=list)
    build_platforms: List[Tuple[int, int]] = field(default_factory=list)
    starting_credits: int = 450
    starting_energy: int = 100
    base_hp: float = 100.0
    total_waves: int = 15

def get_default_map() -> MapDefinition:
    return MapDefinition(
        map_id="map_alpha_outpost",
        name="Sector 7 Outpost",
        width=32,
        height=24,
        spawn_points=[Vector2D(16.0, 16.0), Vector2D(16.0, 700.0)],
        base_objective_pos=Vector2D(980.0, 380.0),
        blocked_cells=[(10, 5), (10, 6), (10, 7), (15, 12), (15, 13), (20, 18)],
        build_platforms=[(x, y) for x in range(4, 28) for y in range(4, 20)]
    )
""")

    # 5. client/campaign/campaign_manager.py
    write_file("client/campaign/campaign_manager.py", """from __future__ import annotations
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
""")

    print("Part 6 Complete.")

if __name__ == "__main__":
    generate()
