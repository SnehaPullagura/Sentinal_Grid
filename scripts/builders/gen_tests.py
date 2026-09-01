import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate():
    print("Generating Comprehensive Test Suites...")

    # 1. tests/unit/test_phase1_kernel.py
    write_file("tests/unit/test_phase1_kernel.py", """import pytest
from client.math.vector2d import Vector2D, Rect2D, Circle2D
from client.core.rng import DeterministicRNG
from client.events.event_bus import EventBus, GameEventType, GameEvent
from client.simulation.spatial_hash import SpatialHashGrid
from client.entities.entity_model import Entity, TransformComponent, HealthComponent
from client.simulation.game_state import SimulationKernel, SimulationStatus

def test_vector2d_algebra():
    v1 = Vector2D(3.0, 4.0)
    assert v1.magnitude() == 5.0
    norm = v1.normalized()
    assert abs(norm.magnitude() - 1.0) < 1e-5
    v2 = Vector2D(1.0, 2.0)
    assert (v1 + v2).x == 4.0
    assert v1.dot(v2) == 11.0

def test_rng_determinism():
    rng1 = DeterministicRNG(seed=9999)
    rng2 = DeterministicRNG(seed=9999)
    seq1 = [rng1.next_float() for _ in range(50)]
    seq2 = [rng2.next_float() for _ in range(50)]
    assert seq1 == seq2

def test_spatial_hash_query():
    grid = SpatialHashGrid(cell_size=50.0)
    grid.insert("e1", Vector2D(10.0, 10.0), radius=5.0)
    grid.insert("e2", Vector2D(30.0, 30.0), radius=5.0)
    grid.insert("e3", Vector2D(200.0, 200.0), radius=5.0)
    
    nearby = grid.query_radius(Vector2D(20.0, 20.0), radius=25.0)
    assert "e1" in nearby
    assert "e2" in nearby
    assert "e3" not in nearby

def test_ecs_entity_damage():
    entity = Entity(name="TestEnemy", tag="Enemy")
    tf = entity.add_component(TransformComponent(position=Vector2D(10, 20)))
    hp = entity.add_component(HealthComponent(max_health=100.0, current_health=100.0, armor=5.0))
    dmg = hp.take_damage(25.0, damage_type="kinetic")
    assert dmg == 20.0
    assert hp.current_health == 80.0

def test_simulation_kernel_lifecycle():
    kernel = SimulationKernel(seed=123)
    kernel.initialize(base_hp=100.0, starting_credits=500)
    t = Entity(name="Turret", tag="Tower")
    t.add_component(TransformComponent(position=Vector2D(50, 50)))
    kernel.register_entity(t)
    assert len(kernel.get_all_towers()) == 1
    assert kernel.spend_credits(200)
    for _ in range(10):
        kernel.step_tick()
    assert kernel.current_tick == 10
""")

    # 2. tests/unit/test_phase2_navigation.py
    write_file("tests/unit/test_phase2_navigation.py", """import pytest
from client.math.vector2d import Vector2D
from client.navigation.grid_graph import GridGraph, TerrainType
from client.navigation.astar import AStarPathfinder
from client.navigation.dynamic_obstacles import DynamicObstacleManager

def test_grid_graph_and_astar():
    graph = GridGraph(width=20, height=20, cell_size=32.0)
    # Block a vertical wall
    for y in range(2, 18):
        graph.set_terrain(10, y, TerrainType.BLOCKED_TERRAIN)
    
    pathfinder = AStarPathfinder(graph)
    start = Vector2D(64.0, 64.0)
    goal = Vector2D(500.0, 64.0)
    
    path = pathfinder.find_path(start, goal)
    assert path is not None
    assert len(path) >= 2
    assert path[0] == start
    assert path[-1] == goal

def test_dynamic_obstacle_rerouting():
    graph = GridGraph(width=15, height=15, cell_size=32.0)
    pathfinder = AStarPathfinder(graph)
    obs_mgr = DynamicObstacleManager(graph)
    
    start = Vector2D(32.0, 32.0)
    goal = Vector2D(400.0, 32.0)
    
    # Add obstacle directly in path
    obs_mgr.add_obstacle("barricade_1", Vector2D(200.0, 32.0), radius=32.0)
    path = pathfinder.find_path(start, goal)
    assert path is not None
""")

    # 3. tests/unit/test_phase3_combat.py
    write_file("tests/unit/test_phase3_combat.py", """import pytest
from client.math.vector2d import Vector2D
from client.entities.entity_model import Entity, TransformComponent, HealthComponent
from client.towers.targeting_system import TargetingStrategy, TargetingPipeline
from client.combat.status_effects import StatusEffectComponent, StatusEffectType
from client.combat.attack_pipeline import AttackPipeline, AttackDefinition
from client.events.event_bus import EventBus
from client.simulation.spatial_hash import SpatialHashGrid

def test_targeting_and_attack_pipeline():
    grid = SpatialHashGrid()
    bus = EventBus()
    entities = {}

    e1 = Entity(name="E1", tag="Enemy")
    e1.add_component(TransformComponent(position=Vector2D(100, 100)))
    e1.add_component(HealthComponent(max_health=100.0, current_health=80.0))
    grid.insert(e1.id, Vector2D(100, 100))
    entities[e1.id] = e1

    e2 = Entity(name="E2", tag="Enemy")
    e2.add_component(TransformComponent(position=Vector2D(120, 100)))
    e2.add_component(HealthComponent(max_health=150.0, current_health=150.0))
    grid.insert(e2.id, Vector2D(120, 100))
    entities[e2.id] = e2

    tower = Entity(name="Tower", tag="Tower")
    tower_pos = Vector2D(90, 100)

    target = TargetingPipeline.select_target(tower_pos, 50.0, TargetingStrategy.STRONGEST, grid, lambda eid: entities.get(eid))
    assert target is not None
    assert target.id == e2.id

    attack_def = AttackDefinition(base_damage=30.0, damage_type="kinetic")
    dealt = AttackPipeline.execute_attack(tower, target, attack_def, bus, lambda eid: entities.get(eid))
    assert dealt == 30.0
    assert e2.get_component(HealthComponent).current_health == 120.0
""")

    # 4. tests/simulation/test_mass_wave_simulation.py
    write_file("tests/simulation/test_mass_wave_simulation.py", """import pytest
from client.core.rng import DeterministicRNG
from client.adaptive.defense_profiler import DefenseProfiler, DefenseProfile
from client.adaptive.event_collector import PlayerDefenseMetrics
from client.adaptive.wave_generator import AdaptiveWaveGenerator

def test_100_wave_adaptive_simulation():
    rng = DeterministicRNG(seed=2026)
    generator = AdaptiveWaveGenerator(rng)
    
    metrics = PlayerDefenseMetrics()
    metrics.towers_built_by_type["KINETIC"] = 4
    metrics.damage_dealt_by_type["kinetic"] = 1500.0
    metrics.cc_applications = 12

    for wave in range(1, 101):
        profile = DefenseProfiler.analyze_profile(metrics)
        wave_def = generator.generate_wave(wave, profile)
        assert wave_def.threat_budget > 0
        assert len(wave_def.spawn_schedule) > 0
        assert wave_def.estimated_duration > 0
""")

    # 5. tests/replay/test_replay_determinism.py
    write_file("tests/replay/test_replay_determinism.py", """import pytest
from client.core.rng import DeterministicRNG
from client.replay.command_recorder import ReplayRecorder, PlayerCommandType
from client.replay.replay_playback import ReplayPlaybackController

def test_replay_recorder_and_playback():
    rec = ReplayRecorder(map_id="map_alpha", random_seed=777)
    rec.record_command(tick=10, command_type=PlayerCommandType.PLACE_TOWER, tower_type="kinetic_gatling", x=120, y=180)
    rec.record_command(tick=60, command_type=PlayerCommandType.START_WAVE, wave=1)
    
    serialized = rec.serialize()
    controller = ReplayPlaybackController(serialized)
    assert controller.header.random_seed == 777
    assert len(controller.commands) == 2

    cmds_tick_10 = controller.get_commands_for_tick(10)
    assert len(cmds_tick_10) == 1
    assert cmds_tick_10[0].params["tower_type"] == "kinetic_gatling"
""")

    print("Test Suites Generated.")

if __name__ == "__main__":
    generate()
