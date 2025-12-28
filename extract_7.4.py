import pdfplumber
import sys
import io

# Create a UTF-8 text stream
output = io.StringIO()

try:
    with pdfplumber.open('AFF_Adventure_Creator.pdf') as pdf:
        # Extract pages 260-280 (0-indexed: 259-279)
        for page_num in range(259, min(280, len(pdf.pages))):
            page = pdf.pages[page_num]
            text = page.extract_text()
            if text:
                output.write(f"\n--- Page {page_num + 1} ---\n")
                output.write(text)
                output.write("\n")
except Exception as e:
    output.write(f"Error: {e}")

# Write to file
with open('section_7.4_extract.txt', 'w', encoding='utf-8') as f:
    f.write(output.getvalue())

print("Extraction complete")

