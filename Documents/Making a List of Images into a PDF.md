# Making a list of Images into a PDF 

## Resizing Images

This script that will upscale and resize images so they fit appropriately on an A4 page when printed. For print quality, we typically aim for a resolution of at least 300 DPI (dots per inch).

The dimensions of an A4 page are 210 x 297 millimeters. 
At 300 DPI, this equates to 2480 x 3508 pixels. 
We'll resize each image to be within these dimensions while preserving the original aspect ratio.

```python
import os
from PIL import Image

def resize_images_for_a4(folder_path, dpi=300):
    # A4 dimensions in pixels at the specified DPI
    a4_width = 8.27 * dpi  # 8.27 inches x 300 DPI
    a4_height = 11.69 * dpi  # 11.69 inches x 300 DPI
    
    # Scan through the directory for image files
    valid_extensions = ['.jpeg', '.jpg', '.png', '.bmp', '.gif', '.tiff']
    image_files = [f for f in os.listdir(folder_path) if os.path.splitext(f)[-1].lower() in valid_extensions]

    for image_file in image_files:
        file_path = os.path.join(folder_path, image_file)
        with Image.open(file_path) as img:
            img_width, img_height = img.size
            aspect = img_height / float(img_width)
            
            # Calculate new dimensions based on the aspect ratio
            if aspect > 1:
                # Portrait orientation
                new_height = int(a4_height)
                new_width = int(new_height / aspect)
            else:
                # Landscape orientation or square
                new_width = int(a4_width)
                new_height = int(new_width * aspect)
                
            img = img.resize((new_width, new_height), Image.LANCZOS)
            img.save(file_path)

# Example usage:
folder_path = '/path/to/your/image/folder'
resize_images_for_a4(folder_path)
```


## Convert Images to Single PDF

This code scans a folder full of images and then converts all the images into a single PDF , one image on each page. 

The codes uses the `Pillow` library for image processing and the `reportlab` library to create the PDF. 

Here's a Python script to accomplish this:

1. First, install the required libraries:

```bash
pip install Pillow reportlab
```

2. Use the following Python script:

```python
import os
from PIL import Image
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas

def convert_images_to_pdf(folder_path, output_filename):
    # Get all files from the specified folder
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    # Filter only the image files
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'))]
    
    # Sort the images by their filename (if necessary)
    image_files.sort()

    # Create a new PDF file
    c = canvas.Canvas(output_filename, pagesize=landscape(letter))

    for image_path in image_files:
        img = Image.open(image_path)
        img_width, img_height = img.size
        aspect = img_height / float(img_width)
        width = landscape(letter)[0]
        height = aspect * width
        
        # Center the image on the page
        x_offset = (landscape(letter)[0] - width) / 2
        y_offset = (landscape(letter)[1] - height) / 2

        c.drawInlineImage(image_path, x_offset, y_offset, width=width, height=height)
        c.showPage()

    c.save()

# Example usage:
folder_path = '/path/to/your/image/folder'
output_pdf_name = 'output.pdf'
convert_images_to_pdf(folder_path, output_pdf_name)
```

Make sure to replace `'/path/to/your/image/folder'` with the path to your folder containing the images.

This script will scan the specified folder for image files, then convert all found images into a single PDF, placing one image on each page. 


## Positioning Images on the Page

To center the image, you need to adjust both the `x_offset` and `y_offset` to take into account the `new_width` and `new_height` of the image relative to the page size and available space.

Also some optimization to the code:

1. Simplify the gathering of image file paths.
2. Adjust calculations to reduce redundant operations.
3. Make use of `os.path.splitext` to determine the file extension.
4. Ensured that resources (images) are released after processing each one by using the `with` statement.

Here's an optimized version:

```python
import os
from PIL import Image
from reportlab.lib.pagesizes import letter, A4, landscape, portrait
from reportlab.pdfgen import canvas

def convert_images_to_pdf(folder_path, output_filename, page_size=letter, orientation='portrait', margins=(50, 50), upscale=False, header_text="Header", footer_text="Footer"):
    
    # Simplified method to get image files
    valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']
    image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.splitext(f)[-1].lower() in valid_extensions]

    # Sort the images by their filename
    image_files.sort()

    # Set orientation
    page_size = landscape(page_size) if orientation == 'landscape' else portrait(page_size)

    # Create a new PDF file
    c = canvas.Canvas(output_filename, pagesize=page_size)
    
    page_number = 1

    for image_path in image_files:
        with Image.open(image_path) as img:  # Using with to ensure resources are released
            img_width, img_height = img.size
            aspect = img_height / float(img_width)

            # Calculate dimensions taking margins into account
            available_width = page_size[0] - 2 * margins[0]
            available_height = page_size[1] - 2 * margins[1] - 30  # Adjusting for header height

            new_width = available_width
            new_height = aspect * available_width
            
            if new_height > available_height or (upscale and new_height < available_height):
                new_height = available_height
                new_width = new_height / aspect

            # Center the image on the page with margins
            x_offset = (page_size[0] - new_width) / 2
            y_offset = (page_size[1] - new_height) - margins[1] - 30  # Start image below the header

            c.drawInlineImage(image_path, x_offset, y_offset, width=new_width, height=new_height)

        # Drawing header, footer, page number
        header_x = page_size[0] / 2
        header_y = page_size[1] - margins[1]
        
        c.drawCentredString(header_x, header_y, header_text)
        c.line(margins[0], header_y - 15, page_size[0] - margins[0], header_y - 15)
        c.drawString(margins[0], margins[1] - 15, footer_text)
        c.drawRightString(page_size[0] - margins[0], margins[1] - 15, f"Page {page_number}")
        
        c.showPage()
        page_number += 1

    c.save()

# Example usage:
folder_path = '/path/to/your/image/folder'
output_pdf_name = 'output.pdf'
convert_images_to_pdf(folder_path, output_pdf_name, page_size=A4, orientation='landscape', margins=(50, 50), upscale=True, header_text="My Custom Header", footer_text="My Custom Footer")
```

## Add Headers and Footers

I've added parameters for header_text and footer_text which you can customize for your PDF. The page numbers will be displayed on the bottom right of each page. Adjust the positions, fonts, and styles as necessary for your specific requirement.

Here's the enhanced script:

```python
import os
from PIL import Image
from reportlab.lib.pagesizes import letter, A4, landscape, portrait
from reportlab.pdfgen import canvas

def convert_images_to_pdf(folder_path, output_filename, page_size=letter, orientation='portrait', margins=(50, 50), upscale=False, header_text="Header", footer_text="Footer"):
    # Get all files from the specified folder
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    # Filter only the image files
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'))]
    
    # Sort the images by their filename (if necessary)
    image_files.sort()

    # Set orientation
    if orientation == 'landscape':
        page_size = landscape(page_size)
    else:
        page_size = portrait(page_size)

    # Create a new PDF file
    c = canvas.Canvas(output_filename, pagesize=page_size)
    
    page_number = 1

    for image_path in image_files:
        img = Image.open(image_path)
        img_width, img_height = img.size
        aspect = img_height / float(img_width)

        # Calculate dimensions taking margins into account
        available_width = page_size[0] - 2 * margins[0]
        available_height = page_size[1] - 2 * margins[1]

        new_width = available_width
        new_height = aspect * available_width
        
        if new_height > available_height or (upscale and new_height < available_height):
            new_height = available_height
            new_width = new_height / aspect

        # Center the image on the page with margins
        x_offset = (page_size[0] - new_width) / 2
        y_offset = (page_size[1] - new_height) / 2

        c.drawInlineImage(image_path, x_offset, y_offset, width=new_width, height=new_height)

        # Draw header and footer
        c.drawString(margins[0], page_size[1] - margins[1], header_text)
        c.drawString(margins[0], margins[1] - 15, footer_text)

        # Draw page number
        page_text = "Page %s" % page_number
        c.drawRightString(page_size[0] - margins[0], margins[1] - 15, page_text)
        
        c.showPage()
        page_number += 1

    c.save()

# Example usage:
folder_path = '/path/to/your/image/folder'
output_pdf_name = 'output.pdf'
convert_images_to_pdf(folder_path, output_pdf_name, page_size=A4, orientation='landscape', margins=(50, 50), upscale=True, header_text="My Custom Header", footer_text="My Custom Footer")
```

## Writing Properities into the PDF

Writing properties to a PDF refers to setting the document's metadata, such as the author, title, and other properties.
The `canvas` object from `reportlab` allows you to set several of these properties.

Here are some common properties you can set:

- `setTitle()`: Sets the title of the PDF.
- `setAuthor()`: Sets the author's name.
- `setSubject()`: Sets the subject of the PDF.
- `setKeywords()`: Sets keywords for the PDF.

I'll add an example of how to set these properties into your code:

```python
def convert_images_to_pdf(folder_path, output_filename, title, page_size=letter, orientation='portrait', margins=(50, 50), upscale=False, header_text="Header", footer_text="Footer"):
    # ... [rest of your code before creating the canvas]

    c = canvas.Canvas(output_filename, pagesize=page_size)

    # Setting PDF properties
    c.setTitle(title)
    c.setAuthor("Your Name")
    c.setSubject("Images converted to PDF")
    c.setKeywords(["Images", "PDF", "Conversion"])

    # ... [rest of your code for processing images and generating pages]

    c.save()

# ... [rest of your existing code]
```

Replace `"Your Name"` with the desired author's name. Similarly, you can adjust the subject and keywords as per your needs.




