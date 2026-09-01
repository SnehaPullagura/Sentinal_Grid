import pytest
from client.towers.specializations.kinetic_vulcan import KineticVulcanTower
from client.towers.specializations.gauss_accelerator import GaussAcceleratorTower
from client.towers.specializations.tachyon_prism import TachyonPrismTower
from client.towers.specializations.frostbite_cryo import FrostbiteCryoTower

def test_specialized_towers_init():
    vulcan = KineticVulcanTower()
    assert vulcan.stats.attack.base_damage == 18.0
    assert vulcan.stats.attack.attack_rate == 4.5
    
    gauss = GaussAcceleratorTower()
    assert gauss.stats.attack.range_radius == 210.0
    assert gauss.stats.attack.base_damage == 120.0
    
    tachyon = TachyonPrismTower()
    assert tachyon.stats.archetype.name == "ENERGY"
