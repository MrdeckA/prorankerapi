import sys
import fitz
fname = 'Alice Clark CV.pdf'
doc = fitz.open(fname)
text = " "
for page in doc:
    text = text + str(page.get_text())
print(text)
