"""
Combat Matchup & Tactical Evaluation Engine: QUANTUM_BLASTER
Calculates time-to-kill (TTK), armor reduction efficiency, damage falloff,
and elemental status synergy against all 20 classified hostile enemy archetypes.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
from client.math.vector2d import Vector2D

@dataclass
class MatchupEvaluation:
    enemy_id: str
    time_to_kill_sec: float
    effective_dps: float
    shots_to_kill: int
    threat_rating: str  # FAVORED, BALANCED, DISFAVORED
    recommended_positioning: str
    elemental_synergy: str

class QuantumBlasterMatchupMatrix:
    def __init__(self):
        self.tower_id: str = "quantum_blaster"
        self.base_damage: float = 120.0
        self.fire_rate: float = 1.5
        self.range_radius: float = 100.0
        self.matchups: Dict[str, MatchupEvaluation] = self._build_matchup_database()

    def _build_matchup_database(self) -> Dict[str, MatchupEvaluation]:
        enemies = [
            ("scout_infiltrator", 65.0, 0.0, 0.0, "FAVORED", "Deploy near entrance to eliminate fast runners"),
            ("armored_juggernaut", 450.0, 0.0, 18.0, "BALANCED", "Requires armor-piercing or corrosive support"),
            ("phantom_infiltrator", 120.0, 0.0, 4.0, "FAVORED", "Use thermal or radar scan to reveal cloaking"),
            ("aero_interceptor", 95.0, 0.0, 0.0, "DISFAVORED" if "quantum_blaster" != "flak_anti_air" else "FAVORED", "High altitude tracking required"),
            ("aegis_shield_bearer", 180.0, 220.0, 5.0, "BALANCED", "Deplete energy barrier with sustained fire"),
            ("nanite_medic", 150.0, 50.0, 2.0, "FAVORED", "High-priority target; eliminate before ally healing"),
            ("emp_saboteur", 140.0, 0.0, 2.0, "DISFAVORED", "Keep at long range to avoid EMP shockwaves"),
            ("hydra_broodmother", 320.0, 0.0, 6.0, "BALANCED", "Prepare area splash damage for split swarm units"),
            ("shadow_assassin", 160.0, 0.0, 5.0, "FAVORED", "Use slowing cryo field to negate evasive speed"),
            ("siege_breaker_ram", 500.0, 0.0, 20.0, "DISFAVORED", "Heavy damage focus required before wall breach"),
            ("dreadnought_titan", 3500.0, 1200.0, 25.0, "DISFAVORED", "Full network focus fire and commander abilities"),
            ("cyber_hive_carrier", 2800.0, 800.0, 15.0, "DISFAVORED", "Anti-air flak and focus fire required"),
            ("glider_swarmer", 25.0, 0.0, 0.0, "FAVORED", "One-shot kill; effective against swarm waves"),
            ("heavy_colossus", 600.0, 0.0, 22.0, "DISFAVORED", "Heavy armor sponge; apply armor shred debuffs"),
            ("leech_parasite", 40.0, 0.0, 0.0, "FAVORED", "Rapid extermination prevents credit siphoning"),
            ("phase_shifter", 160.0, 100.0, 4.0, "BALANCED", "Time attacks between quantum phase cycles"),
            ("warp_striker", 110.0, 0.0, 0.0, "BALANCED", "Stun to prevent reactive teleport jumps"),
            ("vanguard_mech", 380.0, 150.0, 12.0, "BALANCED", "Balanced kinetic/energy dual engagement"),
            ("frost_walker", 220.0, 0.0, 8.0, "BALANCED", "Use kinetic or plasma damage; immune to cryo"),
            ("apocalypse_overlord", 6000.0, 2500.0, 35.0, "DISFAVORED", "Apex confrontation requiring all tier 5 towers")
        ]

        db = {}
        for eid, hp, sh, arm, rating, pos_hint in enemies:
            tot_hp = hp + sh
            eff_dmg = max(1.0, self.base_damage - arm * 0.5)
            dps = eff_dmg * self.fire_rate
            ttk = round(tot_hp / max(1.0, dps), 2)
            shots = int(tot_hp / eff_dmg) + 1

            db[eid] = MatchupEvaluation(
                enemy_id=eid,
                time_to_kill_sec=ttk,
                effective_dps=round(dps, 1),
                shots_to_kill=shots,
                threat_rating=rating,
                recommended_positioning=pos_hint,
                elemental_synergy="Thermal Shock + Cryo" if "quantum_blaster".startswith("plasma") else "Standard Kinetic Burst"
            )
        return db

    def evaluate_against(self, enemy_id: str) -> MatchupEvaluation:
        return self.matchups.get(enemy_id, MatchupEvaluation(
            enemy_id=enemy_id,
            time_to_kill_sec=5.0,
            effective_dps=self.base_damage * self.fire_rate,
            shots_to_kill=10,
            threat_rating="BALANCED",
            recommended_positioning="Default line of sight",
            elemental_synergy="None"
        ))
