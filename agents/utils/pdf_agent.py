import os
from fpdf import FPDF
from PyPDF2 import PdfMerger, PdfReader

class PdfAgent:

    def run(self, page_size="A4", font="Arial", content=0, save_path="workspace/pdf", filename="mypdf.pdf", mode="override"):
        os.makedirs(save_path, exist_ok=True)
        if not isinstance(content, str):
            return {"status": "Fail", "details": "Content must be a string"}
        
        temp_path = os.path.join(save_path, "temp_new.pdf")
        full_path = os.path.join(save_path, filename)

        # Generate new PDF from content
        pdf = FPDF(format=page_size)
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font(font, size=12)
        for line in content.splitlines():
            pdf.multi_cell(0, 10, line)
        pdf.output(temp_path)

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
