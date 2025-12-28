"""
Extract skill description images from Stellar Adventures pages 0009-0012
and insert them into the corresponding skill markdown files.
"""
from PIL import Image
import os
import re

# Define skill locations on each page
# Format: (page_num, skill_name, approximate_bbox as (left, top, right, bottom) or None for full page)
# Coordinates are approximate and will need adjustment
SKILL_LOCATIONS = {
    # Page 0009 (page 8)
    'Acrobatics': ('0009', (100, 600, 300, 750)),  # Bottom right column
    'Animal Skills': ('0009', (100, 750, 300, 900)),  # Bottom right column
    
    # Page 0010 (page 9) - Left column
    'Armor': ('0010', (50, 200, 250, 300)),
    'Astronavigation': ('0010', (50, 300, 250, 400)),
    'Awareness': ('0010', (50, 400, 250, 450)),
    'Bargain': ('0010', (50, 450, 250, 550)),
    'Bureaucracy': ('0010', (50, 550, 250, 650)),
    'Brawling': ('0010', (50, 650, 250, 750)),
    'Communications': ('0010', (50, 750, 250, 850)),
    
    # Page 0010 - Right column
    'Computers': ('0010', (300, 200, 500, 350)),
    'Dodge': ('0010', (300, 400, 500, 500)),
    'Engineering': ('0010', (300, 500, 500, 600)),
    'Etiquette': ('0010', (300, 600, 500, 700)),
    'Evaluate': ('0010', (300, 700, 500, 800)),
    'Firearms - Heavy': ('0010', (300, 800, 500, 900)),
    
    # Page 0011 (page 10) - Left column
    'Firearms - Light': ('0011', (50, 200, 250, 300)),
    'Firearms - Vehicle': ('0011', (50, 300, 250, 400)),
    'Languages': ('0011', (50, 400, 250, 500)),
    'Law': ('0011', (50, 500, 250, 600)),
    'Leadership': ('0011', (50, 600, 250, 700)),
    'Medicine': ('0011', (50, 700, 250, 800)),
    'Melee Weapons': ('0011', (50, 800, 250, 900)),
    
    # Page 0011 - Right column
    'Pilot - Air': ('0011', (300, 200, 500, 300)),
    'Pilot - Ground': ('0011', (300, 300, 500, 400)),
    'Pilot - Space': ('0011', (300, 400, 500, 500)),
    'Pilot - Water': ('0011', (300, 500, 500, 600)),
    'Planetary Navigation': ('0011', (300, 600, 500, 700)),
    'Psionics': ('0011', (300, 700, 500, 800)),
    'Ride': ('0011', (300, 800, 500, 900)),
    'Science': ('0011', (300, 900, 500, 1100)),  # Longer description
    
    # Page 0012 (page 11) - Left column
    'Sensors': ('0012', (50, 200, 250, 300)),
    'Sneak': ('0012', (50, 300, 250, 400)),
    'Starship Gunnery': ('0012', (50, 400, 250, 500)),
    'Survival': ('0012', (50, 500, 250, 650)),  # Longer description
    
    # Page 0012 - Right column
    'Swim': ('0012', (300, 200, 500, 300)),
    'Thrown': ('0012', (300, 300, 500, 400)),
    'Trade Knowledge': ('0012', (300, 400, 500, 550)),
}

# Map skill names to their file paths
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
IMAGES_OUTPUT_DIR = 'CB77011_stellar-adventures_Pages/skill_images'

def create_output_dir():
    """Create output directory for skill images"""
    if not os.path.exists(IMAGES_OUTPUT_DIR):
        os.makedirs(IMAGES_OUTPUT_DIR)
        print(f"Created directory: {IMAGES_OUTPUT_DIR}")

def extract_skill_image(skill_name, page_num, bbox):
    """Extract and save a skill image from a page"""
    page_file = os.path.join(PAGES_DIR, f'page_{page_num}.png')
    
    if not os.path.exists(page_file):
        print(f"Warning: Page file not found: {page_file}")
        return None
    
    try:
        img = Image.open(page_file)
        width, height = img.size
        
        # Adjust bbox to image dimensions if needed
        left, top, right, bottom = bbox
        
        # Ensure coordinates are within image bounds
        left = max(0, min(left, width))
        top = max(0, min(top, height))
        right = max(left, min(right, width))
        bottom = max(top, min(bottom, height))
        
        # Crop the image
        cropped = img.crop((left, top, right, bottom))
        
        # Save the cropped image
        safe_name = skill_name.replace(' ', '-').replace('/', '-')
        output_file = os.path.join(IMAGES_OUTPUT_DIR, f'{safe_name}_page_{page_num}.png')
        cropped.save(output_file)
        
        print(f"Extracted: {skill_name} -> {output_file}")
        return output_file
        
    except Exception as e:
        print(f"Error extracting {skill_name} from page {page_num}: {e}")
        return None

def insert_image_into_markdown(skill_file, image_path, page_num):
    """Insert image reference into markdown file under a source heading"""
    if not os.path.exists(skill_file):
        print(f"Warning: Skill file not found: {skill_file}")
        return False
    
    # Read the file
    with open(skill_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if source section already exists
    source_pattern = r'## Source.*?(?=\n##|\Z)'
    source_match = re.search(source_pattern, content, re.DOTALL)
    
    # Create relative path for image
    rel_image_path = os.path.relpath(image_path, os.path.dirname(skill_file))
    rel_image_path = rel_image_path.replace('\\', '/')
    
    # Image markdown
    image_markdown = f'\n![{skill_file} from page {page_num}]({rel_image_path})\n'
    
    if source_match:
        # Append to existing source section
        source_section = source_match.group(0)
        if image_markdown not in source_section:
            # Add image to existing source section
            new_source = source_section.rstrip() + image_markdown
            content = content.replace(source_section, new_source)
    else:
        # Create new source section
        source_section = f'\n## Source\n\n**CB77011 - Stellar Adventures, Page {page_num}**\n{image_markdown}'
        # Insert before the last line or at the end
        content = content.rstrip() + source_section + '\n'
    
    # Write back
    with open(skill_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated: {skill_file}")
    return True

def main():
    """Main extraction process"""
    print("Extracting skill images from Stellar Adventures pages...")
    print("=" * 80)
    
    create_output_dir()
    
    # First, we need to get actual image dimensions to calculate proper bboxes
    # For now, let's use a simpler approach: extract full sections using text detection
    # or manual coordinate adjustment
    
    print("\nNote: This script uses approximate coordinates.")
    print("You may need to adjust the bbox coordinates in SKILL_LOCATIONS")
    print("based on the actual page layout.\n")
    
    extracted_count = 0
    updated_count = 0
    
    for skill_name, (page_num, bbox) in SKILL_LOCATIONS.items():
        if skill_name not in SKILL_FILE_MAP:
            print(f"Warning: No file mapping for {skill_name}")
            continue
        
        # Extract image
        image_path = extract_skill_image(skill_name, page_num, bbox)
        if image_path:
            extracted_count += 1
            
            # Insert into markdown
            skill_file = SKILL_FILE_MAP[skill_name]
            if insert_image_into_markdown(skill_file, image_path, page_num):
                updated_count += 1
    
    print("\n" + "=" * 80)
    print(f"Extraction complete!")
    print(f"Extracted {extracted_count} images")
    print(f"Updated {updated_count} markdown files")

if __name__ == '__main__':
    main()






