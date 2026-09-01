import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate_scale_modules():
    print("--> Generating Enterprise Scale Domain Modules...")

    # 1. client/combat/calculators/chain_lightning_propagator.py
    write_file("client/combat/calculators/chain_lightning_propagator.py", """from __future__ import annotations
from dataclasses import dataclass
from typing import List, Set, Tuple, Optional
from client.math.vector2d import Vector2D

@dataclass
class ChainTargetHit:
    entity_id: str
    position: Vector2D
    damage_dealt: float
    chain_index: int

class ChainLightningPropagator:
    @staticmethod
    def resolve_chain(
        origin_pos: Vector2D,
        initial_target_id: str,
        initial_target_pos: Vector2D,
        base_damage: float,
        max_chains: int = 4,
        jump_radius: float = 90.0,
        decay_factor: float = 0.75,
        candidate_entities: Optional[List[Tuple[str, Vector2D]]] = None
    ) -> List[ChainTargetHit]:
        hits: List[ChainTargetHit] = []
        visited: Set[str] = {initial_target_id}

        # First hit
        hits.append(ChainTargetHit(
            entity_id=initial_target_id,
            position=initial_target_pos.copy(),
            damage_dealt=base_damage,
            chain_index=0
        ))

        if not candidate_entities:
            return hits

        current_pos = initial_target_pos
        current_damage = base_damage

        for chain_idx in range(1, max_chains):
            current_damage *= decay_factor
            next_candidate = None
            closest_dist_sq = jump_radius * jump_radius

            for eid, pos in candidate_entities:
                if eid in visited:
                    continue
                d_sq = current_pos.distance_to_squared(pos)
                if d_sq <= closest_dist_sq:
                    closest_dist_sq = d_sq
                    next_candidate = (eid, pos)

            if next_candidate:
                eid, pos = next_candidate
                visited.add(eid)
                hits.append(ChainTargetHit(
                    entity_id=eid,
                    position=pos.copy(),
                    damage_dealt=round(current_damage, 2),
                    chain_index=chain_idx
                ))
                current_pos = pos
            else:
                break

        return hits
""")

    # 2. client/combat/calculators/critical_strike_matrix.py
    write_file("client/combat/calculators/critical_strike_matrix.py", """from __future__ import annotations
from dataclasses import dataclass
from client.core.rng import DeterministicRNG

@dataclass
class CritRollResult:
    is_critical: bool
    is_super_critical: bool
    multiplier: float
    total_damage: float

class CriticalStrikeMatrix:
    @staticmethod
    def evaluate_strike(
        raw_damage: float,
        crit_chance: float,
        crit_multiplier: float = 2.0,
        rng: DeterministicRNG = None
    ) -> CritRollResult:
        if rng is None:
            rng = DeterministicRNG()

        roll = rng.next_float()
        if roll <= crit_chance:
            # Check for super critical strike if crit_chance > 1.0
            if crit_chance > 1.0 and (roll <= crit_chance - 1.0):
                return CritRollResult(
                    is_critical=True,
                    is_super_critical=True,
                    multiplier=crit_multiplier * 1.5,
                    total_damage=round(raw_damage * crit_multiplier * 1.5, 2)
                )
            return CritRollResult(
                is_critical=True,
                is_super_critical=False,
                multiplier=crit_multiplier,
                total_damage=round(raw_damage * crit_multiplier, 2)
            )

        return CritRollResult(
            is_critical=False,
            is_super_critical=False,
            multiplier=1.0,
            total_damage=round(raw_damage, 2)
        )
""")

    # 3. client/navigation/advanced/flow_field_generator.py
    write_file("client/navigation/advanced/flow_field_generator.py", """from __future__ import annotations
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
""")

    # 4. client/adaptive/advanced/vulnerability_heatmap.py
    write_file("client/adaptive/advanced/vulnerability_heatmap.py", """from __future__ import annotations
from typing import Dict, Tuple, List
from client.math.vector2d import Vector2D
from client.simulation.spatial_hash import SpatialHashGrid

class VulnerabilityHeatmap:
    def __init__(self, width: int = 32, height: int = 24, cell_size: float = 32.0):
        self.width: int = width
        self.height: int = height
        self.cell_size: float = cell_size
        self.coverage_grid: Dict[Tuple[int, int], float] = {}

    def compute_coverage(self, tower_positions: List[Tuple[Vector2D, float]]) -> None:
        self.coverage_grid.clear()
        for gx in range(self.width):
            for gy in range(self.height):
                cell_world = Vector2D((gx + 0.5) * self.cell_size, (gy + 0.5) * self.cell_size)
                total_coverage = 0.0
                for tpos, trange in tower_positions:
                    d = cell_world.distance_to(tpos)
                    if d <= trange:
                        total_coverage += max(0.1, 1.0 - (d / trange))
                self.coverage_grid[(gx, gy)] = total_coverage

    def find_vulnerable_sectors(self, threshold: float = 0.5) -> List[Tuple[int, int]]:
        return [cell for cell, cov in self.coverage_grid.items() if cov < threshold]
""")

if __name__ == "__main__":
    generate_scale_modules()
