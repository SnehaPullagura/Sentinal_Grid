"""
Sector 11 Tactical Map Layout.
Grid-based terrain classification, dynamic obstacle zones, elevation choke points,
and dual spawn-to-goal vector trajectories.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple
from client.math.vector2d import Vector2D
from client.maps.map_definition import MapDefinition

class Sector11Map:
    @staticmethod
    def create_definition() -> MapDefinition:
        blocked = [(x, y) for x in range(8, 15) for y in range(4, 9)]
        platforms = [(x, y) for x in range(2, 30) for y in range(2, 22) if (x, y) not in blocked]
        
        return MapDefinition(
            map_id="sector_11",
            name="Combat Zone Sector 11",
            width=32,
            height=24,
            cell_size=32.0,
            spawn_points=[Vector2D(16.0, 16.0), Vector2D(16.0, 700.0)],
            base_objective_pos=Vector2D(960.0, 350.0),
            blocked_cells=blocked,
            build_platforms=platforms,
            starting_credits=620,
            starting_energy=155,
            base_hp=100.0,
            total_waves=15
        )
