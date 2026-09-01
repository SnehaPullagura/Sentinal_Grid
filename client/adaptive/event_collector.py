from __future__ import annotations
from typing import Dict, List, Any
from dataclasses import dataclass, field
from client.events.event_bus import EventBus, GameEventType, GameEvent

@dataclass
class PlayerDefenseMetrics:
    towers_built_by_type: Dict[str, int] = field(default_factory=dict)
    damage_dealt_by_type: Dict[str, float] = field(default_factory=dict)
    kills_by_archetype: Dict[str, int] = field(default_factory=dict)
    cc_applications: int = 0
    abilities_used_count: int = 0
    leaked_enemies_count: int = 0
    average_kill_distance_pct: float = 0.5
    tower_density_score: float = 1.0

class AdaptiveEventCollector:
    def __init__(self, event_bus: EventBus):
        self.event_bus: EventBus = event_bus
        self.metrics: PlayerDefenseMetrics = PlayerDefenseMetrics()
        self._subscribe_events()

    def _subscribe_events(self) -> None:
        self.event_bus.subscribe(GameEventType.TOWER_PLACED, self._on_tower_placed)
        self.event_bus.subscribe(GameEventType.DAMAGE_DEALT, self._on_damage_dealt)
        self.event_bus.subscribe(GameEventType.STATUS_EFFECT_APPLIED, self._on_status_applied)
        self.event_bus.subscribe(GameEventType.ENEMY_DEATH, self._on_enemy_death)
        self.event_bus.subscribe(GameEventType.ENEMY_REACHED_GOAL, self._on_enemy_leak)
        self.event_bus.subscribe(GameEventType.ABILITY_TRIGGERED, self._on_ability)

    def _on_tower_placed(self, event: GameEvent) -> None:
        archetype = event.payload.get("archetype", "KINETIC")
        self.metrics.towers_built_by_type[archetype] = self.metrics.towers_built_by_type.get(archetype, 0) + 1

    def _on_damage_dealt(self, event: GameEvent) -> None:
        dmg_type = event.payload.get("damage_type", "kinetic")
        amount = event.payload.get("damage", 0.0)
        self.metrics.damage_dealt_by_type[dmg_type] = self.metrics.damage_dealt_by_type.get(dmg_type, 0.0) + amount

    def _on_status_applied(self, event: GameEvent) -> None:
        self.metrics.cc_applications += 1

    def _on_enemy_death(self, event: GameEvent) -> None:
        arch = event.payload.get("archetype", "BASIC")
        self.metrics.kills_by_archetype[arch] = self.metrics.kills_by_archetype.get(arch, 0) + 1

    def _on_enemy_leak(self, event: GameEvent) -> None:
        self.metrics.leaked_enemies_count += 1

    def _on_ability(self, event: GameEvent) -> None:
        self.metrics.abilities_used_count += 1
