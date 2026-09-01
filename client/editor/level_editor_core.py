from __future__ import annotations
from typing import List, Dict, Tuple, Optional
import json
from client.math.vector2d import Vector2D
from client.maps.map_definition import MapDefinition

class LevelEditorCore:
    def __init__(self, width: int = 32, height: int = 24):
        self.map_def: MapDefinition = MapDefinition(
            map_id="custom_map_01",
            name="Custom Battleground",
            width=width,
            height=height
        )

    def set_cell_blocked(self, gx: int, gy: int, blocked: bool = True) -> None:
        pt = (gx, gy)
        if blocked and pt not in self.map_def.blocked_cells:
            self.map_def.blocked_cells.append(pt)
        elif not blocked and pt in self.map_def.blocked_cells:
            self.map_def.blocked_cells.remove(pt)

    def add_spawn_point(self, world_x: float, world_y: float) -> None:
        self.map_def.spawn_points.append(Vector2D(world_x, world_y))

    def set_base_objective(self, world_x: float, world_y: float) -> None:
        self.map_def.base_objective_pos = Vector2D(world_x, world_y)

    def export_json(self) -> str:
        return json.dumps({
            "map_id": self.map_def.map_id,
            "name": self.map_def.name,
            "width": self.map_def.width,
            "height": self.map_def.height,
            "cell_size": self.map_def.cell_size,
            "spawn_points": [p.to_tuple() for p in self.map_def.spawn_points],
            "base_objective": self.map_def.base_objective_pos.to_tuple(),
            "blocked_cells": self.map_def.blocked_cells,
            "starting_credits": self.map_def.starting_credits,
            "total_waves": self.map_def.total_waves
        }, indent=2)
