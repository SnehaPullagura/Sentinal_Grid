"""
Singularity Vortex Trap (CONTROL) Tower Implementation.
Pulls nearby enemies toward vortex center
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
from client.towers.tower_definitions import TowerArchetype, TowerStats, AttackDefinition, TargetingStrategy
from client.combat.attack_pipeline import AttackPipeline
from client.math.vector2d import Vector2D
from client.entities.entity_model import Entity

@dataclass
class SingularityTrapTower:
    stats: TowerStats = field(default_factory=lambda: TowerStats(
        archetype=TowerArchetype.CONTROL,
        name="Singularity Vortex Trap",
        cost_credits=270,
        cost_energy=27,
        attack=AttackDefinition(
            base_damage=25.0,
            attack_rate=0.5,
            range_radius=120.0,
            damage_type="control"
        )
    ))
    fx_signature: str = "vortex"
    kill_count: int = 0
    total_damage: float = 0.0

    def on_tick(self, delta_time: float) -> None:
        if self.stats.cooldown_remaining > 0.0:
            self.stats.cooldown_remaining = max(0.0, self.stats.cooldown_remaining - delta_time)

    def record_hit(self, damage_amount: float, was_kill: bool = False) -> None:
        self.total_damage += damage_amount
        if was_kill:
            self.kill_count += 1
