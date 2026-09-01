"""
Dreadnought Titan (BOSS) Enemy Controller.
Catastrophic boss with 3 enrage phases
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
from client.enemies.enemy_definitions import EnemyArchetype, EnemyStats
from client.entities.entity_model import Entity, HealthComponent, TransformComponent
from client.navigation.movement_controller import MovementComponent

@dataclass
class DreadnoughtTitanEnemy:
    stats: EnemyStats = field(default_factory=lambda: EnemyStats(
        archetype=EnemyArchetype.BOSS,
        name="Dreadnought Titan",
        base_hp=3500.0,
        shield=1200.0,
        armor=25.0,
        speed=28.0,
        is_flying=False,
        reward_credits=400,
        threat_cost=40.0
    ))
    is_cloaked: bool = False
    phase_cooldown: float = 0.0

    def update_behavior(self, delta_time: float, health: HealthComponent, movement: MovementComponent) -> None:
        if self.phase_cooldown > 0.0:
            self.phase_cooldown = max(0.0, self.phase_cooldown - delta_time)
