"""
Extract all text from Stellar Adventures PDF
"""
import pdfplumber
import sys
import io

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')

pdf_file = "CB77011 - stellar-adventures.pdf"
output_file = "CB77011_Stellar_Adventures_Text.txt"

print(f"Extracting text from {pdf_file}...")

try:
    with pdfplumber.open(pdf_file) as pdf:
        total_pages = len(pdf.pages)
        print(f"Total pages: {total_pages}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for page_num in range(total_pages):
                page = pdf.pages[page_num]
                text = page.extract_text()
                
                if text:
                    f.write(f"\n{'='*80}\n")
                    f.write(f"PAGE {page_num + 1}\n")
                    f.write(f"{'='*80}\n\n")
                    f.write(text)
                    f.write("\n")
                
                if (page_num + 1) % 10 == 0:
                    print(f"Processed {page_num + 1}/{total_pages} pages...")
        
        print(f"\nExtraction complete! Text saved to {output_file}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
