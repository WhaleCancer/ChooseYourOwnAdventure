"""
Extract text from pages likely to contain Stellar Adventures weapon skills
"""
import pdfplumber

pdf_file = "CB77011 - stellar-adventures.pdf"

# Common page ranges for skills chapters
page_ranges = [
    (15, 35),   # Early skills chapter
    (35, 55),   # Mid skills chapter  
    (55, 75),   # Later skills chapter
]

print("Extracting text from potential skills chapters...")
print("="*80)

with pdfplumber.open(pdf_file) as pdf:
    total = len(pdf.pages)
    print(f"Total pages: {total}\n")
    
    for start, end in page_ranges:
        print(f"\n{'='*80}")
        print(f"PAGES {start}-{end}")
        print(f"{'='*80}\n")
        
        for page_num in range(start - 1, min(end, total)):
            page = pdf.pages[page_num]
            text = page.extract_text()
            if text:
                # Check if this page mentions skills or weapons
                text_lower = text.lower()
                if any(term in text_lower for term in ['skill', 'weapon', 'marksmanship', 'blaster', 'characteristic']):
                    print(f"\n--- PAGE {page_num + 1} ---\n")
                    print(text)
                    print("\n" + "-"*80)







