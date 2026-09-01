import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate():
    print("Generating Part 4: 12 Enemy Classes, AI & Boss System...")

    # 1. client/enemies/enemy_definitions.py
    write_file("client/enemies/enemy_definitions.py", """from __future__ import annotations
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from client.entities.entity_model import Component

class EnemyArchetype(Enum):
    BASIC = auto()
    FAST = auto()
    ARMORED = auto()
    FLYING = auto()
    SHIELDED = auto()
    HEALER = auto()
    DISRUPTOR = auto()
    SPLITTER = auto()
    ASSASSIN = auto()
    BUILDER = auto()
    BOSS = auto()
    SWARM = auto()

@dataclass
class EnemyStats:
    archetype: EnemyArchetype = EnemyArchetype.BASIC
    name: str = "Scout Runner"
    base_hp: float = 80.0
    shield: float = 0.0
    armor: float = 0.0
    speed: float = 65.0
    is_flying: bool = False
    reward_credits: int = 15
    reward_energy: int = 2
    threat_cost: float = 1.0  # Budget point cost
    leak_damage: float = 5.0  # Base damage if reaches goal
    abilities: List[str] = field(default_factory=list)

@dataclass
class EnemyComponent(Component):
    stats: EnemyStats = field(default_factory=EnemyStats)
    is_elite: bool = False
    is_boss: bool = False
    active_modifiers: List[str] = field(default_factory=list)
""")

    # 2. client/ai/behavior_tree.py
    write_file("client/ai/behavior_tree.py", """from __future__ import annotations
from enum import Enum, auto
from abc import ABC, abstractmethod
from typing import List, Optional, Callable, Any

class NodeStatus(Enum):
    SUCCESS = auto()
    FAILURE = auto()
    RUNNING = auto()

class BehaviorNode(ABC):
    @abstractmethod
    def tick(self, context: Any) -> NodeStatus:
        pass

class SequenceNode(BehaviorNode):
    def __init__(self, children: List[BehaviorNode]):
        self.children: List[BehaviorNode] = children

    def tick(self, context: Any) -> NodeStatus:
        for child in self.children:
            status = child.tick(context)
            if status != NodeStatus.SUCCESS:
                return status
        return NodeStatus.SUCCESS

class SelectorNode(BehaviorNode):
    def __init__(self, children: List[BehaviorNode]):
        self.children: List[BehaviorNode] = children

    def tick(self, context: Any) -> NodeStatus:
        for child in self.children:
            status = child.tick(context)
            if status != NodeStatus.FAILURE:
                return status
        return NodeStatus.FAILURE

class ActionNode(BehaviorNode):
    def __init__(self, action_fn: Callable[[Any], NodeStatus]):
        self.action_fn: Callable[[Any], NodeStatus] = action_fn

    def tick(self, context: Any) -> NodeStatus:
        return self.action_fn(context)

class ConditionNode(BehaviorNode):
    def __init__(self, predicate_fn: Callable[[Any], bool]):
        self.predicate_fn: Callable[[Any], bool] = predicate_fn

    def tick(self, context: Any) -> NodeStatus:
        return NodeStatus.SUCCESS if self.predicate_fn(context) else NodeStatus.FAILURE
""")

    # 3. client/ai/enemy_ai.py
    write_file("client/ai/enemy_ai.py", """from __future__ import annotations
from typing import Optional, List, Callable
from dataclasses import dataclass
from client.entities.entity_model import Component, Entity, TransformComponent, HealthComponent
from client.navigation.movement_controller import MovementComponent
from client.ai.behavior_tree import BehaviorNode, SequenceNode, SelectorNode, ActionNode, ConditionNode, NodeStatus

@dataclass
class AIContext:
    entity: Entity
    delta_time: float
    nearest_tower: Optional[Entity] = None
    allies_in_range: List[Entity] = None
    target_base_pos: Optional[Any] = None

class EnemyAIComponent(Component):
    def __init__(self):
        self.root_node: Optional[BehaviorNode] = None
        self._build_default_tree()

    def _build_default_tree(self) -> None:
        def move_forward(ctx: AIContext) -> NodeStatus:
            mv = ctx.entity.get_component(MovementComponent)
            tf = ctx.entity.get_component(TransformComponent)
            if mv and tf:
                new_pos, rot = mv.advance_towards_target(tf.position, ctx.delta_time)
                tf.position = new_pos
                tf.rotation = rot
                return NodeStatus.SUCCESS
            return NodeStatus.FAILURE

        self.root_node = ActionNode(move_forward)

    def tick(self, context: AIContext) -> NodeStatus:
        if self.root_node:
            return self.root_node.tick(context)
        return NodeStatus.SUCCESS
""")

    # 4. client/enemies/boss_phase_manager.py
    write_file("client/enemies/boss_phase_manager.py", """from __future__ import annotations
from enum import Enum, auto
from typing import List, Dict, Callable
from dataclasses import dataclass, field
from client.entities.entity_model import Component, HealthComponent
from client.events.event_bus import EventBus, GameEventType

class BossPhase(Enum):
    PHASE_1_SHIELDED = auto()
    PHASE_2_ENRAGED = auto()
    PHASE_3_DESPERATION = auto()

@dataclass
class BossPhaseTrigger:
    phase: BossPhase
    hp_threshold_pct: float  # e.g., 0.65 for 65%
    speed_multiplier: float = 1.0
    armor_buff: float = 0.0
    summon_count: int = 0
    emp_pulse: bool = False

class BossPhaseManager(Component):
    def __init__(self, triggers: Optional[List[BossPhaseTrigger]] = None):
        self.current_phase: BossPhase = BossPhase.PHASE_1_SHIELDED
        self.triggers: List[BossPhaseTrigger] = triggers or [
            BossPhaseTrigger(BossPhase.PHASE_1_SHIELDED, 1.0, 1.0, 5.0, 0),
            BossPhaseTrigger(BossPhase.PHASE_2_ENRAGED, 0.60, 1.45, 10.0, 4, emp_pulse=True),
            BossPhaseTrigger(BossPhase.PHASE_3_DESPERATION, 0.25, 1.85, 15.0, 8, emp_pulse=True)
        ]
        self._activated_phases: set = set()

    def check_phase_transition(self, health: HealthComponent, event_bus: EventBus) -> Optional[BossPhaseTrigger]:
        if not health or not health.is_alive:
            return None

        hp_pct = health.health_percentage
        for trig in sorted(self.triggers, key=lambda t: t.hp_threshold_pct):
            if hp_pct <= trig.hp_threshold_pct and trig.phase not in self._activated_phases:
                self._activated_phases.add(trig.phase)
                self.current_phase = trig.phase
                event_bus.emit(
                    GameEventType.BOSS_PHASE_CHANGED,
                    source_id=self.entity_id,
                    new_phase=trig.phase.name,
                    hp_pct=hp_pct
                )
                return trig
        return None
""")

    # 5. client/enemies/enemy_catalog.py
    write_file("client/enemies/enemy_catalog.py", """from __future__ import annotations
from typing import Dict
from client.enemies.enemy_definitions import EnemyArchetype, EnemyStats

def get_enemy_catalog() -> Dict[str, EnemyStats]:
    return {
        "scout_runner": EnemyStats(
            archetype=EnemyArchetype.FAST,
            name="Scout Runner",
            base_hp=70.0,
            speed=95.0,
            reward_credits=12,
            threat_cost=1.0,
            leak_damage=3.0
        ),
        "heavy_brute": EnemyStats(
            archetype=EnemyArchetype.ARMORED,
            name="Heavy Brute",
            base_hp=320.0,
            armor=8.0,
            speed=40.0,
            reward_credits=28,
            threat_cost=2.8,
            leak_damage=10.0
        ),
        "aero_drone": EnemyStats(
            archetype=EnemyArchetype.FLYING,
            name="Aero Drone",
            base_hp=110.0,
            speed=80.0,
            is_flying=True,
            reward_credits=18,
            threat_cost=1.8,
            leak_damage=5.0
        ),
        "shield_bearer": EnemyStats(
            archetype=EnemyArchetype.SHIELDED,
            name="Shield Bearer",
            base_hp=160.0,
            shield=140.0,
            speed=50.0,
            reward_credits=25,
            threat_cost=2.5,
            leak_damage=6.0
        ),
        "emp_disruptor": EnemyStats(
            archetype=EnemyArchetype.DISRUPTOR,
            name="EMP Disruptor",
            base_hp=140.0,
            speed=65.0,
            reward_credits=30,
            threat_cost=3.0,
            leak_damage=8.0,
            abilities=["emp_aura"]
        ),
        "hydra_splitter": EnemyStats(
            archetype=EnemyArchetype.SPLITTER,
            name="Hydra Splitter",
            base_hp=240.0,
            speed=45.0,
            reward_credits=35,
            threat_cost=3.5,
            leak_damage=12.0,
            abilities=["split_on_death"]
        ),
        "dreadnought_boss": EnemyStats(
            archetype=EnemyArchetype.BOSS,
            name="Dreadnought Titan",
            base_hp=2500.0,
            shield=800.0,
            armor=15.0,
            speed=32.0,
            reward_credits=250,
            reward_energy=50,
            threat_cost=25.0,
            leak_damage=50.0,
            abilities=["phase_shield", "summon_swarm", "emp_surge"]
        ),
        "swarm_cluster": EnemyStats(
            archetype=EnemyArchetype.SWARM,
            name="Swarm Parasite",
            base_hp=30.0,
            speed=110.0,
            reward_credits=5,
            threat_cost=0.4,
            leak_damage=1.0
        )
    }
""")

    print("Part 4 Complete.")

if __name__ == "__main__":
    generate()
