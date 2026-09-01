"""
Production Enemy Implementation: PhaseShifterStalker
Archetype: DISRUPTOR | HP: 160.0 | Shield: 100.0 | Armor: 4.0 | Speed: 75.0 | Flying: False
Description: Quantum phase shifter periodically immune to all incoming attacks
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from client.math.vector2d import Vector2D
from client.enemies.enemy_definitions import EnemyArchetype, EnemyStats
from client.entities.entity_model import HealthComponent, TransformComponent
from client.navigation.movement_controller import MovementComponent

@dataclass
class PhaseShifterStalkerState:
    is_cloaked: bool = False
    is_invulnerable: bool = False
    phase_timer: float = 0.0
    distance_traveled: float = 0.0
    threat_value: float = 3.6
    kill_reward: int = 36

class PhaseShifterStalker:
    def __init__(self, spawn_pos: Vector2D, enemy_id: Optional[str] = None):
        self.enemy_id: str = enemy_id or f"phase_shifter_stalker_{id(self)}"
        self.position: Vector2D = spawn_pos.copy()
        self.stats: EnemyStats = EnemyStats(
            archetype=EnemyArchetype.DISRUPTOR,
            name="PhaseShifterStalker",
            base_hp=160.0,
            shield=100.0,
            armor=4.0,
            speed=75.0,
            is_flying=False,
            reward_credits=36,
            threat_cost=3.6
        )
        self.state: PhaseShifterStalkerState = PhaseShifterStalkerState()

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
