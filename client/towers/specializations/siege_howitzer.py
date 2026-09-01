"""
Siege Howitzer Battery (KINETIC) Tower Implementation.
Ultra-heavy long-range artillery with massive splash
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
from client.towers.tower_definitions import TowerArchetype, TowerStats, AttackDefinition, TargetingStrategy
from client.combat.attack_pipeline import AttackPipeline
from client.math.vector2d import Vector2D
from client.entities.entity_model import Entity

@dataclass
class SiegeHowitzerTower:
    stats: TowerStats = field(default_factory=lambda: TowerStats(
        archetype=TowerArchetype.KINETIC,
        name="Siege Howitzer Battery",
        cost_credits=320,
        cost_energy=32,
        attack=AttackDefinition(
            base_damage=160.0,
            attack_rate=0.35,
            range_radius=260.0,
            damage_type="kinetic"
        )
    ))
    fx_signature: str = "artillery"
    kill_count: int = 0
    total_damage: float = 0.0

    def on_tick(self, delta_time: float) -> None:
        if self.stats.cooldown_remaining > 0.0:
            self.stats.cooldown_remaining = max(0.0, self.stats.cooldown_remaining - delta_time)

    def record_hit(self, damage_amount: float, was_kill: bool = False) -> None:
        self.total_damage += damage_amount
        if was_kill:
            self.kill_count += 1
