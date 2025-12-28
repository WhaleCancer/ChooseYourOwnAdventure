#!/usr/bin/env python3
"""
Extract all weapons, armor, and apparel from Vanilla Expanded mods
"""

import os
import xml.etree.ElementTree as ET
import json
from pathlib import Path

WORKSHOP_DIR = Path("E:/Steam/steamapps/workshop/content/294100")

# Mod IDs for Vanilla Expanded mods
VWE_MODS = {
    "1814383360": "Vanilla Weapons Expanded",
    "1989352844": "Vanilla Weapons Expanded - Laser",
    "2194472657": "Vanilla Weapons Expanded - Grenades",
    "2329126791": "Vanilla Weapons Expanded - Heavy Weapons",
    "2375692535": "Vanilla Weapons Expanded - Coilguns",
    "2419690698": "Vanilla Weapons Expanded - Makeshift",
    "2454918139": "Vanilla Weapons Expanded - Frontier",
    "2454918552": "Vanilla Weapons Expanded - Non-Lethal",
    "2454918354": "Vanilla Weapons Expanded - Tribal",
    "2826922787": "Vanilla Persona Weapons Expanded",
}

VAE_MODS = {
    "1814988282": "Vanilla Armour Expanded",
    "1814987817": "Vanilla Apparel Expanded",
    "2521176396": "Vanilla Apparel Expanded - Accessories",
}

VFE_MODS = {
    "2052918119": "Vanilla Factions Expanded - Settlers",
    "2654846754": "Vanilla Factions Expanded - Ancients",
    "2723801948": "Vanilla Factions Expanded - Pirates",
    "2787850474": "Vanilla Factions Expanded - Classical",
}

def find_latest_version_dir(mod_dir):
    """Find the latest version directory (1.6 > 1.5 > 1.4, etc.)"""
    versions = ["1.6", "1.5", "1.4", "1.3", "1.2", "1.1", "1.0"]
    for version in versions:
        version_path = mod_dir / version
        if version_path.exists():
            return version_path
    return None

def extract_weapon_data(weapon_def):
    """Extract weapon data from ThingDef"""
    data = {
        "defName": weapon_def.get("defName") or "",
        "label": "",
        "description": "",
        "techLevel": "",
        "isMelee": False,
        "damage": 0,
        "dps": 0,
        "cooldown": 0,
        "accuracy": {},
        "range": 0,
        "mass": 0,
    }
    
    for child in weapon_def:
        tag = child.tag
        if tag == "label":
            data["label"] = child.text or ""
        elif tag == "description":
            data["description"] = child.text or ""
        elif tag == "techLevel":
            data["techLevel"] = child.text or ""
        elif tag == "statBases":
            for stat in child:
                stat_name = stat.tag
                try:
                    value = float(stat.text or 0)
                    if stat_name == "MeleeWeapon_AverageDPS":
                        data["dps"] = value
                        data["isMelee"] = True
                    elif stat_name == "MeleeWeapon_DamageMultiplier":
                        data["damage_multiplier"] = value
                        data["isMelee"] = True
                    elif stat_name == "RangedWeapon_Cooldown":
                        data["cooldown"] = value
                    elif stat_name == "RangedWeapon_DamageMultiplier":
                        data["damage_multiplier"] = value
                    elif stat_name.startswith("Accuracy"):
                        data["accuracy"][stat_name] = value
                    elif stat_name == "Mass":
                        data["mass"] = value
                    elif stat_name == "MeleeWeapon_CooldownTime":
                        data["cooldown"] = value
                except:
                    pass
        elif tag == "verbs":
            for verb in child:
                if verb.tag == "li":
                    verb_type = verb.get("class", "")
                    if "Verb_MeleeAttack" in verb_type or "Verb_MeleeApplyHediff" in verb_type:
                        data["isMelee"] = True
                    for verb_child in verb:
                        if verb_child.tag == "damageDef":
                            # Melee damage
                            data["isMelee"] = True
                        elif verb_child.tag == "defaultProjectile":
                            # Ranged weapon
                            pass
                        elif verb_child.tag == "damageAmountBase":
                            try:
                                data["damage"] = float(verb_child.text or 0)
                            except:
                                pass
                        elif verb_child.tag == "range":
                            try:
                                data["range"] = float(verb_child.text or 0)
                            except:
                                pass
    
    # Try to infer DPS for ranged weapons
    if not data["isMelee"] and data["cooldown"] > 0 and data["damage"] > 0:
        data["dps"] = data["damage"] / data["cooldown"]
    
    return data

def extract_armor_data(armor_def):
    """Extract armor/apparel data from ThingDef"""
    data = {
        "defName": armor_def.get("defName") or "",
        "label": "",
        "description": "",
        "techLevel": "",
        "sharpArmor": 0,
        "bluntArmor": 0,
        "heatArmor": 0,
        "mass": 0,
        "bodyPartGroups": [],
        "layers": [],
    }
    
    for child in armor_def:
        tag = child.tag
        if tag == "label":
            data["label"] = child.text or ""
        elif tag == "description":
            data["description"] = child.text or ""
        elif tag == "techLevel":
            data["techLevel"] = child.text or ""
        elif tag == "statBases":
            for stat in child:
                stat_name = stat.tag
                try:
                    value = float(stat.text or 0)
                    if stat_name == "ArmorRating_Sharp":
                        data["sharpArmor"] = value
                    elif stat_name == "ArmorRating_Blunt":
                        data["bluntArmor"] = value
                    elif stat_name == "ArmorRating_Heat":
                        data["heatArmor"] = value
                    elif stat_name == "Mass":
                        data["mass"] = value
                except:
                    pass
        elif tag == "apparel":
            for apparel_child in child:
                if apparel_child.tag == "bodyPartGroups":
                    for bp in apparel_child:
                        if bp.tag == "li":
                            data["bodyPartGroups"].append(bp.text or "")
                elif apparel_child.tag == "layers":
                    for layer in apparel_child:
                        if layer.tag == "li":
                            data["layers"].append(layer.text or "")
    
    return data

def parse_xml_file(xml_path):
    """Parse XML file and return root element"""
    try:
        tree = ET.parse(xml_path)
        return tree.getroot()
    except Exception as e:
        print(f"Error parsing {xml_path}: {e}")
        return None

def scan_mod_for_weapons(mod_dir, mod_name):
    """Scan a mod directory for weapons"""
    version_dir = find_latest_version_dir(mod_dir)
    if not version_dir:
        print(f"No version directory found for {mod_name}")
        return []
    
    weapons = []
    defs_dir = version_dir / "Defs"
    if not defs_dir.exists():
        return []
    
    # Find all XML files in ThingDefs_Misc
    for xml_file in defs_dir.rglob("**/*Weapon*.xml"):
        root = parse_xml_file(xml_file)
        if root is None:
            continue
        
        for thing_def in root.findall(".//ThingDef"):
            if thing_def.get("ParentName") and "Weapon" in thing_def.get("ParentName", ""):
                weapon_data = extract_weapon_data(thing_def)
                if weapon_data["defName"]:
                    weapon_data["mod"] = mod_name
                    weapon_data["modID"] = mod_dir.name
                    weapons.append(weapon_data)
            # Also check for defName containing weapon indicators
            elif "weapon" in thing_def.get("defName", "").lower() or "gun" in thing_def.get("defName", "").lower():
                weapon_data = extract_weapon_data(thing_def)
                if weapon_data["defName"]:
                    weapon_data["mod"] = mod_name
                    weapon_data["modID"] = mod_dir.name
                    weapons.append(weapon_data)
    
    return weapons

def scan_mod_for_armor(mod_dir, mod_name):
    """Scan a mod directory for armor/apparel"""
    version_dir = find_latest_version_dir(mod_dir)
    if not version_dir:
        return []
    
    armors = []
    defs_dir = version_dir / "Defs"
    if not defs_dir.exists():
        return []
    
    # Find all XML files with armor/apparel
    for xml_file in defs_dir.rglob("**/*.xml"):
        if "Armor" not in xml_file.name and "Apparel" not in xml_file.name:
            continue
        
        root = parse_xml_file(xml_file)
        if root is None:
            continue
        
        for thing_def in root.findall(".//ThingDef"):
            # Check if it's apparel/armor
            has_apparel = thing_def.find(".//apparel") is not None
            if has_apparel or "Apparel" in thing_def.get("ParentName", "") or "Armor" in thing_def.get("ParentName", ""):
                armor_data = extract_armor_data(thing_def)
                if armor_data["defName"]:
                    armor_data["mod"] = mod_name
                    armor_data["modID"] = mod_dir.name
                    armors.append(armor_data)
    
    return armors

def main():
    all_weapons = []
    all_armors = []
    
    # Scan VWE mods
    for mod_id, mod_name in VWE_MODS.items():
        mod_dir = WORKSHOP_DIR / mod_id
        if mod_dir.exists():
            print(f"Scanning {mod_name}...")
            weapons = scan_mod_for_weapons(mod_dir, mod_name)
            all_weapons.extend(weapons)
            print(f"  Found {len(weapons)} weapons")
    
    # Scan VAE mods
    for mod_id, mod_name in VAE_MODS.items():
        mod_dir = WORKSHOP_DIR / mod_id
        if mod_dir.exists():
            print(f"Scanning {mod_name}...")
            armors = scan_mod_for_armor(mod_dir, mod_name)
            all_armors.extend(armors)
            print(f"  Found {len(armors)} armor/apparel items")
    
    # Scan VFE mods for weapons and armor
    for mod_id, mod_name in VFE_MODS.items():
        mod_dir = WORKSHOP_DIR / mod_id
        if mod_dir.exists():
            print(f"Scanning {mod_name}...")
            weapons = scan_mod_for_weapons(mod_dir, mod_name)
            armors = scan_mod_for_armor(mod_dir, mod_name)
            all_weapons.extend(weapons)
            all_armors.extend(armors)
            print(f"  Found {len(weapons)} weapons, {len(armors)} armor/apparel items")
    
    # Output results
    output = {
        "weapons": all_weapons,
        "armors": all_armors,
    }
    
    with open("vanilla_expanded_items.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nTotal: {len(all_weapons)} weapons, {len(all_armors)} armor/apparel items")
    print("Results saved to vanilla_expanded_items.json")

if __name__ == "__main__":
    main()



