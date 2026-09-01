from __future__ import annotations
import math

class DamageFalloffModel:
    @staticmethod
    def calculate_ballistic_damage(
        base_damage: float,
        distance: float,
        optimal_range: float,
        max_range: float,
        falloff_exponent: float = 1.5
    ) -> float:
        if distance <= optimal_range:
            return base_damage
        if distance >= max_range:
            return base_damage * 0.25  # Minimum glancing damage

        t = (distance - optimal_range) / max(1.0, max_range - optimal_range)
        decay = (1.0 - t) ** falloff_exponent
        return max(base_damage * 0.25, base_damage * (0.25 + 0.75 * decay))

    @staticmethod
    def calculate_splash_damage(
        center_damage: float,
        impact_dist: float,
        splash_radius: float,
        min_splash_ratio: float = 0.20
    ) -> float:
        if impact_dist >= splash_radius:
            return 0.0
        ratio = max(0.0, min(1.0, 1.0 - (impact_dist / splash_radius)))
        return center_damage * (min_splash_ratio + (1.0 - min_splash_ratio) * ratio)
