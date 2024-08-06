# pip install fpdf
# pip install arabic-reshaper
# pip install python-bidi
# Arabic font file, such as Amiri. You can download it from https://fonts.google.com/share?selection.family=Amiri:ital,wght@0,400;0,700;1,400;1,700

from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display
import warnings

# Ignore specific UserWarnings related to cmap values
warnings.filterwarnings("ignore", message="cmap value too big/small")

class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        pass

    def add_arabic_text(self, lines):
        self.add_page()
        self.set_font('Amiri', '', 16)
        for line in lines:
            # Reshape and display the Arabic text properly
            reshaped_text = arabic_reshaper.reshape(line)
            bidi_text = get_display(reshaped_text)
            self.cell(0, 10, bidi_text, 0, 1, 'R')

def create_pdf(input_markdown_file, output_pdf_file, font_path):
    pdf = PDF()

    # Add Arabic font
    pdf.add_font('Amiri', '', font_path, uni=True)

    # Read markdown file
    with open(input_markdown_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Add Arabic text to the PDF
    pdf.add_arabic_text(lines)

    # Save the PDF to a file
    pdf.output(output_pdf_file)

# Usage example
input_markdown_file = '\input_arabic.md'  # Your Arabic markdown file
output_pdf_file = '\output_arabic.pdf'
font_path = '\Amiri-Regular.ttf'  # Path to your Arabic font file

create_pdf(input_markdown_file, output_pdf_file, font_path)
