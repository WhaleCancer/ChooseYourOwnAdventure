"""
Convert CB77028 - Magic Companion.pdf to PNG page images
Uses PyMuPDF (fitz) which doesn't require poppler
"""
import os
import fitz  # PyMuPDF

def convert_pdf_to_images(pdf_path, output_dir):
    """Convert PDF pages to PNG images"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    
    print(f"Converting {pdf_path} to images...")
    try:
        # Open PDF
        pdf_document = fitz.open(pdf_path)
        page_count = len(pdf_document)
        
        print(f"Found {page_count} pages")
        
        # Convert each page to image
        for page_num in range(page_count):
            page = pdf_document[page_num]
            
            # Render page to image (200 DPI for good quality)
            mat = fitz.Matrix(200/72, 200/72)  # 200 DPI
            pix = page.get_pixmap(matrix=mat)
            
            # Save as PNG
            page_num_str = f"{page_num + 1:04d}"
            filename = f"page_{page_num_str}.png"
            filepath = os.path.join(output_dir, filename)
            pix.save(filepath)
            
            if (page_num + 1) % 10 == 0:
                print(f"Converted {page_num + 1}/{page_count} pages...")
        
        pdf_document.close()
        print(f"Successfully converted {page_count} pages to {output_dir}")
        return page_count
        
    except Exception as e:
        print(f"Error converting PDF: {e}")
        raise

if __name__ == "__main__":
    pdf_file = "CB77028 - Magic Companion.pdf"
    output_directory = "CB77028_Magic_Companion_Pages"
    
    if not os.path.exists(pdf_file):
        print(f"Error: PDF file not found: {pdf_file}")
        exit(1)
    
    page_count = convert_pdf_to_images(pdf_file, output_directory)
    print(f"\nConversion complete! Total pages: {page_count}")

