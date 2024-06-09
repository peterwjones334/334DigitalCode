import os
from PIL import Image
from reportlab.lib.pagesizes import letter, A4, landscape, portrait
from reportlab.pdfgen import canvas

def convert_images_to_pdf(folder_path, output_filename, title, author, page_size=letter, orientation='portrait', margins=(50, 50), upscale=False, header_text="Header", footer_text="Footer"):
    
    valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']
    image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.splitext(f)[-1].lower() in valid_extensions]
    image_files.sort()

    page_size = landscape(page_size) if orientation == 'landscape' else portrait(page_size)

    c = canvas.Canvas(output_filename, pagesize=page_size)
    
    # Title Page
    c.setFont("Helvetica", 24)
    c.drawCentredString(page_size[0] / 2, page_size[1] / 2, title)
    #c.drawCentredString(page_size[0] / 2, page_size[1] / 2, author))
    c.setFont("Helvetica", 18)
    c.drawCentredString(page_size[0] / 2, page_size[1] / 2 - 30, author)  # Adjusting position for author below title
    c.showPage()

    # Blank page after title
    c.showPage()

    page_number = 1

    for image_path in image_files:
        with Image.open(image_path) as img:
            img_width, img_height = img.size
            aspect = img_height / float(img_width)

            available_width = page_size[0] - 2 * margins[0]
            available_height = page_size[1] - 2 * margins[1] - 30

            new_width = available_width
            new_height = aspect * available_width
            
            if new_height > available_height or (upscale and new_height < available_height):
                new_height = available_height
                new_width = new_height / aspect

            x_offset = (page_size[0] - new_width) / 2
            y_offset = (page_size[1] - new_height) - margins[1] - 30

            c.drawInlineImage(image_path, x_offset, y_offset, width=new_width, height=new_height)

        header_x = page_size[0] / 2
        header_y = page_size[1] - margins[1]
        
        c.drawCentredString(header_x, header_y, header_text)
        c.line(margins[0], header_y - 15, page_size[0] - margins[0], header_y - 15)
        c.drawString(margins[0], margins[1] - 15, footer_text)
        c.drawRightString(page_size[0] - margins[0], margins[1] - 15, f"Page {page_number}")
        
        c.showPage()
        page_number += 1

    # Blank page after images
    c.showPage()

    # Setting PDF properties
    c.setTitle(title)
    c.setAuthor(author)
    c.setSubject("Catalogue of Images")
    c.setKeywords(["Images", title, author])

    c.save()

# Example usage:
folder_path = 'c:\folder\images'
title_text = "MyBook"
output_pdf_name = title_text + '.pdf'
Author_text = "MyName"
convert_images_to_pdf(folder_path, output_pdf_name, title_text, Author_text, page_size=A4, orientation='portrait', margins=(50, 50), upscale=True, header_text=title_text, footer_text="Copyright © 2023 " + Author_text)
