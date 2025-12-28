"""
Extract text from specific page ranges of Stellar Adventures to identify sections
"""
import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_file = "CB77011 - stellar-adventures.pdf"

def extract_page_range(start, end):
    """Extract and display text from a page range"""
    print(f"\n{'='*80}")
    print(f"PAGES {start}-{end}")
    print(f"{'='*80}\n")
    
    with pdfplumber.open(pdf_file) as pdf:
        for page_num in range(start - 1, min(end, len(pdf.pages))):
            page = pdf.pages[page_num]
            text = page.extract_text()
            if text:
                print(f"\n--- PAGE {page_num + 1} ---\n")
                print(text[:1000])  # First 1000 chars
                if len(text) > 1000:
                    print("\n[... text continues ...]")

# Extract first 15 pages to identify structure
print("EXTRACTING FIRST 15 PAGES TO IDENTIFY STRUCTURE")
extract_page_range(1, 15)
