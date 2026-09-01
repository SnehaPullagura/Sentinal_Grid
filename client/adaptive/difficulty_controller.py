from __future__ import annotations
from dataclasses import dataclass

@dataclass
class DifficultyState:
    wave_number: int = 1
    base_threat_budget: float = 15.0
    threat_growth_per_wave: float = 6.0
    max_threat_budget: float = 400.0
    player_performance_multiplier: float = 1.0

class DifficultyController:
    def __init__(self):
        self.state: DifficultyState = DifficultyState()

    def calculate_wave_budget(self, wave: int, player_lives_pct: float, response_time_factor: float = 1.0) -> float:
        self.state.wave_number = wave
        raw_budget = min(self.state.max_threat_budget, self.state.base_threat_budget + (wave - 1) * self.state.threat_growth_per_wave)
        
        perf_mult = 1.0
        if player_lives_pct > 0.9:
            perf_mult = 1.15
        elif player_lives_pct < 0.3:
            perf_mult = 0.85

        self.state.player_performance_multiplier = perf_mult
        return raw_budget * perf_mult
