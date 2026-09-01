"""
Thermal Dissipation & Overheat Penalty Engine: CHRONO_DECELERATOR
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class HeatStatusSnapshot:
    current_temp_c: float
    is_overheated: bool
    cooldown_sec_remaining: float
    firerate_penalty_pct: float

class ChronoDeceleratorThermalEngine:
    def __init__(self):
        self.tower_id: str = "chrono_decelerator"
        self.max_temp_c: float = 210.0
        self.heat_per_shot_c: float = 5.5
        self.dissipation_rate_c_per_sec: float = 12.0

    def calculate_thermal_tick(self, current_temp: float, shots_fired: int, delta_time: float) -> HeatStatusSnapshot:
        added_heat = shots_fired * self.heat_per_shot_c
        dissipated = self.dissipation_rate_c_per_sec * delta_time
        temp = max(25.0, current_temp + added_heat - dissipated)
        is_jammed = temp >= self.max_temp_c
        penalty = 0.50 if is_jammed else (temp / self.max_temp_c) * 0.20

        return HeatStatusSnapshot(
            current_temp_c=round(temp, 1),
            is_overheated=is_jammed,
            cooldown_sec_remaining=round((temp - 25.0) / self.dissipation_rate_c_per_sec, 2) if is_jammed else 0.0,
            firerate_penalty_pct=round(penalty, 2)
        )
