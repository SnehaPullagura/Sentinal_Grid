"""
Solar Lance Array (ENERGY) Tower Implementation.
Concentrated orbital solar beam piercing lines of enemies
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
from client.towers.tower_definitions import TowerArchetype, TowerStats, AttackDefinition, TargetingStrategy
from client.combat.attack_pipeline import AttackPipeline
from client.math.vector2d import Vector2D
from client.entities.entity_model import Entity

@dataclass
class SolarLanceTower:
    stats: TowerStats = field(default_factory=lambda: TowerStats(
        archetype=TowerArchetype.ENERGY,
        name="Solar Lance Array",
        cost_credits=350,
        cost_energy=35,
        attack=AttackDefinition(
            base_damage=210.0,
            attack_rate=0.4,
            range_radius=240.0,
            damage_type="energy"
        )
    ))
    fx_signature: str = "solar"
    kill_count: int = 0
    total_damage: float = 0.0

    def on_tick(self, delta_time: float) -> None:
        if self.stats.cooldown_remaining > 0.0:
            self.stats.cooldown_remaining = max(0.0, self.stats.cooldown_remaining - delta_time)

    def record_hit(self, damage_amount: float, was_kill: bool = False) -> None:
        self.total_damage += damage_amount
        if was_kill:
            self.kill_count += 1
