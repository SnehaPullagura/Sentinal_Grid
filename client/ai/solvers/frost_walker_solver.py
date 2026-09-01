"""
Enemy Behavioral & Strategic Solver: FROST_WALKER
Evaluates survival heuristics, evasion maneuvers, threat prioritisation,
and dynamic route optimization.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional
from client.math.vector2d import Vector2D

@dataclass
class EvasionDecision:
    recommended_velocity: Vector2D
    should_cloak: bool
    should_shield: bool
    threat_urgency: float

class FrostWalkerStrategySolver:
    def __init__(self):
        self.archetype_id: str = "frost_walker"
        self.health_pool: float = 200.0
        self.movement_speed: float = 75.0

    def evaluate_threats(
        self,
        current_pos: Vector2D,
        goal_pos: Vector2D,
        nearby_hazard_origins: List[Vector2D],
        current_hp_pct: float
    ) -> EvasionDecision:
        direct_dir = (goal_pos - current_pos).normalized()
        repulsion = Vector2D.zero()

        for hpos in nearby_hazard_origins:
            d = current_pos.distance_to(hpos)
            if d < 80.0:
                away = (current_pos - hpos).normalized()
                repulsion = repulsion + away * (1.0 - (d / 80.0))

        final_dir = (direct_dir * 1.5 + repulsion).normalized()
        vel = final_dir * self.movement_speed

        return EvasionDecision(
            recommended_velocity=vel,
            should_cloak=(current_hp_pct < 0.4 and "frost_walker".startswith("phantom")),
            should_shield=(current_hp_pct < 0.8 and "shield" in "frost_walker"),
            threat_urgency=min(1.0, len(nearby_hazard_origins) * 0.3)
        )
