"""
Add AFF (Advanced Fighting Fantasy) source images to skills that reference Heroes Companion.
For skills that already have Stellar Adventures sources, this will add AFF sources as well,
distinguishing between the two sources.
"""
import os
import re

# Map skills to their AFF Heroes Companion pages
# Format: skill_file_path: (page_number, description)
# Note: These are approximate - you may need to adjust based on actual page content
# Chapter 1 of Heroes Companion typically starts around page 1-2
AFF_SKILL_PAGE_MAP = {
    # Skills from Heroes Companion Chapter 1
    'RULES/Skills/PHYSICAL/Battle-Tactics.md': ('0001', 'Chapter 1'),
    'RULES/Skills/PHYSICAL/Siege-Weapons.md': ('0001', 'Chapter 1'),
    'RULES/Skills/MENTAL/Navigation.md': ('0001', 'Chapter 1'),
    'RULES/Skills/MENTAL/Stewardship.md': ('0001', 'Chapter 1'),
    # Engineering appears in both Stellar Adventures and Heroes Companion
    # We'll add AFF source but keep Stellar Adventures source too
    'RULES/Skills/MENTAL/Engineering.md': ('0001', 'Chapter 1'),
    
    # Add more mappings as needed
}

# Alternative: Map by skill name pattern
AFF_SKILL_PATTERNS = {
    r'Battle.*Tactics': ('0001', 'Heroes Companion Chapter 1'),
    r'Siege.*Weapons': ('0001', 'Heroes Companion Chapter 1'),
    r'Engineering': ('0001', 'Heroes Companion Chapter 1'),  # Note: This overlaps with Stellar Adventures
    r'Navigation': ('0001', 'Heroes Companion Chapter 1'),  # Note: Different from Planetary Navigation
    r'Stewardship': ('0001', 'Heroes Companion Chapter 1'),
}

AFF_PAGES_DIR = 'AFF005_Heroes_Companion_Pages'
AFF_BOOK_TITLE = 'AFF005 - Heroes Companion'

def find_skills_with_aff_source():
    """Find all skill files that mention Heroes Companion or AFF"""
    aff_skills = []
    skills_dir = 'RULES/Skills'
    
    # Normalize paths for comparison
    normalized_map = {}
    for key, value in AFF_SKILL_PAGE_MAP.items():
        normalized_key = key.replace('\\', '/')
        normalized_map[normalized_key] = value
    
    for root, dirs, files in os.walk(skills_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                normalized_path = file_path.replace('\\', '/')
                
                # Check if in explicit mapping
                if normalized_path in normalized_map:
                    aff_skills.append((file_path, normalized_map[normalized_path]))
                    continue
                
                # Otherwise check content
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Check if it mentions Heroes Companion or AFF
                        if re.search(r'Heroes Companion|AFF|Advanced Fighting Fantasy', content, re.IGNORECASE):
                            # Try to get page info
                            page_info = get_aff_page_for_skill(file_path)
                            if page_info:
                                aff_skills.append((file_path, page_info))
                            else:
                                # Default to page 1 if we can't determine
                                aff_skills.append((file_path, ('0001', 'Chapter 1')))
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    return aff_skills

def get_aff_page_for_skill(skill_file):
    """Determine which AFF page a skill comes from"""
    # First check exact mapping
    if skill_file in AFF_SKILL_PAGE_MAP:
        return AFF_SKILL_PAGE_MAP[skill_file]
    
    # Then check pattern matching
    skill_name = os.path.basename(skill_file).replace('.md', '')
    for pattern, (page, desc) in AFF_SKILL_PATTERNS.items():
        if re.search(pattern, skill_name, re.IGNORECASE):
            return (page, desc)
    
    # Default: try to extract from file content
    try:
        with open(skill_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for page references in the content
            page_match = re.search(r'page[_\s]*(\d+)', content, re.IGNORECASE)
            if page_match:
                return (page_match.group(1).zfill(4), 'Heroes Companion')
    except:
        pass
    
    return None

def add_aff_source_to_skill(skill_file, page_num, description):
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
        
        # Check if AFF source already exists
        if AFF_BOOK_TITLE in source_section and f'Page {page_num}' in source_section:
            print(f"  AFF source already exists for {skill_file}")
            return True
        
        # Add AFF source with clear distinction
        # Add a separator if there are multiple sources
        if 'CB77011' in source_section or 'Stellar Adventures' in source_section:
            # Add separator and AFF source
            new_source = source_section.rstrip() + f'\n\n---\n\n**{AFF_BOOK_TITLE}, {description}, Page {page_num}**\n{image_markdown}\n'
        else:
            # Just add AFF source
            new_source = source_section.rstrip() + f'\n\n**{AFF_BOOK_TITLE}, {description}, Page {page_num}**\n{image_markdown}\n'
        
        content = content.replace(source_section, new_source)
    else:
        # Create new source section
        source_section = f'\n\n## Source\n\n**{AFF_BOOK_TITLE}, {description}, Page {page_num}**\n{image_markdown}\n'
        content = content.rstrip() + source_section
    
    # Write back
    with open(skill_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated: {skill_file} with AFF source")
    return True

def main():
    """Main process to add AFF sources"""
    print("Finding skills with AFF/Heroes Companion sources...")
    print("=" * 80)
    
    aff_skills = find_skills_with_aff_source()
    print(f"Found {len(aff_skills)} skills with AFF references")
    
    updated_count = 0
    skipped_count = 0
    
    for skill_file, page_info in aff_skills:
        page_num, description = page_info
        if add_aff_source_to_skill(skill_file, page_num, description):
            updated_count += 1
        else:
            skipped_count += 1
    
    print("\n" + "=" * 80)
    print(f"Update complete!")
    print(f"Updated {updated_count} skill files")
    print(f"Skipped {skipped_count} skill files")
    print(f"\nNote: You may need to manually verify and adjust page numbers")
    print(f"based on the actual content in the AFF Heroes Companion pages.")

if __name__ == '__main__':
    main()






