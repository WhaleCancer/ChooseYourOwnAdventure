"""
Extract skills chapter text from Stellar Adventures and save to file
"""
import pdfplumber

pdf_file = "CB77011 - stellar-adventures.pdf"
output_file = "stellar_skills_extract.txt"

print(f"Extracting skills/weapons text from {pdf_file}...")
print("Saving to", output_file)

with pdfplumber.open(pdf_file) as pdf:
    total = len(pdf.pages)
    print(f"Total pages: {total}\n")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Check pages 15-80 (common range for skills chapters)
        for page_num in range(14, min(80, total)):
            page = pdf.pages[page_num]
            text = page.extract_text()
            if text:
                text_lower = text.lower()
                # Look for pages with skill/weapon/marksmanship content
                if any(term in text_lower for term in ['skill', 'weapon', 'marksmanship', 'blaster', 'characteristic', 'combat']):
                    f.write(f"\n{'='*80}\n")
                    f.write(f"PAGE {page_num + 1}\n")
                    f.write(f"{'='*80}\n\n")
                    f.write(text)
                    f.write("\n\n")

print(f"\nDone! Check {output_file} for extracted skills content.")







