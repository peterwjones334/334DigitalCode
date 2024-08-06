# pip install fpdf arabic-reshaper python-bidi googletrans==4.0.0-rc1
# https://github.com/aliftype/amiri/releases/tag/1.000
# https://www.1001fonts.com/download/scheherazade.zip
# https://fonts.google.com/share?selection.family=Amiri:ital,wght@0,400;0,700;1,400;1,700|Lateef:wght@200;300;400;500;600;700;800

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
    translation = translator.translate(english_text, src='en', dest='ar') #
    arabic_text = translation.text

    # Split the Arabic text into lines for the PDF
    arabic_lines = arabic_text.split('\n')

    # Add Arabic text to the PDF
    pdf.add_arabic_text(arabic_lines)

    # Save the PDF to a file
    pdf.output(output_pdf_file)

# Usage example
input_markdown_file = 'input_english.md'  # Your English markdown file
output_pdf_file = 'output_arabic.pdf'
font_path = 'Amiri-Regular.ttf'  # Path to your Arabic font file "Amiri",  "Scheherazade" or "Lateef".

create_pdf(input_markdown_file, output_pdf_file, font_path)

