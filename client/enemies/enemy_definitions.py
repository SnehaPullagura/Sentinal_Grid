from __future__ import annotations
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
