import pytest
from client.combat.calculators.armor_penetration_calculator import ArmorPenetrationCalculator
from client.combat.calculators.elemental_reaction_engine import ElementalReactionEngine, DamageType, ElementalReaction
from client.combat.calculators.damage_falloff_model import DamageFalloffModel
from client.combat.calculators.chain_lightning_propagator import ChainLightningPropagator
from client.combat.calculators.critical_strike_matrix import CriticalStrikeMatrix
from client.math.vector2d import Vector2D

def test_armor_penetration_calculation():
    res = ArmorPenetrationCalculator.calculate(raw_damage=100.0, target_armor=50.0, flat_penetration=10.0, percent_penetration=0.20)
    assert res.final_damage > 0.0
    assert res.effective_armor == 32.0

def test_elemental_thermal_shock_reaction():
    res = ElementalReactionEngine.evaluate_reaction(DamageType.CRYO, DamageType.PLASMA, base_damage=50.0)
    assert res.reaction == ElementalReaction.THERMAL_SHOCK
    assert res.bonus_damage == 87.5
    assert res.applied_status == "SHATTERED"

def test_chain_lightning_propagation():
    hits = ChainLightningPropagator.resolve_chain(
        origin_pos=Vector2D(0, 0),
        initial_target_id="t1",
        initial_target_pos=Vector2D(50, 50),
        base_damage=100.0,
        max_chains=3,
        jump_radius=60.0,
        decay_factor=0.7,
        candidate_entities=[("t2", Vector2D(80, 50)), ("t3", Vector2D(120, 50))]
    )
    assert len(hits) == 3
    assert hits[0].damage_dealt == 100.0
    assert hits[1].damage_dealt == 70.0
    assert hits[2].damage_dealt == 49.0
