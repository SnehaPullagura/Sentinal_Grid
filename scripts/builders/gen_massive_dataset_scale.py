import os
import sys
import json
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate_massive_datasets():
    print("--> Generating Massive Production Datasets...")

    # 1. campaign_waves_full.json (All 30 sectors, 15 waves each = 450 complete wave objects)
    all_waves_data = {"schema_version": "1.0.0", "sectors": {}}
    for s_idx in range(1, 31):
        s_id = f"sector_{s_idx:02d}"
        s_waves = []
        for w_idx in range(1, 16):
            s_waves.append({
                "wave_number": w_idx,
                "threat_budget": round(25.0 + w_idx * 14.5 + s_idx * 5.0, 1),
                "bonus_credits": 60 + w_idx * 15,
                "spawns": [
                    {
                        "time_offset_sec": 0.0,
                        "enemy_type": "scout_infiltrator" if w_idx < 4 else "armored_juggernaut",
                        "count": 4 + w_idx + (s_idx % 4),
                        "spacing_sec": 1.2,
                        "hp_modifier": round(1.0 + (w_idx * 0.08), 2),
                        "speed_modifier": round(1.0 + (s_idx * 0.02), 2)
                    },
                    {
                        "time_offset_sec": 8.0,
                        "enemy_type": "aero_interceptor" if w_idx % 2 == 0 else "emp_saboteur",
                        "count": 3 + (w_idx // 2),
                        "spacing_sec": 1.5,
                        "hp_modifier": round(1.0 + (w_idx * 0.06), 2),
                        "speed_modifier": 1.0
                    }
                ]
            })
        all_waves_data["sectors"][s_id] = s_waves
    write_file("data/definitions/campaign_waves_full.json", json.dumps(all_waves_data, indent=2))

    # 2. achievements_full.json (50 achievements)
    ach_data = {"schema_version": "1.0.0", "achievements": []}
    for a_idx in range(1, 51):
        cat = ["Combat", "Economy", "Tactics", "Mastery", "Campaign"][a_idx % 5]
        ach_data["achievements"].append({
            "id": f"ach_{a_idx:02d}",
            "title": f"Tactical Distinction #{a_idx:02d}",
            "category": cat,
            "description": f"Successfully execute level {a_idx} operational requirements in {cat} defense theater.",
            "target_value": 50 * a_idx,
            "reward_tokens": 10 + (a_idx % 5) * 5,
            "badge_icon": f"badge_icon_{cat.lower()}_{a_idx % 6}"
        })
    write_file("data/definitions/achievements_full.json", json.dumps(ach_data, indent=2))

    # 3. audio_soundfont_full.json (50 sound effects)
    audio_data = {"schema_version": "1.0.0", "sound_effects": []}
    sfx_names = [
        "shot_kinetic_light", "shot_kinetic_heavy", "shot_railgun", "shot_laser_continuous",
        "shot_plasma_mortar", "shot_cryo_stream", "shot_arc_tesla", "shot_nanite_swarm",
        "shot_missile_launch", "shot_solar_lance", "shot_flak_burst", "shot_sonic_pulse",
        "explosion_plasma", "explosion_artillery", "explosion_emp", "hit_shield_deflect",
        "hit_armor_shred", "hit_flesh_impact", "alarm_base_breach", "alarm_boss_inbound",
        "ability_orbital_strike", "ability_overclock", "ability_cryo_surge", "ability_emp_surge",
        "ui_click", "ui_buy_tower", "ui_sell_tower", "ui_upgrade_tower", "ui_error_denied"
    ]
    for s_idx, sname in enumerate(sfx_names, 1):
        audio_data["sound_effects"].append({
            "name": sname,
            "waveform": "sawtooth" if "shot" in sname else "noise" if "explosion" in sname else "sine",
            "base_frequency_hz": 120.0 + s_idx * 25.0,
            "attack_sec": 0.01,
            "decay_sec": 0.15,
            "sustain_level": 0.4,
            "release_sec": 0.25,
            "volume_gain": 0.8
        })
    write_file("data/definitions/audio_soundfont_full.json", json.dumps(audio_data, indent=2))

    # 4. particle_presets_full.json
    particle_data = {"schema_version": "1.0.0", "presets": []}
    p_names = [
        ("kinetic_spark", "#00f0ff", 15, 80.0, 0.4),
        ("plasma_detonation", "#f59e0b", 35, 140.0, 0.8),
        ("cryo_frost_burst", "#38bdf8", 20, 60.0, 0.6),
        ("tesla_arc_flash", "#a855f7", 25, 110.0, 0.3),
        ("emp_ring_wave", "#3b82f6", 50, 180.0, 0.7),
        ("nanite_corrosion_cloud", "#22c55e", 30, 45.0, 1.2),
        ("orbital_impact_crater", "#ef4444", 60, 220.0, 1.0),
        ("boss_enrage_aura", "#dc2626", 40, 95.0, 1.5)
    ]
    for pname, pcolor, pcount, pspeed, plife in p_names:
        particle_data["presets"].append({
            "preset_id": pname,
            "color_hex": pcolor,
            "count": pcount,
            "speed": pspeed,
            "lifetime_sec": plife,
            "gravity": 0.0,
            "fade_out": True
        })
    write_file("data/definitions/particle_presets_full.json", json.dumps(particle_data, indent=2))

    print("Massive Datasets Generated.")

if __name__ == "__main__":
    generate_massive_datasets()
