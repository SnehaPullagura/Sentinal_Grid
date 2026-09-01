"""
Viper Missile Battery (KINETIC) Tower Implementation.
Multi-target homing kinetic missile salvo
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
from client.towers.tower_definitions import TowerArchetype, TowerStats, AttackDefinition, TargetingStrategy
from client.combat.attack_pipeline import AttackPipeline
from client.math.vector2d import Vector2D
from client.entities.entity_model import Entity

@dataclass
class MissilePodBatteryTower:
    stats: TowerStats = field(default_factory=lambda: TowerStats(
        archetype=TowerArchetype.KINETIC,
        name="Viper Missile Battery",
        cost_credits=260,
        cost_energy=26,
        attack=AttackDefinition(
            base_damage=35.0,
            attack_rate=1.8,
            range_radius=190.0,
            damage_type="kinetic"
        )
    ))
    fx_signature: str = "missile"
    kill_count: int = 0
    total_damage: float = 0.0

    def on_tick(self, delta_time: float) -> None:
        if self.stats.cooldown_remaining > 0.0:
            self.stats.cooldown_remaining = max(0.0, self.stats.cooldown_remaining - delta_time)

    def record_hit(self, damage_amount: float, was_kill: bool = False) -> None:
        self.total_damage += damage_amount
        if was_kill:
            self.kill_count += 1
