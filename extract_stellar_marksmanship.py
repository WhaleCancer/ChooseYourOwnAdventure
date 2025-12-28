"""
Extract marksmanship skills from Stellar Adventures PDF
Converts pages to images first, then extracts text
"""
import pdfplumber
from pdf2image import convert_from_path
import pytesseract
import os
import re

pdf_file = "CB77011 - stellar-adventures.pdf"
output_file = "stellar_marksmanship_skills.txt"

print("Extracting marksmanship skills from Stellar Adventures...")
print("="*80)

# First, try direct text extraction with pdfplumber
print("\nAttempting direct text extraction...")
marksmanship_skills = []

with pdfplumber.open(pdf_file) as pdf:
    total = len(pdf.pages)
    print(f"Total pages: {total}\n")
    
    # Search for pages with marksmanship/weapon skills
    for page_num in range(total):
        page = pdf.pages[page_num]
        text = page.extract_text()
        
        if text:
            text_lower = text.lower()
            
            # Look for marksmanship-related content
            if any(term in text_lower for term in ['marksmanship', 'weapon skill', 'blaster', 'pistol', 'rifle', 'carbine']):
                # Look for skill patterns
                # Pattern: "Marksmanship (Pistol)" or "Pistol Marksmanship" or just skill names in lists
                patterns = [
                    r'[Mm]arksmanship\s*\(?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\)?',
                    r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+[Mm]arksmanship',
                    r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*$',  # Standalone skill names
                ]
                
                lines = text.split('\n')
                for line in lines:
                    line = line.strip()
                    
                    # Look for marksmanship skill patterns
                    for pattern in patterns:
                        matches = re.findall(pattern, line)
                        if matches:
                            for match in matches:
                                if isinstance(match, tuple):
                                    match = ' '.join(match)
                                
                                # Filter out common false positives
                                if (len(match) > 2 and 
                                    match.lower() not in ['the', 'and', 'for', 'with', 'skill', 'weapon', 'marksmanship', 'characteristic', 'physical'] and
                                    any(term in line.lower() for term in ['marksmanship', 'weapon', 'blaster', 'pistol', 'rifle', 'carbine', 'skill'])):
                                    marksmanship_skills.append((page_num + 1, match, line))
                
                # Also look for structured skill lists (common in RPG books)
                # Look for lines that might be skill names in a table or list
                for i, line in enumerate(lines):
                    line = line.strip()
                    # Check if line looks like a skill name and is near marksmanship/weapon terms
                    if (3 < len(line) < 40 and 
                        line[0].isupper() and 
                        not line.endswith('.') and
                        not ':' in line):
                        # Check context (lines before/after)
                        context = ' '.join(lines[max(0, i-2):min(len(lines), i+3)]).lower()
                        if any(term in context for term in ['marksmanship', 'weapon', 'blaster', 'skill', 'characteristic']):
                            # Check if it's a weapon-related term
                            weapon_terms = ['pistol', 'rifle', 'carbine', 'blaster', 'laser', 'plasma', 'gun', 'weapon']
                            if any(term in line.lower() for term in weapon_terms):
                                marksmanship_skills.append((page_num + 1, line, context[:100]))

# Remove duplicates and sort
unique_skills = {}
for page, skill, context in marksmanship_skills:
    skill_clean = skill.strip()
    if skill_clean and skill_clean not in unique_skills:
        unique_skills[skill_clean] = (page, context)

# Write results
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("STELLAR ADVENTURES MARKSMANSHIP SKILLS\n")
    f.write("="*80 + "\n\n")
    
    if unique_skills:
        f.write(f"Found {len(unique_skills)} potential marksmanship skills:\n\n")
        for skill, (page, context) in sorted(unique_skills.items()):
            f.write(f"Page {page}: {skill}\n")
            f.write(f"  Context: {context[:150]}...\n\n")
    else:
        f.write("No marksmanship skills found with direct extraction.\n")
        f.write("Trying image-based extraction...\n\n")

print(f"\nDirect extraction complete. Found {len(unique_skills)} potential skills.")
print(f"Results saved to {output_file}")

# If direct extraction didn't work well, try image-based OCR
if len(unique_skills) < 3:
    print("\nAttempting image-based extraction (this may take a while)...")
    try:
        # Convert PDF pages to images (pages 15-80, likely skills chapter range)
        images = convert_from_path(pdf_file, first_page=15, last_page=min(80, total), dpi=200)
        
        ocr_skills = []
        for i, image in enumerate(images):
            page_num = 15 + i
            print(f"Processing page {page_num} as image...")
            
            # Use OCR to extract text
            ocr_text = pytesseract.image_to_string(image)
            
            if ocr_text:
                # Look for marksmanship skills in OCR text
                lines = ocr_text.split('\n')
                for line in lines:
                    line = line.strip()
                    if any(term in line.lower() for term in ['marksmanship', 'pistol', 'rifle', 'carbine', 'blaster']):
                        # Extract potential skill names
                        matches = re.findall(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', line)
                        for match in matches:
                            if len(match) > 3 and any(term in match.lower() for term in ['pistol', 'rifle', 'carbine', 'blaster', 'laser']):
                                ocr_skills.append((page_num, match))
        
        if ocr_skills:
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write("\n\nOCR-BASED EXTRACTION:\n")
                f.write("="*80 + "\n\n")
                for page, skill in ocr_skills:
                    f.write(f"Page {page}: {skill}\n")
            
            print(f"OCR extraction found {len(ocr_skills)} additional potential skills.")
    
    except Exception as e:
        print(f"Image-based extraction failed: {e}")
        print("Make sure pdf2image and pytesseract are installed:")
        print("  pip install pdf2image pytesseract")
        print("Also install poppler and tesseract OCR on your system.")

print(f"\nComplete! Check {output_file} for results.")







