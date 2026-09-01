import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate_pure_code():
    print("--> Generating 30 Python Map Generators (Pure Code)...")

    for s_idx in range(1, 31):
        grid_rows = []
        for r in range(24):
            cells = [str((c + r + s_idx) % 4) for c in range(32)]
            grid_rows.append(f"            [{', '.join(cells)}]")
        grid_str = ",\n".join(grid_rows)

        m_code = f'''"""
Sector {s_idx:02d} Grid Matrix Terrain & Elevation Data Model.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple, Dict
from client.math.vector2d import Vector2D

@dataclass
class TileProperty:
    tile_type: int
    is_buildable: bool
    is_walkable: bool
    elevation_level: int
    movement_cost: float

class Sector{s_idx:02d}MatrixGrid:
    def __init__(self):
        self.sector_id: str = "sector_{s_idx:02d}"
        self.width: int = 32
        self.height: int = 24
        self.cell_size: float = 32.0
        self.raw_grid_data: List[List[int]] = [
{grid_str}
        ]
        self.tile_properties: Dict[int, TileProperty] = self._init_properties()

    def _init_properties(self) -> Dict[int, TileProperty]:
        return {{
            0: TileProperty(0, is_buildable=True, is_walkable=True, elevation_level=0, movement_cost=1.0),
            1: TileProperty(1, is_buildable=False, is_walkable=False, elevation_level=0, movement_cost=999.0),
            2: TileProperty(2, is_buildable=False, is_walkable=True, elevation_level=0, movement_cost=0.8),
            3: TileProperty(3, is_buildable=True, is_walkable=True, elevation_level=1, movement_cost=1.2)
        }}

    def get_tile(self, x: int, y: int) -> int:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.raw_grid_data[y][x]
        return 1

    def is_cell_buildable(self, x: int, y: int) -> bool:
        t = self.get_tile(x, y)
        return self.tile_properties[t].is_buildable

    def get_cell_cost(self, x: int, y: int) -> float:
        t = self.get_tile(x, y)
        return self.tile_properties[t].movement_cost
'''
        write_file(f"client/maps/sectors_code/sector_{s_idx:02d}_grid.py", m_code)

    print("--> Generating 30 Python Wave Timeline Modules (Pure Code)...")

    for s_idx in range(1, 31):
        wave_blocks = []
        for w in range(1, 16):
            wave_blocks.append(f'''
            WaveTimeline(
                wave_number={w},
                threat_cost={20.0 + w * 12.0 + s_idx * 4.0},
                credit_reward={50 + w * 15},
                energy_reward={10 + w * 2},
                spawn_events=[
                    ("scout_infiltrator" if {w} < 4 else "armored_juggernaut", {4 + w}, 0.0, 1.2),
                    ("aero_interceptor" if {w} % 2 == 0 else "emp_saboteur", {3 + (w // 2)}, 5.0, 1.5),
                    ("hydra_broodmother" if {w} % 3 == 0 else "phantom_infiltrator", {2 + (w // 4)}, 10.0, 2.0)
                ]
            )''')
        waves_joined = ",".join(wave_blocks)

        w_code = f'''"""
Sector {s_idx:02d} Complete Wave Timeline & Threat Matrix.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple, Dict

@dataclass
class WaveTimeline:
    wave_number: int
    threat_cost: float
    credit_reward: int
    energy_reward: int
    spawn_events: List[Tuple[str, int, float, float]]

class Sector{s_idx:02d}WaveCompiler:
    def __init__(self):
        self.sector_id: str = "sector_{s_idx:02d}"
        self.timelines: List[WaveTimeline] = [{waves_joined}
        ]

    def get_timeline(self, wave: int) -> WaveTimeline:
        if 1 <= wave <= len(self.timelines):
            return self.timelines[wave - 1]
        return self.timelines[-1]
'''
        write_file(f"client/campaign/waves_code/sector_{s_idx:02d}_timeline.py", w_code)

    print("--> Generating Frontend TypeScript Game Catalogs...")

    # Frontend TypeScript Game Data
    write_file("frontend/src/game_data/towers_catalog.ts", """export interface TowerData {
  id: string;
  name: string;
  archetype: string;
  cost: number;
  dps: number;
  range: number;
  damageType: string;
  description: string;
}

export const TOWER_CATALOG: TowerData[] = [
  { id: "kinetic_vulcan", name: "Kinetic Vulcan Turret", archetype: "KINETIC", cost: 120, dps: 81, range: 110, damageType: "kinetic", description: "High-RPM rotary kinetic cannon" },
  { id: "gauss_accelerator", name: "Gauss Magnetic Accelerator", archetype: "KINETIC", cost: 240, dps: 72, range: 210, damageType: "kinetic", description: "Long-range anti-armor slug" },
  { id: "tachyon_prism", name: "Tachyon Beam Prism", archetype: "ENERGY", cost: 175, dps: 75, range: 140, damageType: "energy", description: "Continuous energy burn" },
  { id: "frostbite_cryo", name: "Frostbite Cryo Projector", archetype: "CONTROL", cost: 145, dps: 17, range: 115, damageType: "cryo", description: "Sub-zero chilling emitter" },
  { id: "arc_discharger", name: "Arc Tesla Discharger", archetype: "ENERGY", cost: 210, dps: 45, range: 130, damageType: "energy", description: "Chain lightning array" },
  { id: "nanite_hive", name: "Nanite Swarm Spire", archetype: "EXPERIMENTAL", cost: 290, dps: 75, range: 125, damageType: "corrosive", description: "Micro-drone corrosive swarm" },
  { id: "siege_howitzer", name: "Siege Howitzer Battery", archetype: "KINETIC", cost: 320, dps: 56, range: 260, damageType: "explosive", description: "Long-range area artillery" },
  { id: "orbital_uplink", name: "Orbital Command Uplink", archetype: "SUPPORT", cost: 250, dps: 0, range: 180, damageType: "support", description: "Aura damage amplifier" },
  { id: "singularity_trap", name: "Singularity Vortex Trap", archetype: "CONTROL", cost: 270, dps: 13, range: 120, damageType: "gravity", description: "Gravitational vortex" },
  { id: "emp_disruptor_tower", name: "EMP Grid Array", archetype: "CONTROL", cost: 195, dps: 16, range: 100, damageType: "emp", description: "Shield and ability jammer" },
  { id: "flak_anti_air", name: "Flak Quad-Cannon", archetype: "KINETIC", cost: 160, dps: 112, range: 160, damageType: "kinetic", description: "Anti-air fragmentation battery" },
  { id: "plasma_mortar_artillery", name: "Heavy Plasma Mortar", archetype: "EXPERIMENTAL", cost: 310, dps: 48, range: 175, damageType: "plasma", description: "Superheated plasma splash" },
  { id: "chrono_decelerator", name: "Chrono Field Decelerator", archetype: "CONTROL", cost: 230, dps: 8, range: 140, damageType: "chrono", description: "Temporal slowdown field" },
  { id: "resource_refinery", name: "Matter Extraction Core", archetype: "RESOURCE", cost: 200, dps: 0, range: 0, damageType: "economy", description: "Periodic credit harvester" },
  { id: "solar_lance", name: "Solar Lance Array", archetype: "ENERGY", cost: 350, dps: 84, range: 240, damageType: "solar", description: "Orbital solar piercing beam" },
  { id: "sonic_resonator", name: "Sonic Concussion Cannon", archetype: "CONTROL", cost: 180, dps: 26, range: 95, damageType: "sonic", description: "Shockwave repulsor" },
  { id: "tesla_overcharger", name: "Tesla Overcharger Pylon", archetype: "SUPPORT", cost: 220, dps: 0, range: 150, damageType: "support", description: "Energy fire rate booster" },
  { id: "missile_pod_battery", name: "Viper Missile Battery", archetype: "KINETIC", cost: 260, dps: 63, range: 190, damageType: "explosive", description: "Homing missile salvo" },
  { id: "heavy_defense_matrix", name: "Aegis Shield Matrix", archetype: "SUPPORT", cost: 240, dps: 0, range: 160, damageType: "shield", description: "Recharging ally energy barrier" },
  { id: "quantum_blaster", name: "Quantum Phase Blaster", archetype: "EXPERIMENTAL", cost: 380, dps: 126, range: 150, damageType: "quantum", description: "True damage phase emitter" }
];
""")

    print("Pure Code Scale Generated.")

if __name__ == "__main__":
    generate_pure_code()
