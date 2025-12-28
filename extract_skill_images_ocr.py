"""
Extract skill description images from Stellar Adventures pages 0009-0012
using OCR to locate skill text, then crop and insert into markdown files.
"""
from PIL import Image, ImageDraw, ImageFont
import os
import re

# Try to import pytesseract, but make it optional
try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("Warning: pytesseract not available. Using manual coordinate method.")

# Define skill locations with approximate regions
# Format: (page_num, approximate_y_position, approximate_height)
# Scaled for 1224x1584 images
SKILL_REGIONS = {
    # Page 0009 (page 8) - Right column bottom
    'Acrobatics': ('0009', 900, 200),
    'Animal Skills': ('0009', 1100, 200),
    
    # Page 0010 (page 9) - Left column
    'Armor': ('0010', 300, 150),
    'Astronavigation': ('0010', 450, 150),
    'Awareness': ('0010', 600, 100),
    'Bargain': ('0010', 700, 150),
    'Bureaucracy': ('0010', 850, 150),
    'Brawling': ('0010', 1000, 150),
    'Communications': ('0010', 1150, 150),
    
    # Page 0010 - Right column
    'Computers': ('0010', 300, 200),
    'Dodge': ('0010', 600, 150),
    'Engineering': ('0010', 750, 150),
    'Etiquette': ('0010', 900, 150),
    'Evaluate': ('0010', 1050, 150),
    'Firearms - Heavy': ('0010', 1200, 150),
    
    # Page 0011 (page 10) - Left column
    'Firearms - Light': ('0011', 300, 150),
    'Firearms - Vehicle': ('0011', 450, 150),
    'Languages': ('0011', 600, 150),
    'Law': ('0011', 750, 150),
    'Leadership': ('0011', 900, 150),
    'Medicine': ('0011', 1050, 150),
    'Melee Weapons': ('0011', 1200, 150),
    
    # Page 0011 - Right column
    'Pilot - Air': ('0011', 300, 150),
    'Pilot - Ground': ('0011', 450, 150),
    'Pilot - Space': ('0011', 600, 150),
    'Pilot - Water': ('0011', 750, 150),
    'Planetary Navigation': ('0011', 900, 150),
    'Psionics': ('0011', 1050, 150),
    'Ride': ('0011', 1200, 150),
    'Science': ('0011', 1350, 250),  # Longer
    
    # Page 0012 (page 11) - Left column
    'Sensors': ('0012', 300, 150),
    'Sneak': ('0012', 450, 150),
    'Starship Gunnery': ('0012', 600, 150),
    'Survival': ('0012', 750, 200),  # Longer
    
    # Page 0012 - Right column
    'Swim': ('0012', 300, 150),
    'Thrown': ('0012', 450, 150),
    'Trade Knowledge': ('0012', 600, 200),
}

# Column positions (approximate) - scaled for 1224x1584 images
# Actual page is 1224x1584, so we need to scale coordinates
LEFT_COLUMN_LEFT = 100
LEFT_COLUMN_RIGHT = 550
RIGHT_COLUMN_LEFT = 650
RIGHT_COLUMN_RIGHT = 1100

# Skills in left vs right column
LEFT_COLUMN_SKILLS = {
    'Armor', 'Astronavigation', 'Awareness', 'Bargain', 'Bureaucracy', 
    'Brawling', 'Communications', 'Firearms - Light', 'Firearms - Vehicle',
    'Languages', 'Law', 'Leadership', 'Medicine', 'Melee Weapons',
    'Sensors', 'Sneak', 'Starship Gunnery', 'Survival'
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
IMAGES_OUTPUT_DIR = 'CB77011_stellar-adventures_Pages/skill_images'

def create_output_dir():
    """Create output directory for skill images"""
    if not os.path.exists(IMAGES_OUTPUT_DIR):
        os.makedirs(IMAGES_OUTPUT_DIR)
        print(f"Created directory: {IMAGES_OUTPUT_DIR}")

def get_column_bounds(skill_name):
    """Determine which column a skill is in"""
    if skill_name in LEFT_COLUMN_SKILLS or skill_name in ['Acrobatics', 'Animal Skills']:
        # Special case: Acrobatics and Animal Skills are in right column on page 0009
        if skill_name in ['Acrobatics', 'Animal Skills']:
            return RIGHT_COLUMN_LEFT, RIGHT_COLUMN_RIGHT
        return LEFT_COLUMN_LEFT, LEFT_COLUMN_RIGHT
    else:
        return RIGHT_COLUMN_LEFT, RIGHT_COLUMN_RIGHT

def extract_skill_image(skill_name, page_num, y_pos, height):
    """Extract and save a skill image from a page"""
    page_file = os.path.join(PAGES_DIR, f'page_{page_num}.png')
    
    if not os.path.exists(page_file):
        print(f"Warning: Page file not found: {page_file}")
        return None
    
    try:
        img = Image.open(page_file)
        width, img_height = img.size
        
        # Get column bounds
        left, right = get_column_bounds(skill_name)
        
        # Add some padding (scaled for larger images)
        padding = 30
        left = max(0, left - padding)
        right = min(width, right + padding)
        top = max(0, y_pos - padding)
        bottom = min(img_height, y_pos + height + padding)
        
        # Crop the image
        cropped = img.crop((left, top, right, bottom))
        
        # Save the cropped image
        safe_name = skill_name.replace(' ', '-').replace('/', '-').replace(' - ', '-')
        output_file = os.path.join(IMAGES_OUTPUT_DIR, f'{safe_name}_page_{page_num}.png')
        cropped.save(output_file)
        
        print(f"Extracted: {skill_name} -> {output_file}")
        return output_file
        
    except Exception as e:
        print(f"Error extracting {skill_name} from page {page_num}: {e}")
        import traceback
        traceback.print_exc()
        return None

def insert_image_into_markdown(skill_file, image_path, page_num):
    """Insert image reference into markdown file under a source heading"""
    if not os.path.exists(skill_file):
        print(f"Warning: Skill file not found: {skill_file}")
        return False
    
    # Read the file
    with open(skill_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create relative path for image
    skill_dir = os.path.dirname(skill_file)
    rel_image_path = os.path.relpath(image_path, skill_dir)
    rel_image_path = rel_image_path.replace('\\', '/')
    
    # Image markdown
    image_markdown = f'![{os.path.basename(skill_file)} from page {page_num}]({rel_image_path})'
    
    # Check if source section already exists
    source_pattern = r'## Source.*?(?=\n##|\Z)'
    source_match = re.search(source_pattern, content, re.DOTALL | re.IGNORECASE)
    
    if source_match:
        # Append to existing source section
        source_section = source_match.group(0)
        if image_markdown not in source_section:
            # Check if this page is already mentioned
            if f'Page {page_num}' not in source_section:
                # Add new page source
                new_source = source_section.rstrip() + f'\n\n**CB77011 - Stellar Adventures, Page {page_num}**\n{image_markdown}\n'
                content = content.replace(source_section, new_source)
            else:
                # Add image to existing page source
                page_pattern = f'(Page {page_num}[^\\n]*\\n)(.*?)(?=\\n\\*\\*|\\Z)'
                page_match = re.search(page_pattern, source_section, re.DOTALL)
                if page_match:
                    page_header = page_match.group(1)
                    existing_content = page_match.group(2)
                    if image_markdown not in existing_content:
                        new_page_content = page_header + existing_content + '\n' + image_markdown + '\n'
                        content = content.replace(page_match.group(0), new_page_content)
    else:
        # Create new source section at the end
        source_section = f'\n\n## Source\n\n**CB77011 - Stellar Adventures, Page {page_num}**\n{image_markdown}\n'
        content = content.rstrip() + source_section
    
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
    
    print("\nNote: Using approximate coordinates based on typical page layout.")
    print("You may need to manually adjust coordinates if crops are incorrect.\n")
    
    extracted_count = 0
    updated_count = 0
    
    for skill_name, (page_num, y_pos, height) in SKILL_REGIONS.items():
        if skill_name not in SKILL_FILE_MAP:
            print(f"Warning: No file mapping for {skill_name}")
            continue
        
        # Extract image
        image_path = extract_skill_image(skill_name, page_num, y_pos, height)
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
    print(f"\nImages saved to: {IMAGES_OUTPUT_DIR}")
    print("\nPlease review the extracted images and adjust coordinates if needed.")

if __name__ == '__main__':
    main()






