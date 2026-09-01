import os
import sys
import json
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate_definitions_and_tests():
    print("--> Generating JSON Definitions & Test Suites...")

    # 1. towers.json
    towers_data = {
        "schema_version": "1.0.0",
        "towers": [
            {"id": "kinetic_vulcan", "name": "Kinetic Vulcan Turret", "archetype": "KINETIC", "cost": 120, "dps": 81.0, "range": 110.0, "damage_type": "kinetic", "description": "High-RPM rotary kinetic cannon"},
            {"id": "gauss_accelerator", "name": "Gauss Magnetic Accelerator", "archetype": "KINETIC", "cost": 240, "dps": 72.0, "range": 210.0, "damage_type": "kinetic", "description": "Long-range anti-armor slug"},
            {"id": "tachyon_prism", "name": "Tachyon Beam Prism", "archetype": "ENERGY", "cost": 175, "dps": 74.8, "range": 140.0, "damage_type": "energy", "description": "Continuous energy burn"},
            {"id": "frostbite_cryo", "name": "Frostbite Cryo Projector", "archetype": "CONTROL", "cost": 145, "dps": 16.8, "range": 115.0, "damage_type": "cryo", "description": "Sub-zero chilling emitter"},
            {"id": "arc_discharger", "name": "Arc Tesla Discharger", "archetype": "ENERGY", "cost": 210, "dps": 45.0, "range": 130.0, "damage_type": "energy", "description": "Chain lightning array"},
            {"id": "nanite_hive", "name": "Nanite Swarm Spire", "archetype": "EXPERIMENTAL", "cost": 290, "dps": 75.0, "range": 125.0, "damage_type": "corrosive", "description": "Micro-drone corrosive swarm"},
            {"id": "siege_howitzer", "name": "Siege Howitzer Battery", "archetype": "KINETIC", "cost": 320, "dps": 56.0, "range": 260.0, "damage_type": "explosive", "description": "Long-range area artillery"},
            {"id": "orbital_uplink", "name": "Orbital Command Uplink", "archetype": "SUPPORT", "cost": 250, "dps": 0.0, "range": 180.0, "damage_type": "support", "description": "Aura damage amplifier"},
            {"id": "singularity_trap", "name": "Singularity Vortex Trap", "archetype": "CONTROL", "cost": 270, "dps": 12.5, "range": 120.0, "damage_type": "gravity", "description": "Gravitational vortex"},
            {"id": "emp_disruptor_tower", "name": "EMP Grid Array", "archetype": "CONTROL", "cost": 195, "dps": 16.0, "range": 100.0, "damage_type": "emp", "description": "Shield and ability jammer"},
            {"id": "flak_anti_air", "name": "Flak Quad-Cannon", "archetype": "KINETIC", "cost": 160, "dps": 112.0, "range": 160.0, "damage_type": "kinetic", "description": "Anti-air fragmentation battery"},
            {"id": "plasma_mortar_artillery", "name": "Heavy Plasma Mortar", "archetype": "EXPERIMENTAL", "cost": 310, "dps": 47.5, "range": 175.0, "damage_type": "plasma", "description": "Superheated plasma splash"},
            {"id": "chrono_decelerator", "name": "Chrono Field Decelerator", "archetype": "CONTROL", "cost": 230, "dps": 8.0, "range": 140.0, "damage_type": "chrono", "description": "Temporal slowdown field"},
            {"id": "resource_refinery", "name": "Matter Extraction Core", "archetype": "RESOURCE", "cost": 200, "dps": 0.0, "range": 0.0, "damage_type": "economy", "description": "Periodic credit harvester"},
            {"id": "solar_lance", "name": "Solar Lance Array", "archetype": "ENERGY", "cost": 350, "dps": 84.0, "range": 240.0, "damage_type": "solar", "description": "Orbital solar piercing beam"},
            {"id": "sonic_resonator", "name": "Sonic Concussion Cannon", "archetype": "CONTROL", "cost": 180, "dps": 26.4, "range": 95.0, "damage_type": "sonic", "description": "Shockwave repulsor"},
            {"id": "tesla_overcharger", "name": "Tesla Overcharger Pylon", "archetype": "SUPPORT", "cost": 220, "dps": 0.0, "range": 150.0, "damage_type": "support", "description": "Energy fire rate booster"},
            {"id": "missile_pod_battery", "name": "Viper Missile Battery", "archetype": "KINETIC", "cost": 260, "dps": 63.0, "range": 190.0, "damage_type": "explosive", "description": "Homing missile salvo"},
            {"id": "heavy_defense_matrix", "name": "Aegis Shield Matrix", "archetype": "SUPPORT", "cost": 240, "dps": 0.0, "range": 160.0, "damage_type": "shield", "description": "Recharging ally energy barrier"},
            {"id": "quantum_blaster", "name": "Quantum Phase Blaster", "archetype": "EXPERIMENTAL", "cost": 380, "dps": 126.0, "range": 150.0, "damage_type": "quantum", "description": "True damage phase emitter"}
        ]
    }
    write_file("data/definitions/towers.json", json.dumps(towers_data, indent=2))

    # 2. enemies.json
    enemies_data = {
        "schema_version": "1.0.0",
        "enemies": [
            {"id": "scout_infiltrator", "name": "Scout Infiltrator", "archetype": "FAST", "hp": 65.0, "speed": 105.0, "flying": False, "reward": 10},
            {"id": "armored_juggernaut", "name": "Armored Juggernaut", "archetype": "ARMORED", "hp": 450.0, "speed": 35.0, "flying": False, "reward": 35},
            {"id": "phantom_infiltrator", "name": "Phantom Infiltrator", "archetype": "ASSASSIN", "hp": 120.0, "speed": 85.0, "flying": False, "reward": 22},
            {"id": "aero_interceptor", "name": "Aero Interceptor", "archetype": "FLYING", "hp": 95.0, "speed": 90.0, "flying": True, "reward": 16},
            {"id": "aegis_shield_bearer", "name": "Aegis Shield Bearer", "archetype": "SHIELDED", "hp": 180.0, "speed": 45.0, "flying": False, "reward": 30},
            {"id": "nanite_medic", "name": "Nanite Field Medic", "archetype": "HEALER", "hp": 150.0, "speed": 60.0, "flying": False, "reward": 28},
            {"id": "emp_saboteur", "name": "EMP Saboteur", "archetype": "DISRUPTOR", "hp": 140.0, "speed": 70.0, "flying": False, "reward": 32},
            {"id": "hydra_broodmother", "name": "Hydra Broodmother", "archetype": "SPLITTER", "hp": 320.0, "speed": 40.0, "flying": False, "reward": 40},
            {"id": "shadow_assassin", "name": "Shadow Assassin", "archetype": "ASSASSIN", "hp": 160.0, "speed": 95.0, "flying": False, "reward": 34},
            {"id": "siege_breaker_ram", "name": "Siege Breaker Ram", "archetype": "BUILDER", "hp": 500.0, "speed": 30.0, "flying": False, "reward": 50},
            {"id": "dreadnought_titan", "name": "Dreadnought Titan", "archetype": "BOSS", "hp": 3500.0, "speed": 28.0, "flying": False, "reward": 400},
            {"id": "cyber_hive_carrier", "name": "Cyber Hive Carrier", "archetype": "BOSS", "hp": 2800.0, "speed": 32.0, "flying": True, "reward": 350}
        ]
    }
    write_file("data/definitions/enemies.json", json.dumps(enemies_data, indent=2))

    # 3. Unit test expansions
    write_file("tests/unit/test_combat_calculators.py", """import pytest
from client.combat.calculators.armor_penetration_calculator import ArmorPenetrationCalculator
from client.combat.calculators.elemental_reaction_engine import ElementalReactionEngine, DamageType, ElementalReaction
from client.combat.calculators.damage_falloff_model import DamageFalloffModel
from client.combat.calculators.chain_lightning_propagator import ChainLightningPropagator
from client.combat.calculators.critical_strike_matrix import CriticalStrikeMatrix
from client.math.vector2d import Vector2D

def test_armor_penetration_calculation():
    res = ArmorPenetrationCalculator.calculate(raw_damage=100.0, target_armor=50.0, flat_penetration=10.0, percent_penetration=0.20)
    assert res.final_damage > 0.0
    assert res.effective_armor == 32.0

def test_elemental_thermal_shock_reaction():
    res = ElementalReactionEngine.evaluate_reaction(DamageType.CRYO, DamageType.PLASMA, base_damage=50.0)
    assert res.reaction == ElementalReaction.THERMAL_SHOCK
    assert res.bonus_damage == 87.5
    assert res.applied_status == "SHATTERED"

def test_chain_lightning_propagation():
    hits = ChainLightningPropagator.resolve_chain(
        origin_pos=Vector2D(0, 0),
        initial_target_id="t1",
        initial_target_pos=Vector2D(50, 50),
        base_damage=100.0,
        max_chains=3,
        jump_radius=60.0,
        decay_factor=0.7,
        candidate_entities=[("t2", Vector2D(80, 50)), ("t3", Vector2D(120, 50))]
    )
    assert len(hits) == 3
    assert hits[0].damage_dealt == 100.0
    assert hits[1].damage_dealt == 70.0
    assert hits[2].damage_dealt == 49.0
""")

    write_file("tests/unit/test_tower_specializations.py", """import pytest
from client.towers.specializations.kinetic_vulcan import KineticVulcanTower
from client.towers.specializations.gauss_accelerator import GaussAcceleratorTower
from client.towers.specializations.tachyon_prism import TachyonPrismTower
from client.towers.specializations.frostbite_cryo import FrostbiteCryoTower

def test_specialized_towers_init():
    vulcan = KineticVulcanTower()
    assert vulcan.stats.attack.base_damage == 18.0
    assert vulcan.stats.attack.attack_rate == 4.5
    
    gauss = GaussAcceleratorTower()
    assert gauss.stats.attack.range_radius == 210.0
    assert gauss.stats.attack.base_damage == 120.0
    
    tachyon = TachyonPrismTower()
    assert tachyon.stats.archetype.name == "ENERGY"
""")

    write_file("tests/unit/test_flow_field_navigation.py", """import pytest
from client.math.vector2d import Vector2D
from client.navigation.grid_graph import GridGraph, TerrainType
from client.navigation.advanced.flow_field_generator import FlowFieldGenerator

def test_flow_field_generation():
    graph = GridGraph(width=16, height=16, cell_size=32.0)
    flow = FlowFieldGenerator(graph)
    goal = Vector2D(400.0, 400.0)
    flow.generate_field(goal)
    
    vec = flow.get_flow_vector(Vector2D(50.0, 50.0))
    assert vec.magnitude() > 0.0
""")

if __name__ == "__main__":
    generate_definitions_and_tests()
