import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    with pdfplumber.open('AFF_Adventure_Creator.pdf') as pdf:
        # Check pages 260-280 for section 7.4
        for page_num in range(260, min(280, len(pdf.pages))):
            page = pdf.pages[page_num]
            text = page.extract_text()
            if text and ('7.4' in text or 'Hero Backgrounds' in text or 'Lifepath' in text or 'Lifepaths' in text):
                print(f"\n--- Page {page_num + 1} ---\n")
                print(text[:1500])
                break
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)

