"""
Phase Shifter (DISRUPTOR) Enemy Controller.
Phases out of reality for 2s every 6s
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
from client.enemies.enemy_definitions import EnemyArchetype, EnemyStats
from client.entities.entity_model import Entity, HealthComponent, TransformComponent
from client.navigation.movement_controller import MovementComponent

@dataclass
class PhaseShifterEnemy:
    stats: EnemyStats = field(default_factory=lambda: EnemyStats(
        archetype=EnemyArchetype.DISRUPTOR,
        name="Phase Shifter",
        base_hp=160.0,
        shield=100.0,
        armor=4.0,
        speed=75.0,
        is_flying=False,
        reward_credits=36,
        threat_cost=3.6
    ))
    is_cloaked: bool = False
    phase_cooldown: float = 0.0

    def update_behavior(self, delta_time: float, health: HealthComponent, movement: MovementComponent) -> None:
        if self.phase_cooldown > 0.0:
            self.phase_cooldown = max(0.0, self.phase_cooldown - delta_time)
