import os
import unicodedata
from PyPDF2 import PdfMerger, PdfReader
from weasyprint import HTML

class PdfAgent:

    def clean_text(self, text):
        return unicodedata.normalize('NFKD', text)

    def run(self, page_size="A4", content="", save_path="workspace/pdf", filename="styled.pdf", mode="override"):
        os.makedirs(save_path, exist_ok=True)
        temp_path = os.path.join(save_path, "temp_new.pdf")
        full_path = os.path.join(save_path, filename)

        # Map known sizes
        size_map = {
            "A4": "210mm 297mm",
            "6x9": "152.4mm 228.6mm",
            "Letter": "216mm 279mm"
        }
        page_dimensions = size_map.get(page_size, "210mm 297mm")  # Default to A4

        # Inject page size CSS
        style = f"@page {{ size: {page_dimensions}; margin: 20mm; }}\n"
        content = f"<style>{style}</style>\n" + self.clean_text(content)

        try:
            HTML(string=content).write_pdf(temp_path)
        except Exception as e:
            return {"status": "Fail", "details": str(e)}

        if mode == "append" and os.path.exists(full_path):
            merger = PdfMerger()
            merger.append(PdfReader(full_path, strict=False))
            merger.append(PdfReader(temp_path, strict=False))
            merger.write(full_path)
            merger.close()
            os.remove(temp_path)
        else:
            os.rename(temp_path, full_path)

        return {"status": "Success", "details": full_path}
