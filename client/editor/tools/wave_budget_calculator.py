"""
Level Editor Tool: WaveBudgetCalculator
Estimates economic viability and threat balance curve across 20+ waves
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional
from client.math.vector2d import Vector2D
from client.maps.map_definition import MapDefinition
from client.navigation.grid_graph import GridGraph
from client.navigation.astar import AStarPathfinder

class WaveBudgetCalculator:
    def __init__(self):
        self.validation_errors: List[str] = []
        self.is_valid: bool = True

    def validate_map(self, map_def: MapDefinition) -> bool:
        self.validation_errors.clear()
        self.is_valid = True

        if len(map_def.spawn_points) == 0:
            self.validation_errors.append("Map requires at least one valid spawn point.")
            self.is_valid = False

        if map_def.base_objective_pos == Vector2D.zero():
            self.validation_errors.append("Base objective coordinate cannot be at origin.")
            self.is_valid = False

        return self.is_valid

    def get_summary(self) -> dict:
        return {
            "tool": "WaveBudgetCalculator",
            "is_valid": self.is_valid,
            "errors": list(self.validation_errors)
        }
