"""
Sector 25 Spatial Density & Defense Heatmap Integrator.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from client.math.vector2d import Vector2D

@dataclass
class HeatmapCell:
    x: int
    y: int
    damage_density: float
    casualty_count: int
    chokepoint_rating: float

class Sector25HeatmapAnalyzer:
    def __init__(self):
        self.sector_id: str = "sector_25"
        self.width: int = 32
        self.height: int = 24
        self.cells: Dict[Tuple[int, int], HeatmapCell] = self._init_cells()

    def _init_cells(self) -> Dict[Tuple[int, int], HeatmapCell]:
        grid = {}
        for y in range(self.height):
            for x in range(self.width):
                is_choke = (x in (10, 20) and 8 <= y <= 16)
                grid[(x, y)] = HeatmapCell(
                    x=x,
                    y=y,
                    damage_density=round((x * y * 25) % 100 / 10.0, 2),
                    casualty_count=(x + y + 25) % 15,
                    chokepoint_rating=0.85 if is_choke else 0.20
                )
        return grid

    def get_cell_density(self, x: int, y: int) -> float:
        c = self.cells.get((x, y))
        return c.damage_density if c else 0.0

    def get_top_chokepoints(self) -> List[Tuple[int, int]]:
        return [pos for pos, cell in self.cells.items() if cell.chokepoint_rating > 0.8]
