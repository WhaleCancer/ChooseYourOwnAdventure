"""
Extract text from Magic Companion PDF and create organized markdown articles
"""
import os
import sys
import pdfplumber
import re

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')

# Define the structure with subfolders
structure = [
    {
        'folder': 'Introduction',
        'title': 'Front-Cover-and-Contents',
        'pages': (1, 6),
        'description': 'Front cover, title page, and table of contents'
    },
    {
        'folder': 'Introduction',
        'title': 'History-of-Magic',
        'pages': (7, 8),
        'description': 'Chapter 1: A History of Magic'
    },
    {
        'folder': 'Introduction',
        'title': 'Existing-Magical-Styles',
        'pages': (9, 12),
        'description': 'Chapter 2: Existing Magical Styles'
    },
    {
        'folder': 'Rules',
        'title': 'New-Talents-and-Special-Skills',
        'pages': (13, 16),
        'description': 'Chapter 3: New Talents and Special Skills'
    },
    {
        'folder': 'Rules',
        'title': 'New-and-Optional-Rules',
        'pages': (17, 24),
        'description': 'Chapter 4: New and Optional Rules'
    },
    {
        'folder': 'Magical-Styles',
        'title': 'New-Magical-Styles-Introduction',
        'pages': (25, 35),
        'description': 'Chapter 5: New Magical Styles - Introduction and Basics'
    },
    {
        'folder': 'Magical-Styles',
        'title': 'New-Magical-Styles-Part-1',
        'pages': (36, 50),
        'description': 'Chapter 5: New Magical Styles - Part 1'
    },
    {
        'folder': 'Magical-Styles',
        'title': 'New-Magical-Styles-Part-2',
        'pages': (51, 65),
        'description': 'Chapter 5: New Magical Styles - Part 2'
    },
    {
        'folder': 'Magical-Styles',
        'title': 'New-Magical-Styles-Part-3',
        'pages': (66, 80),
        'description': 'Chapter 5: New Magical Styles - Part 3'
    },
    {
        'folder': 'Magical-Styles',
        'title': 'New-Magical-Styles-Part-4',
        'pages': (81, 92),
        'description': 'Chapter 5: New Magical Styles - Part 4'
    },
    {
        'folder': 'Spells',
        'title': 'New-Spells',
        'pages': (93, 102),
        'description': 'Chapter 6: New Spells'
    },
    {
        'folder': 'Monsters',
        'title': 'Magical-Monsters',
        'pages': (103, 113),
        'description': 'Chapter 7: Magical Monsters'
    },
]

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
    """Create a markdown article with extracted text"""
    folder = item['folder']
    title = item['title']
    pages = item['pages']
    description = item['description']
    
    # Create subfolder if needed
    folder_path = os.path.join(base_output_dir, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")
    
    # Extract text from PDF
    print(f"Extracting text from pages {pages[0]}-{pages[1]}...")
    extracted_text = extract_pages_text(pdf_path, pages[0], pages[1])
    
    # Convert title to readable format
    readable_title = title.replace('-', ' ')
    readable_title = ' '.join(word.capitalize() for word in readable_title.split())
    
    # Generate image references
    image_refs = []
    for page_num in range(pages[0], pages[1] + 1):
        page_str = f"{page_num:04d}"
        # Relative path from subfolder to CB77028_Magic_Companion_Pages/
        image_path = f"../../../CB77028_Magic_Companion_Pages/page_{page_str}.png"
        image_refs.append(f"![Page {page_num}]({image_path})")
    
    # Create markdown content
    content = f"""# {readable_title}

**Source:** CB77028 - Magic Companion  
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
    filepath = os.path.join(folder_path, f"{title}.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath

def update_index(base_output_dir):
    """Update the main index file"""
    index_path = os.path.join(base_output_dir, "Magic-Companion-Index.md")
    
    content = """# Magic Companion Index

**Source:** CB77028 - Magic Companion  
**Total Pages:** 113

This index provides access to all articles extracted from the Magic Companion sourcebook, organized by topic.

## Table of Contents

### Introduction

1. **[Front Cover And Contents](Introduction/Front-Cover-and-Contents.md)** (Pages 1-6, 6 pages)
   - Front cover, title page, and table of contents

2. **[History Of Magic](Introduction/History-of-Magic.md)** (Pages 7-8, 2 pages)
   - Chapter 1: A History of Magic

3. **[Existing Magical Styles](Introduction/Existing-Magical-Styles.md)** (Pages 9-12, 4 pages)
   - Chapter 2: Existing Magical Styles

### Rules

4. **[New Talents And Special Skills](Rules/New-Talents-and-Special-Skills.md)** (Pages 13-16, 4 pages)
   - Chapter 3: New Talents and Special Skills

5. **[New And Optional Rules](Rules/New-and-Optional-Rules.md)** (Pages 17-24, 8 pages)
   - Chapter 4: New and Optional Rules

### Magical Styles

6. **[New Magical Styles Introduction](Magical-Styles/New-Magical-Styles-Introduction.md)** (Pages 25-35, 11 pages)
   - Chapter 5: New Magical Styles - Introduction and Basics

7. **[New Magical Styles Part 1](Magical-Styles/New-Magical-Styles-Part-1.md)** (Pages 36-50, 15 pages)
   - Chapter 5: New Magical Styles - Part 1

8. **[New Magical Styles Part 2](Magical-Styles/New-Magical-Styles-Part-2.md)** (Pages 51-65, 15 pages)
   - Chapter 5: New Magical Styles - Part 2

9. **[New Magical Styles Part 3](Magical-Styles/New-Magical-Styles-Part-3.md)** (Pages 66-80, 15 pages)
   - Chapter 5: New Magical Styles - Part 3

10. **[New Magical Styles Part 4](Magical-Styles/New-Magical-Styles-Part-4.md)** (Pages 81-92, 12 pages)
    - Chapter 5: New Magical Styles - Part 4

### Spells

11. **[New Spells](Spells/New-Spells.md)** (Pages 93-102, 10 pages)
    - Chapter 6: New Spells

### Monsters

12. **[Magical Monsters](Monsters/Magical-Monsters.md)** (Pages 103-113, 11 pages)
    - Chapter 7: Magical Monsters

## Source Information

- **Source Document:** CB77028 - Magic Companion
- **Page Images:** Located in `CB77028_Magic_Companion_Pages/`
- **Article Format:** Markdown files with extracted text content and embedded page images

## Notes

All articles contain extracted text from the original PDF along with page images for reference. The content is organized by topic/chapter into logical subfolders for easy navigation.

"""
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated index: {index_path}")

def main():
    pdf_file = "CB77028 - Magic Companion.pdf"
    base_output_dir = "RULES/Magic-Companion"
    
    if not os.path.exists(pdf_file):
        print(f"Error: PDF file not found: {pdf_file}")
        return
    
    if not os.path.exists(base_output_dir):
        os.makedirs(base_output_dir)
        print(f"Created directory: {base_output_dir}")
    
    print(f"Extracting text and creating {len(structure)} articles...")
    print("=" * 60)
    
    created_files = []
    for item in structure:
        try:
            filepath = create_article(item, pdf_file, base_output_dir)
            created_files.append(filepath)
            print(f"  [OK] Created: {filepath}")
        except Exception as e:
            print(f"  [ERROR] Error creating {item['title']}: {e}")
    
    # Update index
    update_index(base_output_dir)
    
    print("=" * 60)
    print(f"\nSuccessfully created {len(created_files)} articles in {base_output_dir}")
    print(f"Organized into subfolders: Introduction, Rules, Magical-Styles, Spells, Monsters")

if __name__ == "__main__":
    main()
