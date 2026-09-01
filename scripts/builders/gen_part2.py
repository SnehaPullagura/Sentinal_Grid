import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate():
    print("Generating Part 2: Dual-Layer Navigation & Pathfinding...")

    # 1. client/navigation/grid_graph.py
    write_file("client/navigation/grid_graph.py", """from __future__ import annotations
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
""")

    # 2. client/navigation/astar.py
    write_file("client/navigation/astar.py", """from __future__ import annotations
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
""")

    # 3. client/navigation/dynamic_obstacles.py
    write_file("client/navigation/dynamic_obstacles.py", """from __future__ import annotations
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
""")

    # 4. client/navigation/path_cache.py
    write_file("client/navigation/path_cache.py", """from __future__ import annotations
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
""")

    # 5. client/navigation/movement_controller.py
    write_file("client/navigation/movement_controller.py", """from __future__ import annotations
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
""")

    print("Part 2 Complete.")

if __name__ == "__main__":
    generate()
