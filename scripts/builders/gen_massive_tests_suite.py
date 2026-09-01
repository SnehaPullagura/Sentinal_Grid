import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate_extensive_tests():
    print("--> Generating 30+ Comprehensive Test Files...")

    # 1. 20 Tower Solver Unit Tests
    towers = [
        "kinetic_vulcan", "gauss_accelerator", "tachyon_prism", "frostbite_cryo",
        "arc_discharger", "nanite_hive", "siege_howitzer", "orbital_uplink",
        "singularity_trap", "emp_disruptor_tower", "flak_anti_air", "plasma_mortar_artillery",
        "chrono_decelerator", "resource_refinery", "solar_lance", "sonic_resonator",
        "tesla_overcharger", "missile_pod_battery", "heavy_defense_matrix", "quantum_blaster"
    ]
    for tid in towers:
        t_test = f'''import pytest
from client.math.vector2d import Vector2D
from client.combat.solvers.{tid}_solver import {tid.title().replace("_", "")}CombatSolver

def test_{tid}_combat_solver_intercept():
    solver = {tid.title().replace("_", "")}CombatSolver()
    origin = Vector2D(50.0, 50.0)
    target_pos = Vector2D(100.0, 50.0)
    target_vel = Vector2D(10.0, 0.0)

    solution = solver.calculate_intercept(origin, target_pos, target_vel)
    assert solution.time_to_target_sec >= 0.0
    assert solution.effective_damage > 0.0
    assert solution.hit_probability > 0.0
'''
        write_file(f"tests/unit/towers/test_{tid}_solver.py", t_test)

    # 2. 20 Enemy Solver Unit Tests
    enemies = [
        "scout_infiltrator", "armored_juggernaut", "phantom_infiltrator", "aero_interceptor",
        "aegis_shield_bearer", "nanite_medic", "emp_saboteur", "hydra_broodmother",
        "shadow_assassin", "siege_breaker_ram", "dreadnought_titan", "cyber_hive_carrier",
        "glider_swarmer", "heavy_colossus", "leech_parasite", "phase_shifter",
        "warp_striker", "vanguard_mech", "frost_walker", "apocalypse_overlord"
    ]
    for eid in enemies:
        e_test = f'''import pytest
from client.math.vector2d import Vector2D
from client.ai.solvers.{eid}_solver import {eid.title().replace("_", "")}StrategySolver

def test_{eid}_strategy_solver_evasion():
    solver = {eid.title().replace("_", "")}StrategySolver()
    cur = Vector2D(10.0, 10.0)
    goal = Vector2D(200.0, 10.0)
    hazards = [Vector2D(50.0, 10.0)]

    decision = solver.evaluate_threats(cur, goal, hazards, current_hp_pct=0.8)
    assert decision.recommended_velocity.magnitude() > 0.0
    assert decision.threat_urgency >= 0.0
'''
        write_file(f"tests/unit/enemies/test_{eid}_solver.py", e_test)

    # 3. 10 Campaign Model Unit Tests
    for m in range(1, 11):
        m_test = f'''import pytest
from client.campaign.mission_models.mission_{m:02d}_model import Mission{m:02d}DataModel

def test_mission_{m:02d}_data_model_waves():
    model = Mission{m:02d}DataModel()
    assert model.mission_index == {m}
    assert len(model.waves_data) > 0
    w1 = model.get_wave_config(1)
    assert w1 is not None
    assert w1.threat_cap > 0.0
'''
        write_file(f"tests/unit/campaign/test_mission_{m:02d}_model.py", m_test)

    print("Extensive Tests Generated.")

if __name__ == "__main__":
    generate_extensive_tests()
