"""
Extract detailed structure from Magic Companion PDF
Read page content to identify topics and sections
"""
import pdfplumber
import re

def extract_detailed_structure(pdf_path):
    """Extract detailed structure by reading page headers and content"""
    structure = []
    
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        
        print(f"Analyzing {total_pages} pages...\n")
        
        current_chapter = None
        current_section = None
        
        for page_num in range(total_pages):
            page = pdf.pages[page_num]
            text = page.extract_text()
            
            if not text:
                continue
            
            # Look for chapter headers (usually at top of page)
            lines = text.split('\n')[:10]  # Check first 10 lines
            
            for line in lines:
                line_clean = line.strip()
                
                # Check for chapter markers
                if re.search(r'Chapter\s+\d+', line_clean, re.IGNORECASE):
                    current_chapter = line_clean
                    structure.append({
                        'type': 'chapter',
                        'title': line_clean,
                        'page': page_num + 1
                    })
                    print(f"Page {page_num + 1}: {line_clean}")
                
                # Check for major section headers (all caps or bold patterns)
                elif re.search(r'^[A-Z][A-Z\s]{10,}$', line_clean) and len(line_clean) < 60:
                    if current_chapter:
                        structure.append({
                            'type': 'section',
                            'title': line_clean,
                            'page': page_num + 1,
                            'chapter': current_chapter
                        })
                        print(f"  Page {page_num + 1}: {line_clean}")
    
    return structure

if __name__ == "__main__":
    pdf_file = "CB77028 - Magic Companion.pdf"
    structure = extract_detailed_structure(pdf_file)
    
    print(f"\n\nFound {len(structure)} structural elements")










