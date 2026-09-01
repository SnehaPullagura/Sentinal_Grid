import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate():
    print("--> Generating 20 Tower Specialization Modules...")
    
    towers = [
        ("kinetic_vulcan", "Kinetic Vulcan Turret", "KINETIC", 120, 18.0, 4.5, 110.0, "High-RPM rotary kinetic cannon", "bullet"),
        ("gauss_accelerator", "Gauss Magnetic Accelerator", "KINETIC", 240, 120.0, 0.6, 210.0, "Long-range hyper-dense magnetic slug", "slug"),
        ("tachyon_prism", "Tachyon Beam Prism", "ENERGY", 175, 34.0, 2.2, 140.0, "Continuous high-frequency energy burn", "beam"),
        ("frostbite_cryo", "Frostbite Cryo Projector", "CONTROL", 145, 12.0, 1.4, 115.0, "Cryogenic sub-zero slowing emitter", "frost"),
        ("arc_discharger", "Arc Tesla Discharger", "ENERGY", 210, 45.0, 1.0, 130.0, "Chain lightning jumping up to 4 targets", "lightning"),
        ("nanite_hive", "Nanite Swarm Spire", "EXPERIMENTAL", 290, 50.0, 1.5, 125.0, "Micro-drone corrosive nanite swarm", "nanite"),
        ("siege_howitzer", "Siege Howitzer Battery", "KINETIC", 320, 160.0, 0.35, 260.0, "Ultra-heavy long-range artillery with massive splash", "artillery"),
        ("orbital_uplink", "Orbital Command Uplink", "SUPPORT", 250, 0.0, 0.0, 180.0, "Buffs all adjacent tower damage by 35%", "aura"),
        ("singularity_trap", "Singularity Vortex Trap", "CONTROL", 270, 25.0, 0.5, 120.0, "Pulls nearby enemies toward vortex center", "vortex"),
        ("emp_disruptor_tower", "EMP Grid Array", "CONTROL", 195, 20.0, 0.8, 100.0, "Periodic EMP burst disabling enemy shields and abilities", "emp"),
        ("flak_anti_air", "Flak Quad-Cannon", "KINETIC", 160, 40.0, 2.8, 160.0, "Dedicated anti-air fragmentation battery", "flak"),
        ("plasma_mortar_artillery", "Heavy Plasma Mortar", "EXPERIMENTAL", 310, 95.0, 0.5, 175.0, "Superheated plasma sphere splash artillery", "plasma"),
        ("chrono_decelerator", "Chrono Field Decelerator", "CONTROL", 230, 8.0, 1.0, 140.0, "Local temporal distortion field slowing enemies by 65%", "chrono"),
        ("resource_refinery", "Matter Extraction Core", "RESOURCE", 200, 0.0, 0.0, 0.0, "Generates 25 credits every 10 seconds", "economy"),
        ("solar_lance", "Solar Lance Array", "ENERGY", 350, 210.0, 0.4, 240.0, "Concentrated orbital solar beam piercing lines of enemies", "solar"),
        ("sonic_resonator", "Sonic Concussion Cannon", "CONTROL", 180, 22.0, 1.2, 95.0, "Shockwave pushing enemies backwards along the route", "sonic"),
        ("tesla_overcharger", "Tesla Overcharger Pylon", "SUPPORT", 220, 0.0, 0.0, 150.0, "Increases adjacent energy tower firing rate by 45%", "support"),
        ("missile_pod_battery", "Viper Missile Battery", "KINETIC", 260, 35.0, 1.8, 190.0, "Multi-target homing kinetic missile salvo", "missile"),
        ("heavy_defense_matrix", "Aegis Shield Matrix", "SUPPORT", 240, 0.0, 0.0, 160.0, "Provides recharging energy shields to friendly towers", "shield"),
        ("quantum_blaster", "Quantum Phase Blaster", "EXPERIMENTAL", 380, 140.0, 0.9, 150.0, "Bypasses all physical armor and elemental shields", "quantum")
    ]

    for tid, name, arch, cost, dmg, rate, rng, desc, fxtype in towers:
        fcontent = f'''"""
{name} ({arch}) Tower Implementation.
{desc}
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
from client.towers.tower_definitions import TowerArchetype, TowerStats, AttackDefinition, TargetingStrategy
from client.combat.attack_pipeline import AttackPipeline
from client.math.vector2d import Vector2D
from client.entities.entity_model import Entity

@dataclass
class {tid.title().replace("_", "")}Tower:
    stats: TowerStats = field(default_factory=lambda: TowerStats(
        archetype=TowerArchetype.{arch},
        name="{name}",
        cost_credits={cost},
        cost_energy={int(cost * 0.1)},
        attack=AttackDefinition(
            base_damage={dmg},
            attack_rate={rate},
            range_radius={rng},
            damage_type="{arch.lower()}"
        )
    ))
    fx_signature: str = "{fxtype}"
    kill_count: int = 0
    total_damage: float = 0.0

    def on_tick(self, delta_time: float) -> None:
        if self.stats.cooldown_remaining > 0.0:
            self.stats.cooldown_remaining = max(0.0, self.stats.cooldown_remaining - delta_time)

    def record_hit(self, damage_amount: float, was_kill: bool = False) -> None:
        self.total_damage += damage_amount
        if was_kill:
            self.kill_count += 1
'''
        write_file(f"client/towers/specializations/{tid}.py", fcontent)

    print("--> Generating 20 Enemy Specialization Modules...")
    enemies = [
        ("scout_infiltrator", "Scout Infiltrator", "FAST", 65.0, 0.0, 0.0, 105.0, False, 10, 1.0, "Rapid recon sprinter"),
        ("armored_juggernaut", "Armored Juggernaut", "ARMORED", 450.0, 0.0, 18.0, 35.0, False, 35, 3.5, "Massive tank with high armor plating"),
        ("phantom_infiltrator", "Phantom Infiltrator", "ASSASSIN", 120.0, 0.0, 4.0, 85.0, False, 22, 2.2, "Cloaked unit avoiding long range detection"),
        ("aero_interceptor", "Aero Interceptor", "FLYING", 95.0, 0.0, 0.0, 90.0, True, 16, 1.6, "High-altitude flyer ignoring ground obstacles"),
        ("aegis_shield_bearer", "Aegis Shield Bearer", "SHIELDED", 180.0, 220.0, 5.0, 45.0, False, 30, 3.0, "Heavy energy shield projection"),
        ("nanite_medic", "Nanite Field Medic", "HEALER", 150.0, 50.0, 2.0, 60.0, False, 28, 2.8, "Aura healing nearby damaged allies"),
        ("emp_saboteur", "EMP Saboteur", "DISRUPTOR", 140.0, 0.0, 2.0, 70.0, False, 32, 3.2, "Periodic EMP burst disabling towers"),
        ("hydra_broodmother", "Hydra Broodmother", "SPLITTER", 320.0, 0.0, 6.0, 40.0, False, 40, 4.0, "Splits into 3 swarm units upon destruction"),
        ("shadow_assassin", "Shadow Assassin", "ASSASSIN", 160.0, 0.0, 5.0, 95.0, False, 34, 3.4, "High-speed objective rusher with dodge chance"),
        ("siege_breaker_ram", "Siege Breaker Ram", "BUILDER", 500.0, 0.0, 20.0, 30.0, False, 50, 5.0, "Demolishes friendly barricades on impact"),
        ("dreadnought_titan", "Dreadnought Titan", "BOSS", 3500.0, 1200.0, 25.0, 28.0, False, 400, 40.0, "Catastrophic boss with 3 enrage phases"),
        ("cyber_hive_carrier", "Cyber Hive Carrier", "BOSS", 2800.0, 800.0, 15.0, 32.0, True, 350, 35.0, "Flying boss spawning endless aero drones"),
        ("glider_swarmer", "Glider Swarmer", "SWARM", 25.0, 0.0, 0.0, 115.0, True, 4, 0.3, "Tiny fast flying swarm creature"),
        ("heavy_colossus", "Heavy Colossus", "ARMORED", 600.0, 0.0, 22.0, 32.0, False, 55, 5.5, "Gigantic walking fortress"),
        ("leech_parasite", "Leech Parasite", "SWARM", 40.0, 0.0, 0.0, 95.0, False, 6, 0.5, "Drains player credits on leak"),
        ("phase_shifter", "Phase Shifter", "DISRUPTOR", 160.0, 100.0, 4.0, 75.0, False, 36, 3.6, "Phases out of reality for 2s every 6s"),
        ("warp_striker", "Warp Striker", "FAST", 110.0, 0.0, 0.0, 120.0, False, 20, 2.0, "Teleports forward 100 units on taking damage"),
        ("vanguard_mech", "Vanguard Bipedal Mech", "ARMORED", 380.0, 150.0, 12.0, 50.0, False, 42, 4.2, "Dual shield & physical armor warrior"),
        ("frost_walker", "Frost Walker", "BASIC", 220.0, 0.0, 8.0, 55.0, False, 26, 2.6, "Immune to Cryo slow status effects"),
        ("apocalypse_overlord", "Apocalypse Overlord", "BOSS", 6000.0, 2500.0, 35.0, 25.0, False, 800, 80.0, "Ultimate sector campaign final boss")
    ]

    for eid, name, arch, hp, sh, arm, spd, fly, rew, threat, desc in enemies:
        fcontent = f'''"""
{name} ({arch}) Enemy Controller.
{desc}
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
from client.enemies.enemy_definitions import EnemyArchetype, EnemyStats
from client.entities.entity_model import Entity, HealthComponent, TransformComponent
from client.navigation.movement_controller import MovementComponent

@dataclass
class {eid.title().replace("_", "")}Enemy:
    stats: EnemyStats = field(default_factory=lambda: EnemyStats(
        archetype=EnemyArchetype.{arch},
        name="{name}",
        base_hp={hp},
        shield={sh},
        armor={arm},
        speed={spd},
        is_flying={fly},
        reward_credits={rew},
        threat_cost={threat}
    ))
    is_cloaked: bool = False
    phase_cooldown: float = 0.0

    def update_behavior(self, delta_time: float, health: HealthComponent, movement: MovementComponent) -> None:
        if self.phase_cooldown > 0.0:
            self.phase_cooldown = max(0.0, self.phase_cooldown - delta_time)
'''
        write_file(f"client/enemies/specializations/{eid}.py", fcontent)

if __name__ == "__main__":
    generate()
