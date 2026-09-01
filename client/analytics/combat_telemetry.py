from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
from client.events.event_bus import EventBus, GameEventType, GameEvent

@dataclass
class TelemetryFrame:
    tick: int
    active_enemies: int
    total_towers: int
    dps_average: float
    base_hp_remaining: float
    credits_current: int

class CombatTelemetryAggregator:
    def __init__(self, event_bus: EventBus):
        self.event_bus: EventBus = event_bus
        self.damage_events: List[float] = []
        self.kill_locations: List[Tuple[float, float]] = []
        self.frames: List[TelemetryFrame] = []
        self._subscribe()

    def _subscribe(self) -> None:
        self.event_bus.subscribe(GameEventType.DAMAGE_DEALT, self._on_dmg)
        self.event_bus.subscribe(GameEventType.ENEMY_DEATH, self._on_kill)

    def _on_dmg(self, ev: GameEvent) -> None:
        self.damage_events.append(ev.payload.get("damage", 0.0))

    def _on_kill(self, ev: GameEvent) -> None:
        pos = ev.payload.get("position")
        if pos:
            self.kill_locations.append((pos[0], pos[1]))

    def record_frame(self, tick: int, enemies: int, towers: int, hp: float, credits: int) -> None:
        dps = sum(self.damage_events[-60:]) if self.damage_events else 0.0
        self.frames.append(TelemetryFrame(
            tick=tick,
            active_enemies=enemies,
            total_towers=towers,
            dps_average=dps,
            base_hp_remaining=hp,
            credits_current=credits
        ))

    def get_summary(self) -> dict:
        return {
            "total_damage_recorded": sum(self.damage_events),
            "total_kills_recorded": len(self.kill_locations),
            "frames_count": len(self.frames),
            "peak_dps": max([f.dps_average for f in self.frames], default=0.0)
        }
