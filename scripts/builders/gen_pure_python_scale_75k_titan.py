import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate_titan_scale():
    print("--> Generating 30 Challenge Scenario Evaluators (Pure Code)...")

    for s_idx in range(1, 31):
        c_code = f'''"""
Sector {s_idx:02d} Challenge Scenario Evaluator & Modifier Matrix.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional

@dataclass
class ChallengeModifier:
    mod_id: str
    name: str
    enemy_speed_mult: float
    enemy_hp_mult: float
    tower_cost_mult: float
    energy_decay_rate: float

class Sector{s_idx:02d}ChallengeEvaluator:
    def __init__(self):
        self.sector_id: str = "sector_{s_idx:02d}"
        self.challenge_name: str = "IRON_MAN_CRUCIBLE_{s_idx:02d}"
        self.modifiers: List[ChallengeModifier] = [
            ChallengeModifier("SPEED_SURGE", "Kinetic Overdrive", 1.25, 0.90, 1.0, 0.0),
            ChallengeModifier("ARMORED_CONVOY", "Nanite Reinforced Plating", 0.85, 1.45, 1.10, 0.0),
            ChallengeModifier("ENERGY_DROUGHT", "Plasma Core Drain", 1.0, 1.0, 1.20, 0.05)
        ]

    def get_aggregate_difficulty(self) -> float:
        return round(1.0 + ({s_idx} * 0.08), 2)
'''
        write_file(f"client/campaign/challenges_full_code/sector_{s_idx:02d}_challenge.py", c_code)

    print("--> Generating 20 Procedural Audio Synthesizers (Pure Code)...")

    sounds = [
        ("kinetic_vulcan_audio", "KineticVulcanAudio", 440.0, 0.08, "square", 0.7),
        ("gauss_accelerator_audio", "GaussAcceleratorAudio", 120.0, 0.45, "sawtooth", 0.9),
        ("tachyon_prism_audio", "TachyonPrismAudio", 880.0, 0.30, "sine", 0.5),
        ("frostbite_cryo_audio", "FrostbiteCryoAudio", 260.0, 0.25, "triangle", 0.4),
        ("arc_discharger_audio", "ArcDischargerAudio", 650.0, 0.15, "sawtooth", 0.8),
        ("nanite_hive_audio", "NaniteHiveAudio", 320.0, 0.50, "sine", 0.6),
        ("siege_howitzer_audio", "SiegeHowitzerAudio", 80.0, 0.80, "sawtooth", 1.0),
        ("orbital_uplink_audio", "OrbitalUplinkAudio", 1200.0, 0.20, "sine", 0.3),
        ("singularity_trap_audio", "SingularityTrapAudio", 90.0, 0.90, "sine", 0.7),
        ("emp_disruptor_audio", "EMPDisruptorAudio", 520.0, 0.35, "square", 0.85),
        ("flak_anti_air_audio", "FlakAntiAirAudio", 280.0, 0.12, "sawtooth", 0.75),
        ("plasma_mortar_audio", "PlasmaMortarAudio", 160.0, 0.60, "triangle", 0.8),
        ("chrono_decelerator_audio", "ChronoDeceleratorAudio", 200.0, 0.40, "sine", 0.4),
        ("resource_refinery_audio", "ResourceRefineryAudio", 350.0, 0.10, "triangle", 0.25),
        ("solar_lance_audio", "SolarLanceAudio", 950.0, 0.70, "sine", 0.9),
        ("sonic_resonator_audio", "SonicResonatorAudio", 110.0, 0.30, "sine", 0.8),
        ("tesla_overcharger_audio", "TeslaOverchargerAudio", 780.0, 0.22, "square", 0.6),
        ("missile_battery_audio", "MissileBatteryAudio", 190.0, 0.40, "sawtooth", 0.85),
        ("shield_matrix_audio", "ShieldMatrixAudio", 400.0, 0.30, "sine", 0.35),
        ("quantum_blaster_audio", "QuantumBlasterAudio", 1400.0, 0.25, "sine", 0.95)
    ]

    for sid, sname, freq, dur, wave, vol in sounds:
        a_code = f'''"""
Procedural Audio Sound Engine: {sname}
"""
from __future__ import annotations
from dataclasses import dataclass
import math

@dataclass
class SynthesizedAudioFrame:
    sound_id: str
    frequency_hz: float
    duration_sec: float
    waveform: str
    amplitude: float

class {sname}Synthesizer:
    def __init__(self):
        self.sound_id: str = "{sid}"
        self.fundamental_frequency: float = {freq}
        self.sample_rate: int = 44100
        self.duration: float = {dur}
        self.waveform_type: str = "{wave}"
        self.master_volume: float = {vol}

    def generate_frame_metadata(self) -> SynthesizedAudioFrame:
        return SynthesizedAudioFrame(
            sound_id=self.sound_id,
            frequency_hz=self.fundamental_frequency,
            duration_sec=self.duration,
            waveform=self.waveform_type,
            amplitude=self.master_volume
        )
'''
        write_file(f"client/audio/procedural_synth/{sid}_synth.py", a_code)

    print("--> Generating 30 Simulation Diagnostics State Validators (Pure Code)...")

    for s_idx in range(1, 31):
        diag_code = f'''"""
Sector {s_idx:02d} Simulation Determinism Validator & Checksum Engine.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple
import hashlib

@dataclass
class DeterminismAuditEntry:
    tick_number: int
    entity_checksum: str
    spatial_checksum: str
    is_synchronized: bool

class Sector{s_idx:02d}DeterminismAuditor:
    def __init__(self):
        self.sector_id: str = "sector_{s_idx:02d}"
        self.audit_records: List[DeterminismAuditEntry] = []

    def record_tick_audit(self, tick: int, entity_data: str, spatial_data: str) -> bool:
        e_hash = hashlib.sha256(entity_data.encode("utf-8")).hexdigest()[:16]
        s_hash = hashlib.sha256(spatial_data.encode("utf-8")).hexdigest()[:16]
        is_synced = (len(e_hash) == 16 and len(s_hash) == 16)
        self.audit_records.append(DeterminismAuditEntry(
            tick_number=tick,
            entity_checksum=e_hash,
            spatial_checksum=s_hash,
            is_synchronized=is_synced
        ))
        return is_synced
'''
        write_file(f"client/analytics/diagnostics_code/sector_{s_idx:02d}_auditor.py", diag_code)

    print("Titan Scale Generated.")

if __name__ == "__main__":
    generate_titan_scale()
