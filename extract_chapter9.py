import PyPDF2
import sys

# Set UTF-8 encoding for output
sys.stdout.reconfigure(encoding='utf-8')

pdf = open('AFF_Adventure_Creator.pdf', 'rb')
reader = PyPDF2.PdfReader(pdf)

text = ''
for i in range(277, 315):
    page_text = reader.pages[i].extract_text()
    text += f'\n--- Page {i+1} ---\n' + page_text

print(text)
pdf.close()

