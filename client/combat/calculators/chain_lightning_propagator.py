from __future__ import annotations
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
