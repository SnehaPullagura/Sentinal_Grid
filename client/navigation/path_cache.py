from __future__ import annotations
from typing import Dict, Tuple, Optional, List
from client.math.vector2d import Vector2D
from client.navigation.astar import AStarPathfinder

class PathCache:
    def __init__(self, pathfinder: AStarPathfinder, max_entries: int = 500):
        self.pathfinder: AStarPathfinder = pathfinder
        self.max_entries: int = max_entries
        self._cache: Dict[Tuple[int, int, int, int], List[Vector2D]] = {}

    def _make_key(self, start: Vector2D, goal: Vector2D) -> Tuple[int, int, int, int]:
        sgx, sgy = self.pathfinder.graph.world_to_grid(start)
        ggx, ggy = self.pathfinder.graph.world_to_grid(goal)
        return (sgx, sgy, ggx, ggy)

    def get_path(self, start: Vector2D, goal: Vector2D) -> Optional[List[Vector2D]]:
        key = self._make_key(start, goal)
        if key in self._cache:
            path = self._cache[key]
            res = [p.copy() for p in path]
            if res:
                res[0] = start.copy()
                res[-1] = goal.copy()
            return res

        path = self.pathfinder.find_path(start, goal)
        if path:
            if len(self._cache) >= self.max_entries:
                self._cache.pop(next(iter(self._cache)))
            self._cache[key] = [p.copy() for p in path]
        return path

    def invalidate(self) -> None:
        self._cache.clear()
