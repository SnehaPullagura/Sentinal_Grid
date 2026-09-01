from __future__ import annotations
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
