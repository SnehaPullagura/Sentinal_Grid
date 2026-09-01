"""
Aero Interceptor (FLYING) Enemy Controller.
High-altitude flyer ignoring ground obstacles
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
from client.enemies.enemy_definitions import EnemyArchetype, EnemyStats
from client.entities.entity_model import Entity, HealthComponent, TransformComponent
from client.navigation.movement_controller import MovementComponent

@dataclass
class AeroInterceptorEnemy:
    stats: EnemyStats = field(default_factory=lambda: EnemyStats(
        archetype=EnemyArchetype.FLYING,
        name="Aero Interceptor",
        base_hp=95.0,
        shield=0.0,
        armor=0.0,
        speed=90.0,
        is_flying=True,
        reward_credits=16,
        threat_cost=1.6
    ))
    is_cloaked: bool = False
    phase_cooldown: float = 0.0

    def update_behavior(self, delta_time: float, health: HealthComponent, movement: MovementComponent) -> None:
        if self.phase_cooldown > 0.0:
            self.phase_cooldown = max(0.0, self.phase_cooldown - delta_time)
