import os
import re

# Files to process
base_path = 'RULES'

def replace_in_file(filepath):
    """Replace Hero/Agent with Character in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace Hero with Character (case-sensitive)
        content = re.sub(r'\bHero\b', 'Character', content)
        content = re.sub(r'\bHero\'s\b', "Character's", content)
        content = re.sub(r'\bHeroes\b', 'Characters', content)
        
        # Replace Agent with Character (case-sensitive)
        content = re.sub(r'\bAgent\b', 'Character', content)
        content = re.sub(r'\bAgent\'s\b', "Character's", content)
        content = re.sub(r'\bAgents\b', 'Characters', content)
        
        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f'Error processing {filepath}: {e}')
        return False

# Walk through all directories
updated_count = 0
for root, dirs, files in os.walk(base_path):
    for file in files:
        if file.endswith('.md'):
            filepath = os.path.join(root, file)
            if replace_in_file(filepath):
                updated_count += 1
                print(f'Updated: {filepath}')

print(f'\nUpdated {updated_count} files!')













