# pip install fpdf arabic-reshaper python-bidi googletrans==4.0.0-rc1

from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display
from googletrans import Translator

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
            self.multi_cell(0, 10, bidi_text, 0, 'R')

def create_pdf(input_markdown_file, output_pdf_file, font_path):
    pdf = PDF()

    # Add Arabic font
    pdf.add_font('Amiri', '', font_path, uni=True)

    # Read markdown file
    with open(input_markdown_file, 'r', encoding='utf-8') as file:
        english_text = file.read()

    # Translate text to Arabic
    translator = Translator()
    translation = translator.translate(english_text, src='en', dest='ar')
    arabic_text = translation.text

    # Split the Arabic text into lines for the PDF
    arabic_lines = arabic_text.split('\n')

    # Add Arabic text to the PDF
    pdf.add_arabic_text(arabic_lines)

    # Save the PDF to a file
    pdf.output(output_pdf_file)

# Usage example
input_markdown_file = 'D:\\Process\\Project77\\test.md'  # Your English markdown file
output_pdf_file = 'D:\\Process\\Project77\\output_arabic2.pdf'
font_path = 'D:\\Process\\Project77\\Amiri-Regular.ttf'  # Path to your Arabic font file

create_pdf(input_markdown_file, output_pdf_file, font_path)

