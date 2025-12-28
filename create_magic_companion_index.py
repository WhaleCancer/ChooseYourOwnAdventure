"""
Create index file for Magic Companion articles
"""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

topic_chunks = [
    {
        'title': 'Front-Cover-and-Contents',
        'pages': (1, 6),
        'description': 'Front cover, title page, and table of contents'
    },
    {
        'title': 'History-of-Magic',
        'pages': (7, 8),
        'description': 'Chapter 1: A History of Magic'
    },
    {
        'title': 'Existing-Magical-Styles',
        'pages': (9, 12),
        'description': 'Chapter 2: Existing Magical Styles'
    },
    {
        'title': 'New-Talents-and-Special-Skills',
        'pages': (13, 16),
        'description': 'Chapter 3: New Talents and Special Skills'
    },
    {
        'title': 'New-and-Optional-Rules',
        'pages': (17, 24),
        'description': 'Chapter 4: New and Optional Rules'
    },
    {
        'title': 'New-Magical-Styles-Introduction',
        'pages': (25, 35),
        'description': 'Chapter 5: New Magical Styles - Introduction and Basics'
    },
    {
        'title': 'New-Magical-Styles-Part-1',
        'pages': (36, 50),
        'description': 'Chapter 5: New Magical Styles - Part 1'
    },
    {
        'title': 'New-Magical-Styles-Part-2',
        'pages': (51, 65),
        'description': 'Chapter 5: New Magical Styles - Part 2'
    },
    {
        'title': 'New-Magical-Styles-Part-3',
        'pages': (66, 80),
        'description': 'Chapter 5: New Magical Styles - Part 3'
    },
    {
        'title': 'New-Magical-Styles-Part-4',
        'pages': (81, 92),
        'description': 'Chapter 5: New Magical Styles - Part 4'
    },
    {
        'title': 'New-Spells',
        'pages': (93, 102),
        'description': 'Chapter 6: New Spells'
    },
    {
        'title': 'Magical-Monsters',
        'pages': (103, 113),
        'description': 'Chapter 7: Magical Monsters'
    },
]

def create_index(output_dir):
    """Create index markdown file"""
    index_path = os.path.join(output_dir, "Magic-Companion-Index.md")
    
    content = """# Magic Companion Index

**Source:** CB77028 - Magic Companion  
**Total Pages:** 113

This index provides access to all articles extracted from the Magic Companion sourcebook.

## Table of Contents

"""
    
    # Add entries for each topic chunk
    for i, chunk in enumerate(topic_chunks, 1):
        readable_title = chunk['title'].replace('-', ' ')
        readable_title = ' '.join(word.capitalize() for word in readable_title.split())
        
        filename = f"{chunk['title']}.md"
        page_range = f"{chunk['pages'][0]}-{chunk['pages'][1]}"
        page_count = chunk['pages'][1] - chunk['pages'][0] + 1
        
        content += f"{i}. **[{readable_title}]({filename})** (Pages {page_range}, {page_count} pages)\n"
        content += f"   - {chunk['description']}\n\n"
    
    content += """## Source Information

- **Source Document:** CB77028 - Magic Companion
- **Page Images:** Located in `CB77028_Magic_Companion_Pages/`
- **Article Format:** Markdown files with embedded page images

## Notes

All articles contain page images from the original PDF. The content is organized by topic/chapter for easy navigation.

"""
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Created index: {index_path}")
    return index_path

if __name__ == "__main__":
    output_dir = "RULES/Magic-Companion"
    create_index(output_dir)










