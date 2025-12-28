"""
Update skill markdown files to reference full page images instead of cropped images.
"""
import os
import re

# Map skills to their source pages
SKILL_PAGE_MAP = {
    # Page 0009 (page 8)
    'Acrobatics': '0009',
    'Animal Skills': '0009',
    
    # Page 0010 (page 9)
    'Armor': '0010',
    'Astronavigation': '0010',
    'Awareness': '0010',
    'Bargain': '0010',
    'Bureaucracy': '0010',
    'Brawling': '0010',
    'Communications': '0010',
    'Computers': '0010',
    'Dodge': '0010',
    'Engineering': '0010',
    'Etiquette': '0010',
    'Evaluate': '0010',
    'Firearms - Heavy': '0010',
    
    # Page 0011 (page 10)
    'Firearms - Light': '0011',
    'Firearms - Vehicle': '0011',
    'Languages': '0011',
    'Law': '0011',
    'Leadership': '0011',
    'Medicine': '0011',
    'Melee Weapons': '0011',
    'Pilot - Air': '0011',
    'Pilot - Ground': '0011',
    'Pilot - Space': '0011',
    'Pilot - Water': '0011',
    'Planetary Navigation': '0011',
    'Psionics': '0011',
    'Ride': '0011',
    'Science': '0011',
    
    # Page 0012 (page 11)
    'Sensors': '0012',
    'Sneak': '0012',
    'Starship Gunnery': '0012',
    'Survival': '0012',
    'Swim': '0012',
    'Thrown': '0012',
    'Trade Knowledge': '0012',
}

SKILL_FILE_MAP = {
    'Acrobatics': 'RULES/Skills/PHYSICAL/Movement/Acrobatics.md',
    'Animal Skills': 'RULES/Skills/MENTAL/Lore/Animal-Lore.md',
    'Armor': 'RULES/Skills/PHYSICAL/Armor (Special Skill).md',
    'Astronavigation': 'RULES/Skills/MENTAL/Astronavigation.md',
    'Awareness': 'RULES/Skills/MENTAL/Awareness.md',
    'Bargain': 'RULES/Skills/LUCK/Bargain.md',
    'Bureaucracy': 'RULES/Skills/LUCK/Bureaucracy.md',
    'Brawling': 'RULES/Skills/PHYSICAL/Melee Weapons/Brawling.md',
    'Communications': 'RULES/Skills/MENTAL/Communications.md',
    'Computers': 'RULES/Skills/MENTAL/Computers.md',
    'Dodge': 'RULES/Skills/PHYSICAL/Movement/Dodge.md',
    'Engineering': 'RULES/Skills/MENTAL/Engineering.md',
    'Etiquette': 'RULES/Skills/LUCK/Etiquette.md',
    'Evaluate': 'RULES/Skills/MENTAL/Evaluate.md',
    'Firearms - Heavy': 'RULES/Skills/PHYSICAL/Missile Weapons/Firearms-Heavy.md',
    'Firearms - Light': 'RULES/Skills/PHYSICAL/Missile Weapons/Firearms-Light.md',
    'Firearms - Vehicle': 'RULES/Skills/PHYSICAL/Firearms-Vehicle.md',
    'Languages': 'RULES/Skills/LUCK/Languages.md',
    'Law': 'RULES/Skills/MENTAL/Law.md',
    'Leadership': 'RULES/Skills/MENTAL/Leadership.md',
    'Medicine': 'RULES/Skills/MENTAL/Medicine.md',
    'Melee Weapons': 'RULES/Skills/PHYSICAL/Melee-Weapons.md',
    'Pilot - Air': 'RULES/Skills/PHYSICAL/Pilot-Air.md',
    'Pilot - Ground': 'RULES/Skills/PHYSICAL/Pilot-Ground.md',
    'Pilot - Space': 'RULES/Skills/MENTAL/Pilot-Space.md',
    'Pilot - Water': 'RULES/Skills/PHYSICAL/Pilot-Water.md',
    'Planetary Navigation': 'RULES/Skills/MENTAL/Planetary-Navigation.md',
    'Psionics': 'RULES/Skills/MENTAL/Magic-Psionics.md',
    'Ride': 'RULES/Skills/PHYSICAL/Movement/Ride.md',
    'Science': 'RULES/Skills/MENTAL/Science.md',
    'Sensors': 'RULES/Skills/MENTAL/Sensors.md',
    'Sneak': 'RULES/Skills/PHYSICAL/Sneak.md',
    'Starship Gunnery': 'RULES/Skills/PHYSICAL/Ship-Gunnery.md',
    'Survival': 'RULES/Skills/MENTAL/Survival.md',
    'Swim': 'RULES/Skills/PHYSICAL/Movement/Swim.md',
    'Thrown': 'RULES/Skills/PHYSICAL/Missile Weapons/Thrown.md',
    'Trade Knowledge': 'RULES/Skills/MENTAL/Trade-Knowledge.md',
}

PAGES_DIR = 'CB77011_stellar-adventures_Pages'

def update_skill_source(skill_file, page_num):
    """Update skill markdown file to reference full page image"""
    if not os.path.exists(skill_file):
        print(f"Warning: Skill file not found: {skill_file}")
        return False
    
    # Read the file
    with open(skill_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create relative path for full page image
    skill_dir = os.path.dirname(skill_file)
    page_image_path = os.path.join(PAGES_DIR, f'page_{page_num}.png')
    rel_image_path = os.path.relpath(page_image_path, skill_dir)
    rel_image_path = rel_image_path.replace('\\', '/')
    
    # Image markdown
    image_markdown = f'![Page {page_num}]({rel_image_path})'
    
    # Check if source section already exists
    source_pattern = r'## Source.*?(?=\n##|\Z)'
    source_match = re.search(source_pattern, content, re.DOTALL | re.IGNORECASE)
    
    if source_match:
        # Replace existing source section
        source_section = source_match.group(0)
        # Check if this page is already in the source
        if f'Page {page_num}' in source_section:
            # Update existing page reference
            # Remove old image references for this page
            page_pattern = f'(\\*\\*CB77011 - Stellar Adventures, Page {page_num}\\*\\*\\n)(.*?)(?=\\n\\*\\*|\\Z)'
            page_match = re.search(page_pattern, source_section, re.DOTALL)
            if page_match:
                # Replace with new full page image
                new_page_content = f'**CB77011 - Stellar Adventures, Page {page_num}**\n{image_markdown}\n'
                content = content.replace(page_match.group(0), new_page_content)
        else:
            # Add new page source
            new_source = source_section.rstrip() + f'\n\n**CB77011 - Stellar Adventures, Page {page_num}**\n{image_markdown}\n'
            content = content.replace(source_section, new_source)
    else:
        # Create new source section at the end
        source_section = f'\n\n## Source\n\n**CB77011 - Stellar Adventures, Page {page_num}**\n{image_markdown}\n'
        content = content.rstrip() + source_section
    
    # Remove any references to skill_images directory
    content = re.sub(r'!\[.*?\]\(.*?skill_images.*?\)\n?', '', content)
    
    # Write back
    with open(skill_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated: {skill_file}")
    return True

def main():
    """Main update process"""
    print("Updating skill sources to use full page images...")
    print("=" * 80)
    
    updated_count = 0
    
    for skill_name, page_num in SKILL_PAGE_MAP.items():
        if skill_name not in SKILL_FILE_MAP:
            print(f"Warning: No file mapping for {skill_name}")
            continue
        
        skill_file = SKILL_FILE_MAP[skill_name]
        if update_skill_source(skill_file, page_num):
            updated_count += 1
    
    print("\n" + "=" * 80)
    print(f"Update complete!")
    print(f"Updated {updated_count} markdown files")
    print(f"\nAll skills now reference full page images from {PAGES_DIR}")

if __name__ == '__main__':
    main()






