import os
from fpdf import FPDF, HTMLMixin
from PyPDF2 import PdfMerger, PdfReader
import unicodedata
from fpdf.html import HTML2FPDF
import html

# Patch unescape to fix compatibility issue
HTML2FPDF.unescape = staticmethod(html.unescape)


class HTMLPDF(FPDF, HTMLMixin):
    pass

class PdfAgent:

    def clean_text(self, text):
        return unicodedata.normalize('NFKD', text).encode('latin-1', 'ignore').decode('latin-1')
    
    def run(self, page_size="A4", content="", save_path="workspace/pdf", filename="styled.pdf", mode="override"):
        os.makedirs(save_path, exist_ok=True)
        temp_path = os.path.join(save_path, "temp_new.pdf")
        full_path = os.path.join(save_path, filename)

        pdf = HTMLPDF(format=page_size)
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        content = self.clean_text(content)
        try:
            pdf.write_html(content)
        except Exception as e:
            return {"status": "Fail", "details": str(e)}

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
