"""
Cyber Hive Carrier (BOSS) Enemy Controller.
Flying boss spawning endless aero drones
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
from client.enemies.enemy_definitions import EnemyArchetype, EnemyStats
from client.entities.entity_model import Entity, HealthComponent, TransformComponent
from client.navigation.movement_controller import MovementComponent

@dataclass
class CyberHiveCarrierEnemy:
    stats: EnemyStats = field(default_factory=lambda: EnemyStats(
        archetype=EnemyArchetype.BOSS,
        name="Cyber Hive Carrier",
        base_hp=2800.0,
        shield=800.0,
        armor=15.0,
        speed=32.0,
        is_flying=True,
        reward_credits=350,
        threat_cost=35.0
    ))
    is_cloaked: bool = False
    phase_cooldown: float = 0.0

    def update_behavior(self, delta_time: float, health: HealthComponent, movement: MovementComponent) -> None:
        if self.phase_cooldown > 0.0:
            self.phase_cooldown = max(0.0, self.phase_cooldown - delta_time)
