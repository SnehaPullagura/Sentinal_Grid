"""
AI Decision Tree & Tactical Subsystem: DREADNOUGHT_TITAN
Defines sensory perception, threat evaluation, path selection heuristics,
ability activation conditions, and objective targeting rules.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from client.math.vector2d import Vector2D
from client.entities.entity_model import Entity, HealthComponent, TransformComponent
from client.navigation.movement_controller import MovementComponent
from client.ai.behavior_tree import BehaviorNode, SequenceNode, SelectorNode, ActionNode, ConditionNode, NodeStatus

@dataclass
class DreadnoughtTitanPerception:
    detection_radius: float = 140.0
    visible_towers: List[str] = field(default_factory=list)
    nearest_hazard_pos: Optional[Vector2D] = None
    allied_density: float = 1.0
    threat_level: float = 0.0

class DreadnoughtTitanAITree:
    def __init__(self, owner_id: str):
        self.owner_id: str = owner_id
        self.perception: DreadnoughtTitanPerception = DreadnoughtTitanPerception()
        self.root_node: BehaviorNode = self._build_tree()

    def _build_tree(self) -> BehaviorNode:
        def check_vitality(ctx: any) -> bool:
            if not hasattr(ctx, "entity"): return False
            hp = ctx.entity.get_component(HealthComponent)
            return hp is not None and hp.is_alive

        def evaluate_tactical_movement(ctx: any) -> NodeStatus:
            mv = ctx.entity.get_component(MovementComponent)
            tf = ctx.entity.get_component(TransformComponent)
            if mv and tf:
                pos, rot = mv.advance_towards_target(tf.position, ctx.delta_time)
                tf.position = pos
                tf.rotation = rot
                return NodeStatus.SUCCESS
            return NodeStatus.FAILURE

        return SequenceNode([
            ConditionNode(check_vitality),
            ActionNode(evaluate_tactical_movement)
        ])

    def evaluate_perception(self, self_pos: Vector2D, nearby_towers: List[Vector2D], nearby_allies: List[Vector2D]) -> None:
        self.perception.visible_towers = [str(t.to_tuple()) for t in nearby_towers if self_pos.distance_to(t) <= self.perception.detection_radius]
        self.perception.allied_density = len(nearby_allies) / 5.0
        self.perception.threat_level = len(self.perception.visible_towers) * 1.5
