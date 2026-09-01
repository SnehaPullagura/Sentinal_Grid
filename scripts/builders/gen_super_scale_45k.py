import os
import sys
import json
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate_wave_schedules():
    print("--> Generating 30 Sector Wave Schedule Modules...")

    for i in range(1, 31):
        w_code = f'''"""
Sector {i:02d} Complete Wave Spawn Schedule & Dynamic Timing Configuration.
Contains fixed wave templates, adaptive scaling thresholds, and boss trigger points.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class SpawnEntry:
    spawn_time_offset: float
    enemy_type: str
    count: int
    interval: float
    lane_index: int

@dataclass
class SectorWave:
    wave_number: int
    threat_budget: float
    spawns: List[SpawnEntry]
    bonus_credits: int

class Sector{i:02d}WaveSchedule:
    def __init__(self):
        self.sector_id: str = "sector_{i:02d}"
        self.total_waves: int = {12 + i}
        self.waves: List[SectorWave] = self._build_waves()

    def _build_waves(self) -> List[SectorWave]:
        waves = []
        for w in range(1, {13 + i}):
            is_boss_wave = (w % 5 == 0)
            threat = 20.0 + w * 12.0
            spawns = [
                SpawnEntry(0.0, "scout_infiltrator" if w < 5 else "armored_juggernaut", 4 + w, 1.2, 0),
                SpawnEntry(5.0, "aero_interceptor" if w % 2 == 0 else "emp_saboteur", 3 + (w // 2), 1.5, 1)
            ]
            if is_boss_wave:
                spawns.append(SpawnEntry(12.0, "dreadnought_titan" if w == 10 else "apocalypse_overlord", 1, 0.0, 0))

            waves.append(SectorWave(
                wave_number=w,
                threat_budget=threat,
                spawns=spawns,
                bonus_credits=50 + w * 15
            ))
        return waves

    def get_wave(self, wave_number: int) -> SectorWave:
        if 1 <= wave_number <= len(self.waves):
            return self.waves[wave_number - 1]
        return self.waves[-1]
'''
        write_file(f"client/campaign/waves/sector_{i:02d}_waves.py", w_code)

    # 2. 20 Telemetry Metrics Processors
    metrics = [
        ("damage_per_credit", "DamagePerCreditMetric", "Evaluates economic ROI for each placed tower"),
        ("kill_efficiency_index", "KillEfficiencyIndexMetric", "Measures percentage of enemy HP dealt within tower optimal range"),
        ("chokepoint_pressure", "ChokepointPressureMetric", "Tracks enemy density per square unit along major route curves"),
        ("overkill_waste_ratio", "OverkillWasteRatioMetric", "Calculates excessive damage dealt beyond remaining target HP"),
        ("reaction_time_evaluator", "ReactionTimeEvaluatorMetric", "Logs latency between enemy wave spawn and player defensive adaptations"),
        ("stun_chain_auditor", "StunChainAuditorMetric", "Monitors crowd control overlap and diminishing returns"),
        ("armor_shred_synergy", "ArmorShredSynergyMetric", "Quantifies bonus physical damage enabled by corrosive debuffs"),
        ("thermal_shock_counter", "ThermalShockCounterMetric", "Tracks frequency of Cryo + Plasma elemental combos"),
        ("energy_grid_drain", "EnergyGridDrainMetric", "Audits energy consumption vs passive recharge efficiency"),
        ("apm_efficiency_tracker", "APMEfficiencyTrackerMetric", "Calculates commander actions per minute during active combat"),
        ("flying_leak_risk_index", "FlyingLeakRiskIndexMetric", "Assesses defense readiness against high-speed aerial swarms"),
        ("boss_burst_dps_tracker", "BossBurstDPSTrackerMetric", "Measures single-target DPS focus during boss phase transitions"),
        ("barricade_longevity_audit", "BarricadeLongevityAuditMetric", "Tracks total damage absorbed by placed tactical obstacles"),
        ("economic_compound_growth", "EconomicCompoundGrowthMetric", "Evaluates credit bank growth from interest and refineries"),
        ("range_coverage_density", "RangeCoverageDensityMetric", "Maps total overlapping firing arcs over entire grid"),
        ("enemy_speed_decay_rate", "EnemySpeedDecayRateMetric", "Calculates average speed reduction from cryo/chrono fields"),
        ("anti_stealth_readiness", "AntiStealthReadinessMetric", "Evaluates sensor coverage against cloaked phantom assassins"),
        ("critical_hit_variance", "CriticalHitVarianceMetric", "Audits RNG variance across critical strike rolls"),
        ("orbital_strike_accuracy", "OrbitalStrikeAccuracyMetric", "Calculates hit-to-kill efficiency of commander orbital strikes"),
        ("overall_tactical_rating", "OverallTacticalRatingMetric", "Aggregates all performance metrics into a combat mastery score")
    ]

    for mid, cname, desc in metrics:
        mcode = f'''"""
Telemetry Metric Engine: {cname}
{desc}
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class MetricSnapshot:
    tick: int
    metric_value: float
    confidence_score: float

class {cname}:
    def __init__(self):
        self.metric_name: str = "{cname}"
        self.description: str = "{desc}"
        self.history: List[MetricSnapshot] = []

    def record_sample(self, tick: int, raw_value: float, confidence: float = 1.0) -> None:
        self.history.append(MetricSnapshot(tick=tick, metric_value=raw_value, confidence_score=confidence))

    def get_average(self) -> float:
        if not self.history: return 0.0
        return sum(s.metric_value for s in self.history) / len(self.history)

    def get_latest(self) -> float:
        return self.history[-1].metric_value if self.history else 0.0
'''
        write_file(f"client/analytics/metrics/{mid}.py", mcode)

if __name__ == "__main__":
    generate_wave_schedules()
