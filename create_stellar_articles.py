"""
Create Stellar Adventures articles from defined structure
Run this after filling in stellar_adventures_structure_template.py
"""
import os
import sys
import pdfplumber
import re
from stellar_adventures_structure_template import structure

sys.stdout.reconfigure(encoding='utf-8')

pdf_file = "CB77011 - stellar-adventures.pdf"
base_output_dir = "RULES/Stellar-Adventures"
pages_dir = "stellar-adventures_Pages"

def clean_text(text):
    """Clean and format extracted text"""
    if not text:
        return ""
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    text = text.replace('\x0c', '')
    return text.strip()

def extract_pages_text(pdf_path, start_page, end_page):
    """Extract text from a range of pages"""
    text_parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num in range(start_page - 1, min(end_page, len(pdf.pages))):
            page = pdf.pages[page_num]
            text = page.extract_text()
            if text:
                text_parts.append(clean_text(text))
    return '\n\n'.join(text_parts)

def create_article(item, pdf_path, base_output_dir):
    """Create a markdown article"""
    folder = item['folder']
    title = item['title']
    pages = item['pages']
    description = item['description']
    
    # Create subfolder
    folder_path = os.path.join(base_output_dir, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")
    
    # Extract text
    print(f"Extracting pages {pages[0]}-{pages[1]}...")
    extracted_text = extract_pages_text(pdf_path, pages[0], pages[1])
    
    # Generate image references
    image_refs = []
    for page_num in range(pages[0], pages[1] + 1):
        page_str = f"{page_num:04d}"
        image_path = f"../../../{pages_dir}/page_{page_str}.png"
        image_refs.append(f"![Page {page_num}]({image_path})")
    
    # Create markdown
    readable_title = title.replace('-', ' ')
    content = f"""# {readable_title}

**Source:** CB77011 - Stellar Adventures  
**Pages:** {pages[0]}-{pages[1]}

{description}

"""
    
    if extracted_text:
        content += "## Content\n\n"
        content += extracted_text
        content += "\n\n---\n\n"
    
    content += "## Page Images\n\n"
    content += '\n'.join(image_refs)
    content += '\n'
    
    # Write file
    filename = title.replace(' ', '-')
    filepath = os.path.join(folder_path, f"{filename}.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath

def main():
    if not os.path.exists(pdf_file):
        print(f"Error: PDF file not found: {pdf_file}")
        return
    
    if not os.path.exists(base_output_dir):
        os.makedirs(base_output_dir)
    
    print(f"Creating {len(structure)} articles...")
    print("=" * 60)
    
    for item in structure:
        try:
            filepath = create_article(item, pdf_file, base_output_dir)
            print(f"  [OK] {filepath}")
        except Exception as e:
            print(f"  [ERROR] {item['title']}: {e}")
    
    print("=" * 60)
    print(f"Complete! Created articles in {base_output_dir}")

if __name__ == "__main__":
    main()
