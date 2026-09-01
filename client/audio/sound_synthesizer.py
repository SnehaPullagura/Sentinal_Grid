from __future__ import annotations
from enum import Enum, auto
from typing import Dict, List, Optional
from dataclasses import dataclass

class SoundEffect(Enum):
    KINETIC_SHOT = auto()
    RAILGUN_SLUG = auto()
    LASER_BEAM = auto()
    CRYO_CHILL = auto()
    PLASMA_EXPLOSION = auto()
    EMP_PULSE = auto()
    ORBITAL_STRIKE = auto()
    ENEMY_DEATH = auto()
    BASE_ALARM = auto()
    WAVE_START = auto()
    VICTORY_FANFARE = auto()
    DEFEAT_ALARM = auto()

@dataclass
class SynthWaveform:
    wave_type: str = "sine"  # sine, square, sawtooth, triangle, noise
    frequency_hz: float = 440.0
    attack_sec: float = 0.01
    decay_sec: float = 0.1
    sustain_level: float = 0.5
    release_sec: float = 0.2
    gain: float = 0.8
    pitch_bend_hz: float = 0.0

class SoundSynthesizer:
    def __init__(self):
        self.master_volume: float = 0.8
        self.sfx_volume: float = 1.0
        self.music_volume: float = 0.7
        self.synth_profiles: Dict[SoundEffect, List[SynthWaveform]] = self._build_profiles()

    def _build_profiles(self) -> Dict[SoundEffect, List[SynthWaveform]]:
        return {
            SoundEffect.KINETIC_SHOT: [
                SynthWaveform(wave_type="sawtooth", frequency_hz=320.0, attack_sec=0.005, decay_sec=0.06, sustain_level=0.1, release_sec=0.05, pitch_bend_hz=-180.0),
                SynthWaveform(wave_type="noise", frequency_hz=800.0, attack_sec=0.002, decay_sec=0.03, sustain_level=0.0, release_sec=0.02, gain=0.6)
            ],
            SoundEffect.RAILGUN_SLUG: [
                SynthWaveform(wave_type="sawtooth", frequency_hz=160.0, attack_sec=0.01, decay_sec=0.25, sustain_level=0.2, release_sec=0.2, pitch_bend_hz=-90.0, gain=1.0),
                SynthWaveform(wave_type="square", frequency_hz=90.0, attack_sec=0.01, decay_sec=0.3, sustain_level=0.1, release_sec=0.15, gain=0.8)
            ],
            SoundEffect.LASER_BEAM: [
                SynthWaveform(wave_type="triangle", frequency_hz=880.0, attack_sec=0.02, decay_sec=0.15, sustain_level=0.6, release_sec=0.1, pitch_bend_hz=220.0)
            ],
            SoundEffect.PLASMA_EXPLOSION: [
                SynthWaveform(wave_type="noise", frequency_hz=250.0, attack_sec=0.02, decay_sec=0.4, sustain_level=0.3, release_sec=0.35, gain=1.0),
                SynthWaveform(wave_type="sine", frequency_hz=75.0, attack_sec=0.01, decay_sec=0.3, sustain_level=0.2, release_sec=0.25, pitch_bend_hz=-35.0)
            ],
            SoundEffect.ORBITAL_STRIKE: [
                SynthWaveform(wave_type="sine", frequency_hz=120.0, attack_sec=0.1, decay_sec=0.8, sustain_level=0.6, release_sec=0.6, pitch_bend_hz=-60.0, gain=1.0),
                SynthWaveform(wave_type="noise", frequency_hz=400.0, attack_sec=0.05, decay_sec=1.2, sustain_level=0.4, release_sec=0.8, gain=0.9)
            ],
            SoundEffect.BASE_ALARM: [
                SynthWaveform(wave_type="square", frequency_hz=660.0, attack_sec=0.02, decay_sec=0.1, sustain_level=0.8, release_sec=0.05, pitch_bend_hz=-120.0)
            ],
            SoundEffect.WAVE_START: [
                SynthWaveform(wave_type="triangle", frequency_hz=440.0, attack_sec=0.05, decay_sec=0.3, sustain_level=0.4, release_sec=0.2, pitch_bend_hz=440.0)
            ]
        }

    def trigger_sfx(self, effect: SoundEffect) -> Optional[dict]:
        waveforms = self.synth_profiles.get(effect)
        if not waveforms:
            return None
        return {
            "effect": effect.name,
            "master_volume": self.master_volume * self.sfx_volume,
            "tracks": [
                {
                    "wave": w.wave_type,
                    "freq": w.frequency_hz,
                    "attack": w.attack_sec,
                    "decay": w.decay_sec,
                    "sustain": w.sustain_level,
                    "release": w.release_sec,
                    "gain": w.gain,
                    "bend": w.pitch_bend_hz
                }
                for w in waveforms
            ]
        }
