"""
Extract marksmanship skills from Stellar Adventures and update the skills table
"""
import pdfplumber
import re

pdf_file = "CB77011 - stellar-adventures.pdf"
skills_file = "RULES/Skills/Skills-by-Campaign-Setting.md"

print("Extracting marksmanship skills from Stellar Adventures...")
print("="*80)

marksmanship_skills = []

with pdfplumber.open(pdf_file) as pdf:
    total = len(pdf.pages)
    print(f"Total pages: {total}\n")
    
    # Search pages 10-100 for skills chapter
    for page_num in range(9, min(100, total)):
        page = pdf.pages[page_num]
        text = page.extract_text()
        
        if text:
            text_lower = text.lower()
            
            # Look for marksmanship/weapon skills section
            if any(term in text_lower for term in ['marksmanship', 'weapon skill', 'blaster', 'pistol', 'rifle', 'carbine']):
                print(f"\n{'='*80}")
                print(f"PAGE {page_num + 1}")
                print(f"{'='*80}\n")
                
                # Print full page for review
                print(text)
                print("\n")
                
                # Try to extract skill names
                lines = text.split('\n')
                
                # Look for patterns like:
                # - "Marksmanship (Pistol)"
                # - "Pistol Marksmanship"
                # - Skill names in lists/tables
                for line in lines:
                    line = line.strip()
                    
                    # Pattern 1: "Marksmanship (Weapon Type)"
                    match = re.search(r'[Mm]arksmanship\s*\(([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\)', line)
                    if match:
                        skill = match.group(1)
                        if skill not in marksmanship_skills:
                            marksmanship_skills.append(skill)
                            print(f"Found: {skill} (from pattern: Marksmanship (X))")
                    
                    # Pattern 2: "Weapon Type Marksmanship"
                    match = re.search(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+[Mm]arksmanship', line)
                    if match:
                        skill = match.group(1)
                        if skill not in marksmanship_skills:
                            marksmanship_skills.append(skill)
                            print(f"Found: {skill} (from pattern: X Marksmanship)")
                    
                    # Pattern 3: Standalone weapon skill names in context
                    if (3 < len(line) < 40 and 
                        line[0].isupper() and 
                        any(term in line.lower() for term in ['pistol', 'rifle', 'carbine', 'blaster', 'laser', 'plasma'])):
                        # Check if nearby context mentions marksmanship
                        line_idx = lines.index(line.strip())
                        context = ' '.join(lines[max(0, line_idx-3):min(len(lines), line_idx+3)]).lower()
                        if 'marksmanship' in context or 'weapon' in context:
                            # Extract just the weapon type
                            weapon_match = re.search(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', line)
                            if weapon_match:
                                skill = weapon_match.group(1)
                                if (skill.lower() not in ['the', 'and', 'for', 'with', 'skill', 'weapon'] and
                                    skill not in marksmanship_skills):
                                    marksmanship_skills.append(skill)
                                    print(f"Found: {skill} (from context)")

print(f"\n{'='*80}")
print("SUMMARY")
print(f"{'='*80}\n")
print(f"Found {len(marksmanship_skills)} marksmanship skills:")
for skill in marksmanship_skills:
    print(f"  - {skill}")

# Now update the skills file
if marksmanship_skills:
    print(f"\n{'='*80}")
    print("UPDATING SKILLS FILE")
    print(f"{'='*80}\n")
    
    with open(skills_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the Stellar Adventures Marksmanship Skills section
    # Replace the placeholder rows with actual skills
    placeholder_pattern = r'(\|\s*\*Blaster Pistol\*\s*\|[^\n]+\n)'
    
    # Build new table rows
    new_rows = []
    for skill in marksmanship_skills:
        # Create markdown link format
        skill_link = skill.replace(' ', '-')
        new_rows.append(f"| [[PHYSICAL/Missile Weapons/{skill_link}\\|{skill}]] | — | ✓ | — | — | — |")
    
    # Find and replace the placeholder section
    section_pattern = r'(\|\s*\*Blaster Pistol\*\s*\|[^\n]+\n)(\|\s*\*Blaster Rifle\*\s*\|[^\n]+\n)(\|\s*\*Carbine\*\s*\|[^\n]+\n)(\|\s*\*Heavy Blaster\*\s*\|[^\n]+\n)'
    
    if re.search(section_pattern, content):
        replacement = '\n'.join(new_rows) + '\n'
        content = re.sub(section_pattern, replacement, content)
        
        # Also update the note
        note_pattern = r'\*\*Note:\*\* The marksmanship skill names above are placeholders.*?Run `extract_stellar_skills_to_file\.py` to extract the skills chapter text for review\.'
        new_note = f"**Note:** The following marksmanship skills are from the Stellar Adventures sourcebook."
        content = re.sub(note_pattern, new_note, content)
        
        with open(skills_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated {skills_file} with {len(marksmanship_skills)} marksmanship skills!")
    else:
        print("Could not find placeholder section to replace.")
        print("Please manually update the skills file with the following skills:")
        for skill in marksmanship_skills:
            print(f"  - {skill}")
else:
    print("\nNo marksmanship skills found. The extraction may need manual review.")
    print("Check the page output above to identify the correct skill names.")







