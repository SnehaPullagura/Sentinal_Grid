from __future__ import annotations
import heapq
import math
from typing import Dict, List, Tuple, Optional, Set
from client.math.vector2d import Vector2D
from client.navigation.grid_graph import GridGraph

class AStarPathfinder:
    def __init__(self, graph: GridGraph):
        self.graph: GridGraph = graph

    def _heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        dx = abs(a[0] - b[0])
        dy = abs(a[1] - b[1])
        # Octile heuristic
        return (dx + dy) + (1.4142 - 2.0) * min(dx, dy)

    def find_path(
        self,
        start_world: Vector2D,
        goal_world: Vector2D,
        allow_diagonal: bool = True
    ) -> Optional[List[Vector2D]]:
        start_grid = self.graph.world_to_grid(start_world)
        goal_grid = self.graph.world_to_grid(goal_world)

        if start_grid == goal_grid:
            return [start_world.copy(), goal_world.copy()]

        goal_cell = self.graph.get_cell(*goal_grid)
        if not goal_cell or math.isinf(goal_cell.travel_cost):
            return None

        # Priority queue stores (f_score, counter, (gx, gy))
        open_set = []
        counter = 0
        heapq.heappush(open_set, (0.0, counter, start_grid))
        
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        g_score: Dict[Tuple[int, int], float] = {start_grid: 0.0}
        f_score: Dict[Tuple[int, int], float] = {start_grid: self._heuristic(start_grid, goal_grid)}
        closed_set: Set[Tuple[int, int]] = set()

        while open_set:
            _, _, current = heapq.heappop(open_set)

            if current == goal_grid:
                # Reconstruct path
                path_grid = [current]
                while current in came_from:
                    current = came_from[current]
                    path_grid.append(current)
                path_grid.reverse()

                # Convert to world coords
                waypoints = [self.graph.grid_to_world(gx, gy) for gx, gy in path_grid]
                if waypoints:
                    waypoints[0] = start_world.copy()
                    waypoints[-1] = goal_world.copy()
                return self._smooth_path(waypoints)

            closed_set.add(current)

            for nx, ny, move_cost in self.graph.get_neighbors(current[0], current[1], allow_diagonal):
                neighbor = (nx, ny)
                if neighbor in closed_set:
                    continue

                tentative_g = g_score[current] + move_cost
                if tentative_g < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    h = self._heuristic(neighbor, goal_grid)
                    f = tentative_g + h
                    f_score[neighbor] = f
                    counter += 1
                    heapq.heappush(open_set, (f, counter, neighbor))

        return None

    def _smooth_path(self, waypoints: List[Vector2D]) -> List[Vector2D]:
        if len(waypoints) <= 2:
            return waypoints
        smoothed = [waypoints[0]]
        i = 0
        while i < len(waypoints) - 1:
            furthest = i + 1
            for j in range(len(waypoints) - 1, i + 1, -1):
                if self._has_line_of_sight(waypoints[i], waypoints[j]):
                    furthest = j
                    break
            smoothed.append(waypoints[furthest])
            i = furthest
        return smoothed

    def _has_line_of_sight(self, p1: Vector2D, p2: Vector2D) -> bool:
        dist = p1.distance_to(p2)
        steps = max(2, int(dist / (self.graph.cell_size * 0.4)))
        for s in range(1, steps):
            t = s / steps
            inter = p1.lerp(p2, t)
            gx, gy = self.graph.world_to_grid(inter)
            cell = self.graph.get_cell(gx, gy)
            if not cell or math.isinf(cell.travel_cost):
                return False
        return True
