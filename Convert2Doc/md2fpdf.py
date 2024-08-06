from fpdf import FPDF

# Define a class inheriting from FPDF to customize the PDF
class PDF(FPDF):
    def header(self):
        # Optional: Add a header if needed
        pass

    def footer(self):
        # Optional: Add a footer if needed
        pass

    def chapter_title(self, title):
        # Set font
        self.set_font('Arial', 'B', 16)
        # Title
        self.cell(0, 10, title, 0, 1, 'C')
        # Line break
        self.ln(10)

    def chapter_body(self, body):
        # Read text file
        self.set_font('Arial', '', 14)
        # Output justified text
        self.multi_cell(0, 10, body)
        # Line break
        self.ln()

    def add_markdown_text(self, lines):
        self.set_font('Arial', '', 16)
        for line in lines:
            # Add a cell with the line, and force a line break
            self.cell(0, 10, line, 0, 1)

# Function to create the PDF
def create_pdf(input_markdown_file, output_pdf_file):
    # Create instance of FPDF class
    pdf = PDF()

    # Add a page
    pdf.add_page()

    # Read markdown file
    with open(input_markdown_file, 'r') as file:
        lines = file.readlines()

    # Add markdown text to the PDF
    pdf.add_markdown_text(lines)

    # Save the PDF to a file
    pdf.output(output_pdf_file)

# Usage example
input_markdown_file = 'input.md'
output_pdf_file = 'output.pdf'
create_pdf(input_markdown_file, output_pdf_file)
