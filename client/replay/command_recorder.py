from __future__ import annotations
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import json

class PlayerCommandType(Enum):
    PLACE_TOWER = auto()
    UPGRADE_TOWER = auto()
    SELL_TOWER = auto()
    TRIGGER_ABILITY = auto()
    CHANGE_TARGETING = auto()
    START_WAVE = auto()
    SPEED_CHANGE = auto()

@dataclass
class PlayerCommand:
    tick: int
    command_type: PlayerCommandType
    params: Dict[str, Any]

@dataclass
class ReplayHeader:
    version: str = "1.0.0"
    map_id: str = "map_alpha_outpost"
    random_seed: int = 1337
    total_ticks: int = 0
    final_score: int = 0
    player_name: str = "Commander"

class ReplayRecorder:
    def __init__(self, map_id: str, random_seed: int):
        self.header: ReplayHeader = ReplayHeader(map_id=map_id, random_seed=random_seed)
        self.commands: List[PlayerCommand] = []

    def record_command(self, tick: int, command_type: PlayerCommandType, **params) -> None:
        self.commands.append(PlayerCommand(tick=tick, command_type=command_type, params=params))

    def serialize(self) -> str:
        return json.dumps({
            "header": {
                "version": self.header.version,
                "map_id": self.header.map_id,
                "random_seed": self.header.random_seed,
                "total_ticks": self.header.total_ticks,
                "final_score": self.header.final_score
            },
            "commands": [
                {
                    "tick": cmd.tick,
                    "type": cmd.command_type.name,
                    "params": cmd.params
                }
                for cmd in self.commands
            ]
        }, indent=2)
