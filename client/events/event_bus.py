from __future__ import annotations
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
