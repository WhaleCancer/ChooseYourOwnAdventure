"""
Simple extraction of marksmanship skills from Stellar Adventures
"""
import pdfplumber
import re

pdf_file = "CB77011 - stellar-adventures.pdf"

print("Searching for marksmanship skills...")

with pdfplumber.open(pdf_file) as pdf:
    total = len(pdf.pages)
    print(f"Total pages: {total}\n")
    
    all_text = []
    skills_found = []
    
    # Extract text from pages 10-100 (likely skills chapter range)
    for page_num in range(9, min(100, total)):
        page = pdf.pages[page_num]
        text = page.extract_text()
        if text:
            all_text.append((page_num + 1, text))
    
    # Search for marksmanship-related sections
    print("Searching for marksmanship/weapon skills...\n")
    
    for page_num, text in all_text:
        text_lower = text.lower()
        
        # Look for pages with marksmanship content
        if any(term in text_lower for term in ['marksmanship', 'weapon skill', 'blaster', 'pistol marksmanship', 'rifle marksmanship']):
            print(f"\n{'='*80}")
            print(f"PAGE {page_num}")
            print(f"{'='*80}\n")
            
            # Print the full page text
            print(text)
            print("\n")
            
            # Try to extract skill names
            lines = text.split('\n')
            for i, line in enumerate(lines):
                line = line.strip()
                
                # Look for patterns like "Marksmanship (Pistol)" or skill names in lists
                if re.search(r'[Mm]arksmanship|^[A-Z][a-z]+\s+(Pistol|Rifle|Carbine|Blaster)', line, re.IGNORECASE):
                    # Extract potential skill name
                    match = re.search(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', line)
                    if match:
                        skill = match.group(1)
                        if len(skill) > 2 and skill.lower() not in ['The', 'And', 'For', 'With']:
                            skills_found.append((page_num, skill, line))
    
    print(f"\n{'='*80}")
    print("SUMMARY OF POTENTIAL SKILLS:")
    print(f"{'='*80}\n")
    
    for page, skill, context in skills_found[:20]:
        print(f"Page {page}: {skill}")
        print(f"  Line: {context[:80]}...")
        print()







