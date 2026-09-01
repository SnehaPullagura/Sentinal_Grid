import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate():
    print("Generating Part 1: Core Simulation, Math, ECS...")
    
    # 1. client/math/vector2d.py
    write_file("client/math/vector2d.py", """from __future__ import annotations
import math
from typing import Tuple, Union, List, Optional
from dataclasses import dataclass

EPSILON = 1e-6

@dataclass(slots=True)
class Vector2D:
    x: float
    y: float

    @classmethod
    def zero(cls) -> Vector2D: return cls(0.0, 0.0)
    @classmethod
    def one(cls) -> Vector2D: return cls(1.0, 1.0)
    @classmethod
    def up(cls) -> Vector2D: return cls(0.0, -1.0)
    @classmethod
    def down(cls) -> Vector2D: return cls(0.0, 1.0)
    @classmethod
    def left(cls) -> Vector2D: return cls(-1.0, 0.0)
    @classmethod
    def right(cls) -> Vector2D: return cls(1.0, 0.0)
    @classmethod
    def from_angle(cls, radians: float, magnitude: float = 1.0) -> Vector2D:
        return cls(math.cos(radians) * magnitude, math.sin(radians) * magnitude)
    @classmethod
    def from_tuple(cls, t: Tuple[float, float]) -> Vector2D:
        return cls(float(t[0]), float(t[1]))

    def to_tuple(self) -> Tuple[float, float]: return (self.x, self.y)
    def to_int_tuple(self) -> Tuple[int, int]: return (int(round(self.x)), int(round(self.y)))
    def copy(self) -> Vector2D: return Vector2D(self.x, self.y)

    def __add__(self, other: Union[Vector2D, float, Tuple[float, float]]) -> Vector2D:
        if isinstance(other, Vector2D): return Vector2D(self.x + other.x, self.y + other.y)
        if isinstance(other, (int, float)): return Vector2D(self.x + other, self.y + other)
        if isinstance(other, tuple) and len(other) == 2: return Vector2D(self.x + other[0], self.y + other[1])
        return NotImplemented

    def __radd__(self, other: Union[Vector2D, float, Tuple[float, float]]) -> Vector2D: return self.__add__(other)

    def __sub__(self, other: Union[Vector2D, float, Tuple[float, float]]) -> Vector2D:
        if isinstance(other, Vector2D): return Vector2D(self.x - other.x, self.y - other.y)
        if isinstance(other, (int, float)): return Vector2D(self.x - other, self.y - other)
        if isinstance(other, tuple) and len(other) == 2: return Vector2D(self.x - other[0], self.y - other[1])
        return NotImplemented

    def __rsub__(self, other: Union[Vector2D, float, Tuple[float, float]]) -> Vector2D:
        if isinstance(other, (int, float)): return Vector2D(other - self.x, other - self.y)
        if isinstance(other, tuple) and len(other) == 2: return Vector2D(other[0] - self.x, other[1] - self.y)
        return NotImplemented

    def __mul__(self, scalar: Union[int, float, Vector2D]) -> Vector2D:
        if isinstance(scalar, (int, float)): return Vector2D(self.x * scalar, self.y * scalar)
        if isinstance(scalar, Vector2D): return Vector2D(self.x * scalar.x, self.y * scalar.y)
        return NotImplemented

    def __rmul__(self, scalar: Union[int, float, Vector2D]) -> Vector2D: return self.__mul__(scalar)

    def __truediv__(self, scalar: Union[int, float, Vector2D]) -> Vector2D:
        if isinstance(scalar, (int, float)):
            if abs(scalar) < EPSILON: raise ZeroDivisionError("Cannot divide Vector2D by zero.")
            return Vector2D(self.x / scalar, self.y / scalar)
        if isinstance(scalar, Vector2D):
            if abs(scalar.x) < EPSILON or abs(scalar.y) < EPSILON: raise ZeroDivisionError("Cannot divide Vector2D by zero.")
            return Vector2D(self.x / scalar.x, self.y / scalar.y)
        return NotImplemented

    def __neg__(self) -> Vector2D: return Vector2D(-self.x, -self.y)
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector2D): return False
        return abs(self.x - other.x) <= EPSILON and abs(self.y - other.y) <= EPSILON

    def magnitude_squared(self) -> float: return self.x * self.x + self.y * self.y
    def magnitude(self) -> float: return math.sqrt(self.magnitude_squared())
    def normalized(self) -> Vector2D:
        m = self.magnitude()
        return Vector2D.zero() if m <= EPSILON else Vector2D(self.x / m, self.y / m)

    def dot(self, other: Vector2D) -> float: return self.x * other.x + self.y * other.y
    def cross(self, other: Vector2D) -> float: return self.x * other.y - self.y * other.x
    def distance_to_squared(self, other: Vector2D) -> float:
        dx, dy = self.x - other.x, self.y - other.y
        return dx * dx + dy * dy
    def distance_to(self, other: Vector2D) -> float: return math.sqrt(self.distance_to_squared(other))
    def manhattan_distance_to(self, other: Vector2D) -> float: return abs(self.x - other.x) + abs(self.y - other.y)
    def angle(self) -> float: return math.atan2(self.y, self.x)
    def angle_to(self, other: Vector2D) -> float: return math.atan2(other.y - self.y, other.x - self.x)

    def rotate(self, radians: float) -> Vector2D:
        c, s = math.cos(radians), math.sin(radians)
        return Vector2D(self.x * c - self.y * s, self.x * s + self.y * c)

    def lerp(self, target: Vector2D, alpha: float) -> Vector2D:
        a = max(0.0, min(1.0, alpha))
        return Vector2D(self.x + (target.x - self.x) * a, self.y + (target.y - self.y) * a)

    def move_towards(self, target: Vector2D, max_delta: float) -> Vector2D:
        to_v = target - self
        d = to_v.magnitude()
        if d <= max_delta or d <= EPSILON: return target.copy()
        return self + (to_v / d) * max_delta

    def clamp_magnitude(self, max_length: float) -> Vector2D:
        m_sq = self.magnitude_squared()
        if m_sq > max_length * max_length and m_sq > 0:
            return self.normalized() * max_length
        return self.copy()

    def round_to(self, decimals: int = 4) -> Vector2D:
        return Vector2D(round(self.x, decimals), round(self.y, decimals))

    def as_dict(self) -> dict: return {"x": self.x, "y": self.y}

@dataclass(slots=True)
class Rect2D:
    x: float
    y: float
    width: float
    height: float

    @property
    def left(self) -> float: return self.x
    @property
    def right(self) -> float: return self.x + self.width
    @property
    def top(self) -> float: return self.y
    @property
    def bottom(self) -> float: return self.y + self.height
    @property
    def center(self) -> Vector2D: return Vector2D(self.x + self.width * 0.5, self.y + self.height * 0.5)

    def contains_point(self, point: Vector2D) -> bool:
        return self.left <= point.x <= self.right and self.top <= point.y <= self.bottom

    def intersects(self, other: Rect2D) -> bool:
        return not (self.right < other.left or self.left > other.right or self.bottom < other.top or self.top > other.bottom)

    def intersects_circle(self, center: Vector2D, radius: float) -> bool:
        cx = max(self.left, min(center.x, self.right))
        cy = max(self.top, min(center.y, self.bottom))
        dx, dy = center.x - cx, center.y - cy
        return (dx * dx + dy * dy) <= (radius * radius)

    def expand(self, amount: float) -> Rect2D:
        return Rect2D(self.x - amount, self.y - amount, self.width + amount * 2.0, self.height + amount * 2.0)

@dataclass(slots=True)
class Circle2D:
    center: Vector2D
    radius: float

    def contains_point(self, point: Vector2D) -> bool:
        return self.center.distance_to_squared(point) <= (self.radius * self.radius)

    def intersects_circle(self, other: Circle2D) -> bool:
        tot = self.radius + other.radius
        return self.center.distance_to_squared(other.center) <= (tot * tot)

    def get_bounding_box(self) -> Rect2D:
        return Rect2D(self.center.x - self.radius, self.center.y - self.radius, self.radius * 2.0, self.radius * 2.0)
""")

    # 2. client/core/rng.py
    write_file("client/core/rng.py", """from __future__ import annotations
import math
from typing import List, Sequence, TypeVar, Any

T = TypeVar("T")

class DeterministicRNG:
    __slots__ = ("_state", "_inc", "_initial_seed", "_call_count")

    def __init__(self, seed: int = 42, sequence: int = 54):
        self._initial_seed = seed & 0xFFFFFFFFFFFFFFFF
        self._state: int = 0
        self._inc: int = (sequence << 1) | 1
        self._call_count: int = 0
        self.reseed(seed, sequence)

    def reseed(self, seed: int, sequence: int = 54) -> None:
        self._initial_seed = seed & 0xFFFFFFFFFFFFFFFF
        self._state = 0
        self._inc = (sequence << 1) | 1
        self._step()
        self._state = (self._state + self._initial_seed) & 0xFFFFFFFFFFFFFFFF
        self._step()
        self._call_count = 0

    def _step(self) -> None:
        self._state = (self._state * 6364136223846793005 + self._inc) & 0xFFFFFFFFFFFFFFFF

    def next_u32(self) -> int:
        self._call_count += 1
        old_state = self._state
        self._step()
        xorshifted = (((old_state >> 18) ^ old_state) >> 27) & 0xFFFFFFFF
        rot = (old_state >> 59) & 0x1F
        result = ((xorshifted >> rot) | (xorshifted << ((-rot) & 31))) & 0xFFFFFFFF
        return result

    def next_float(self) -> float:
        return self.next_u32() / 4294967296.0

    def random(self) -> float: return self.next_float()

    def uniform(self, a: float, b: float) -> float:
        return a + (b - a) * self.next_float()

    def randint(self, a: int, b: int) -> int:
        if a > b: raise ValueError(f"Lower bound {a} cannot exceed upper bound {b}")
        span = (b - a) + 1
        return a + (self.next_u32() % span)

    def choice(self, seq: Sequence[T]) -> T:
        if not seq: raise IndexError("Cannot choose from an empty sequence")
        idx = self.next_u32() % len(seq)
        return seq[idx]

    def shuffle(self, lst: List[Any]) -> None:
        n = len(lst)
        for i in range(n - 1, 0, -1):
            j = self.randint(0, i)
            lst[i], lst[j] = lst[j], lst[i]

    def chance(self, probability: float) -> bool:
        return self.next_float() < probability

    def gaussian(self, mean: float = 0.0, std_dev: float = 1.0) -> float:
        u1 = max(1e-15, self.next_float())
        u2 = self.next_float()
        z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
        return mean + z0 * std_dev

    @property
    def call_count(self) -> int: return self._call_count

    def serialize_state(self) -> dict:
        return {
            "initial_seed": self._initial_seed,
            "state": self._state,
            "inc": self._inc,
            "call_count": self._call_count
        }

    def deserialize_state(self, data: dict) -> None:
        self._initial_seed = int(data["initial_seed"])
        self._state = int(data["state"])
        self._inc = int(data["inc"])
        self._call_count = int(data.get("call_count", 0))
""")

    # 3. client/events/event_bus.py
    write_file("client/events/event_bus.py", """from __future__ import annotations
from enum import Enum, auto
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, field
import time

class EventPriority(Enum):
    CRITICAL = 0
    HIGH = 10
    NORMAL = 20
    LOW = 30
    MONITOR = 40

class GameEventType(Enum):
    SIMULATION_INITIALIZED = auto()
    SIMULATION_STARTED = auto()
    SIMULATION_PAUSED = auto()
    SIMULATION_RESUMED = auto()
    SIMULATION_TICK = auto()
    GAME_WON = auto()
    GAME_LOST = auto()
    
    WAVE_SCHEDULED = auto()
    WAVE_STARTED = auto()
    WAVE_COMPLETED = auto()
    ENEMY_SPAWNED = auto()
    ENEMY_REACHED_GOAL = auto()
    ENEMY_DEATH = auto()
    BOSS_PHASE_CHANGED = auto()
    
    TOWER_PLACEMENT_REQUESTED = auto()
    TOWER_PLACED = auto()
    TOWER_UPGRADED = auto()
    TOWER_SOLD = auto()
    TOWER_TARGET_ACQUIRED = auto()
    TOWER_ATTACK = auto()
    TOWER_DISABLED = auto()
    
    PROJECTILE_FIRED = auto()
    PROJECTILE_IMPACT = auto()
    BEAM_SWEEP = auto()
    DAMAGE_DEALT = auto()
    STATUS_EFFECT_APPLIED = auto()
    STATUS_EFFECT_EXPIRED = auto()
    
    CREDITS_CHANGED = auto()
    ENERGY_CHANGED = auto()
    TOKENS_CHANGED = auto()
    ABILITY_TRIGGERED = auto()
    BASE_HEALTH_CHANGED = auto()
    
    PLAYER_TACTIC_DETECTED = auto()
    THREAT_PROFILE_UPDATED = auto()
    DEFENSE_VULNERABILITY_FOUND = auto()

@dataclass(slots=True)
class GameEvent:
    event_type: GameEventType
    payload: Dict[str, Any]
    tick: int = 0
    timestamp: float = field(default_factory=time.time)
    source_id: Optional[str] = None
    target_id: Optional[str] = None

@dataclass
class _Subscriber:
    callback: Callable[[GameEvent], None]
    priority: EventPriority
    once: bool = False

class EventBus:
    def __init__(self):
        self._listeners: Dict[GameEventType, List[_Subscriber]] = {}
        self._global_listeners: List[_Subscriber] = []
        self._event_history: List[GameEvent] = []
        self._history_limit: int = 1000
        self._is_dispatching: bool = False
        self._queued_events: List[GameEvent] = []

    def subscribe(
        self,
        event_type: GameEventType,
        callback: Callable[[GameEvent], None],
        priority: EventPriority = EventPriority.NORMAL,
        once: bool = False
    ) -> Callable[[], None]:
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        sub = _Subscriber(callback=callback, priority=priority, once=once)
        self._listeners[event_type].append(sub)
        self._listeners[event_type].sort(key=lambda s: s.priority.value)

        def unsubscribe():
            if event_type in self._listeners and sub in self._listeners[event_type]:
                self._listeners[event_type].remove(sub)
        return unsubscribe

    def subscribe_all(
        self,
        callback: Callable[[GameEvent], None],
        priority: EventPriority = EventPriority.MONITOR
    ) -> Callable[[], None]:
        sub = _Subscriber(callback=callback, priority=priority)
        self._global_listeners.append(sub)
        self._global_listeners.sort(key=lambda s: s.priority.value)

        def unsubscribe():
            if sub in self._global_listeners:
                self._global_listeners.remove(sub)
        return unsubscribe

    def publish(self, event: GameEvent) -> None:
        if self._is_dispatching:
            self._queued_events.append(event)
            return

        self._is_dispatching = True
        try:
            self._dispatch_single(event)
            while self._queued_events:
                next_ev = self._queued_events.pop(0)
                self._dispatch_single(next_ev)
        finally:
            self._is_dispatching = False

    def _dispatch_single(self, event: GameEvent) -> None:
        self._event_history.append(event)
        if len(self._event_history) > self._history_limit:
            self._event_history.pop(0)

        if event.event_type in self._listeners:
            subscribers = list(self._listeners[event.event_type])
            for sub in subscribers:
                try:
                    sub.callback(event)
                    if sub.once and sub in self._listeners[event.event_type]:
                        self._listeners[event.event_type].remove(sub)
                except Exception as ex:
                    print(f"Error in listener for {event.event_type.name}: {ex}")

        for sub in list(self._global_listeners):
            try:
                sub.callback(event)
            except Exception as ex:
                print(f"Error in global listener: {ex}")

    def emit(self, event_type: GameEventType, tick: int = 0, source_id: Optional[str] = None, target_id: Optional[str] = None, **payload) -> None:
        self.publish(GameEvent(
            event_type=event_type,
            payload=payload,
            tick=tick,
            source_id=source_id,
            target_id=target_id
        ))

    def clear(self) -> None:
        self._listeners.clear()
        self._global_listeners.clear()
        self._event_history.clear()
        self._queued_events.clear()

    def get_history(self, event_type: Optional[GameEventType] = None) -> List[GameEvent]:
        if event_type is None:
            return list(self._event_history)
        return [e for e in self._event_history if e.event_type == event_type]
""")

    # 4. client/simulation/spatial_hash.py
    write_file("client/simulation/spatial_hash.py", """from __future__ import annotations
from typing import Dict, List, Set, Tuple, Any, Optional
from client.math.vector2d import Vector2D, Rect2D, Circle2D

class SpatialHashGrid:
    def __init__(self, cell_size: float = 64.0):
        self._cell_size: float = max(8.0, cell_size)
        self._grid: Dict[Tuple[int, int], Set[str]] = {}
        self._entity_cells: Dict[str, Set[Tuple[int, int]]] = {}
        self._entity_positions: Dict[str, Vector2D] = {}
        self._entity_radii: Dict[str, float] = {}

    @property
    def cell_size(self) -> float: return self._cell_size

    def _get_cells_for_circle(self, center: Vector2D, radius: float) -> Set[Tuple[int, int]]:
        cells = set()
        min_gx = int((center.x - radius) // self._cell_size)
        max_gx = int((center.x + radius) // self._cell_size)
        min_gy = int((center.y - radius) // self._cell_size)
        max_gy = int((center.y + radius) // self._cell_size)

        for gx in range(min_gx, max_gx + 1):
            for gy in range(min_gy, max_gy + 1):
                cells.add((gx, gy))
        return cells

    def insert(self, entity_id: str, position: Vector2D, radius: float = 12.0) -> None:
        self.remove(entity_id)
        cells = self._get_cells_for_circle(position, radius)
        for cell in cells:
            if cell not in self._grid:
                self._grid[cell] = set()
            self._grid[cell].add(entity_id)

        self._entity_cells[entity_id] = cells
        self._entity_positions[entity_id] = position.copy()
        self._entity_radii[entity_id] = radius

    def update(self, entity_id: str, new_position: Vector2D, radius: Optional[float] = None) -> None:
        r = radius if radius is not None else self._entity_radii.get(entity_id, 12.0)
        self.insert(entity_id, new_position, r)

    def remove(self, entity_id: str) -> bool:
        if entity_id not in self._entity_cells: return False
        cells = self._entity_cells.pop(entity_id)
        for cell in cells:
            if cell in self._grid and entity_id in self._grid[cell]:
                self._grid[cell].remove(entity_id)
                if not self._grid[cell]:
                    del self._grid[cell]
        self._entity_positions.pop(entity_id, None)
        self._entity_radii.pop(entity_id, None)
        return True

    def query_radius(self, center: Vector2D, radius: float) -> List[str]:
        query_cells = self._get_cells_for_circle(center, radius)
        candidate_ids: Set[str] = set()
        for cell in query_cells:
            if cell in self._grid:
                candidate_ids.update(self._grid[cell])

        results: List[str] = []
        radius_sq = radius * radius
        for eid in candidate_ids:
            pos = self._entity_positions.get(eid)
            if pos is not None:
                e_rad = self._entity_radii.get(eid, 0.0)
                tot_rad = radius + e_rad
                if center.distance_to_squared(pos) <= (tot_rad * tot_rad):
                    results.append(eid)
        return results

    def query_rect(self, rect: Rect2D) -> List[str]:
        min_gx = int(rect.left // self._cell_size)
        max_gx = int(rect.right // self._cell_size)
        min_gy = int(rect.top // self._cell_size)
        max_gy = int(rect.bottom // self._cell_size)

        candidate_ids: Set[str] = set()
        for gx in range(min_gx, max_gx + 1):
            for gy in range(min_gy, max_gy + 1):
                cell = (gx, gy)
                if cell in self._grid:
                    candidate_ids.update(self._grid[cell])

        results = []
        for eid in candidate_ids:
            pos = self._entity_positions.get(eid)
            rad = self._entity_radii.get(eid, 0.0)
            if pos and rect.intersects_circle(pos, rad):
                results.append(eid)
        return results

    def clear(self) -> None:
        self._grid.clear()
        self._entity_cells.clear()
        self._entity_positions.clear()
        self._entity_radii.clear()

    def get_count(self) -> int: return len(self._entity_cells)
""")

    # 5. client/entities/entity_model.py
    write_file("client/entities/entity_model.py", """from __future__ import annotations
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
""")

    # 6. client/simulation/game_state.py
    write_file("client/simulation/game_state.py", """from __future__ import annotations
from enum import Enum, auto
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from client.math.vector2d import Vector2D
from client.core.rng import DeterministicRNG
from client.events.event_bus import EventBus, GameEventType, GameEvent
from client.entities.entity_model import Entity, TransformComponent, HealthComponent
from client.simulation.spatial_hash import SpatialHashGrid

class SimulationStatus(Enum):
    UNINITIALIZED = auto()
    READY = auto()
    RUNNING = auto()
    PAUSED = auto()
    VICTORY = auto()
    DEFEAT = auto()

@dataclass
class SimulationStats:
    total_ticks: int = 0
    elapsed_sim_time: float = 0.0
    enemies_spawned: int = 0
    enemies_killed: int = 0
    towers_built: int = 0
    towers_sold: int = 0
    total_damage_dealt: float = 0.0
    credits_earned: int = 0
    credits_spent: int = 0
    abilities_used: int = 0

class SimulationKernel:
    def __init__(self, seed: int = 1337, tick_rate: int = 60):
        self.tick_rate: int = tick_rate
        self.delta_time: float = 1.0 / float(tick_rate)
        self.current_tick: int = 0
        self.status: SimulationStatus = SimulationStatus.UNINITIALIZED
        
        self.rng: DeterministicRNG = DeterministicRNG(seed=seed)
        self.event_bus: EventBus = EventBus()
        self.spatial_grid: SpatialHashGrid = SpatialHashGrid(cell_size=64.0)
        
        self._entities: Dict[str, Entity] = {}
        self._towers: Dict[str, Entity] = {}
        self._enemies: Dict[str, Entity] = {}
        self._projectiles: Dict[str, Entity] = {}
        
        self.base_max_hp: float = 100.0
        self.base_current_hp: float = 100.0
        self.credits: int = 400
        self.energy: int = 100
        self.tech_tokens: int = 0
        
        self.stats: SimulationStats = SimulationStats()
        self._tick_listeners: List[Callable[[int, float], None]] = []

    def initialize(self, base_hp: float = 100.0, starting_credits: int = 400, starting_energy: int = 100) -> None:
        self.current_tick = 0
        self.base_max_hp = base_hp
        self.base_current_hp = base_hp
        self.credits = starting_credits
        self.energy = starting_energy
        self.tech_tokens = 0
        self.status = SimulationStatus.READY
        self.stats = SimulationStats()
        self._entities.clear()
        self._towers.clear()
        self._enemies.clear()
        self._projectiles.clear()
        self.spatial_grid.clear()
        self.event_bus.clear()
        
        self.event_bus.emit(GameEventType.SIMULATION_INITIALIZED, tick=0, base_hp=base_hp, credits=starting_credits)

    def register_entity(self, entity: Entity) -> Entity:
        self._entities[entity.id] = entity
        if entity.tag == "Tower":
            self._towers[entity.id] = entity
            self.stats.towers_built += 1
        elif entity.tag == "Enemy":
            self._enemies[entity.id] = entity
            self.stats.enemies_spawned += 1
        elif entity.tag == "Projectile":
            self._projectiles[entity.id] = entity

        tf = entity.get_component(TransformComponent)
        if tf is not None:
            self.spatial_grid.insert(entity.id, tf.position, tf.bounding_radius)
        return entity

    def unregister_entity(self, entity_id: str) -> Optional[Entity]:
        entity = self._entities.pop(entity_id, None)
        if entity:
            self._towers.pop(entity_id, None)
            self._enemies.pop(entity_id, None)
            self._projectiles.pop(entity_id, None)
            self.spatial_grid.remove(entity_id)
            entity.destroy()
        return entity

    def get_entity(self, entity_id: str) -> Optional[Entity]: return self._entities.get(entity_id)
    def get_all_enemies(self) -> List[Entity]: return list(self._enemies.values())
    def get_all_towers(self) -> List[Entity]: return list(self._towers.values())

    def add_tick_listener(self, listener: Callable[[int, float], None]) -> None:
        self._tick_listeners.append(listener)

    def step_tick(self) -> None:
        if self.status not in (SimulationStatus.RUNNING, SimulationStatus.READY): return
        self.status = SimulationStatus.RUNNING
        self.current_tick += 1
        self.stats.total_ticks += 1
        self.stats.elapsed_sim_time += self.delta_time

        for enemy in list(self._enemies.values()):
            tf = enemy.get_component(TransformComponent)
            if tf and enemy.is_active:
                self.spatial_grid.update(enemy.id, tf.position, tf.bounding_radius)

        for listener in self._tick_listeners:
            listener(self.current_tick, self.delta_time)

        dead_entities = [e for e in self._entities.values() if e.is_destroyed or not e.is_active]
        for e in dead_entities:
            self.unregister_entity(e.id)

        if self.base_current_hp <= 0.0 and self.status == SimulationStatus.RUNNING:
            self.status = SimulationStatus.DEFEAT
            self.event_bus.emit(GameEventType.GAME_LOST, tick=self.current_tick, stats=self.stats)

    def damage_base(self, amount: float) -> None:
        old_hp = self.base_current_hp
        self.base_current_hp = max(0.0, self.base_current_hp - amount)
        self.event_bus.emit(GameEventType.BASE_HEALTH_CHANGED, tick=self.current_tick, old_hp=old_hp, new_hp=self.base_current_hp, max_hp=self.base_max_hp)
        if self.base_current_hp <= 0.0:
            self.status = SimulationStatus.DEFEAT
            self.event_bus.emit(GameEventType.GAME_LOST, tick=self.current_tick)

    def add_credits(self, amount: int) -> None:
        if amount <= 0: return
        self.credits += amount
        self.stats.credits_earned += amount
        self.event_bus.emit(GameEventType.CREDITS_CHANGED, tick=self.current_tick, delta=amount, total=self.credits)

    def spend_credits(self, amount: int) -> bool:
        if amount < 0 or self.credits < amount: return False
        self.credits -= amount
        self.stats.credits_spent += amount
        self.event_bus.emit(GameEventType.CREDITS_CHANGED, tick=self.current_tick, delta=-amount, total=self.credits)
        return True

    def pause(self) -> None:
        if self.status == SimulationStatus.RUNNING:
            self.status = SimulationStatus.PAUSED
            self.event_bus.emit(GameEventType.SIMULATION_PAUSED, tick=self.current_tick)

    def resume(self) -> None:
        if self.status == SimulationStatus.PAUSED:
            self.status = SimulationStatus.RUNNING
            self.event_bus.emit(GameEventType.SIMULATION_RESUMED, tick=self.current_tick)
""")

    print("Part 1 Complete.")

if __name__ == "__main__":
    generate()
