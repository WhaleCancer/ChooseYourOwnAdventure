"""
Define topic-based chunks for Magic Companion articles
Based on TOC analysis: 7 chapters, 113 pages total
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Based on TOC analysis:
# Chapter 1 - History of Magic (Page 7)
# Chapter 2 - Existing Magical Styles (Page 9)
# Chapter 3 - New Talents and Special Skills (Page 13)
# Chapter 4 - New and Optional Rules (Page 17)
# Chapter 5 - New Magical Styles (Page 25)
# Chapter 6 - New Spells (Page 93)
# Chapter 7 - Magical Monsters (Page 103)

# Define topic chunks (page ranges approximate, will need adjustment)
topic_chunks = [
    # Front matter
    {
        'title': 'Front-Cover-and-Contents',
        'pages': (1, 6),
        'description': 'Front cover, title page, and table of contents'
    },
    
    # Chapter 1
    {
        'title': 'History-of-Magic',
        'pages': (7, 8),
        'description': 'Chapter 1: A History of Magic'
    },
    
    # Chapter 2
    {
        'title': 'Existing-Magical-Styles',
        'pages': (9, 12),
        'description': 'Chapter 2: Existing Magical Styles'
    },
    
    # Chapter 3
    {
        'title': 'New-Talents-and-Special-Skills',
        'pages': (13, 16),
        'description': 'Chapter 3: New Talents and Special Skills'
    },
    
    # Chapter 4
    {
        'title': 'New-and-Optional-Rules',
        'pages': (17, 24),
        'description': 'Chapter 4: New and Optional Rules'
    },
    
    # Chapter 5 - This is a large chapter (pages 25-92, ~68 pages)
    # Break it into logical topics
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
    
    # Chapter 6
    {
        'title': 'New-Spells',
        'pages': (93, 102),
        'description': 'Chapter 6: New Spells'
    },
    
    # Chapter 7
    {
        'title': 'Magical-Monsters',
        'pages': (103, 113),
        'description': 'Chapter 7: Magical Monsters'
    },
]

print("Topic Chunks Defined:")
print("=" * 60)
for i, chunk in enumerate(topic_chunks, 1):
    page_range = f"{chunk['pages'][0]}-{chunk['pages'][1]}"
    print(f"{i:2d}. {chunk['title']:40s} Pages {page_range:8s} ({chunk['pages'][1] - chunk['pages'][0] + 1} pages)")

print(f"\nTotal chunks: {len(topic_chunks)}")
print(f"Total pages covered: {sum(chunk['pages'][1] - chunk['pages'][0] + 1 for chunk in topic_chunks)}")










