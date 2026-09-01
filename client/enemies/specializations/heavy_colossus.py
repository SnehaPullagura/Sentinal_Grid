"""
Heavy Colossus (ARMORED) Enemy Controller.
Gigantic walking fortress
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
from client.enemies.enemy_definitions import EnemyArchetype, EnemyStats
from client.entities.entity_model import Entity, HealthComponent, TransformComponent
from client.navigation.movement_controller import MovementComponent

@dataclass
class HeavyColossusEnemy:
    stats: EnemyStats = field(default_factory=lambda: EnemyStats(
        archetype=EnemyArchetype.ARMORED,
        name="Heavy Colossus",
        base_hp=600.0,
        shield=0.0,
        armor=22.0,
        speed=32.0,
        is_flying=False,
        reward_credits=55,
        threat_cost=5.5
    ))
    is_cloaked: bool = False
    phase_cooldown: float = 0.0

    def update_behavior(self, delta_time: float, health: HealthComponent, movement: MovementComponent) -> None:
        if self.phase_cooldown > 0.0:
            self.phase_cooldown = max(0.0, self.phase_cooldown - delta_time)
