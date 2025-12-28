"""
Process Stellar Adventures PDF by examining pages and creating organized articles
Similar to Magic Companion processing but for Stellar Adventures
"""
import os
import sys
import pdfplumber
import re

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')

pdf_file = "CB77011 - stellar-adventures.pdf"
base_output_dir = "RULES/Stellar-Adventures"
pages_dir = "stellar-adventures_Pages"

def clean_text(text):
    """Clean and format extracted text"""
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    
    # Fix common OCR/PDF extraction issues
    text = text.replace('\x0c', '')  # Form feed
    text = text.strip()
    
    return text

def extract_page_text(pdf_path, page_num):
    """Extract text from a specific page (1-indexed)"""
    with pdfplumber.open(pdf_path) as pdf:
        if page_num > len(pdf.pages):
            return ""
        page = pdf.pages[page_num - 1]  # Convert to 0-indexed
        text = page.extract_text()
        return clean_text(text) if text else ""

def find_chapter_headers(pdf_path, max_pages=20):
    """Scan first few pages to find table of contents and chapter structure"""
    print("Scanning for chapter structure...")
    toc_pages = []
    
    with pdfplumber.open(pdf_path) as pdf:
        # Check first 20 pages for table of contents
        for page_num in range(min(20, len(pdf.pages))):
            page = pdf.pages[page_num]
            text = page.extract_text()
            if text:
                # Look for common TOC indicators
                if any(keyword in text.lower() for keyword in ['contents', 'chapter', 'introduction', 'table of']):
                    toc_pages.append((page_num + 1, text))
                    print(f"Found potential TOC on page {page_num + 1}")
    
    return toc_pages

def create_article(title, pages, description, pdf_path, base_output_dir, subfolder=""):
    """Create a markdown article with extracted text and page images"""
    
    # Create subfolder if needed
    if subfolder:
        folder_path = os.path.join(base_output_dir, subfolder)
    else:
        folder_path = base_output_dir
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")
    
    # Extract text from all pages
    print(f"Extracting text from pages {pages[0]}-{pages[1]}...")
    extracted_text_parts = []
    for page_num in range(pages[0], pages[1] + 1):
        page_text = extract_page_text(pdf_path, page_num)
        if page_text:
            extracted_text_parts.append(f"### Page {page_num}\n\n{page_text}")
    
    extracted_text = "\n\n".join(extracted_text_parts)
    
    # Generate image references
    image_refs = []
    for page_num in range(pages[0], pages[1] + 1):
        page_str = f"{page_num:04d}"
        # Relative path from article location to pages folder
        if subfolder:
            image_path = f"../../../{pages_dir}/page_{page_str}.png"
        else:
            image_path = f"../../{pages_dir}/page_{page_str}.png"
        image_refs.append(f"![Page {page_num}]({image_path})")
    
    # Create markdown content
    content = f"""# {title}

**Source:** CB77011 - Stellar Adventures  
**Pages:** {pages[0]}-{pages[1]}

{description}

"""
    
    # Add extracted text if available
    if extracted_text:
        content += "## Content\n\n"
        content += extracted_text
        content += "\n\n---\n\n"
    
    # Add image references
    content += "## Page Images\n\n"
    content += '\n'.join(image_refs)
    content += '\n'
    
    # Write file
    filename = title.lower().replace(' ', '-').replace(':', '').replace(',', '')
    filename = re.sub(r'[^\w\-]', '', filename)
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
        print(f"Created directory: {base_output_dir}")
    
    # First, let's scan for table of contents
    toc_info = find_chapter_headers(pdf_file)
    
    print("\n" + "="*60)
    print("STELLAR ADVENTURES PROCESSING")
    print("="*60)
    print("\nTo process Stellar Adventures, you'll need to:")
    print("1. Examine the page images to identify chapter/section boundaries")
    print("2. Define the structure (similar to Magic Companion)")
    print("3. Run this script with the structure defined")
    print("\nFor now, this script can help extract text from specific page ranges.")
    print("\nExample usage:")
    print("  create_article('Introduction', (1, 10), 'Introduction to Stellar Adventures', pdf_file, base_output_dir)")
    
    # Extract first few pages to help identify structure
    print("\nExtracting first 10 pages to help identify structure...")
    for page_num in range(1, min(11, 131)):  # Assuming ~130 pages
        text = extract_page_text(pdf_file, page_num)
        if text:
            # Look for chapter markers
            if re.search(r'chapter\s+\d+', text, re.IGNORECASE):
                print(f"\nPage {page_num} contains chapter marker:")
                print(text[:200] + "...")

if __name__ == "__main__":
    main()
