"""
Apocalypse Overlord (BOSS) Enemy Controller.
Ultimate sector campaign final boss
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
from client.enemies.enemy_definitions import EnemyArchetype, EnemyStats
from client.entities.entity_model import Entity, HealthComponent, TransformComponent
from client.navigation.movement_controller import MovementComponent

@dataclass
class ApocalypseOverlordEnemy:
    stats: EnemyStats = field(default_factory=lambda: EnemyStats(
        archetype=EnemyArchetype.BOSS,
        name="Apocalypse Overlord",
        base_hp=6000.0,
        shield=2500.0,
        armor=35.0,
        speed=25.0,
        is_flying=False,
        reward_credits=800,
        threat_cost=80.0
    ))
    is_cloaked: bool = False
    phase_cooldown: float = 0.0

    def update_behavior(self, delta_time: float, health: HealthComponent, movement: MovementComponent) -> None:
        if self.phase_cooldown > 0.0:
            self.phase_cooldown = max(0.0, self.phase_cooldown - delta_time)
