from __future__ import annotations
from enum import Enum, auto
from typing import List, Optional, Callable
from client.math.vector2d import Vector2D
from client.entities.entity_model import Entity, TransformComponent, HealthComponent
from client.navigation.movement_controller import MovementComponent
from client.simulation.spatial_hash import SpatialHashGrid

class TargetingStrategy(Enum):
    FIRST = auto()
    LAST = auto()
    CLOSEST = auto()
    STRONGEST = auto()
    WEAKEST = auto()
    HIGHEST_THREAT = auto()
    FLYING_ONLY = auto()
    GROUND_ONLY = auto()

class TargetingPipeline:
    @staticmethod
    def select_target(
        tower_pos: Vector2D,
        range_radius: float,
        strategy: TargetingStrategy,
        spatial_grid: SpatialHashGrid,
        entity_resolver: Callable[[str], Optional[Entity]]
    ) -> Optional[Entity]:
        candidate_ids = spatial_grid.query_radius(tower_pos, range_radius)
        if not candidate_ids:
            return None

        candidates: List[Entity] = []
        for cid in candidate_ids:
            ent = entity_resolver(cid)
            if ent and ent.is_active and ent.tag == "Enemy":
                hp = ent.get_component(HealthComponent)
                if hp and hp.is_alive:
                    candidates.append(ent)

        if not candidates:
            return None

        if strategy == TargetingStrategy.CLOSEST:
            return min(candidates, key=lambda e: tower_pos.distance_to_squared(e.require_component(TransformComponent).position))

        if strategy == TargetingStrategy.STRONGEST:
            return max(candidates, key=lambda e: e.require_component(HealthComponent).current_health)

        if strategy == TargetingStrategy.WEAKEST:
            return min(candidates, key=lambda e: e.require_component(HealthComponent).current_health)

        if strategy == TargetingStrategy.FIRST:
            return max(candidates, key=lambda e: getattr(e.get_component(MovementComponent), "total_distance_traveled", 0.0))

        if strategy == TargetingStrategy.LAST:
            return min(candidates, key=lambda e: getattr(e.get_component(MovementComponent), "total_distance_traveled", 0.0))

        if strategy == TargetingStrategy.FLYING_ONLY:
            flying = [c for c in candidates if getattr(c.get_component(MovementComponent), "is_flying", False)]
            return flying[0] if flying else None

        if strategy == TargetingStrategy.GROUND_ONLY:
            ground = [c for c in candidates if not getattr(c.get_component(MovementComponent), "is_flying", False)]
            return ground[0] if ground else None

        return candidates[0]
