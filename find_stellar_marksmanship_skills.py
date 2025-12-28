"""
Search for marksmanship/weapon skills in Stellar Adventures PDF
"""
import pdfplumber
import re

pdf_file = "CB77011 - stellar-adventures.pdf"

print("Searching for marksmanship and weapon skills in Stellar Adventures...")
print("="*80)

# Keywords to search for
weapon_keywords = [
    'marksmanship', 'blaster', 'pistol', 'rifle', 'carbine', 
    'weapon skill', 'weapon characteristic', 'firearm', 'gun',
    'energy weapon', 'laser', 'plasma'
]

with pdfplumber.open(pdf_file) as pdf:
    total = len(pdf.pages)
    print(f"Total pages: {total}\n")
    
    relevant_pages = []
    
    # Scan all pages for weapon-related content
    for i in range(total):
        page = pdf.pages[i]
        text = page.extract_text()
        if text:
            text_lower = text.lower()
            # Look for weapon/marksmanship keywords
            found_keywords = [kw for kw in weapon_keywords if kw in text_lower]
            
            if found_keywords:
                # Check if it looks like a skills section
                is_skills_section = any(term in text_lower for term in ['skill', 'characteristic', 'marksmanship', 'weapon'])
                preview = text[:300].replace('\n', ' ')
                
                relevant_pages.append({
                    'page': i + 1,
                    'is_skills': is_skills_section,
                    'keywords': found_keywords,
                    'preview': preview
                })
    
    print(f"Found {len(relevant_pages)} pages with weapon/marksmanship content:\n")
    
    for item in relevant_pages:
        skills_marker = " [SKILLS SECTION]" if item['is_skills'] else ""
        print(f"Page {item['page']:3d}{skills_marker}: {', '.join(item['keywords'])}")
        print(f"  Preview: {item['preview']}...")
        print()
    
    # Now extract text from pages that look like skills sections
    print("\n" + "="*80)
    print("EXTRACTING POTENTIAL SKILLS SECTIONS")
    print("="*80 + "\n")
    
    skills_pages = [p for p in relevant_pages if p['is_skills']]
    
    if skills_pages:
        for item in skills_pages[:10]:  # Show first 10 skills pages
            page_num = item['page'] - 1
            page = pdf.pages[page_num]
            text = page.extract_text()
            if text:
                print(f"\n{'='*80}")
                print(f"PAGE {item['page']}")
                print(f"{'='*80}\n")
                print(text[:2000])  # First 2000 chars
                if len(text) > 2000:
                    print("\n[... continues ...]")
    
    # Try to find specific marksmanship skill names
    print("\n" + "="*80)
    print("SEARCHING FOR SPECIFIC MARKSMANSHIP SKILL NAMES")
    print("="*80 + "\n")
    
    marksmanship_patterns = [
        r'[Mm]arksmanship\s+[A-Z][a-z]+',
        r'[Bb]laster\s+[Pp]istol',
        r'[Bb]laster\s+[Rr]ifle',
        r'[Cc]arbine',
        r'[Hh]eavy\s+[Bb]laster',
        r'[Ll]ight\s+[Bb]laster',
    ]
    
    for i in range(min(100, total)):  # Check first 100 pages
        page = pdf.pages[i]
        text = page.extract_text()
        if text:
            for pattern in marksmanship_patterns:
                matches = re.findall(pattern, text)
                if matches:
                    print(f"Page {i+1}: Found {matches}")
                    # Show context
                    for match in matches[:3]:  # First 3 matches
                        idx = text.find(match)
                        if idx >= 0:
                            context = text[max(0, idx-50):min(len(text), idx+200)]
                            print(f"  Context: ...{context}...")
                            print()







