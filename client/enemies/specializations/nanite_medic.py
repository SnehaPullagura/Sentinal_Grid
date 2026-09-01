"""
Nanite Field Medic (HEALER) Enemy Controller.
Aura healing nearby damaged allies
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
from client.enemies.enemy_definitions import EnemyArchetype, EnemyStats
from client.entities.entity_model import Entity, HealthComponent, TransformComponent
from client.navigation.movement_controller import MovementComponent

@dataclass
class NaniteMedicEnemy:
    stats: EnemyStats = field(default_factory=lambda: EnemyStats(
        archetype=EnemyArchetype.HEALER,
        name="Nanite Field Medic",
        base_hp=150.0,
        shield=50.0,
        armor=2.0,
        speed=60.0,
        is_flying=False,
        reward_credits=28,
        threat_cost=2.8
    ))
    is_cloaked: bool = False
    phase_cooldown: float = 0.0

    def update_behavior(self, delta_time: float, health: HealthComponent, movement: MovementComponent) -> None:
        if self.phase_cooldown > 0.0:
            self.phase_cooldown = max(0.0, self.phase_cooldown - delta_time)
