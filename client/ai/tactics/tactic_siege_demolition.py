"""
AI Tactic Behavior: SiegeDemolitionTactic
Focuses primary attacks on player barricades and support towers
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
from client.math.vector2d import Vector2D
from client.entities.entity_model import Entity, HealthComponent, TransformComponent
from client.navigation.movement_controller import MovementComponent
from client.ai.behavior_tree import BehaviorNode, NodeStatus

class SiegeDemolitionTactic(BehaviorNode):
    def __init__(self, priority_weight: float = 1.0):
        self.priority_weight: float = priority_weight
        self.last_execution_tick: int = 0

    def tick(self, context: any) -> NodeStatus:
        if not context or not hasattr(context, "entity"):
            return NodeStatus.FAILURE
        
        ent: Entity = context.entity
        hp = ent.get_component(HealthComponent)
        mv = ent.get_component(MovementComponent)
        
        if hp and hp.is_alive and mv:
            # Execute behavior
            return NodeStatus.SUCCESS
        return NodeStatus.FAILURE
