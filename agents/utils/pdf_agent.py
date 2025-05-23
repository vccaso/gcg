import os
import unicodedata
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from weasyprint import HTML
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

class PdfAgent:

    def clean_text(self, text):
        return unicodedata.normalize('NFKD', text)

    def run(self, page_size="A4", content="", save_path="workspace/pdf", filename="styled.pdf", mode="override", add_page_number="True"):
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
            HTML(string=content, base_url=os.getcwd()).write_pdf(temp_path)
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

        print(f"add_page_number: {add_page_number}")
        if str(add_page_number).lower() in ["true", "1", "yes"]:
            self.add_page_numbers(full_path)

        return {"status": "Success", "details": full_path}

    def add_page_numbers(self, pdf_path):
        # Read existing PDF
        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        for page_num in range(len(reader.pages)):
            packet = BytesIO()
            can = canvas.Canvas(packet, pagesize=(432, 648))  # 6in x 9in in points
            can.setFont("Helvetica", 10)
            can.drawCentredString(216, 30, f"Page {page_num + 1}")
            can.save()

            packet.seek(0)
            overlay = PdfReader(packet)
            page = reader.pages[page_num]
            page.merge_page(overlay.pages[0])
            writer.add_page(page)

        with open(pdf_path, "wb") as f:
            writer.write(f)
