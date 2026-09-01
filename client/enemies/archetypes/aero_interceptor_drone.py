"""
Production Enemy Implementation: AeroInterceptorDrone
Archetype: FLYING | HP: 95.0 | Shield: 0.0 | Armor: 0.0 | Speed: 90.0 | Flying: True
Description: High-speed atmospheric flying unit ignoring ground pathing
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from client.math.vector2d import Vector2D
from client.enemies.enemy_definitions import EnemyArchetype, EnemyStats
from client.entities.entity_model import HealthComponent, TransformComponent
from client.navigation.movement_controller import MovementComponent

@dataclass
class AeroInterceptorDroneState:
    is_cloaked: bool = False
    is_invulnerable: bool = False
    phase_timer: float = 0.0
    distance_traveled: float = 0.0
    threat_value: float = 1.6
    kill_reward: int = 16

class AeroInterceptorDrone:
    def __init__(self, spawn_pos: Vector2D, enemy_id: Optional[str] = None):
        self.enemy_id: str = enemy_id or f"aero_interceptor_drone_{id(self)}"
        self.position: Vector2D = spawn_pos.copy()
        self.stats: EnemyStats = EnemyStats(
            archetype=EnemyArchetype.FLYING,
            name="AeroInterceptorDrone",
            base_hp=95.0,
            shield=0.0,
            armor=0.0,
            speed=90.0,
            is_flying=True,
            reward_credits=16,
            threat_cost=1.6
        )
        self.state: AeroInterceptorDroneState = AeroInterceptorDroneState()

    def update_agent(self, delta_time: float, health: HealthComponent, movement: MovementComponent) -> None:
        if self.state.phase_timer > 0.0:
            self.state.phase_timer = max(0.0, self.state.phase_timer - delta_time)
        if movement:
            self.state.distance_traveled = movement.total_distance_traveled

    def get_summary(self) -> dict:
        return {
            "enemy_id": self.enemy_id,
            "name": self.stats.name,
            "flying": self.stats.is_flying,
            "speed": self.stats.speed,
            "threat": self.state.threat_value,
            "distance": round(self.state.distance_traveled, 1)
        }
