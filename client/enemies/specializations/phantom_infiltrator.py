"""
Phantom Infiltrator (ASSASSIN) Enemy Controller.
Cloaked unit avoiding long range detection
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
from client.enemies.enemy_definitions import EnemyArchetype, EnemyStats
from client.entities.entity_model import Entity, HealthComponent, TransformComponent
from client.navigation.movement_controller import MovementComponent

@dataclass
class PhantomInfiltratorEnemy:
    stats: EnemyStats = field(default_factory=lambda: EnemyStats(
        archetype=EnemyArchetype.ASSASSIN,
        name="Phantom Infiltrator",
        base_hp=120.0,
        shield=0.0,
        armor=4.0,
        speed=85.0,
        is_flying=False,
        reward_credits=22,
        threat_cost=2.2
    ))
    is_cloaked: bool = False
    phase_cooldown: float = 0.0

    def update_behavior(self, delta_time: float, health: HealthComponent, movement: MovementComponent) -> None:
        if self.phase_cooldown > 0.0:
            self.phase_cooldown = max(0.0, self.phase_cooldown - delta_time)
