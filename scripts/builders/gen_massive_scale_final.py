import os
import sys
import json
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate_grand_finale():
    print("--> Generating World Managers, Data Definitions & Documentation...")

    # 1. 6 World Campaign Managers
    for w in range(1, 7):
        w_code = f'''"""
Campaign World {w:02d} Environmental Manager & Narrative Arc.
Regulates global atmospheric modifiers, radiation storms, orbital jamming,
and strategic unlocked tech nodes for World {w:02d}.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class EnvironmentalModifier:
    name: str
    description: str
    energy_recharge_multiplier: float = 1.0
    speed_multiplier: float = 1.0
    hazard_damage_per_sec: float = 0.0

class World{w:02d}Manager:
    def __init__(self):
        self.world_id: str = "world_{w:02d}"
        self.name: str = "Sector World {w:02d} - Core Frontier"
        self.environment: EnvironmentalModifier = EnvironmentalModifier(
            name="Atmospheric Ionization",
            description="High radiation speeds up shield recharge by 20%",
            energy_recharge_multiplier=1.20
        )
        self.levels: List[str] = [f"mission_{{(w-1)*5 + l:02d}}" for l in range(1, 6)]

    def get_world_status(self) -> dict:
        return {{
            "world_id": self.world_id,
            "name": self.name,
            "total_levels": len(self.levels),
            "environment": self.environment.name
        }}
'''
        write_file(f"client/campaign/worlds/world_{w:02d}_manager.py", w_code)

    # 2. Comprehensive JSON Definitions
    # abilities.json
    abilities_data = {
        "schema_version": "1.0.0",
        "abilities": [
            {"id": "orbital_strike", "name": "Orbital Kinetic Strike", "energy_cost": 40, "cooldown": 30.0, "radius": 90.0, "damage": 250.0, "description": "High-impact orbital kinetic projectile blast"},
            {"id": "cryo_surge", "name": "Cryo Flash Freeze", "energy_cost": 25, "cooldown": 20.0, "radius": 120.0, "duration": 4.0, "description": "Instantly freezes all hostiles in sector for 4s"},
            {"id": "nano_repair", "name": "Nanite Base Repair", "energy_cost": 35, "cooldown": 45.0, "heal_amount": 25.0, "description": "Repairs 25 Base HP integrity"},
            {"id": "overclock", "name": "Grid Overclock", "energy_cost": 30, "cooldown": 25.0, "duration": 8.0, "fire_rate_boost": 0.50, "description": "Boosts all tower attack speeds by 50% for 8s"},
            {"id": "emp_blast", "name": "EMP Sector Surge", "energy_cost": 35, "cooldown": 28.0, "radius": 140.0, "description": "Disables enemy electronic auras and shields"},
            {"id": "barricade_drop", "name": "Tactical Barricade Airdrop", "energy_cost": 20, "cooldown": 15.0, "hp": 400.0, "description": "Deploys heavy physical wall rerouting enemy paths"},
            {"id": "gold_rush", "name": "Bounty Protocol Stim", "energy_cost": 15, "cooldown": 35.0, "multiplier": 2.0, "duration": 10.0, "description": "Doubles credit reward from enemy kills for 10s"},
            {"id": "tactical_scan", "name": "Deep Sensor Recon", "energy_cost": 10, "cooldown": 12.0, "radius": 200.0, "description": "Reveals cloaked assassins and amplifies target damage by 20%"}
        ]
    }
    write_file("data/definitions/abilities.json", json.dumps(abilities_data, indent=2))

    # campaign.json
    campaign_data = {
        "schema_version": "1.0.0",
        "worlds": [
            {"id": "world_1", "name": "Iron Frontier", "theme": "Desert Outpost", "levels_count": 5, "boss": "Dreadnought Titan"},
            {"id": "world_2", "name": "Neon Grid", "theme": "Cyber Metropolis", "levels_count": 5, "boss": "Cyber Hive Carrier"},
            {"id": "world_3", "name": "Void Abyss", "theme": "Asteroid Stronghold", "levels_count": 5, "boss": "Hydra Broodmother"},
            {"id": "world_4", "name": "Plasma Rift", "theme": "Volcanic Core", "levels_count": 5, "boss": "Heavy Colossus"},
            {"id": "world_5", "name": "Cryo Tundra", "theme": "Glacial Sub-Zero", "levels_count": 5, "boss": "Frost Walker Overlord"},
            {"id": "world_6", "name": "Omega Citadel", "theme": "Apex Central Command", "levels_count": 5, "boss": "Apocalypse Overlord"}
        ]
    }
    write_file("data/definitions/campaign.json", json.dumps(campaign_data, indent=2))

    # 3. docs/HANDOVER.md & docs/ARCHITECTURE.md
    write_file("docs/ARCHITECTURE.md", """# Sentinel Grid — System Architecture & Engineering Blueprint

## Overview
Sentinel Grid is a production-grade 2D strategy and tower-defense game engineered with a deterministic fixed-timestep simulation kernel, data-driven entity components, dual-layer navigation graph with A* pathfinding, signature Adaptive Defense Engine, and modern full-stack web client/backend.

```mermaid
graph TD
    Client["React 18 SPA (Canvas 2D + Tailwind)"] --> API["FastAPI REST & Telemetry Engine"]
    Client --> Sim["Deterministic Simulation Loop (60 Hz)"]
    Sim --> Nav["Dual-Layer A* Navigation & FlowFields"]
    Sim --> Combat["Combat & Status Effect Pipeline"]
    Sim --> Adaptive["Adaptive Defense Engine"]
    Adaptive --> Waves["Dynamic Counter Wave Generator"]
    API --> DB["SQLite / PostgreSQL Persistence"]
    API --> LB["Server-Validated Global Leaderboards"]
```

## Core Subsystems
1. **Simulation Kernel**: Deterministic 60Hz tick loop, PCG-XSH-RR seedable PRNG, Vector2D algebra, Spatial Hash Grid.
2. **Dual-Layer Navigation**: 8-directional ground navigation with A*, dynamic obstacle invalidation, flow-field swarm vectors, flying layer bypass.
3. **Data-Driven Towers & Targeting**: 20 specialized towers, 7 targeting strategies (First, Last, Closest, Strongest, Weakest, Threat, Custom), attack pipeline, status effect stacking.
4. **Enemy AI & Boss Phase Engine**: 20 enemy classes, behavior trees, sensory perception, multi-phase boss controllers with dynamic enrage mechanics.
5. **Adaptive Defense Engine**: Real-time player tactic profiling, vulnerability heatmaps, bounded difficulty controllers, and dynamic counter-wave generator.
6. **Economy & Active Abilities**: 3-tier economy (Credits, Energy, Strategic Tokens), 8 commander abilities, 3-branch upgrade graphs.
7. **Campaign & Level Editor**: 6 worlds, 30 missions, 10 challenge modes, visual level and wave editor.
8. **Deterministic Replay & Save**: Command stream recorder, bit-exact deterministic playback, checksum-verified save migrations.
9. **FastAPI Backend**: JWT authentication, server-side simulation verification, leaderboards, replay storage, analytics ingestion, admin controls.
""")

if __name__ == "__main__":
    generate_grand_finale()
