"""
Extract and adapt the Psionics chapter from Stellar Adventures
UPDATE PAGE NUMBERS after examining the book
"""
import pdfplumber
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_file = "CB77011 - stellar-adventures.pdf"
pages_dir = "stellar-adventures_Pages"
output_dir = "RULES/Stellar-Adventures"

# UPDATE THESE after examining the page images
PSIONICS_START_PAGE = 60  # Change this
PSIONICS_END_PAGE = 90    # Change this

def clean_text(text):
    """Clean extracted text"""
    if not text:
        return ""
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    text = text.replace('\x0c', '')
    return text.strip()

def adapt_text_for_epic(text):
    """Adapt Stellar Adventures text for EPIC setting"""
    # Replace "Hero" with "Character" 
    text = re.sub(r'\bHero\b', 'Character', text)
    text = re.sub(r'\bHeroes\b', 'Characters', text)
    
    # Replace "Director" references if needed (EPIC uses "Director" too, so this might be fine)
    # Add other adaptations as needed
    
    return text

def create_psionics_article():
    """Create the adapted psionics article"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"Extracting psionics chapter from pages {PSIONICS_START_PAGE}-{PSIONICS_END_PAGE}...")
    
    text_parts = []
    with pdfplumber.open(pdf_file) as pdf:
        total_pages = len(pdf.pages)
        print(f"Total pages in PDF: {total_pages}")
        
        end_page = min(PSIONICS_END_PAGE, total_pages)
        
        for page_num in range(PSIONICS_START_PAGE - 1, end_page):
            if page_num >= len(pdf.pages):
                break
            page = pdf.pages[page_num]
            text = page.extract_text()
            if text:
                cleaned = clean_text(text)
                adapted = adapt_text_for_epic(cleaned)
                text_parts.append(f"### Page {page_num + 1}\n\n{adapted}")
    
    extracted_text = '\n\n'.join(text_parts)
    
    # Generate image references
    image_refs = []
    for page_num in range(PSIONICS_START_PAGE, min(PSIONICS_END_PAGE + 1, total_pages + 1)):
        page_str = f"{page_num:04d}"
        image_path = f"../../{pages_dir}/page_{page_str}.png"
        image_refs.append(f"![Page {page_num}]({image_path})")
    
    # Create markdown content
    content = f"""# Psionics (Stellar Adventures)

**Source:** CB77011 - Stellar Adventures  
**Pages:** {PSIONICS_START_PAGE}-{PSIONICS_END_PAGE}

This chapter covers psionic abilities and rules from the Stellar Adventures sourcebook, adapted for use in EPIC campaigns.

## Content

{extracted_text}

---

## Page Images

{chr(10).join(image_refs)}

"""
    
    filepath = os.path.join(output_dir, "Psionics-Stellar-Adventures.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\nCreated: {filepath}")
    return filepath

if __name__ == "__main__":
    if not os.path.exists(pdf_file):
        print(f"Error: PDF file not found: {pdf_file}")
        sys.exit(1)
    
    print("="*60)
    print("STELLAR ADVENTURES PSIONICS EXTRACTION")
    print("="*60)
    print(f"\nCurrent page range: {PSIONICS_START_PAGE}-{PSIONICS_END_PAGE}")
    print("If this is incorrect, update PSIONICS_START_PAGE and PSIONICS_END_PAGE in this script.")
    print("\nExtracting and adapting...")
    
    create_psionics_article()
    print("\nDone! Review the created file and adjust page numbers if needed.")
