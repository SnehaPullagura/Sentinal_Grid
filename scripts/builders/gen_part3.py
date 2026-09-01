import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate():
    print("Generating Part 3: Data-Driven Towers, Targeting & Combat Pipeline...")

    # 1. client/combat/status_effects.py
    write_file("client/combat/status_effects.py", """from __future__ import annotations
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
""")

    # 2. client/towers/targeting_system.py
    write_file("client/towers/targeting_system.py", """from __future__ import annotations
from enum import Enum, auto
from typing import List, Optional, Callable
from client.math.vector2d import Vector2D
from client.entities.entity_model import Entity, TransformComponent, HealthComponent
from client.navigation.movement_controller import MovementComponent
from client.simulation.spatial_hash import SpatialHashGrid

class TargetingStrategy(Enum):
    FIRST = auto()
    LAST = auto()
    CLOSEST = auto()
    STRONGEST = auto()
    WEAKEST = auto()
    HIGHEST_THREAT = auto()
    FLYING_ONLY = auto()
    GROUND_ONLY = auto()

class TargetingPipeline:
    @staticmethod
    def select_target(
        tower_pos: Vector2D,
        range_radius: float,
        strategy: TargetingStrategy,
        spatial_grid: SpatialHashGrid,
        entity_resolver: Callable[[str], Optional[Entity]]
    ) -> Optional[Entity]:
        candidate_ids = spatial_grid.query_radius(tower_pos, range_radius)
        if not candidate_ids:
            return None

        candidates: List[Entity] = []
        for cid in candidate_ids:
            ent = entity_resolver(cid)
            if ent and ent.is_active and ent.tag == "Enemy":
                hp = ent.get_component(HealthComponent)
                if hp and hp.is_alive:
                    candidates.append(ent)

        if not candidates:
            return None

        if strategy == TargetingStrategy.CLOSEST:
            return min(candidates, key=lambda e: tower_pos.distance_to_squared(e.require_component(TransformComponent).position))

        if strategy == TargetingStrategy.STRONGEST:
            return max(candidates, key=lambda e: e.require_component(HealthComponent).current_health)

        if strategy == TargetingStrategy.WEAKEST:
            return min(candidates, key=lambda e: e.require_component(HealthComponent).current_health)

        if strategy == TargetingStrategy.FIRST:
            return max(candidates, key=lambda e: getattr(e.get_component(MovementComponent), "total_distance_traveled", 0.0))

        if strategy == TargetingStrategy.LAST:
            return min(candidates, key=lambda e: getattr(e.get_component(MovementComponent), "total_distance_traveled", 0.0))

        if strategy == TargetingStrategy.FLYING_ONLY:
            flying = [c for c in candidates if getattr(c.get_component(MovementComponent), "is_flying", False)]
            return flying[0] if flying else None

        if strategy == TargetingStrategy.GROUND_ONLY:
            ground = [c for c in candidates if not getattr(c.get_component(MovementComponent), "is_flying", False)]
            return ground[0] if ground else None

        return candidates[0]
""")

    # 3. client/combat/attack_pipeline.py
    write_file("client/combat/attack_pipeline.py", """from __future__ import annotations
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
""")

    # 4. client/towers/tower_definitions.py
    write_file("client/towers/tower_definitions.py", """from __future__ import annotations
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from client.entities.entity_model import Component
from client.towers.targeting_system import TargetingStrategy
from client.combat.attack_pipeline import AttackDefinition

class TowerArchetype(Enum):
    KINETIC = auto()
    ENERGY = auto()
    CONTROL = auto()
    SUPPORT = auto()
    RESOURCE = auto()
    EXPERIMENTAL = auto()

@dataclass
class TowerStats:
    archetype: TowerArchetype = TowerArchetype.KINETIC
    name: str = "Gatling Turret"
    cost_credits: int = 100
    cost_energy: int = 10
    level: int = 1
    max_level: int = 5
    sell_ratio: float = 0.75
    attack: AttackDefinition = field(default_factory=AttackDefinition)
    cooldown_remaining: float = 0.0
    targeting_strategy: TargetingStrategy = TargetingStrategy.FIRST
    kills_count: int = 0
    total_damage_dealt: float = 0.0

@dataclass
class TowerComponent(Component):
    stats: TowerStats = field(default_factory=TowerStats)
    is_active: bool = True
    is_disabled: bool = False

    def can_attack(self) -> bool:
        return self.is_active and not self.is_disabled and self.stats.cooldown_remaining <= 0.0

    def update_cooldown(self, delta_time: float) -> None:
        if self.stats.cooldown_remaining > 0.0:
            self.stats.cooldown_remaining = max(0.0, self.stats.cooldown_remaining - delta_time)

    def trigger_attack(self) -> None:
        self.stats.cooldown_remaining = 1.0 / max(0.1, self.stats.attack.attack_rate)
""")

    # 5. client/towers/tower_catalog.py
    write_file("client/towers/tower_catalog.py", """from __future__ import annotations
from typing import Dict
from client.towers.tower_definitions import TowerArchetype, TowerStats, AttackDefinition, TargetingStrategy
from client.combat.status_effects import StatusEffectType

def get_tower_catalog() -> Dict[str, TowerStats]:
    return {
        "kinetic_gatling": TowerStats(
            archetype=TowerArchetype.KINETIC,
            name="Gatling Turret",
            cost_credits=100,
            cost_energy=5,
            attack=AttackDefinition(base_damage=14.0, attack_rate=3.5, range_radius=110.0, damage_type="kinetic")
        ),
        "heavy_railgun": TowerStats(
            archetype=TowerArchetype.KINETIC,
            name="Heavy Railgun",
            cost_credits=220,
            cost_energy=15,
            attack=AttackDefinition(base_damage=85.0, attack_rate=0.7, range_radius=180.0, damage_type="kinetic")
        ),
        "laser_prism": TowerStats(
            archetype=TowerArchetype.ENERGY,
            name="Laser Prism",
            cost_credits=150,
            cost_energy=20,
            attack=AttackDefinition(base_damage=28.0, attack_rate=2.0, range_radius=130.0, damage_type="energy", projectile_speed=0.0)
        ),
        "cryo_emitter": TowerStats(
            archetype=TowerArchetype.CONTROL,
            name="Cryo Emitter",
            cost_credits=130,
            cost_energy=15,
            attack=AttackDefinition(
                base_damage=8.0,
                attack_rate=1.2,
                range_radius=100.0,
                damage_type="energy",
                status_effect=StatusEffectType.FROZEN,
                status_duration=2.5,
                status_magnitude=0.55
            )
        ),
        "plasma_mortar": TowerStats(
            archetype=TowerArchetype.EXPERIMENTAL,
            name="Plasma Mortar",
            cost_credits=280,
            cost_energy=25,
            attack=AttackDefinition(base_damage=60.0, attack_rate=0.5, range_radius=160.0, splash_radius=48.0, damage_type="explosive")
        ),
        "emp_pulse": TowerStats(
            archetype=TowerArchetype.CONTROL,
            name="EMP Pulse Array",
            cost_credits=190,
            cost_energy=30,
            attack=AttackDefinition(
                base_damage=12.0,
                attack_rate=0.8,
                range_radius=90.0,
                damage_type="energy",
                status_effect=StatusEffectType.STUNNED,
                status_duration=1.2,
                status_magnitude=1.0
            )
        )
    }
""")

    print("Part 3 Complete.")

if __name__ == "__main__":
    generate()
