import fitz
doc = fitz.open("ALJIBE VILLAS Nº 7C.pdf")
print(doc[0].get_text())