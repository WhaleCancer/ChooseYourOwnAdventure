"""
Extract all pages from a PDF as flattened images
"""
import fitz  # PyMuPDF
import os

pdf_file = "CB77011 - stellar-adventures.pdf"
output_folder = "CB77011_stellar-adventures_Pages"

print(f"Extracting pages from {pdf_file}...")
print("="*80)

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Created folder: {output_folder}")
else:
    print(f"Using existing folder: {output_folder}")

try:
    # Open the PDF
    doc = fitz.open(pdf_file)
    total_pages = len(doc)
    print(f"\nTotal pages to extract: {total_pages}\n")
    
    # Extract each page as an image
    for page_num in range(total_pages):
        page = doc[page_num]
        
        # Render page to an image (pixmap)
        # zoom=2.0 gives 144 DPI (good quality), zoom=2.78 gives 200 DPI
        zoom = 2.0  # 144 DPI
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        
        # Save as PNG
        filename = f"page_{page_num + 1:04d}.png"
        filepath = os.path.join(output_folder, filename)
        pix.save(filepath)
        
        if (page_num + 1) % 10 == 0 or (page_num + 1) == total_pages:
            print(f"Extracted page {page_num + 1}/{total_pages}...")
    
    doc.close()
    
    print(f"\nSuccessfully extracted {total_pages} pages to {output_folder}/")
    print(f"  Files saved as: page_0001.png, page_0002.png, ...")
    
except Exception as e:
    print(f"\nError: {e}")
    print("\nMake sure PyMuPDF is installed:")
    print("  pip install PyMuPDF")
