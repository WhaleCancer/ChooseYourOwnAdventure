"""
Extract and process the Psionics chapter from Stellar Adventures
"""
import pdfplumber
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_file = "CB77011 - stellar-adventures.pdf"
pages_dir = "stellar-adventures_Pages"

def clean_text(text):
    """Clean and format extracted text"""
    if not text:
        return ""
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    text = text.replace('\x0c', '')
    return text.strip()

def find_psionics_chapter(pdf_path):
    """Find the psionics chapter by scanning for keywords"""
    print("Scanning for Psionics chapter...")
    psionics_pages = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            text = page.extract_text()
            if text:
                text_lower = text.lower()
                # Look for psionics-related keywords
                if any(keyword in text_lower for keyword in ['psionic', 'psionics', 'psychic', 'mental power']):
                    # Check if it's a chapter header
                    if re.search(r'chapter\s+\d+.*psionic', text_lower) or \
                       re.search(r'psionic.*chapter', text_lower) or \
                       ('psionic' in text_lower and len(text) < 500):  # Likely a header
                        print(f"Found potential Psionics chapter marker on page {page_num + 1}")
                        psionics_pages.append((page_num + 1, text[:300]))
    
    return psionics_pages

def extract_chapter(pdf_path, start_page, end_page):
    """Extract text from a chapter"""
    text_parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num in range(start_page - 1, min(end_page, len(pdf.pages))):
            page = pdf.pages[page_num]
            text = page.extract_text()
            if text:
                text_parts.append(f"### Page {page_num + 1}\n\n{clean_text(text)}")
    return '\n\n'.join(text_parts)

def create_psionics_article(pdf_path, start_page, end_page, output_dir):
    """Create the adapted psionics article"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Extract text
    print(f"Extracting pages {start_page}-{end_page}...")
    extracted_text = extract_chapter(pdf_path, start_page, end_page)
    
    # Generate image references
    image_refs = []
    for page_num in range(start_page, end_page + 1):
        page_str = f"{page_num:04d}"
        image_path = f"../../{pages_dir}/page_{page_str}.png"
        image_refs.append(f"![Page {page_num}]({image_path})")
    
    # Create markdown
    content = f"""# Psionics (Stellar Adventures)

**Source:** CB77011 - Stellar Adventures  
**Pages:** {start_page}-{end_page}

This chapter covers psionic abilities and rules for the Stellar Adventures setting.

## Content

{extracted_text}

---

## Page Images

{chr(10).join(image_refs)}

"""
    
    filepath = os.path.join(output_dir, "Psionics-Stellar-Adventures.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath

# First, scan to find the chapter
print("="*60)
print("FINDING PSIONICS CHAPTER")
print("="*60)
psionics_markers = find_psionics_chapter(pdf_file)

if psionics_markers:
    print(f"\nFound {len(psionics_markers)} potential markers:")
    for page_num, preview in psionics_markers:
        print(f"  Page {page_num}: {preview[:100]}...")
    print("\nPlease review the page images to identify the exact chapter boundaries.")
    print("Then update this script with the correct start and end pages.")
else:
    print("\nNo psionics chapter markers found automatically.")
    print("Please examine the page images manually to find the chapter.")

# For now, let's try a common range - update this after examining pages
# Typical RPG books have psionics around pages 30-50 or 60-80
print("\n" + "="*60)
print("EXTRACTING SAMPLE RANGES")
print("="*60)

# Try extracting a few potential ranges to help identify
potential_ranges = [(30, 50), (50, 70), (70, 90), (90, 110)]
for start, end in potential_ranges:
    print(f"\nChecking pages {start}-{end}...")
    with pdfplumber.open(pdf_file) as pdf:
        if end <= len(pdf.pages):
            # Check a few pages in this range
            for page_num in range(start - 1, min(start + 2, end, len(pdf.pages))):
                page = pdf.pages[page_num]
                text = page.extract_text()
                if text:
                    text_lower = text.lower()
                    if 'psionic' in text_lower or 'psychic' in text_lower:
                        print(f"  Page {page_num + 1} contains psionics content:")
                        print(f"    {text[:200]}...")
