"""
Aegis Shield Bearer (SHIELDED) Enemy Controller.
Heavy energy shield projection
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
from client.enemies.enemy_definitions import EnemyArchetype, EnemyStats
from client.entities.entity_model import Entity, HealthComponent, TransformComponent
from client.navigation.movement_controller import MovementComponent

@dataclass
class AegisShieldBearerEnemy:
    stats: EnemyStats = field(default_factory=lambda: EnemyStats(
        archetype=EnemyArchetype.SHIELDED,
        name="Aegis Shield Bearer",
        base_hp=180.0,
        shield=220.0,
        armor=5.0,
        speed=45.0,
        is_flying=False,
        reward_credits=30,
        threat_cost=3.0
    ))
    is_cloaked: bool = False
    phase_cooldown: float = 0.0

    def update_behavior(self, delta_time: float, health: HealthComponent, movement: MovementComponent) -> None:
        if self.phase_cooldown > 0.0:
            self.phase_cooldown = max(0.0, self.phase_cooldown - delta_time)
