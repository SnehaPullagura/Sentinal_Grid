from __future__ import annotations
from typing import Dict, List, Set, Tuple, Any, Optional
from client.math.vector2d import Vector2D, Rect2D, Circle2D

class SpatialHashGrid:
    def __init__(self, cell_size: float = 64.0):
        self._cell_size: float = max(8.0, cell_size)
        self._grid: Dict[Tuple[int, int], Set[str]] = {}
        self._entity_cells: Dict[str, Set[Tuple[int, int]]] = {}
        self._entity_positions: Dict[str, Vector2D] = {}
        self._entity_radii: Dict[str, float] = {}

    @property
    def cell_size(self) -> float: return self._cell_size

    def _get_cells_for_circle(self, center: Vector2D, radius: float) -> Set[Tuple[int, int]]:
        cells = set()
        min_gx = int((center.x - radius) // self._cell_size)
        max_gx = int((center.x + radius) // self._cell_size)
        min_gy = int((center.y - radius) // self._cell_size)
        max_gy = int((center.y + radius) // self._cell_size)

        for gx in range(min_gx, max_gx + 1):
            for gy in range(min_gy, max_gy + 1):
                cells.add((gx, gy))
        return cells

    def insert(self, entity_id: str, position: Vector2D, radius: float = 12.0) -> None:
        self.remove(entity_id)
        cells = self._get_cells_for_circle(position, radius)
        for cell in cells:
            if cell not in self._grid:
                self._grid[cell] = set()
            self._grid[cell].add(entity_id)

        self._entity_cells[entity_id] = cells
        self._entity_positions[entity_id] = position.copy()
        self._entity_radii[entity_id] = radius

    def update(self, entity_id: str, new_position: Vector2D, radius: Optional[float] = None) -> None:
        r = radius if radius is not None else self._entity_radii.get(entity_id, 12.0)
        self.insert(entity_id, new_position, r)

    def remove(self, entity_id: str) -> bool:
        if entity_id not in self._entity_cells: return False
        cells = self._entity_cells.pop(entity_id)
        for cell in cells:
            if cell in self._grid and entity_id in self._grid[cell]:
                self._grid[cell].remove(entity_id)
                if not self._grid[cell]:
                    del self._grid[cell]
        self._entity_positions.pop(entity_id, None)
        self._entity_radii.pop(entity_id, None)
        return True

    def query_radius(self, center: Vector2D, radius: float) -> List[str]:
        query_cells = self._get_cells_for_circle(center, radius)
        candidate_ids: Set[str] = set()
        for cell in query_cells:
            if cell in self._grid:
                candidate_ids.update(self._grid[cell])

        results: List[str] = []
        radius_sq = radius * radius
        for eid in candidate_ids:
            pos = self._entity_positions.get(eid)
            if pos is not None:
                e_rad = self._entity_radii.get(eid, 0.0)
                tot_rad = radius + e_rad
                if center.distance_to_squared(pos) <= (tot_rad * tot_rad):
                    results.append(eid)
        return results

    def query_rect(self, rect: Rect2D) -> List[str]:
        min_gx = int(rect.left // self._cell_size)
        max_gx = int(rect.right // self._cell_size)
        min_gy = int(rect.top // self._cell_size)
        max_gy = int(rect.bottom // self._cell_size)

        candidate_ids: Set[str] = set()
        for gx in range(min_gx, max_gx + 1):
            for gy in range(min_gy, max_gy + 1):
                cell = (gx, gy)
                if cell in self._grid:
                    candidate_ids.update(self._grid[cell])

        results = []
        for eid in candidate_ids:
            pos = self._entity_positions.get(eid)
            rad = self._entity_radii.get(eid, 0.0)
            if pos and rect.intersects_circle(pos, rad):
                results.append(eid)
        return results

    def clear(self) -> None:
        self._grid.clear()
        self._entity_cells.clear()
        self._entity_positions.clear()
        self._entity_radii.clear()

    def get_count(self) -> int: return len(self._entity_cells)
