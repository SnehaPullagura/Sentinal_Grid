"""
Campaign Mission 16: World 4 - Level 1
Hostile Zone Offensive
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
    reward_tokens: int = 15

@dataclass
class ScriptedWaveEvent:
    wave_number: int
    trigger_delay: float
    enemy_types: List[str]
    count: int
    dialogue_cue: str

class Mission16Controller:
    def __init__(self):
        self.mission_id: str = "mission_16"
        self.world_number: int = 4
        self.level_number: int = 1
        self.is_boss_mission: bool = False
        self.starting_credits: int = 820
        self.starting_energy: int = 200
        self.target_waves: int = 28
        self.objectives: List[MissionObjective] = self._build_objectives()
        self.scripted_events: List[ScriptedWaveEvent] = self._build_events()

    def _build_objectives(self) -> List[MissionObjective]:
        return [
            MissionObjective("obj_survive", "Survive all waves", is_mandatory=True, reward_tokens=20),
            MissionObjective("obj_base_hp", "Maintain base integrity above 80%", is_mandatory=False, reward_tokens=30),
            MissionObjective("obj_speed_clear", "Complete mission in record time", is_mandatory=False, reward_tokens=25)
        ]

    def _build_events(self) -> List[ScriptedWaveEvent]:
        events = []
        for w in range(1, 29):
            events.append(ScriptedWaveEvent(
                wave_number=w,
                trigger_delay=2.0,
                enemy_types=["armored_juggernaut", "dreadnought_titan"] if w % 5 == 0 else ["aero_interceptor", "emp_saboteur"],
                count=6 + w * 2,
                dialogue_cue="Tactical Command: High threat wave engaging defensive grid!"
            ))
        return events

    def get_map_definition(self) -> MapDefinition:
        return MapDefinition(
            map_id="map_sector_16",
            name="Sector 16",
            width=32,
            height=24,
            spawn_points=[Vector2D(16.0, 16.0), Vector2D(16.0, 680.0)],
            base_objective_pos=Vector2D(960.0, 350.0),
            starting_credits=self.starting_credits,
            starting_energy=self.starting_energy,
            total_waves=self.target_waves
        )
