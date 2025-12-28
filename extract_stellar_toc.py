import pdfplumber

pdf_file = "CB77011 - stellar-adventures.pdf"
output_file = "stellar_toc_analysis.txt"

with open(output_file, 'w', encoding='utf-8') as f:
    with pdfplumber.open(pdf_file) as pdf:
        total_pages = len(pdf.pages)
        f.write(f"Total pages: {total_pages}\n\n")
        f.write("="*80 + "\n")
        f.write("FIRST 25 PAGES - STRUCTURE ANALYSIS\n")
        f.write("="*80 + "\n\n")
        
        for i in range(min(25, total_pages)):
            page = pdf.pages[i]
            text = page.extract_text()
            if text:
                f.write(f"\n{'='*80}\n")
                f.write(f"PAGE {i+1}\n")
                f.write(f"{'='*80}\n\n")
                # Get first 800 chars to identify headers
                preview = text[:800]
                f.write(preview)
                if len(text) > 800:
                    f.write("\n[... continues ...]")
                f.write("\n")

print(f"Extracted first 25 pages to {output_file}")
print("Review this file to identify chapter/section boundaries")
