"""
Production Enemy Implementation: NaniteFieldMedicDrone
Archetype: HEALER | HP: 150.0 | Shield: 50.0 | Armor: 2.0 | Speed: 60.0 | Flying: False
Description: Mobile nanite field medic repairing damaged allied armor
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from client.math.vector2d import Vector2D
from client.enemies.enemy_definitions import EnemyArchetype, EnemyStats
from client.entities.entity_model import HealthComponent, TransformComponent
from client.navigation.movement_controller import MovementComponent

@dataclass
class NaniteFieldMedicDroneState:
    is_cloaked: bool = False
    is_invulnerable: bool = False
    phase_timer: float = 0.0
    distance_traveled: float = 0.0
    threat_value: float = 2.8
    kill_reward: int = 28

class NaniteFieldMedicDrone:
    def __init__(self, spawn_pos: Vector2D, enemy_id: Optional[str] = None):
        self.enemy_id: str = enemy_id or f"nanite_field_medic_drone_{id(self)}"
        self.position: Vector2D = spawn_pos.copy()
        self.stats: EnemyStats = EnemyStats(
            archetype=EnemyArchetype.HEALER,
            name="NaniteFieldMedicDrone",
            base_hp=150.0,
            shield=50.0,
            armor=2.0,
            speed=60.0,
            is_flying=False,
            reward_credits=28,
            threat_cost=2.8
        )
        self.state: NaniteFieldMedicDroneState = NaniteFieldMedicDroneState()

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
