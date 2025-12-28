"""
Create markdown articles for Magic Companion topic chunks
"""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Topic chunks from define_topic_chunks.py
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

def create_article(chunk, output_dir):
    """Create a markdown article for a topic chunk"""
    filename = f"{chunk['title']}.md"
    filepath = os.path.join(output_dir, filename)
    
    # Convert title to readable format
    readable_title = chunk['title'].replace('-', ' ')
    readable_title = ' '.join(word.capitalize() for word in readable_title.split())
    
    # Generate image references
    image_refs = []
    for page_num in range(chunk['pages'][0], chunk['pages'][1] + 1):
        page_str = f"{page_num:04d}"
        # Relative path from RULES/Magic-Companion/ to CB77028_Magic_Companion_Pages/
        image_path = f"../../CB77028_Magic_Companion_Pages/page_{page_str}.png"
        image_refs.append(f"![Page {page_num}]({image_path})")
    
    # Create markdown content
    content = f"""# {readable_title}

**Source:** CB77028 - Magic Companion  
**Pages:** {chunk['pages'][0]}-{chunk['pages'][1]}

{chunk['description']}

"""
    
    # Add image references
    content += '\n'.join(image_refs)
    content += '\n'
    
    # Write file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filename

def main():
    output_dir = "RULES/Magic-Companion"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    
    print(f"Creating {len(topic_chunks)} articles...")
    
    created_files = []
    for chunk in topic_chunks:
        filename = create_article(chunk, output_dir)
        created_files.append(filename)
        print(f"  Created: {filename}")
    
    print(f"\nSuccessfully created {len(created_files)} articles in {output_dir}")
    return created_files

if __name__ == "__main__":
    main()










