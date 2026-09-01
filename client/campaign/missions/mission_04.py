"""
Campaign Mission 04: World 1 - Level 4
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from client.math.vector2d import Vector2D
from client.maps.map_definition import MapDefinition

@dataclass
class MissionObjective:
    objective_id: str
    description: str
    is_mandatory: bool = True
    is_completed: bool = False
    reward_tokens: int = 10

@dataclass
class ScriptedWaveEvent:
    wave_number: int
    trigger_delay: float
    enemy_types: List[str]
    count: int
    dialogue_cue: str

class Mission04Controller:
    def __init__(self):
        self.mission_id: str = "mission_04"
        self.world_number: int = 1
        self.level_number: int = 4
        self.is_boss_mission: bool = False
        self.starting_credits: int = 500
        self.starting_energy: int = 120
        self.target_waves: int = 14
        self.objectives: List[MissionObjective] = self._build_objectives()
        self.scripted_events: List[ScriptedWaveEvent] = self._build_events()

    def _build_objectives(self) -> List[MissionObjective]:
        return [
            MissionObjective("obj_survive", "Survive all waves", is_mandatory=True, reward_tokens=15),
            MissionObjective("obj_base_hp", "Maintain base integrity above 75%", is_mandatory=False, reward_tokens=25),
            MissionObjective("obj_speed_clear", "Complete mission in record time", is_mandatory=False, reward_tokens=20)
        ]

    def _build_events(self) -> List[ScriptedWaveEvent]:
        events = []
        for w in range(1, 15):
            events.append(ScriptedWaveEvent(
                wave_number=w,
                trigger_delay=2.0,
                enemy_types=["scout_infiltrator", "armored_juggernaut"] if w % 2 == 0 else ["aero_interceptor", "shield_bearer"],
                count=5 + w * 2,
                dialogue_cue="Tactical HQ: Hostiles inbound!"
            ))
        return events

    def get_map_definition(self) -> MapDefinition:
        return MapDefinition(
            map_id="map_sector_04",
            name="Sector 04",
            width=32,
            height=24,
            spawn_points=[Vector2D(16.0, 16.0), Vector2D(16.0, 680.0)],
            base_objective_pos=Vector2D(960.0, 350.0),
            starting_credits=self.starting_credits,
            starting_energy=self.starting_energy,
            total_waves=self.target_waves
        )
