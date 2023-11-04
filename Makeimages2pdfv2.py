import os
from datetime import datetime
from PIL import Image, PngImagePlugin
import piexif
from reportlab.lib.pagesizes import letter, A4, landscape, portrait
from reportlab.pdfgen import canvas

PAPER_SIZES = {
    "A4": (8.27, 11.69),
    "Letter": (8.5, 11)
}

def rename_and_add_metadata(folder_path, author, copyright, prefix):
    """
    Function to rename image files and add metadata to them.

    Parameters:
    - folder_path (str): The directory path containing the image files.
    - Author (str): The author or creator of the images.
    - Copyright (str): Copyright statement for the images.
    - prefix (str): A prefix for the renamed files. Default is "Image".
    """
    
    # Define valid image file extensions
    valid_extensions = ['.jpeg', '.jpg', '.png']
    
    # Get list of image files in the folder
    image_files = [f for f in os.listdir(folder_path) if os.path.splitext(f)[-1].lower() in valid_extensions]
    
    # Sort the images
    image_files.sort()

    # Get the current date in YYYYMMDD format
    today = datetime.today().strftime('%Y%m%d')
    number = 1

    for image_file in image_files:
        file_path = os.path.join(folder_path, image_file)
        file_extension = os.path.splitext(image_file)[-1].lower()

        # Construct new file name using prefix, sequence number, and date
        new_name = f"{prefix}_{number}_{today}{file_extension}"
        new_path = os.path.join(folder_path, new_name)

        try:
            # Rename the file
            os.rename(file_path, new_path)
        except FileExistsError:
            print(f"File {new_name} already exists. Skipping renaming for this file.")
            continue

        try:
            with Image.open(new_path) as img:
                # Add metadata based on image file type
                if file_extension in ['.jpeg', '.jpg']:
                    # If the image has existing EXIF data, load it
                    if 'exif' in img.info:
                        exif_data = piexif.load(img.info['exif'])
                    else:
                        exif_data = {'0th': {}, 'Exif': {}, 'GPS': {}, '1st': {}}

                    # Set the Author and Copyright metadata fields
                    exif_data["0th"][piexif.ImageIFD.Artist] = author
                    exif_data["0th"][piexif.ImageIFD.Copyright] = copyright
                    
                    # Save the image with the new metadata
                    new_exif = piexif.dump(exif_data)
                    img.save(new_path, "JPEG", exif=new_exif)

                elif file_extension == '.png':
                    # For PNG images (which don't support EXIF), we'll add custom metadata
                    metadata = PngImagePlugin.PngInfo()
                    metadata.add_text("Author", author)
                    metadata.add_text("Copyright", copyright)
                    
                    # Save the PNG with the new metadata
                    img.save(new_path, "PNG", pnginfo=metadata)
        except Exception as e:
            print(f"Error processing {new_name}. Details: {str(e)}")
            continue

        number += 1  # Increment the image sequence number


def resize_images_for_print(folder_path, paper_size="Letter", orientation="portrait", dpi=300):
    """
    Resizes images in the specified folder to fit the given paper size and orientation, taking DPI into account.

    Parameters:
    - folder_path (str): Path to the folder containing images.
    - paper_size (str): Desired paper size ("A4" or "Letter"). Default is "A4".
    - orientation (str): Desired orientation ("portrait" or "landscape"). Default is "portrait".
    - dpi (int): Dots Per Inch for size calculation. Default is 300.

    Notes:
    - A4 dimensions are 8.27 x 11.69 inches.
    - Letter dimensions are 8.5 x 11 inches.
    """

    # Define paper dimensions in inches
    sizes = {
        "A4": (8.27, 11.69),
        "Letter": (8.5, 11)
    }

    # Check if the given paper size and orientation are valid
    if paper_size not in sizes:
        raise ValueError("Invalid paper size. Choose either 'A4' or 'Letter'.")
    if orientation not in ["portrait", "landscape"]:
        raise ValueError("Invalid orientation. Choose either 'portrait' or 'landscape'.")

    # Determine the width and height based on the orientation
    width, height = sizes[paper_size]
    if orientation == "landscape":
        width, height = height, width

    # Convert dimensions from inches to pixels
    width_px = int(width * dpi)
    height_px = int(height * dpi)

    # Define valid image file extensions for processing
    valid_extensions = ['.jpeg', '.jpg', '.png', '.bmp', '.gif', '.tiff']

    # Retrieve image files from the folder based on valid extensions
    image_files = [f for f in os.listdir(folder_path) if os.path.splitext(f)[-1].lower() in valid_extensions]

    for image_file in image_files:
        file_path = os.path.join(folder_path, image_file)
        
        with Image.open(file_path) as img:
            img_width, img_height = img.size

            # Check if the image already matches the desired dimensions
            if (img_width, img_height) == (width_px, height_px):
                print(f"Skipping {image_file} as it already matches the desired dimensions.")
                continue

            aspect = img_height / float(img_width)  # Calculate aspect ratio
            
            # Determine new dimensions based on aspect ratio
            if aspect > height / float(width):
                new_height = height_px
                new_width = int(new_height / aspect)
            else:
                new_width = width_px
                new_height = int(new_width * aspect)
                
            # Resize the image
            img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Save the resized image, overwriting the original
            img.save(file_path)


def convert_images_to_pdf(folder_path, output_filename, title, author, paper_size="Letter", orientation='portrait', margins=(50, 50), upscale=False, header_text="Header", footer_text="Footer"):
    
    valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']
    image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.splitext(f)[-1].lower() in valid_extensions]
    image_files.sort()

    if paper_size not in PAPER_SIZES:
        raise ValueError(f"Invalid paper size: {paper_size}. Supported sizes are: {', '.join(PAPER_SIZES.keys())}.")

    actual_paper_size = PAPER_SIZES[paper_size]
    page_size = landscape(actual_paper_size) if orientation == 'landscape' else portrait(actual_paper_size)

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
        print(f"Processing {image_path}...")
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
            print(f"Image {image_path} drawn to PDF.")
#        except Exception as e:
#        print(f"Error processing {image_path}. Details: {str(e)}")

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
if __name__ == "__main__":

    folder_path = 'f:\folder\images'
    prefix_text="_Image"
    title_text = "MyBook"
    author_text = "MyName"
    copyright_text = f"Copyright © 2023 {author_text}"
    paper_size="A4"
    orientation="portrait"
    output_pdf_name = title_text + '.pdf'

rename_and_add_metadata(folder_path, author_text, copyright_text,prefix_text)

resize_images_for_print(folder_path, paper_size, orientation)

convert_images_to_pdf(folder_path, output_pdf_name, title_text, author_text, paper_size, orientation, margins=(50, 50), upscale=True, header_text=title_text, footer_text=copyright_text)
