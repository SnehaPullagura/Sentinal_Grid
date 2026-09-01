from __future__ import annotations
from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, List, Optional, Callable
from client.math.vector2d import Vector2D
from client.events.event_bus import EventBus, GameEventType
from client.economy.economy_service import EconomyService

@dataclass
class CommanderAbility:
    ability_id: str
    name: str
    energy_cost: int
    cooldown_seconds: float
    current_cooldown: float = 0.0
    radius: float = 80.0
    description: str = ""

class AbilityManager:
    def __init__(self, event_bus: EventBus, economy: EconomyService):
        self.event_bus: EventBus = event_bus
        self.economy: EconomyService = economy
        self.abilities: Dict[str, CommanderAbility] = {
            "orbital_strike": CommanderAbility("orbital_strike", "Orbital Kinetic Strike", 40, 30.0, radius=90.0, description="Massive area damage blast"),
            "cryo_surge": CommanderAbility("cryo_surge", "Cryo Flash Freeze", 25, 20.0, radius=120.0, description="Freezes all enemies in area for 4s"),
            "nano_repair": CommanderAbility("nano_repair", "Nanite Base Repair", 35, 45.0, description="Restores 25 Base HP"),
            "overclock": CommanderAbility("overclock", "Grid Overclock", 30, 25.0, description="Boosts all tower attack speeds by 50% for 8s")
        }

    def update_cooldowns(self, delta_time: float) -> None:
        for ab in self.abilities.values():
            if ab.current_cooldown > 0.0:
                ab.current_cooldown = max(0.0, ab.current_cooldown - delta_time)

    def trigger_ability(self, ability_id: str, target_pos: Optional[Vector2D] = None) -> bool:
        ab = self.abilities.get(ability_id)
        if not ab or ab.current_cooldown > 0.0:
            return False

        if not self.economy.spend(energy=ab.energy_cost, reason=f"ability_{ability_id}"):
            return False

        ab.current_cooldown = ab.cooldown_seconds
        self.event_bus.emit(
            GameEventType.ABILITY_TRIGGERED,
            ability_id=ability_id,
            target_pos=target_pos.to_tuple() if target_pos else None
        )
        return True
