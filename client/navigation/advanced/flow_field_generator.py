from __future__ import annotations
from typing import Dict, Tuple, List, Optional
import math
from client.math.vector2d import Vector2D
from client.navigation.grid_graph import GridGraph

class FlowFieldGenerator:
    def __init__(self, graph: GridGraph):
        self.graph: GridGraph = graph
        self.integration_field: Dict[Tuple[int, int], float] = {}
        self.vector_field: Dict[Tuple[int, int], Vector2D] = {}

    def generate_field(self, goal_world: Vector2D) -> None:
        gx, gy = self.graph.world_to_grid(goal_world)
        self.integration_field.clear()
        self.vector_field.clear()

        # Step 1: Initialize Integration Field with Dijkstra BFS
        queue: List[Tuple[int, int]] = [(gx, gy)]
        self.integration_field[(gx, gy)] = 0.0

        while queue:
            cx, cy = queue.pop(0)
            cur_cost = self.integration_field[(cx, cy)]

            for nx, ny, move_cost in self.graph.get_neighbors(cx, cy, allow_diagonal=True):
                new_cost = cur_cost + move_cost
                if (nx, ny) not in self.integration_field or new_cost < self.integration_field[(nx, ny)]:
                    self.integration_field[(nx, ny)] = new_cost
                    queue.append((nx, ny))

        # Step 2: Calculate Flow Vectors pointing down the gradient
        for cx in range(self.graph.width):
            for cy in range(self.graph.height):
                best_cost = self.integration_field.get((cx, cy), float("inf"))
                best_dir = Vector2D.zero()

                for dx, dy in [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]:
                    nx, ny = cx + dx, cy + dy
                    cost = self.integration_field.get((nx, ny), float("inf"))
                    if cost < best_cost:
                        best_cost = cost
                        best_dir = Vector2D(float(dx), float(dy)).normalized()

                self.vector_field[(cx, cy)] = best_dir

    def get_flow_vector(self, world_pos: Vector2D) -> Vector2D:
        gx, gy = self.graph.world_to_grid(world_pos)
        return self.vector_field.get((gx, gy), Vector2D.zero())
