from __future__ import annotations
from typing import Optional, List, Callable
from dataclasses import dataclass
from client.entities.entity_model import Component, Entity, TransformComponent, HealthComponent
from client.navigation.movement_controller import MovementComponent
from client.ai.behavior_tree import BehaviorNode, SequenceNode, SelectorNode, ActionNode, ConditionNode, NodeStatus

@dataclass
class AIContext:
    entity: Entity
    delta_time: float
    nearest_tower: Optional[Entity] = None
    allies_in_range: List[Entity] = None
    target_base_pos: Optional[Any] = None

class EnemyAIComponent(Component):
    def __init__(self):
        self.root_node: Optional[BehaviorNode] = None
        self._build_default_tree()

    def _build_default_tree(self) -> None:
        def move_forward(ctx: AIContext) -> NodeStatus:
            mv = ctx.entity.get_component(MovementComponent)
            tf = ctx.entity.get_component(TransformComponent)
            if mv and tf:
                new_pos, rot = mv.advance_towards_target(tf.position, ctx.delta_time)
                tf.position = new_pos
                tf.rotation = rot
                return NodeStatus.SUCCESS
            return NodeStatus.FAILURE

        self.root_node = ActionNode(move_forward)

    def tick(self, context: AIContext) -> NodeStatus:
        if self.root_node:
            return self.root_node.tick(context)
        return NodeStatus.SUCCESS
