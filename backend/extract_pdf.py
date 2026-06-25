import fitz  # pymupdf
import os

pdf_path = r"C:\Users\Ranim\euklydia\backend\Parcours_AI_Project_Manager_v1.1.pdf"
out_path = r"C:\Users\Ranim\euklydia\backend\pdf_extracted.txt"

doc = fitz.open(pdf_path)
print(f"Total pages: {len(doc)}")

with open(out_path, "w", encoding="utf-8") as f:
    for i, page in enumerate(doc):
        text = page.get_text()
        f.write(f"\n\n{'='*60}\n PAGE {i+1}\n{'='*60}\n")
        f.write(text)

doc.close()
print(f"Done. Extracted to {out_path}")
