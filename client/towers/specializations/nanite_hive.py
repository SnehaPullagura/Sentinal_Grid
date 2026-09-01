"""
Nanite Swarm Spire (EXPERIMENTAL) Tower Implementation.
Micro-drone corrosive nanite swarm
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
from client.towers.tower_definitions import TowerArchetype, TowerStats, AttackDefinition, TargetingStrategy
from client.combat.attack_pipeline import AttackPipeline
from client.math.vector2d import Vector2D
from client.entities.entity_model import Entity

@dataclass
class NaniteHiveTower:
    stats: TowerStats = field(default_factory=lambda: TowerStats(
        archetype=TowerArchetype.EXPERIMENTAL,
        name="Nanite Swarm Spire",
        cost_credits=290,
        cost_energy=29,
        attack=AttackDefinition(
            base_damage=50.0,
            attack_rate=1.5,
            range_radius=125.0,
            damage_type="experimental"
        )
    ))
    fx_signature: str = "nanite"
    kill_count: int = 0
    total_damage: float = 0.0

    def on_tick(self, delta_time: float) -> None:
        if self.stats.cooldown_remaining > 0.0:
            self.stats.cooldown_remaining = max(0.0, self.stats.cooldown_remaining - delta_time)

    def record_hit(self, damage_amount: float, was_kill: bool = False) -> None:
        self.total_damage += damage_amount
        if was_kill:
            self.kill_count += 1
