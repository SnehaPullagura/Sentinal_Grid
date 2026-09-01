"""
Production Enemy Implementation: ScoutInfiltratorAgent
Archetype: FAST | HP: 65.0 | Shield: 0.0 | Armor: 0.0 | Speed: 105.0 | Flying: False
Description: Rapid lightweight reconnaissance unit with high dodge chance
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from client.math.vector2d import Vector2D
from client.enemies.enemy_definitions import EnemyArchetype, EnemyStats
from client.entities.entity_model import HealthComponent, TransformComponent
from client.navigation.movement_controller import MovementComponent

@dataclass
class ScoutInfiltratorAgentState:
    is_cloaked: bool = False
    is_invulnerable: bool = False
    phase_timer: float = 0.0
    distance_traveled: float = 0.0
    threat_value: float = 1.0
    kill_reward: int = 10

class ScoutInfiltratorAgent:
    def __init__(self, spawn_pos: Vector2D, enemy_id: Optional[str] = None):
        self.enemy_id: str = enemy_id or f"scout_infiltrator_agent_{id(self)}"
        self.position: Vector2D = spawn_pos.copy()
        self.stats: EnemyStats = EnemyStats(
            archetype=EnemyArchetype.FAST,
            name="ScoutInfiltratorAgent",
            base_hp=65.0,
            shield=0.0,
            armor=0.0,
            speed=105.0,
            is_flying=False,
            reward_credits=10,
            threat_cost=1.0
        )
        self.state: ScoutInfiltratorAgentState = ScoutInfiltratorAgentState()

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
