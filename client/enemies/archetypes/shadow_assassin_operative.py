"""
Production Enemy Implementation: ShadowAssassinOperative
Archetype: ASSASSIN | HP: 160.0 | Shield: 0.0 | Armor: 5.0 | Speed: 95.0 | Flying: False
Description: High-priority objective rusher with active kinetic evasion
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from client.math.vector2d import Vector2D
from client.enemies.enemy_definitions import EnemyArchetype, EnemyStats
from client.entities.entity_model import HealthComponent, TransformComponent
from client.navigation.movement_controller import MovementComponent

@dataclass
class ShadowAssassinOperativeState:
    is_cloaked: bool = False
    is_invulnerable: bool = False
    phase_timer: float = 0.0
    distance_traveled: float = 0.0
    threat_value: float = 3.4
    kill_reward: int = 34

class ShadowAssassinOperative:
    def __init__(self, spawn_pos: Vector2D, enemy_id: Optional[str] = None):
        self.enemy_id: str = enemy_id or f"shadow_assassin_operative_{id(self)}"
        self.position: Vector2D = spawn_pos.copy()
        self.stats: EnemyStats = EnemyStats(
            archetype=EnemyArchetype.ASSASSIN,
            name="ShadowAssassinOperative",
            base_hp=160.0,
            shield=0.0,
            armor=5.0,
            speed=95.0,
            is_flying=False,
            reward_credits=34,
            threat_cost=3.4
        )
        self.state: ShadowAssassinOperativeState = ShadowAssassinOperativeState()

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
