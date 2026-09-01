from __future__ import annotations
from enum import Enum, auto
from typing import Dict, List, Optional
from dataclasses import dataclass
from client.entities.entity_model import Component, HealthComponent
from client.navigation.movement_controller import MovementComponent

class StatusEffectType(Enum):
    BURNING = auto()
    FROZEN = auto()
    SLOWED = auto()
    POISONED = auto()
    SHIELDED = auto()
    WEAKENED = auto()
    STUNNED = auto()
    EMP_DISABLED = auto()
    ATTACK_BUFF = auto()
    ARMOR_SHRED = auto()

@dataclass
class StatusEffectInstance:
    effect_type: StatusEffectType
    duration_remaining: float
    magnitude: float
    source_id: str
    tick_interval: float = 0.5
    next_tick: float = 0.0

@dataclass
class StatusEffectComponent(Component):
    active_effects: Dict[StatusEffectType, StatusEffectInstance] = None

    def __post_init__(self):
        if self.active_effects is None:
            self.active_effects = {}

    def apply_effect(self, effect_type: StatusEffectType, duration: float, magnitude: float, source_id: str) -> None:
        if effect_type in self.active_effects:
            curr = self.active_effects[effect_type]
            curr.duration_remaining = max(curr.duration_remaining, duration)
            curr.magnitude = max(curr.magnitude, magnitude)
        else:
            self.active_effects[effect_type] = StatusEffectInstance(
                effect_type=effect_type,
                duration_remaining=duration,
                magnitude=magnitude,
                source_id=source_id
            )

    def update_effects(self, delta_time: float, health: Optional[HealthComponent], movement: Optional[MovementComponent]) -> None:
        expired = []
        slow_multiplier = 1.0
        is_stunned = False

        for eff_type, inst in self.active_effects.items():
            inst.duration_remaining -= delta_time
            if inst.duration_remaining <= 0.0:
                expired.append(eff_type)
                continue

            inst.next_tick -= delta_time
            if inst.next_tick <= 0.0:
                inst.next_tick = inst.tick_interval
                # Periodic damage effects
                if eff_type == StatusEffectType.BURNING and health:
                    health.take_damage(inst.magnitude, damage_type="energy")
                elif eff_type == StatusEffectType.POISONED and health:
                    health.take_damage(inst.magnitude, damage_type="kinetic")

            if eff_type in (StatusEffectType.SLOWED, StatusEffectType.FROZEN):
                slow_multiplier = min(slow_multiplier, max(0.1, 1.0 - inst.magnitude))
            elif eff_type == StatusEffectType.STUNNED:
                is_stunned = True

        for exp in expired:
            del self.active_effects[exp]

        if movement:
            movement.speed_multiplier = 0.0 if is_stunned else slow_multiplier
