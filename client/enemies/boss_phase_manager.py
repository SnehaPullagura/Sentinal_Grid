from __future__ import annotations
from enum import Enum, auto
from typing import List, Dict, Callable
from dataclasses import dataclass, field
from client.entities.entity_model import Component, HealthComponent
from client.events.event_bus import EventBus, GameEventType

class BossPhase(Enum):
    PHASE_1_SHIELDED = auto()
    PHASE_2_ENRAGED = auto()
    PHASE_3_DESPERATION = auto()

@dataclass
class BossPhaseTrigger:
    phase: BossPhase
    hp_threshold_pct: float  # e.g., 0.65 for 65%
    speed_multiplier: float = 1.0
    armor_buff: float = 0.0
    summon_count: int = 0
    emp_pulse: bool = False

class BossPhaseManager(Component):
    def __init__(self, triggers: Optional[List[BossPhaseTrigger]] = None):
        self.current_phase: BossPhase = BossPhase.PHASE_1_SHIELDED
        self.triggers: List[BossPhaseTrigger] = triggers or [
            BossPhaseTrigger(BossPhase.PHASE_1_SHIELDED, 1.0, 1.0, 5.0, 0),
            BossPhaseTrigger(BossPhase.PHASE_2_ENRAGED, 0.60, 1.45, 10.0, 4, emp_pulse=True),
            BossPhaseTrigger(BossPhase.PHASE_3_DESPERATION, 0.25, 1.85, 15.0, 8, emp_pulse=True)
        ]
        self._activated_phases: set = set()

    def check_phase_transition(self, health: HealthComponent, event_bus: EventBus) -> Optional[BossPhaseTrigger]:
        if not health or not health.is_alive:
            return None

        hp_pct = health.health_percentage
        for trig in sorted(self.triggers, key=lambda t: t.hp_threshold_pct):
            if hp_pct <= trig.hp_threshold_pct and trig.phase not in self._activated_phases:
                self._activated_phases.add(trig.phase)
                self.current_phase = trig.phase
                event_bus.emit(
                    GameEventType.BOSS_PHASE_CHANGED,
                    source_id=self.entity_id,
                    new_phase=trig.phase.name,
                    hp_pct=hp_pct
                )
                return trig
        return None
