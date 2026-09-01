import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate():
    print("Generating Expanded Game Systems & Domain Modules...")

    # 1. client/audio/sound_synthesizer.py
    write_file("client/audio/sound_synthesizer.py", """from __future__ import annotations
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
""")

    # 2. client/particles/particle_system.py
    write_file("client/particles/particle_system.py", """from __future__ import annotations
from typing import List, Dict, Optional
from dataclasses import dataclass, field
import random
from client.math.vector2d import Vector2D

@dataclass
class ParticleInstance:
    position: Vector2D
    velocity: Vector2D
    life_remaining: float
    max_life: float
    color_hex: str
    size: float
    fade_out: bool = True
    gravity: float = 0.0

class ParticleSystem:
    def __init__(self, max_particles: int = 2000):
        self.max_particles: int = max_particles
        self.particles: List[ParticleInstance] = []

    def emit_burst(
        self,
        origin: Vector2D,
        count: int = 15,
        color_hex: str = "#00f0ff",
        min_speed: float = 30.0,
        max_speed: float = 120.0,
        lifetime: float = 0.5,
        particle_size: float = 3.0
    ) -> None:
        for _ in range(count):
            if len(self.particles) >= self.max_particles:
                break
            angle = random.uniform(0.0, 6.28318)
            speed = random.uniform(min_speed, max_speed)
            vel = Vector2D.from_angle(angle, speed)
            p = ParticleInstance(
                position=origin.copy(),
                velocity=vel,
                life_remaining=lifetime,
                max_life=lifetime,
                color_hex=color_hex,
                size=particle_size
            )
            self.particles.append(p)

    def emit_trail(self, start_pos: Vector2D, end_pos: Vector2D, steps: int = 8, color_hex: str = "#38bdf8") -> None:
        for s in range(steps):
            t = s / max(1, steps)
            pos = start_pos.lerp(end_pos, t)
            p = ParticleInstance(
                position=pos,
                velocity=Vector2D((random.random() - 0.5) * 10.0, (random.random() - 0.5) * 10.0),
                life_remaining=0.3,
                max_life=0.3,
                color_hex=color_hex,
                size=2.0
            )
            self.particles.append(p)

    def update(self, delta_time: float) -> None:
        surviving = []
        for p in self.particles:
            p.life_remaining -= delta_time
            if p.life_remaining > 0.0:
                p.position.x += p.velocity.x * delta_time
                p.position.y += (p.velocity.y + p.gravity) * delta_time
                surviving.append(p)
        self.particles = surviving

    def clear(self) -> None:
        self.particles.clear()
""")

    # 3. client/progression/tech_tree.py
    write_file("client/progression/tech_tree.py", """from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional

@dataclass
class TechNode:
    tech_id: str
    name: str
    tree_branch: str  # Ballistics, Energy, Cryo, Armor, Commander, Economy
    tier: int
    token_cost: int
    prerequisites: List[str] = field(default_factory=list)
    stat_modifiers: Dict[str, float] = field(default_factory=dict)
    unlocked: bool = False
    description: str = ""

class TechTreeManager:
    def __init__(self):
        self.nodes: Dict[str, TechNode] = self._build_tech_tree()
        self.unlocked_techs: Set[str] = set()

    def _build_tech_tree(self) -> Dict[str, TechNode]:
        tree = {}
        # Ballistics Branch
        tree["bal_1"] = TechNode("bal_1", "Rifled Barrels", "Ballistics", 1, 20, stat_modifiers={"kinetic_damage": 0.15}, description="+15% Kinetic damage")
        tree["bal_2"] = TechNode("bal_2", "Depleted Uranium Munitions", "Ballistics", 2, 50, prerequisites=["bal_1"], stat_modifiers={"armor_penetration": 0.30}, description="+30% Armor penetration")
        tree["bal_3"] = TechNode("bal_3", "Magnetic Acceleration Coils", "Ballistics", 3, 100, prerequisites=["bal_2"], stat_modifiers={"railgun_fire_rate": 0.40}, description="+40% Railgun attack rate")

        # Energy Branch
        tree["nrg_1"] = TechNode("nrg_1", "Focusing Crystals", "Energy", 1, 20, stat_modifiers={"energy_damage": 0.15}, description="+15% Energy damage")
        tree["nrg_2"] = TechNode("nrg_2", "Continuous Beam Modulation", "Energy", 2, 55, prerequisites=["nrg_1"], stat_modifiers={"laser_range": 0.25}, description="+25% Laser range")
        tree["nrg_3"] = TechNode("nrg_3", "Plasma Superheating", "Energy", 3, 110, prerequisites=["nrg_2"], stat_modifiers={"plasma_splash_radius": 0.50}, description="+50% Plasma splash radius")

        # Cryo & Control Branch
        tree["cry_1"] = TechNode("cry_1", "Sub-Zero Coolant", "Cryo", 1, 25, stat_modifiers={"slow_potency": 0.20}, description="+20% Freeze slow strength")
        tree["cry_2"] = TechNode("cry_2", "Cryo Flash Condenser", "Cryo", 2, 60, prerequisites=["cry_1"], stat_modifiers={"freeze_duration": 0.35}, description="+35% Freeze duration")
        tree["cry_3"] = TechNode("cry_3", "Absolute Zero Core", "Cryo", 3, 120, prerequisites=["cry_2"], stat_modifiers={"cryo_damage_dot": 25.0}, description="Cryo attacks deal heavy DoT")

        # Commander Ops Branch
        tree["cmd_1"] = TechNode("cmd_1", "Orbital Telemetry", "Commander", 1, 30, stat_modifiers={"orbital_radius": 0.30}, description="+30% Orbital strike area")
        tree["cmd_2"] = TechNode("cmd_2", "Tactical Capacitor Array", "Commander", 2, 70, prerequisites=["cmd_1"], stat_modifiers={"max_energy": 50.0}, description="+50 Max energy pool")
        tree["cmd_3"] = TechNode("cmd_3", "Overclock Overdrive", "Commander", 3, 130, prerequisites=["cmd_2"], stat_modifiers={"overclock_duration": 5.0}, description="+5s Overclock duration")

        return tree

    def can_unlock(self, tech_id: str, available_tokens: int) -> bool:
        node = self.nodes.get(tech_id)
        if not node or node.unlocked or available_tokens < node.token_cost:
            return False
        return all(p in self.unlocked_techs for p in node.prerequisites)

    def unlock_tech(self, tech_id: str, available_tokens: int) -> Optional[int]:
        if not self.can_unlock(tech_id, available_tokens):
            return None
        node = self.nodes[tech_id]
        node.unlocked = True
        self.unlocked_techs.add(tech_id)
        return available_tokens - node.token_cost
""")

    # 4. client/analytics/combat_telemetry.py
    write_file("client/analytics/combat_telemetry.py", """from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
from client.events.event_bus import EventBus, GameEventType, GameEvent

@dataclass
class TelemetryFrame:
    tick: int
    active_enemies: int
    total_towers: int
    dps_average: float
    base_hp_remaining: float
    credits_current: int

class CombatTelemetryAggregator:
    def __init__(self, event_bus: EventBus):
        self.event_bus: EventBus = event_bus
        self.damage_events: List[float] = []
        self.kill_locations: List[Tuple[float, float]] = []
        self.frames: List[TelemetryFrame] = []
        self._subscribe()

    def _subscribe(self) -> None:
        self.event_bus.subscribe(GameEventType.DAMAGE_DEALT, self._on_dmg)
        self.event_bus.subscribe(GameEventType.ENEMY_DEATH, self._on_kill)

    def _on_dmg(self, ev: GameEvent) -> None:
        self.damage_events.append(ev.payload.get("damage", 0.0))

    def _on_kill(self, ev: GameEvent) -> None:
        pos = ev.payload.get("position")
        if pos:
            self.kill_locations.append((pos[0], pos[1]))

    def record_frame(self, tick: int, enemies: int, towers: int, hp: float, credits: int) -> None:
        dps = sum(self.damage_events[-60:]) if self.damage_events else 0.0
        self.frames.append(TelemetryFrame(
            tick=tick,
            active_enemies=enemies,
            total_towers=towers,
            dps_average=dps,
            base_hp_remaining=hp,
            credits_current=credits
        ))

    def get_summary(self) -> dict:
        return {
            "total_damage_recorded": sum(self.damage_events),
            "total_kills_recorded": len(self.kill_locations),
            "frames_count": len(self.frames),
            "peak_dps": max([f.dps_average for f in self.frames], default=0.0)
        }
""")

    print("Expanded Systems Generated.")

if __name__ == "__main__":
    generate()
