"""
Quantum Phase Blaster (EXPERIMENTAL) Tower Implementation.
Bypasses all physical armor and elemental shields
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
from client.towers.tower_definitions import TowerArchetype, TowerStats, AttackDefinition, TargetingStrategy
from client.combat.attack_pipeline import AttackPipeline
from client.math.vector2d import Vector2D
from client.entities.entity_model import Entity

@dataclass
class QuantumBlasterTower:
    stats: TowerStats = field(default_factory=lambda: TowerStats(
        archetype=TowerArchetype.EXPERIMENTAL,
        name="Quantum Phase Blaster",
        cost_credits=380,
        cost_energy=38,
        attack=AttackDefinition(
            base_damage=140.0,
            attack_rate=0.9,
            range_radius=150.0,
            damage_type="experimental"
        )
    ))
    fx_signature: str = "quantum"
    kill_count: int = 0
    total_damage: float = 0.0

    def on_tick(self, delta_time: float) -> None:
        if self.stats.cooldown_remaining > 0.0:
            self.stats.cooldown_remaining = max(0.0, self.stats.cooldown_remaining - delta_time)

    def record_hit(self, damage_amount: float, was_kill: bool = False) -> None:
        self.total_damage += damage_amount
        if was_kill:
            self.kill_count += 1
