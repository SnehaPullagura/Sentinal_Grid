"""
Arc Tesla Discharger (ENERGY) Tower Implementation.
Chain lightning jumping up to 4 targets
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
from client.towers.tower_definitions import TowerArchetype, TowerStats, AttackDefinition, TargetingStrategy
from client.combat.attack_pipeline import AttackPipeline
from client.math.vector2d import Vector2D
from client.entities.entity_model import Entity

@dataclass
class ArcDischargerTower:
    stats: TowerStats = field(default_factory=lambda: TowerStats(
        archetype=TowerArchetype.ENERGY,
        name="Arc Tesla Discharger",
        cost_credits=210,
        cost_energy=21,
        attack=AttackDefinition(
            base_damage=45.0,
            attack_rate=1.0,
            range_radius=130.0,
            damage_type="energy"
        )
    ))
    fx_signature: str = "lightning"
    kill_count: int = 0
    total_damage: float = 0.0

    def on_tick(self, delta_time: float) -> None:
        if self.stats.cooldown_remaining > 0.0:
            self.stats.cooldown_remaining = max(0.0, self.stats.cooldown_remaining - delta_time)

    def record_hit(self, damage_amount: float, was_kill: bool = False) -> None:
        self.total_damage += damage_amount
        if was_kill:
            self.kill_count += 1
