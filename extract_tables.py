import re

# Read the original text file
with open('AFF_Adventure_Creator_Text.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find all table locations
tables = {}

# Table 6.1.1 - Random Wilderness Generator
start = None
for i, line in enumerate(lines):
    if 'Table 6.1.1 Random Wilderness Generator' in line:
        start = i
        break

if start:
    # Extract the table - it has Region names and then roll results
    table_data = []
    current_region = None
    current_row = []
    
    i = start + 1
    while i < len(lines) and 'Table 6.1.2' not in lines[i]:
        line = lines[i].strip()
        if not line or '--- PAGE' in line:
            i += 1
            continue
        
        # Check if this is a region name (ends with (code))
        if re.match(r'^[A-Z][a-z]+.*\([A-Z][a-z]+\)', line):
            if current_region:
                table_data.append((current_region, current_row))
            # Extract region name and code
            match = re.match(r'^([A-Z][a-z\s&]+)\s*\(([A-Z][a-z]+)\)', line)
            if match:
                current_region = match.group(1).strip()
                current_row = []
        elif current_region and line:
            # This should be the roll results
            parts = line.split()
            if len(parts) >= 11:  # Should have 11 values (2-12)
                current_row = parts[:11]
            elif len(parts) > 0:
                # Might be split across lines
                current_row.extend(parts)
        
        i += 1
    
    if current_region:
        table_data.append((current_region, current_row))
    
    tables['6.1.1'] = table_data

print(f"Found {len(tables)} tables")
print(f"Table 6.1.1 has {len(tables.get('6.1.1', []))} rows")

# Let me try a different approach - read the specific sections more carefully
print("\nExtracting tables from specific line ranges...")

