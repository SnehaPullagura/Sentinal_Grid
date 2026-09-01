from __future__ import annotations
from abc import ABC
from typing import Dict, Type, TypeVar, Optional, List
from dataclasses import dataclass, field
import uuid
from client.math.vector2d import Vector2D

C = TypeVar("C", bound="Component")

class Component(ABC):
    entity_id: str = ""
    def on_attach(self, entity: Entity) -> None: self.entity_id = entity.id
    def on_detach(self) -> None: self.entity_id = ""
    def serialize(self) -> dict: return {}
    def deserialize(self, data: dict) -> None: pass

class Entity:
    __slots__ = ("id", "name", "tag", "is_active", "is_destroyed", "created_tick", "_components")

    def __init__(self, name: str = "Entity", tag: str = "Untagged", entity_id: Optional[str] = None, tick: int = 0):
        self.id: str = entity_id or str(uuid.uuid4())
        self.name: str = name
        self.tag: str = tag
        self.is_active: bool = True
        self.is_destroyed: bool = False
        self.created_tick: int = tick
        self._components: Dict[Type[Component], Component] = {}

    def add_component(self, component: C) -> C:
        comp_type = type(component)
        if comp_type in self._components:
            self._components[comp_type].on_detach()
        self._components[comp_type] = component
        component.on_attach(self)
        return component

    def get_component(self, comp_type: Type[C]) -> Optional[C]:
        return self._components.get(comp_type) # type: ignore

    def require_component(self, comp_type: Type[C]) -> C:
        comp = self.get_component(comp_type)
        if comp is None:
            raise KeyError(f"Entity {self.name} missing component {comp_type.__name__}")
        return comp

    def has_component(self, comp_type: Type[Component]) -> bool:
        return comp_type in self._components

    def remove_component(self, comp_type: Type[Component]) -> bool:
        if comp_type in self._components:
            comp = self._components.pop(comp_type)
            comp.on_detach()
            return True
        return False

    def destroy(self) -> None:
        self.is_active = False
        self.is_destroyed = True
        for comp in list(self._components.values()):
            comp.on_detach()
        self._components.clear()

    def get_all_components(self) -> List[Component]:
        return list(self._components.values())

@dataclass
class TransformComponent(Component):
    position: Vector2D = field(default_factory=Vector2D.zero)
    rotation: float = 0.0
    scale: Vector2D = field(default_factory=Vector2D.one)
    bounding_radius: float = 16.0

    def serialize(self) -> dict:
        return {"position": self.position.as_dict(), "rotation": self.rotation, "bounding_radius": self.bounding_radius}

    def deserialize(self, data: dict) -> None:
        if "position" in data:
            self.position = Vector2D(data["position"]["x"], data["position"]["y"])
        self.rotation = float(data.get("rotation", 0.0))
        self.bounding_radius = float(data.get("bounding_radius", 16.0))

@dataclass
class HealthComponent(Component):
    max_health: float = 100.0
    current_health: float = 100.0
    shield_max: float = 0.0
    shield_current: float = 0.0
    armor: float = 0.0
    resistance_energy: float = 0.0
    resistance_kinetic: float = 0.0
    is_invulnerable: bool = False

    @property
    def is_alive(self) -> bool: return self.current_health > 0.0
    @property
    def health_percentage(self) -> float: return max(0.0, min(1.0, self.current_health / max(1.0, self.max_health)))
    @property
    def total_effective_hp(self) -> float: return self.current_health + self.shield_current

    def take_damage(self, amount: float, damage_type: str = "kinetic") -> float:
        if self.is_invulnerable or amount <= 0.0: return 0.0

        dmg = amount
        if damage_type == "kinetic":
            dmg = max(1.0, dmg - self.armor) * (1.0 - max(-1.0, min(0.9, self.resistance_kinetic)))
        elif damage_type == "energy":
            dmg = dmg * (1.0 - max(-1.0, min(0.9, self.resistance_energy)))

        actual_damage = dmg
        if self.shield_current > 0.0:
            if self.shield_current >= actual_damage:
                self.shield_current -= actual_damage
                return actual_damage
            else:
                actual_damage -= self.shield_current
                self.shield_current = 0.0

        self.current_health = max(0.0, self.current_health - actual_damage)
        return dmg

    def heal(self, amount: float) -> float:
        if not self.is_alive or amount <= 0.0: return 0.0
        old = self.current_health
        self.current_health = min(self.max_health, self.current_health + amount)
        return self.current_health - old

    def recharge_shield(self, amount: float) -> float:
        if self.shield_max <= 0.0 or amount <= 0.0: return 0.0
        old = self.shield_current
        self.shield_current = min(self.shield_max, self.shield_current + amount)
        return self.shield_current - old
