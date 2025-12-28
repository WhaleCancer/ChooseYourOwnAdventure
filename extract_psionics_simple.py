"""
Simple extraction of psionics chapter - update page numbers as needed
"""
import pdfplumber
import os

pdf_file = "CB77011 - stellar-adventures.pdf"
output_file = "stellar_psionics_raw.txt"

# UPDATE THESE PAGE NUMBERS after examining the book
PSIONICS_START = 60  # Update this
PSIONICS_END = 90    # Update this

print(f"Extracting pages {PSIONICS_START}-{PSIONICS_END} from {pdf_file}...")

with open(output_file, 'w', encoding='utf-8') as f:
    with pdfplumber.open(pdf_file) as pdf:
        total_pages = len(pdf.pages)
        print(f"Total pages in PDF: {total_pages}")
        
        if PSIONICS_END > total_pages:
            PSIONICS_END = total_pages
            print(f"Adjusted end page to {PSIONICS_END}")
        
        for page_num in range(PSIONICS_START - 1, PSIONICS_END):
            if page_num >= len(pdf.pages):
                break
            page = pdf.pages[page_num]
            text = page.extract_text()
            if text:
                f.write(f"\n{'='*80}\n")
                f.write(f"PAGE {page_num + 1}\n")
                f.write(f"{'='*80}\n\n")
                f.write(text)
                f.write("\n")

print(f"\nExtraction complete! Saved to {output_file}")
print("Review this file to confirm it's the psionics chapter, then we can adapt it.")
