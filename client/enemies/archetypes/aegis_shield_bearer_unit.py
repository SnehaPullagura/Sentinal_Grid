"""
Production Enemy Implementation: AegisShieldBearerUnit
Archetype: SHIELDED | HP: 180.0 | Shield: 220.0 | Armor: 5.0 | Speed: 45.0 | Flying: False
Description: Heavy energy shield projection unit protecting rear echelons
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from client.math.vector2d import Vector2D
from client.enemies.enemy_definitions import EnemyArchetype, EnemyStats
from client.entities.entity_model import HealthComponent, TransformComponent
from client.navigation.movement_controller import MovementComponent

@dataclass
class AegisShieldBearerUnitState:
    is_cloaked: bool = False
    is_invulnerable: bool = False
    phase_timer: float = 0.0
    distance_traveled: float = 0.0
    threat_value: float = 3.0
    kill_reward: int = 30

class AegisShieldBearerUnit:
    def __init__(self, spawn_pos: Vector2D, enemy_id: Optional[str] = None):
        self.enemy_id: str = enemy_id or f"aegis_shield_bearer_unit_{id(self)}"
        self.position: Vector2D = spawn_pos.copy()
        self.stats: EnemyStats = EnemyStats(
            archetype=EnemyArchetype.SHIELDED,
            name="AegisShieldBearerUnit",
            base_hp=180.0,
            shield=220.0,
            armor=5.0,
            speed=45.0,
            is_flying=False,
            reward_credits=30,
            threat_cost=3.0
        )
        self.state: AegisShieldBearerUnitState = AegisShieldBearerUnitState()

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
