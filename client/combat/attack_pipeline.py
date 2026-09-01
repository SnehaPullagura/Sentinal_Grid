from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Callable
from client.math.vector2d import Vector2D
from client.entities.entity_model import Entity, TransformComponent, HealthComponent
from client.combat.status_effects import StatusEffectComponent, StatusEffectType
from client.events.event_bus import EventBus, GameEventType

@dataclass
class AttackDefinition:
    base_damage: float = 25.0
    damage_type: str = "kinetic"  # kinetic, energy, explosive, thermal
    attack_rate: float = 1.0  # attacks per second
    range_radius: float = 120.0
    splash_radius: float = 0.0
    chain_targets: int = 0
    chain_decay: float = 0.7
    status_effect: Optional[StatusEffectType] = None
    status_duration: float = 0.0
    status_magnitude: float = 0.0
    projectile_speed: float = 350.0  # 0 for instant beam

class AttackPipeline:
    @staticmethod
    def execute_attack(
        attacker: Entity,
        target: Entity,
        attack_def: AttackDefinition,
        event_bus: EventBus,
        entity_resolver: Callable[[str], Optional[Entity]],
        spatial_query_fn: Optional[Callable[[Vector2D, float], List[str]]] = None
    ) -> float:
        tgt_hp = target.get_component(HealthComponent)
        if not tgt_hp or not tgt_hp.is_alive:
            return 0.0

        # Apply primary damage
        dealt = tgt_hp.take_damage(attack_def.base_damage, damage_type=attack_def.damage_type)
        event_bus.emit(
            GameEventType.DAMAGE_DEALT,
            source_id=attacker.id,
            target_id=target.id,
            damage=dealt,
            damage_type=attack_def.damage_type
        )

        # Apply status effect
        if attack_def.status_effect:
            eff_comp = target.get_component(StatusEffectComponent)
            if not eff_comp:
                eff_comp = target.add_component(StatusEffectComponent())
            eff_comp.apply_effect(
                attack_def.status_effect,
                attack_def.status_duration,
                attack_def.status_magnitude,
                source_id=attacker.id
            )

        # Handle Splash
        if attack_def.splash_radius > 0.0 and spatial_query_fn:
            tgt_pos = target.require_component(TransformComponent).position
            nearby = spatial_query_fn(tgt_pos, attack_def.splash_radius)
            for nid in nearby:
                if nid != target.id:
                    other = entity_resolver(nid)
                    if other and other.tag == "Enemy":
                        oth_hp = other.get_component(HealthComponent)
                        if oth_hp and oth_hp.is_alive:
                            splash_dmg = oth_hp.take_damage(attack_def.base_damage * 0.5, damage_type=attack_def.damage_type)
                            event_bus.emit(GameEventType.DAMAGE_DEALT, source_id=attacker.id, target_id=nid, damage=splash_dmg)

        return dealt
