import sys
import fitz
fname = './uploads/cv1.pdf'
doc = fitz.open(fname)
text = " "
for page in doc:
    text = text + str(page.get_text())
print(text)
