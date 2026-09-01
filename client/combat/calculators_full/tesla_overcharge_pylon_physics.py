"""
Weapon Physics & Ballistic Kinematics Engine: TeslaOverchargePylon
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Tuple, Optional
from client.math.vector2d import Vector2D

@dataclass
class BallisticTrajectory:
    initial_position: Vector2D
    target_position: Vector2D
    flight_velocity: Vector2D
    travel_time_sec: float
    total_kinetic_energy: float
    penetration_factor: float

class TeslaOverchargePylonPhysicsEngine:
    def __init__(self):
        self.weapon_id: str = "tesla_overcharge_pylon"
        self.base_damage: float = 0.0
        self.muzzle_velocity: float = 0.0
        self.base_penetration: float = 0.0
        self.firing_fx: str = "rate_boost"

    def calculate_trajectory(self, muzzle_pos: Vector2D, target_pos: Vector2D) -> BallisticTrajectory:
        dist = muzzle_pos.distance_to(target_pos)
        flight_sec = dist / max(1.0, self.muzzle_velocity) if self.muzzle_velocity < 9000.0 else 0.0
        direction = (target_pos - muzzle_pos).normalized()
        vel = direction * self.muzzle_velocity if self.muzzle_velocity < 9000.0 else Vector2D.zero()

        energy = 0.5 * self.base_damage * (self.muzzle_velocity ** 2) if self.muzzle_velocity < 9000.0 else self.base_damage * 1000.0

        return BallisticTrajectory(
            initial_position=muzzle_pos.copy(),
            target_position=target_pos.copy(),
            flight_velocity=vel,
            travel_time_sec=round(flight_sec, 3),
            total_kinetic_energy=round(energy, 1),
            penetration_factor=self.base_penetration
        )
