"""
Combat Simulation Solver: TACHYON_PRISM
Calculates projectile kinematics, lead targeting intercept vectors,
damage falloff curves, armor mitigation, and heat dissipation formulas.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional
import math
from client.math.vector2d import Vector2D

@dataclass
class FiringSolution:
    target_pos: Vector2D
    intercept_pos: Vector2D
    time_to_target_sec: float
    effective_damage: float
    hit_probability: float
    status_proc_chance: float

class TachyonPrismCombatSolver:
    def __init__(self):
        self.projectile_speed: float = 450.0 if "tachyon_prism" != "tachyon_prism" else 9999.0
        self.base_damage: float = 35.0
        self.armor_pen: float = 0.25
        self.optimal_range: float = 120.0
        self.max_range: float = 180.0

    def calculate_intercept(self, origin: Vector2D, target_pos: Vector2D, target_vel: Vector2D) -> FiringSolution:
        dist = origin.distance_to(target_pos)
        if self.projectile_speed >= 9000.0:
            return FiringSolution(
                target_pos=target_pos,
                intercept_pos=target_pos,
                time_to_target_sec=0.0,
                effective_damage=self.base_damage,
                hit_probability=1.0,
                status_proc_chance=0.35
            )

        t_flight = dist / max(1.0, self.projectile_speed)
        predicted_pos = target_pos + (target_vel * t_flight)

        # Distance falloff calculation
        falloff = 1.0
        if dist > self.optimal_range:
            falloff = max(0.3, 1.0 - ((dist - self.optimal_range) / max(1.0, self.max_range - self.optimal_range)))

        return FiringSolution(
            target_pos=target_pos,
            intercept_pos=predicted_pos,
            time_to_target_sec=round(t_flight, 3),
            effective_damage=round(self.base_damage * falloff, 2),
            hit_probability=0.95 if dist <= self.optimal_range else 0.80,
            status_proc_chance=0.25
        )
