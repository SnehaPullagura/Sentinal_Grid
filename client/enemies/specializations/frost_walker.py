"""
Frost Walker (BASIC) Enemy Controller.
Immune to Cryo slow status effects
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
from client.enemies.enemy_definitions import EnemyArchetype, EnemyStats
from client.entities.entity_model import Entity, HealthComponent, TransformComponent
from client.navigation.movement_controller import MovementComponent

@dataclass
class FrostWalkerEnemy:
    stats: EnemyStats = field(default_factory=lambda: EnemyStats(
        archetype=EnemyArchetype.BASIC,
        name="Frost Walker",
        base_hp=220.0,
        shield=0.0,
        armor=8.0,
        speed=55.0,
        is_flying=False,
        reward_credits=26,
        threat_cost=2.6
    ))
    is_cloaked: bool = False
    phase_cooldown: float = 0.0

    def update_behavior(self, delta_time: float, health: HealthComponent, movement: MovementComponent) -> None:
        if self.phase_cooldown > 0.0:
            self.phase_cooldown = max(0.0, self.phase_cooldown - delta_time)
