"""
Extract weapon/marksmanship skills from Stellar Adventures
"""
import pdfplumber
import re

pdf_file = "CB77011 - stellar-adventures.pdf"

print("Extracting weapon skills from Stellar Adventures...")
print("="*80)

# Common page ranges for skills/weapons chapters in RPG books
# We'll check multiple potential ranges
potential_ranges = [
    (1, 50),    # Early chapters
    (50, 100),  # Mid chapters
    (100, 150), # Later chapters
]

all_weapon_skills = set()

with pdfplumber.open(pdf_file) as pdf:
    total = len(pdf.pages)
    print(f"Total pages: {total}\n")
    
    # Look for patterns that indicate weapon skills
    # Common patterns: "Marksmanship (Pistol)", "Blaster Pistol", "Weapon Skill: X", etc.
    skill_patterns = [
        r'[Mm]arksmanship\s+\(?([A-Z][a-z]+)\)?',
        r'([A-Z][a-z]+)\s+[Mm]arksmanship',
        r'[Bb]laster\s+([A-Z][a-z]+)',
        r'([A-Z][a-z]+)\s+[Bb]laster',
        r'[Ww]eapon\s+[Ss]kill[:\s]+([A-Z][a-z]+)',
        r'([A-Z][a-z]+)\s+[Ww]eapon',
    ]
    
    # Also look for skill lists or tables
    for start, end in potential_ranges:
        print(f"\nChecking pages {start}-{end}...")
        for page_num in range(start - 1, min(end, total)):
            page = pdf.pages[page_num]
            text = page.extract_text()
            if text:
                # Look for skill patterns
                for pattern in skill_patterns:
                    matches = re.findall(pattern, text)
                    if matches:
                        for match in matches:
                            if len(match) > 2 and match.lower() not in ['the', 'and', 'for', 'with', 'skill', 'weapon']:
                                all_weapon_skills.add(match)
                
                # Look for lines that might be skill names (short lines, capitalized)
                lines = text.split('\n')
                for line in lines:
                    line = line.strip()
                    # Look for short capitalized words that might be skill names
                    if 3 < len(line) < 30 and line[0].isupper():
                        # Check if it's near weapon-related terms
                        if any(term in text[max(0, text.find(line)-100):text.find(line)+100].lower() 
                               for term in ['weapon', 'marksmanship', 'blaster', 'skill', 'characteristic']):
                            all_weapon_skills.add(line.split()[0] if ' ' in line else line)
    
    print(f"\n{'='*80}")
    print("POTENTIAL WEAPON SKILLS FOUND:")
    print(f"{'='*80}\n")
    
    # Filter and display
    filtered_skills = sorted([s for s in all_weapon_skills if len(s) > 2])
    for skill in filtered_skills[:20]:  # Show first 20
        print(f"  - {skill}")
    
    # Also try to find a skills chapter by looking for chapter headers
    print(f"\n{'='*80}")
    print("LOOKING FOR SKILLS/WEAPONS CHAPTER")
    print(f"{'='*80}\n")
    
    for page_num in range(min(100, total)):
        page = pdf.pages[page_num]
        text = page.extract_text()
        if text:
            text_lower = text.lower()
            # Look for chapter headers with weapon/skill keywords
            if (('chapter' in text_lower or 'section' in text_lower) and 
                any(term in text_lower for term in ['weapon', 'skill', 'marksmanship', 'combat', 'equipment'])):
                print(f"\nPage {page_num + 1} - Potential Skills/Weapons Chapter:")
                print(text[:500])
                print("\n" + "-"*80)







