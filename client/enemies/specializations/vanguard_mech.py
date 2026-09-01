"""
Vanguard Bipedal Mech (ARMORED) Enemy Controller.
Dual shield & physical armor warrior
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
from client.enemies.enemy_definitions import EnemyArchetype, EnemyStats
from client.entities.entity_model import Entity, HealthComponent, TransformComponent
from client.navigation.movement_controller import MovementComponent

@dataclass
class VanguardMechEnemy:
    stats: EnemyStats = field(default_factory=lambda: EnemyStats(
        archetype=EnemyArchetype.ARMORED,
        name="Vanguard Bipedal Mech",
        base_hp=380.0,
        shield=150.0,
        armor=12.0,
        speed=50.0,
        is_flying=False,
        reward_credits=42,
        threat_cost=4.2
    ))
    is_cloaked: bool = False
    phase_cooldown: float = 0.0

    def update_behavior(self, delta_time: float, health: HealthComponent, movement: MovementComponent) -> None:
        if self.phase_cooldown > 0.0:
            self.phase_cooldown = max(0.0, self.phase_cooldown - delta_time)
