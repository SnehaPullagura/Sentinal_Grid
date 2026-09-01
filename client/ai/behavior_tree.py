from __future__ import annotations
from enum import Enum, auto
from abc import ABC, abstractmethod
from typing import List, Optional, Callable, Any

class NodeStatus(Enum):
    SUCCESS = auto()
    FAILURE = auto()
    RUNNING = auto()

class BehaviorNode(ABC):
    @abstractmethod
    def tick(self, context: Any) -> NodeStatus:
        pass

class SequenceNode(BehaviorNode):
    def __init__(self, children: List[BehaviorNode]):
        self.children: List[BehaviorNode] = children

    def tick(self, context: Any) -> NodeStatus:
        for child in self.children:
            status = child.tick(context)
            if status != NodeStatus.SUCCESS:
                return status
        return NodeStatus.SUCCESS

class SelectorNode(BehaviorNode):
    def __init__(self, children: List[BehaviorNode]):
        self.children: List[BehaviorNode] = children

    def tick(self, context: Any) -> NodeStatus:
        for child in self.children:
            status = child.tick(context)
            if status != NodeStatus.FAILURE:
                return status
        return NodeStatus.FAILURE

class ActionNode(BehaviorNode):
    def __init__(self, action_fn: Callable[[Any], NodeStatus]):
        self.action_fn: Callable[[Any], NodeStatus] = action_fn

    def tick(self, context: Any) -> NodeStatus:
        return self.action_fn(context)

class ConditionNode(BehaviorNode):
    def __init__(self, predicate_fn: Callable[[Any], bool]):
        self.predicate_fn: Callable[[Any], bool] = predicate_fn

    def tick(self, context: Any) -> NodeStatus:
        return NodeStatus.SUCCESS if self.predicate_fn(context) else NodeStatus.FAILURE
