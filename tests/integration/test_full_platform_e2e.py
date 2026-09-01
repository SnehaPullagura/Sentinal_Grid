import pytest
from client.simulation.game_state import SimulationKernel
from client.math.vector2d import Vector2D
from client.entities.entity_model import Entity, TransformComponent, HealthComponent
from client.towers.specializations.kinetic_vulcan import KineticVulcanTower
from client.enemies.specializations.scout_infiltrator import ScoutInfiltratorEnemy
from client.adaptive.wave_generator import AdaptiveWaveGenerator
from client.adaptive.defense_profiler import DefenseProfiler, DefenseProfile
from client.adaptive.event_collector import PlayerDefenseMetrics
from client.core.rng import DeterministicRNG
from client.replay.command_recorder import ReplayRecorder, PlayerCommandType
from client.replay.replay_playback import ReplayPlaybackController
from backend.app.core.database import SessionLocal, init_db
from backend.app.auth.service import AuthService
from backend.app.leaderboard.service import LeaderboardService
from backend.app.replay.service import ReplayService

def test_full_platform_end_to_end():
    # 1. Initialize Deterministic Simulation Kernel
    rng = DeterministicRNG(seed=2026)
    kernel = SimulationKernel(seed=2026)
    kernel.initialize(base_hp=100.0, starting_credits=500)
    assert kernel.credits == 500
    assert kernel.base_current_hp == 100.0

    # 2. Place Tower & Record Command
    recorder = ReplayRecorder(map_id="sector_01", random_seed=2026)
    recorder.record_command(tick=1, command_type=PlayerCommandType.PLACE_TOWER, tower_type="kinetic_vulcan", x=100, y=100)
    assert kernel.spend_credits(120)
    assert kernel.credits == 380

    # 3. Simulate Waves & Adaptive Generation
    metrics = PlayerDefenseMetrics()
    metrics.towers_built_by_type["KINETIC"] = 2
    metrics.damage_dealt_by_type["kinetic"] = 800.0
    profile = DefenseProfiler.analyze_profile(metrics)
    assert profile.kinetic_dominance > 0.5

    wave_gen = AdaptiveWaveGenerator(rng)
    wave_1 = wave_gen.generate_wave(1, profile)
    assert len(wave_1.spawn_schedule) > 0

    for _ in range(60):
        kernel.step_tick()
    assert kernel.current_tick == 60

    # 4. Replay Verification
    serialized_rep = recorder.serialize()
    controller = ReplayPlaybackController(serialized_rep)
    assert controller.header.map_id == "sector_01"
    assert len(controller.commands) == 1

    # 5. Backend Database & Services Integration
    init_db()
    db = SessionLocal()
    try:
        user = AuthService.register_user(db, "E2E_Tester_Unique", "test@sentinel.grid", "Password123")
        assert user.id is not None

        lb_entry = LeaderboardService.record_score(db, "E2E_Tester_Unique", "sector_01", score=12500, waves_cleared=10)
        assert lb_entry.score == 12500

        top_scores = LeaderboardService.get_top_scores(db, "sector_01", limit=10)
        assert len(top_scores) >= 1

        rep_rec = ReplayService.save_replay(db, "E2E_Tester_Unique", "sector_01", 12500, serialized_rep)
        assert rep_rec.replay_id is not None
    finally:
        db.close()
