"""
Production Tower Implementation: SolarLanceArray
Archetype: ENERGY | Cost: 350 | Base Damage: 210.0 | Rate: 0.4/s | Range: 240.0
Description: Orbital solar concentrator piercing straight lines through multiple enemies
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple
from client.math.vector2d import Vector2D
from client.towers.tower_definitions import TowerArchetype, TowerStats, AttackDefinition, TargetingStrategy
from client.entities.entity_model import Entity, HealthComponent, TransformComponent
from client.combat.attack_pipeline import AttackPipeline

@dataclass
class SolarLanceArrayState:
    current_level: int = 1
    total_damage_dealt: float = 0.0
    total_kills: int = 0
    heat_level: float = 0.0
    max_heat: float = 100.0
    is_overheated: bool = False
    cooldown_timer: float = 0.0
    ammo_remaining: int = 50
    max_ammo: int = 50
    reload_time: float = 1.5
    current_target_id: Optional[str] = None

class SolarLanceArray:
    def __init__(self, position: Vector2D, tower_id: Optional[str] = None):
        self.tower_id: str = tower_id or f"solar_lance_array_{id(self)}"
        self.position: Vector2D = position.copy()
        self.stats: TowerStats = TowerStats(
            archetype=TowerArchetype.ENERGY,
            name="SolarLanceArray",
            cost_credits=350,
            cost_energy=35,
            attack=AttackDefinition(
                base_damage=210.0,
                attack_rate=0.4,
                range_radius=240.0,
                damage_type="energy"
            )
        )
        self.state: SolarLanceArrayState = SolarLanceArrayState()
        self.targeting_strategy: TargetingStrategy = TargetingStrategy.FIRST

    def tick(self, delta_time: float) -> None:
        if self.state.cooldown_timer > 0.0:
            self.state.cooldown_timer = max(0.0, self.state.cooldown_timer - delta_time)
        if self.state.heat_level > 0.0:
            self.state.heat_level = max(0.0, self.state.heat_level - 15.0 * delta_time)
            if self.state.heat_level < 20.0:
                self.state.is_overheated = False

    def can_fire(self) -> bool:
        return self.state.cooldown_timer <= 0.0 and not self.state.is_overheated and self.state.ammo_remaining > 0

    def record_attack(self, damage: float, is_kill: bool = False) -> None:
        self.state.total_damage_dealt += damage
        if is_kill:
            self.state.total_kills += 1
        self.state.cooldown_timer = 1.0 / max(0.1, self.stats.attack.attack_rate)
        self.state.heat_level = min(self.state.max_heat, self.state.heat_level + 8.0)
        if self.state.heat_level >= self.state.max_heat:
            self.state.is_overheated = True

    def get_telemetry_snapshot(self) -> dict:
        return {
            "tower_id": self.tower_id,
            "name": self.stats.name,
            "level": self.state.current_level,
            "damage_dealt": round(self.state.total_damage_dealt, 1),
            "kills": self.state.total_kills,
            "heat_pct": round((self.state.heat_level / self.state.max_heat) * 100, 1),
            "ammo": self.state.ammo_remaining
        }
