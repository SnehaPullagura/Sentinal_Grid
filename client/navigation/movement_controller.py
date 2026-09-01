from __future__ import annotations
from typing import List, Optional
from dataclasses import dataclass, field
from client.math.vector2d import Vector2D
from client.entities.entity_model import Component, TransformComponent

@dataclass
class MovementComponent(Component):
    speed: float = 60.0  # units per sec
    base_speed: float = 60.0
    speed_multiplier: float = 1.0
    waypoints: List[Vector2D] = field(default_factory=list)
    current_waypoint_index: int = 0
    is_flying: bool = False
    has_reached_goal: bool = False
    total_distance_traveled: float = 0.0

    @property
    def current_speed(self) -> float:
        return max(5.0, self.speed * self.speed_multiplier)

    def set_path(self, waypoints: List[Vector2D]) -> None:
        self.waypoints = [w.copy() for w in waypoints]
        self.current_waypoint_index = 0
        self.has_reached_goal = False

    def get_current_target(self) -> Optional[Vector2D]:
        if not self.waypoints or self.current_waypoint_index >= len(self.waypoints):
            return None
        return self.waypoints[self.current_waypoint_index]

    def advance_towards_target(self, current_pos: Vector2D, delta_time: float) -> Tuple[Vector2D, float]:
        target = self.get_current_target()
        if not target:
            self.has_reached_goal = True
            return (current_pos, 0.0)

        step = self.current_speed * delta_time
        to_target = target - current_pos
        dist = to_target.magnitude()

        if dist <= step or dist <= 1e-4:
            self.total_distance_traveled += dist
            self.current_waypoint_index += 1
            if self.current_waypoint_index >= len(self.waypoints):
                self.has_reached_goal = True
                return (target.copy(), to_target.angle())
            return (target.copy(), to_target.angle())

        new_pos = current_pos + (to_target / dist) * step
        self.total_distance_traveled += step
        return (new_pos, to_target.angle())
