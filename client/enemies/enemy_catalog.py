from __future__ import annotations
from typing import Dict
from client.enemies.enemy_definitions import EnemyArchetype, EnemyStats

def get_enemy_catalog() -> Dict[str, EnemyStats]:
    return {
        "scout_runner": EnemyStats(
            archetype=EnemyArchetype.FAST,
            name="Scout Runner",
            base_hp=70.0,
            speed=95.0,
            reward_credits=12,
            threat_cost=1.0,
            leak_damage=3.0
        ),
        "heavy_brute": EnemyStats(
            archetype=EnemyArchetype.ARMORED,
            name="Heavy Brute",
            base_hp=320.0,
            armor=8.0,
            speed=40.0,
            reward_credits=28,
            threat_cost=2.8,
            leak_damage=10.0
        ),
        "aero_drone": EnemyStats(
            archetype=EnemyArchetype.FLYING,
            name="Aero Drone",
            base_hp=110.0,
            speed=80.0,
            is_flying=True,
            reward_credits=18,
            threat_cost=1.8,
            leak_damage=5.0
        ),
        "shield_bearer": EnemyStats(
            archetype=EnemyArchetype.SHIELDED,
            name="Shield Bearer",
            base_hp=160.0,
            shield=140.0,
            speed=50.0,
            reward_credits=25,
            threat_cost=2.5,
            leak_damage=6.0
        ),
        "emp_disruptor": EnemyStats(
            archetype=EnemyArchetype.DISRUPTOR,
            name="EMP Disruptor",
            base_hp=140.0,
            speed=65.0,
            reward_credits=30,
            threat_cost=3.0,
            leak_damage=8.0,
            abilities=["emp_aura"]
        ),
        "hydra_splitter": EnemyStats(
            archetype=EnemyArchetype.SPLITTER,
            name="Hydra Splitter",
            base_hp=240.0,
            speed=45.0,
            reward_credits=35,
            threat_cost=3.5,
            leak_damage=12.0,
            abilities=["split_on_death"]
        ),
        "dreadnought_boss": EnemyStats(
            archetype=EnemyArchetype.BOSS,
            name="Dreadnought Titan",
            base_hp=2500.0,
            shield=800.0,
            armor=15.0,
            speed=32.0,
            reward_credits=250,
            reward_energy=50,
            threat_cost=25.0,
            leak_damage=50.0,
            abilities=["phase_shield", "summon_swarm", "emp_surge"]
        ),
        "swarm_cluster": EnemyStats(
            archetype=EnemyArchetype.SWARM,
            name="Swarm Parasite",
            base_hp=30.0,
            speed=110.0,
            reward_credits=5,
            threat_cost=0.4,
            leak_damage=1.0
        )
    }
