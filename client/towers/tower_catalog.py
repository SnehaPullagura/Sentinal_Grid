from __future__ import annotations
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
