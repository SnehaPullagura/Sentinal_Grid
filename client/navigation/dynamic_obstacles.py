from __future__ import annotations
from typing import Dict, List, Set, Tuple, Optional, Callable
from client.math.vector2d import Vector2D
from client.navigation.grid_graph import GridGraph

class DynamicObstacleManager:
    def __init__(self, graph: GridGraph):
        self.graph: GridGraph = graph
        self._obstacles: Dict[str, List[Tuple[int, int]]] = {}
        self._on_grid_invalidated: List[Callable[[], None]] = []

    def register_invalidation_listener(self, listener: Callable[[], None]) -> None:
        self._on_grid_invalidated.append(listener)

    def add_obstacle(self, obstacle_id: str, world_pos: Vector2D, radius: float = 16.0) -> bool:
        center_gx, center_gy = self.graph.world_to_grid(world_pos)
        grid_r = max(1, int(radius // self.graph.cell_size))

        occupied_cells = []
        for dx in range(-grid_r, grid_r + 1):
            for dy in range(-grid_r, grid_r + 1):
                gx, gy = center_gx + dx, center_gy + dy
                cell = self.graph.get_cell(gx, gy)
                if cell:
                    cell.is_blocked = True
                    occupied_cells.append((gx, gy))

        self._obstacles[obstacle_id] = occupied_cells
        self._notify_invalidated()
        return True

    def remove_obstacle(self, obstacle_id: str) -> bool:
        if obstacle_id not in self._obstacles:
            return False
        cells = self._obstacles.pop(obstacle_id)
        for gx, gy in cells:
            cell = self.graph.get_cell(gx, gy)
            if cell and not cell.has_tower:
                cell.is_blocked = False
        self._notify_invalidated()
        return True

    def _notify_invalidated(self) -> None:
        for cb in self._on_grid_invalidated:
            try:
                cb()
            except Exception as ex:
                print(f"Obstacle invalidation listener error: {ex}")
