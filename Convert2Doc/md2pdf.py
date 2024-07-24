from markdown import markdown
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, TableOfContents
from reportlab.lib.units import inch

def markdown_to_pdf(markdown_text, cover_image_path, back_cover_image_path, output_pdf_path):
    """
    Converts markdown text to a structured PDF with a cover, copyright, title page, table of contents, and back cover.
    
    Args:
    markdown_text (str): Markdown formatted text.
    cover_image_path (str): Path to the front cover image.
    back_cover_image_path (str): Path to the back cover image.
    output_pdf_path (str): Path to save the generated PDF.
    """
    # Convert Markdown to HTML
    html_text = markdown(markdown_text)
    
    # Parse HTML for structure
    soup = BeautifulSoup(html_text, 'html.parser')
    
    # Create PDF document
    doc = SimpleDocTemplate(output_pdf_path, pagesize=letter)
    story = []
    
    # Cover page
    story.append(Image(cover_image_path, width=7*inch, height=9*inch))
    story.append(PageBreak())
    
    # Copyright page
    copy_right = "© 2024 All Rights Reserved"
    story.append(Paragraph(copy_right, getSampleStyleSheet()['BodyText']))
    story.append(PageBreak())
    
    # Title page
    title = soup.find('h1').text if soup.find('h1') else "No Title"
    story.append(Paragraph(title, getSampleStyleSheet()['Title']))
    story.append(PageBreak())
    
    # Table of contents
    toc = TableOfContents()
    story.append(toc)
    story.append(PageBreak())
    
    # Content pages
    styles = getSampleStyleSheet()
    for element in soup:
        if element.name == 'h1':
            story.append(Paragraph(element.text, styles['Title']))
        elif element.name == 'h2':
            story.append(Paragraph(element.text, styles['Heading2']))
        elif element.name == 'h3':
            story.append(Paragraph(element.text, styles['Heading3']))
        elif element.name == 'p':
            story.append(Paragraph(element.text, styles['BodyText']))
        story.append(Spacer(1, 0.2*inch))
    
    # Back cover
    story.append(PageBreak())
    story.append(Image(back_cover_image_path, width=7*inch, height=9*inch))
    
    # Build PDF
    doc.build(story)

# Uncomment the line below to use the function with your specific file paths and Markdown content.
# markdown_to_pdf('# Your Markdown Here', 'path_to_front_cover.jpg', 'path_to_back_cover.jpg', 'output_file.pdf')
