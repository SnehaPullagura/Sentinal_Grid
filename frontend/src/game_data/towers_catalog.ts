export interface TowerData {
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
