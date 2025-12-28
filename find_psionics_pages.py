"""
Quick script to find psionics-related pages in Stellar Adventures
"""
import pdfplumber

pdf_file = "CB77011 - stellar-adventures.pdf"

print("Scanning for psionics-related pages...")
print("="*60)

with pdfplumber.open(pdf_file) as pdf:
    total = len(pdf.pages)
    print(f"Total pages: {total}\n")
    
    psionics_pages = []
    
    # Scan all pages
    for i in range(total):
        page = pdf.pages[i]
        text = page.extract_text()
        if text:
            text_lower = text.lower()
            # Look for psionics keywords
            keywords = ['psionic', 'psionics', 'psychic', 'mental power', 'psi point', 'psionics characteristic']
            found_keywords = [kw for kw in keywords if kw in text_lower]
            
            if found_keywords:
                # Check if it looks like a chapter header (short text, or contains "chapter")
                is_header = len(text) < 500 or 'chapter' in text_lower
                preview = text[:150].replace('\n', ' ')
                
                psionics_pages.append({
                    'page': i + 1,
                    'is_header': is_header,
                    'keywords': found_keywords,
                    'preview': preview
                })
    
    print(f"Found {len(psionics_pages)} pages with psionics content:\n")
    
    for item in psionics_pages:
        header_marker = " [HEADER]" if item['is_header'] else ""
        print(f"Page {item['page']:3d}{header_marker}: {', '.join(item['keywords'])}")
        print(f"  Preview: {item['preview']}...")
        print()
    
    # Suggest a range
    if psionics_pages:
        first = psionics_pages[0]['page']
        last = psionics_pages[-1]['page']
        print(f"\nSuggested page range: {first}-{last}")
        print(f"Update PSIONICS_START_PAGE and PSIONICS_END_PAGE in process_stellar_psionics.py")
