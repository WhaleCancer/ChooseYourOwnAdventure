"""
Add AFF Advanced Fighting Fantasy 2nd Ed page sources to skills based on actual page content.
"""
import os
import re

# Map skills to their AFF Advanced Fighting Fantasy 2nd Ed pages
# Based on actual page content review (corrected - pages are one number higher)
AFF2_SKILL_PAGE_MAP = {
    # Page 0025 - Characteristics (LUCK, MAGIC)
    'RULES/Skills/LUCK/Bargain.md': '0025',
    'RULES/Skills/LUCK/Bureaucracy.md': '0025',
    'RULES/Skills/LUCK/Etiquette.md': '0025',
    'RULES/Skills/LUCK/Languages.md': '0025',
    'RULES/Skills/MENTAL/Magic-Psionics.md': '0025',
    'RULES/Skills/MENTAL/Magic-Battle-Magic.md': '0025',
    'RULES/Skills/MENTAL/Magic-Chaos-Magic.md': '0025',
    'RULES/Skills/MENTAL/Magic-Conjuration.md': '0025',
    'RULES/Skills/MENTAL/Magic-Enchanting.md': '0025',
    'RULES/Skills/MENTAL/Magic-Mask-Magic.md': '0025',
    'RULES/Skills/MENTAL/Magic-Necromancy.md': '0025',
    'RULES/Skills/MENTAL/Magic-Tattooing.md': '0025',
    
    # Page 0026 - General Special Skills introduction, racial skills
    'RULES/Skills/MENTAL/Lore/Animal-Lore.md': '0026',
    'RULES/Skills/MENTAL/Lore/World-Lore.md': '0026',
    'RULES/Skills/MENTAL/Lore/City-Lore.md': '0026',
    'RULES/Skills/MENTAL/Lore/Religion-Lore.md': '0026',
    'RULES/Skills/MENTAL/Lore/Forest-Lore.md': '0026',
    'RULES/Skills/MENTAL/Lore/Underground-Lore.md': '0026',
    'RULES/Skills/MENTAL/Crafting.md': '0026',
    'RULES/Skills/PHYSICAL/Movement/Ride.md': '0026',
    
    # Page 0027 - Combat skills descriptions
    'RULES/Skills/PHYSICAL/Armor (Special Skill).md': '0027',
    'RULES/Skills/PHYSICAL/Melee Weapons/Axes.md': '0027',
    'RULES/Skills/PHYSICAL/Missile Weapons/Bows.md': '0027',
    'RULES/Skills/PHYSICAL/Melee Weapons/Brawling.md': '0027',
    'RULES/Skills/PHYSICAL/Melee Weapons/Clubs.md': '0027',
    
    # Page 0028 - More combat and movement skills
    'RULES/Skills/PHYSICAL/Melee Weapons/Polearms.md': '0028',
    'RULES/Skills/PHYSICAL/Melee Weapons/Staves.md': '0028',
    'RULES/Skills/PHYSICAL/Strength.md': '0028',
    'RULES/Skills/PHYSICAL/Melee Weapons/Swords.md': '0028',
    'RULES/Skills/PHYSICAL/Missile Weapons/Thrown.md': '0028',
    'RULES/Skills/PHYSICAL/Movement/Climb.md': '0028',
    'RULES/Skills/PHYSICAL/Movement/Dodge.md': '0028',
    'RULES/Skills/PHYSICAL/Movement/Jump.md': '0028',
    'RULES/Skills/PHYSICAL/Movement/Ride.md': '0028',
    'RULES/Skills/PHYSICAL/Movement/Swim.md': '0028',
    'RULES/Skills/PHYSICAL/Movement/Acrobatics.md': '0028',
    
    # Page 0029 - Stealth and Knowledge skills
    'RULES/Skills/MENTAL/Awareness.md': '0029',
    'RULES/Skills/MENTAL/Disguise.md': '0029',
    'RULES/Skills/MENTAL/Locks.md': '0029',
    'RULES/Skills/MENTAL/Sleight-of-Hand.md': '0029',
    'RULES/Skills/PHYSICAL/Sneak.md': '0029',
    'RULES/Skills/MENTAL/Trap-Knowledge.md': '0029',
    'RULES/Skills/MENTAL/Lore/Animal-Lore.md': '0029',
    'RULES/Skills/LUCK/Bargain.md': '0029',
    'RULES/Skills/MENTAL/Lore/City-Lore.md': '0029',
    'RULES/Skills/LUCK/Con.md': '0029',
    'RULES/Skills/MENTAL/Crafting.md': '0029',
    'RULES/Skills/LUCK/Etiquette.md': '0029',
    'RULES/Skills/MENTAL/Evaluate.md': '0029',
    'RULES/Skills/MENTAL/Lore/Forest-Lore.md': '0029',
    
    # Page 0030 - More Knowledge skills
    'RULES/Skills/MENTAL/Medicine.md': '0030',
    'RULES/Skills/MENTAL/Survival.md': '0030',
    'RULES/Skills/LUCK/Languages.md': '0030',
    'RULES/Skills/MENTAL/Law.md': '0030',
    'RULES/Skills/MENTAL/Leadership.md': '0030',
    'RULES/Skills/MENTAL/Lore/Religion-Lore.md': '0030',
    'RULES/Skills/MENTAL/Lore/Sea-Lore.md': '0030',
    'RULES/Skills/MENTAL/Secret-Signs.md': '0030',
    'RULES/Skills/MENTAL/Lore/Underground-Lore.md': '0030',
    'RULES/Skills/MENTAL/Lore/World-Lore.md': '0030',
    
    # Page 0031 - Magical skills
    'RULES/Skills/MENTAL/Magic-Psionics.md': '0031',
    
    # Page 0035 - Starting equipment and character creation (mentions Armour, Magic skills, weapon skills)
    'RULES/Skills/PHYSICAL/Armor (Special Skill).md': '0035',
    'RULES/Skills/PHYSICAL/Melee-Weapons.md': '0035',
}

AFF2_PAGES_DIR = 'AFF_Advanced_Fighting_Fantasy_2nd_Ed_Pages'
AFF2_BOOK_TITLE = 'AFF - Advanced Fighting Fantasy 2nd Ed'

def add_aff2_source_to_skill(skill_file, page_num):
    """Add AFF Advanced Fighting Fantasy 2nd Ed source image to a skill file"""
    if not os.path.exists(skill_file):
        print(f"Warning: Skill file not found: {skill_file}")
        return False
    
    # Check if AFF2 page exists
    aff2_page_path = os.path.join(AFF2_PAGES_DIR, f'page_{page_num}.png')
    if not os.path.exists(aff2_page_path):
        print(f"Warning: AFF2 page not found: {aff2_page_path}")
        return False
    
    # Read the file
    with open(skill_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create relative path for AFF2 page image
    skill_dir = os.path.dirname(skill_file)
    rel_image_path = os.path.relpath(aff2_page_path, skill_dir)
    rel_image_path = rel_image_path.replace('\\', '/')
    
    # Image markdown
    image_markdown = f'![Page {page_num}]({rel_image_path})'
    
    # Check if source section already exists
    source_pattern = r'## Source.*?(?=\n##|\Z)'
    source_match = re.search(source_pattern, content, re.DOTALL | re.IGNORECASE)
    
    if source_match:
        # Append to existing source section
        source_section = source_match.group(0)
        
        # Check if AFF2 source already exists for this page
        if AFF2_BOOK_TITLE in source_section and f'Page {page_num}' in source_section:
            print(f"  AFF2 source already exists for {skill_file} (page {page_num})")
            return True
        
        # Add AFF2 source with clear distinction
        # Add a separator if there are other sources
        if 'CB77011' in source_section or 'AFF005' in source_section or 'Stellar Adventures' in source_section or 'Heroes Companion' in source_section:
            # Add separator and AFF2 source
            new_source = source_section.rstrip() + f'\n\n---\n\n**{AFF2_BOOK_TITLE}, Page {page_num}**\n{image_markdown}\n'
        else:
            # Just add AFF2 source
            new_source = source_section.rstrip() + f'\n\n**{AFF2_BOOK_TITLE}, Page {page_num}**\n{image_markdown}\n'
        
        content = content.replace(source_section, new_source)
    else:
        # Create new source section
        source_section = f'\n\n## Source\n\n**{AFF2_BOOK_TITLE}, Page {page_num}**\n{image_markdown}\n'
        content = content.rstrip() + source_section
    
    # Write back
    with open(skill_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated: {skill_file} with AFF2 source (page {page_num})")
    return True

def main():
    """Main process to add AFF2 sources"""
    print("Adding AFF Advanced Fighting Fantasy 2nd Ed page sources to skills...")
    print("=" * 80)
    
    updated_count = 0
    skipped_count = 0
    
    # Group by page to show progress
    pages_processed = {}
    
    for skill_file, page_num in AFF2_SKILL_PAGE_MAP.items():
        if add_aff2_source_to_skill(skill_file, page_num):
            updated_count += 1
            if page_num not in pages_processed:
                pages_processed[page_num] = []
            pages_processed[page_num].append(skill_file)
        else:
            skipped_count += 1
    
    print("\n" + "=" * 80)
    print(f"Update complete!")
    print(f"Updated {updated_count} skill files")
    print(f"Skipped {skipped_count} skill files")
    print(f"\nPages processed:")
    for page_num in sorted(pages_processed.keys()):
        print(f"  Page {page_num}: {len(pages_processed[page_num])} skills")

if __name__ == '__main__':
    main()






