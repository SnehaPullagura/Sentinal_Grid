"""
Penetration & Kinetic Ricochet Solver: ORBITAL_UPLINK
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class BallisticPenetrationOutcome:
    raw_kinetic_energy: float
    penetration_depth_mm: float
    armor_fracture_factor: float
    ricochet_probability: float
    is_critical_fracture: bool

class OrbitalUplinkPenetrationSolver:
    def __init__(self):
        self.tower_id: str = "orbital_uplink"
        self.nominal_caliber_mm: float = 44.7
        self.hardness_rating_hrc: float = 64.0

    def evaluate_penetration(self, armor_thickness_mm: float, impact_angle_deg: float) -> BallisticPenetrationOutcome:
        eff_thickness = armor_thickness_mm / max(0.2, (90.0 - impact_angle_deg) / 90.0)
        energy = self.nominal_caliber_mm * 150.0
        depth = energy / max(1.0, eff_thickness)
        ricochet = max(0.0, min(0.95, (impact_angle_deg - 45.0) / 45.0)) if impact_angle_deg > 45.0 else 0.0

        return BallisticPenetrationOutcome(
            raw_kinetic_energy=round(energy, 1),
            penetration_depth_mm=round(depth, 2),
            armor_fracture_factor=round(min(1.0, depth / max(1.0, armor_thickness_mm)), 3),
            ricochet_probability=round(ricochet, 3),
            is_critical_fracture=(depth > armor_thickness_mm * 1.5)
        )
