"""
EMP Grid Array (CONTROL) Tower Implementation.
Periodic EMP burst disabling enemy shields and abilities
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
from client.towers.tower_definitions import TowerArchetype, TowerStats, AttackDefinition, TargetingStrategy
from client.combat.attack_pipeline import AttackPipeline
from client.math.vector2d import Vector2D
from client.entities.entity_model import Entity

@dataclass
class EmpDisruptorTowerTower:
    stats: TowerStats = field(default_factory=lambda: TowerStats(
        archetype=TowerArchetype.CONTROL,
        name="EMP Grid Array",
        cost_credits=195,
        cost_energy=19,
        attack=AttackDefinition(
            base_damage=20.0,
            attack_rate=0.8,
            range_radius=100.0,
            damage_type="control"
        )
    ))
    fx_signature: str = "emp"
    kill_count: int = 0
    total_damage: float = 0.0

    def on_tick(self, delta_time: float) -> None:
        if self.stats.cooldown_remaining > 0.0:
            self.stats.cooldown_remaining = max(0.0, self.stats.cooldown_remaining - delta_time)

    def record_hit(self, damage_amount: float, was_kill: bool = False) -> None:
        self.total_damage += damage_amount
        if was_kill:
            self.kill_count += 1
