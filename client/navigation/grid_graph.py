from __future__ import annotations
from enum import Enum, auto
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from client.math.vector2d import Vector2D

class TerrainType(Enum):
    OPEN_GROUND = 1
    BLOCKED_TERRAIN = 2
    BUILD_PLATFORM = 3
    HAZARD_ZONE = 4
    HIGHWAY_PATH = 5
    WATER_OBSTACLE = 6
    ELEVATED_GROUND = 7

@dataclass
class GridCell:
    x: int
    y: int
    terrain: TerrainType = TerrainType.OPEN_GROUND
    base_cost: float = 1.0
    dynamic_cost_modifier: float = 0.0
    is_blocked: bool = False
    is_buildable: bool = False
    has_tower: bool = False
    tower_id: Optional[str] = None

    @property
    def travel_cost(self) -> float:
        if self.is_blocked or self.has_tower or self.terrain == TerrainType.BLOCKED_TERRAIN:
            return float("inf")
        return max(0.1, self.base_cost + self.dynamic_cost_modifier)

class GridGraph:
    def __init__(self, width: int = 32, height: int = 24, cell_size: float = 32.0):
        self.width: int = width
        self.height: int = height
        self.cell_size: float = cell_size
        self.cells: Dict[Tuple[int, int], GridCell] = {}
        self._initialize_grid()

    def _initialize_grid(self) -> None:
        for x in range(self.width):
            for y in range(self.height):
                self.cells[(x, y)] = GridCell(x=x, y=y, is_buildable=True)

    def world_to_grid(self, world_pos: Vector2D) -> Tuple[int, int]:
        gx = int(world_pos.x // self.cell_size)
        gy = int(world_pos.y // self.cell_size)
        return (max(0, min(self.width - 1, gx)), max(0, min(self.height - 1, gy)))

    def grid_to_world(self, gx: int, gy: int) -> Vector2D:
        return Vector2D((gx + 0.5) * self.cell_size, (gy + 0.5) * self.cell_size)

    def get_cell(self, gx: int, gy: int) -> Optional[GridCell]:
        return self.cells.get((gx, gy))

    def set_terrain(self, gx: int, gy: int, terrain: TerrainType, is_buildable: bool = False) -> None:
        cell = self.get_cell(gx, gy)
        if cell:
            cell.terrain = terrain
            cell.is_buildable = is_buildable
            if terrain == TerrainType.BLOCKED_TERRAIN:
                cell.is_blocked = True
                cell.base_cost = float("inf")
            elif terrain == TerrainType.HIGHWAY_PATH:
                cell.base_cost = 0.5
                cell.is_blocked = False

    def place_tower(self, gx: int, gy: int, tower_id: str) -> bool:
        cell = self.get_cell(gx, gy)
        if not cell or not cell.is_buildable or cell.has_tower or cell.is_blocked:
            return False
        cell.has_tower = True
        cell.tower_id = tower_id
        return True

    def remove_tower(self, gx: int, gy: int) -> bool:
        cell = self.get_cell(gx, gy)
        if not cell or not cell.has_tower:
            return False
        cell.has_tower = False
        cell.tower_id = None
        return True

    def get_neighbors(self, gx: int, gy: int, allow_diagonal: bool = True) -> List[Tuple[int, int, float]]:
        neighbors = []
        # Orthogonal
        ortho_dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in ortho_dirs:
            nx, ny = gx + dx, gy + dy
            cell = self.get_cell(nx, ny)
            if cell and not math.isinf(cell.travel_cost):
                neighbors.append((nx, ny, cell.travel_cost))

        # Diagonal
        if allow_diagonal:
            diag_dirs = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dx, dy in diag_dirs:
                nx, ny = gx + dx, gy + dy
                cell = self.get_cell(nx, ny)
                c_orth1 = self.get_cell(gx + dx, gy)
                c_orth2 = self.get_cell(gx, gy + dy)
                if (cell and not math.isinf(cell.travel_cost) and
                    c_orth1 and not math.isinf(c_orth1.travel_cost) and
                    c_orth2 and not math.isinf(c_orth2.travel_cost)):
                    neighbors.append((nx, ny, cell.travel_cost * 1.4142))
        return neighbors
import math
