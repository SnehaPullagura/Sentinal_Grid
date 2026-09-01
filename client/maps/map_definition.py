from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from client.math.vector2d import Vector2D

@dataclass
class MapDefinition:
    map_id: str
    name: str
    width: int = 32
    height: int = 24
    cell_size: float = 32.0
    spawn_points: List[Vector2D] = field(default_factory=list)
    base_objective_pos: Vector2D = field(default_factory=Vector2D.zero)
    blocked_cells: List[Tuple[int, int]] = field(default_factory=list)
    build_platforms: List[Tuple[int, int]] = field(default_factory=list)
    starting_credits: int = 450
    starting_energy: int = 100
    base_hp: float = 100.0
    total_waves: int = 15

def get_default_map() -> MapDefinition:
    return MapDefinition(
        map_id="map_alpha_outpost",
        name="Sector 7 Outpost",
        width=32,
        height=24,
        spawn_points=[Vector2D(16.0, 16.0), Vector2D(16.0, 700.0)],
        base_objective_pos=Vector2D(980.0, 380.0),
        blocked_cells=[(10, 5), (10, 6), (10, 7), (15, 12), (15, 13), (20, 18)],
        build_platforms=[(x, y) for x in range(4, 28) for y in range(4, 20)]
    )
