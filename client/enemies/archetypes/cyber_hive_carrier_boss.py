"""
Production Enemy Implementation: CyberHiveCarrierBoss
Archetype: BOSS | HP: 2800.0 | Shield: 800.0 | Armor: 15.0 | Speed: 32.0 | Flying: True
Description: Colossal aerial command carrier spawning relentless swarm fighters
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from client.math.vector2d import Vector2D
from client.enemies.enemy_definitions import EnemyArchetype, EnemyStats
from client.entities.entity_model import HealthComponent, TransformComponent
from client.navigation.movement_controller import MovementComponent

@dataclass
class CyberHiveCarrierBossState:
    is_cloaked: bool = False
    is_invulnerable: bool = False
    phase_timer: float = 0.0
    distance_traveled: float = 0.0
    threat_value: float = 35.0
    kill_reward: int = 350

class CyberHiveCarrierBoss:
    def __init__(self, spawn_pos: Vector2D, enemy_id: Optional[str] = None):
        self.enemy_id: str = enemy_id or f"cyber_hive_carrier_boss_{id(self)}"
        self.position: Vector2D = spawn_pos.copy()
        self.stats: EnemyStats = EnemyStats(
            archetype=EnemyArchetype.BOSS,
            name="CyberHiveCarrierBoss",
            base_hp=2800.0,
            shield=800.0,
            armor=15.0,
            speed=32.0,
            is_flying=True,
            reward_credits=350,
            threat_cost=35.0
        )
        self.state: CyberHiveCarrierBossState = CyberHiveCarrierBossState()

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
