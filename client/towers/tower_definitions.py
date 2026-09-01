from __future__ import annotations
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from client.entities.entity_model import Component
from client.towers.targeting_system import TargetingStrategy
from client.combat.attack_pipeline import AttackDefinition

class TowerArchetype(Enum):
    KINETIC = auto()
    ENERGY = auto()
    CONTROL = auto()
    SUPPORT = auto()
    RESOURCE = auto()
    EXPERIMENTAL = auto()

@dataclass
class TowerStats:
    archetype: TowerArchetype = TowerArchetype.KINETIC
    name: str = "Gatling Turret"
    cost_credits: int = 100
    cost_energy: int = 10
    level: int = 1
    max_level: int = 5
    sell_ratio: float = 0.75
    attack: AttackDefinition = field(default_factory=AttackDefinition)
    cooldown_remaining: float = 0.0
    targeting_strategy: TargetingStrategy = TargetingStrategy.FIRST
    kills_count: int = 0
    total_damage_dealt: float = 0.0

@dataclass
class TowerComponent(Component):
    stats: TowerStats = field(default_factory=TowerStats)
    is_active: bool = True
    is_disabled: bool = False

    def can_attack(self) -> bool:
        return self.is_active and not self.is_disabled and self.stats.cooldown_remaining <= 0.0

    def update_cooldown(self, delta_time: float) -> None:
        if self.stats.cooldown_remaining > 0.0:
            self.stats.cooldown_remaining = max(0.0, self.stats.cooldown_remaining - delta_time)

    def trigger_attack(self) -> None:
        self.stats.cooldown_remaining = 1.0 / max(0.1, self.stats.attack.attack_rate)
