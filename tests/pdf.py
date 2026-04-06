from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("helvetica", "B", size=45)
pdf.cell(100, 10, text="This is a test PDF file for upload.", align="C")
pdf_output = pdf.output("tests/api/manual_loader/test_files/test_file.pdf")