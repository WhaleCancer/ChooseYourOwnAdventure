"""
Add AFF Heroes Companion page sources to skills based on actual page content.
"""
import os
import re

# Map skills to their AFF Heroes Companion pages based on actual page content
# Format: skill_file_path: page_number
AFF_SKILL_PAGE_MAP = {
    # Page 0010 (page 9) - Full descriptions
    'RULES/Skills/MENTAL/Engineering.md': '0010',
    'RULES/Skills/MENTAL/Navigation.md': '0010',
    'RULES/Skills/MENTAL/Stewardship.md': '0010',
    'RULES/Skills/PHYSICAL/Battle-Tactics.md': '0010',
    'RULES/Skills/PHYSICAL/Siege-Weapons.md': '0010',
    'RULES/Skills/MENTAL/Magic-Mask-Magic.md': '0010',
    'RULES/Skills/MENTAL/Magic-Conjuration.md': '0010',
    
    # Page 0011 (page 10) - Full descriptions
    'RULES/Skills/MENTAL/Magic-Necromancy.md': '0011',
    'RULES/Skills/MENTAL/Magic-Tattooing.md': '0011',
    'RULES/Skills/MENTAL/Magic-Battle-Magic.md': '0011',
    'RULES/Skills/MENTAL/Magic-Enchanting.md': '0011',
    'RULES/Skills/MENTAL/Magic-Chaos-Magic.md': '0011',
    
    # Page 0012 (page 11) - Full descriptions
    # Note: Talents are in Talents folder, not Skills folder
    # But we'll check if any skill files reference these
    
    # Page 0012 also lists the skills, so we can add it as a secondary source
    # for skills that have full descriptions on page 0010
}

AFF_PAGES_DIR = 'AFF005_Heroes_Companion_Pages'
AFF_BOOK_TITLE = 'AFF005 - Heroes Companion'

def add_aff_source_to_skill(skill_file, page_num):
    """Add AFF source image to a skill file"""
    if not os.path.exists(skill_file):
        print(f"Warning: Skill file not found: {skill_file}")
        return False
    
    # Check if AFF page exists
    aff_page_path = os.path.join(AFF_PAGES_DIR, f'page_{page_num}.png')
    if not os.path.exists(aff_page_path):
        print(f"Warning: AFF page not found: {aff_page_path}")
        return False
    
    # Read the file
    with open(skill_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create relative path for AFF page image
    skill_dir = os.path.dirname(skill_file)
    rel_image_path = os.path.relpath(aff_page_path, skill_dir)
    rel_image_path = rel_image_path.replace('\\', '/')
    
    # Image markdown
    image_markdown = f'![Page {page_num}]({rel_image_path})'
    
    # Check if source section already exists
    source_pattern = r'## Source.*?(?=\n##|\Z)'
    source_match = re.search(source_pattern, content, re.DOTALL | re.IGNORECASE)
    
    if source_match:
        # Append to existing source section
        source_section = source_match.group(0)
        
        # Check if AFF source already exists for this page
        if AFF_BOOK_TITLE in source_section and f'Page {page_num}' in source_section:
            print(f"  AFF source already exists for {skill_file} (page {page_num})")
            return True
        
        # Add AFF source with clear distinction
        # Add a separator if there are Stellar Adventures sources
        if 'CB77011' in source_section or 'Stellar Adventures' in source_section:
            # Add separator and AFF source
            new_source = source_section.rstrip() + f'\n\n---\n\n**{AFF_BOOK_TITLE}, Page {page_num}**\n{image_markdown}\n'
        else:
            # Just add AFF source
            new_source = source_section.rstrip() + f'\n\n**{AFF_BOOK_TITLE}, Page {page_num}**\n{image_markdown}\n'
        
        content = content.replace(source_section, new_source)
    else:
        # Create new source section
        source_section = f'\n\n## Source\n\n**{AFF_BOOK_TITLE}, Page {page_num}**\n{image_markdown}\n'
        content = content.rstrip() + source_section
    
    # Write back
    with open(skill_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated: {skill_file} with AFF source (page {page_num})")
    return True

def main():
    """Main process to add AFF sources"""
    print("Adding AFF Heroes Companion page sources to skills...")
    print("=" * 80)
    
    updated_count = 0
    skipped_count = 0
    
    for skill_file, page_num in AFF_SKILL_PAGE_MAP.items():
        if add_aff_source_to_skill(skill_file, page_num):
            updated_count += 1
        else:
            skipped_count += 1
    
    print("\n" + "=" * 80)
    print(f"Update complete!")
    print(f"Updated {updated_count} skill files")
    print(f"Skipped {skipped_count} skill files")

if __name__ == '__main__':
    main()






