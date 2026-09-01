import pytest
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
