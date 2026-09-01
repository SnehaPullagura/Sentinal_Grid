"""
Production Enemy Implementation: GliderSwarmerParasite
Archetype: SWARM | HP: 25.0 | Shield: 0.0 | Armor: 0.0 | Speed: 115.0 | Flying: True
Description: Extremely agile lightweight flyer moving in dense swarms
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from client.math.vector2d import Vector2D
from client.enemies.enemy_definitions import EnemyArchetype, EnemyStats
from client.entities.entity_model import HealthComponent, TransformComponent
from client.navigation.movement_controller import MovementComponent

@dataclass
class GliderSwarmerParasiteState:
    is_cloaked: bool = False
    is_invulnerable: bool = False
    phase_timer: float = 0.0
    distance_traveled: float = 0.0
    threat_value: float = 0.3
    kill_reward: int = 4

class GliderSwarmerParasite:
    def __init__(self, spawn_pos: Vector2D, enemy_id: Optional[str] = None):
        self.enemy_id: str = enemy_id or f"glider_swarmer_parasite_{id(self)}"
        self.position: Vector2D = spawn_pos.copy()
        self.stats: EnemyStats = EnemyStats(
            archetype=EnemyArchetype.SWARM,
            name="GliderSwarmerParasite",
            base_hp=25.0,
            shield=0.0,
            armor=0.0,
            speed=115.0,
            is_flying=True,
            reward_credits=4,
            threat_cost=0.3
        )
        self.state: GliderSwarmerParasiteState = GliderSwarmerParasiteState()

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
