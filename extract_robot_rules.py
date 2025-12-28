"""
Extract robot rules from pages 46-51 of Stellar Adventures PDF
"""
import pdfplumber
import os

pdf_file = "CB77011 - stellar-adventures.pdf"
output_file = "robot_rules_extract.txt"

print("Extracting robot rules from pages 46-51...")
print("="*80)

with pdfplumber.open(pdf_file) as pdf:
    total = len(pdf.pages)
    print(f"Total pages in PDF: {total}\n")
    
    # Extract pages 46-51 (0-indexed: 45-50)
    extracted_text = []
    
    for page_num in range(45, min(51, total)):  # Pages 46-51 (0-indexed: 45-50)
        page = pdf.pages[page_num]
        text = page.extract_text()
        
        if text:
            extracted_text.append(f"\n{'='*80}\n")
            extracted_text.append(f"PAGE {page_num + 1}\n")
            extracted_text.append(f"{'='*80}\n\n")
            extracted_text.append(text)
            extracted_text.append("\n\n")
            print(f"Extracted page {page_num + 1}...")
        else:
            print(f"Warning: No text found on page {page_num + 1}")

# Write to file
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("".join(extracted_text))

print(f"\nExtraction complete! Text saved to {output_file}")

