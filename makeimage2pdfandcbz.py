import os
import uuid
import zipfile
import shutil
from datetime import datetime
from PIL import Image, PngImagePlugin
import piexif
from reportlab.lib.pagesizes import letter, A4, landscape, portrait
from reportlab.lib.colors import Color, black, HexColor
from reportlab.pdfgen import canvas

# Global constants
# VALID_IMAGE_EXTENSIONS = ['.jpeg', '.jpg', '.png', '.bmp', '.gif', '.tiff']

# def get_image_files_from_folder(folder_path):
#    """Return list of image files in the specified folder."""
#    return [f for f in os.listdir(folder_path) if os.path.splitext(f)[-1].lower() in VALID_IMAGE_EXTENSIONS]

def get_image_files_from_folder(folder_path):
    """Helper function to get sorted list of image files from the folder, excluding PNG files."""
    allowed_extensions = ['.jpeg', '.jpg']
    image_files = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in allowed_extensions]
    return sorted(image_files)

def find_and_move_cover_to_front(image_files):
    """Find the cover image by filename and move it to the beginning of the list."""
    cover_image = None
    for i, file_path in enumerate(image_files):
        filename = os.path.basename(file_path)
        if filename.lower().startswith('cover'):
            cover_image = image_files.pop(i)
            break
    if cover_image:
        image_files.insert(0, cover_image)
    return image_files

def convert_png_to_jpeg(folder_path):
    for filename in os.listdir(folder_path):
        # Skip files that start with an underscore
        #if filename.startswith('_'):
        #    continue

        if filename.endswith('.png'):
            img_path = os.path.join(folder_path, filename)
            img = Image.open(img_path)
            rgb_img = img.convert('RGB')  # Convert to RGB
            new_filename = filename[:-4] + '.jpeg'
            new_img_path = os.path.join(folder_path, new_filename)
            rgb_img.save(new_img_path, 'jpeg')
            print(f'Converted {filename} to {new_filename}')

            # Rename the original PNG file
            new_png_filename = "_" + filename
            new_png_path = os.path.join(folder_path, new_png_filename)
            os.rename(img_path, new_png_path)
            print(f'Renamed {filename} to {new_png_filename}')

def convert_jpeg_to_png(folder_path):
    for filename in os.listdir(folder_path):
        # Skip files that start with an underscore
        if filename.startswith('_'):
            continue

        if filename.lower().endswith('.jpeg') or filename.lower().endswith('.jpg'):
            img_path = os.path.join(folder_path, filename)
            img = Image.open(img_path)
            new_filename = filename[:-5] if filename.lower().endswith('.jpeg') else filename[:-4]
            new_filename += '.png'
            new_img_path = os.path.join(folder_path, new_filename)
            img.save(new_img_path, 'png')
            print(f'Converted {filename} to {new_filename}')

            # Rename the original JPEG file
            new_jpeg_filename = "_" + filename
            new_jpeg_path = os.path.join(folder_path, new_jpeg_filename)
            os.rename(img_path, new_jpeg_path)
            print(f'Renamed {filename} to {new_jpeg_filename}')

def rename_and_add_metadata(folder_path, author, copyright, prefix):
    """
    Function to rename image files and add metadata to them.

    Parameters:
    - folder_path (str): The directory path containing the image files.
    - Author (str): The author or creator of the images.
    - Copyright (str): Copyright statement for the images.
    - prefix (str): A prefix for the renamed files. Default is "Image".
    """
    image_files = get_image_files_from_folder(folder_path)
    image_files.sort()

    # Get the current date in YYYYMMDD format
    today = datetime.today().strftime('%Y%m%d')
    number = 1

    for image_file in image_files:
        # Skip files that start with an underscore
        if image_file.startswith('_'):
            continue

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

def rename_files_in_folder(folder_path):
    """Rename all files in the specified folder with UUID names, only if they are JPEG, JPG, or PNG files."""
    # Define the allowed extensions
    allowed_extensions = {'.jpeg', '.jpg', '.png'}
    
    for filename in os.listdir(folder_path):
        # Check if it's a file and not a folder
        if os.path.isfile(os.path.join(folder_path, filename)):
            # Split the filename into name and extension
            name, ext = os.path.splitext(filename)
            # Convert extension to lowercase for case-insensitive comparison
            ext = ext.lower()
            
            # Check if the file has one of the allowed extensions
            if ext in allowed_extensions:
                # Generate a new UUID name and add the original extension
                new_name = str(uuid.uuid4()) + ext
                # Construct full file paths
                old_file = os.path.join(folder_path, filename)
                new_file = os.path.join(folder_path, new_name)
                # Rename the file
                os.rename(old_file, new_file)
                print(f'Renamed {filename} to {new_name}')

# rename files in order

def rename_files_in_numerical_order(folder_path):
    """Rename JPEG, JPG, and PNG files in the specified folder in numerical order."""
    # Define the allowed extensions
    allowed_extensions = {'.jpeg', '.jpg'}
    
    # List all files in the directory and filter by allowed extensions
    files = [file for file in sorted(os.listdir(folder_path)) 
             if os.path.splitext(file)[1].lower() in allowed_extensions]

    # Rename files in numerical order
    for index, file in enumerate(files, start=1):
        old_path = os.path.join(folder_path, file)
        new_filename = f"{index:03d}{os.path.splitext(file)[1]}"
        new_path = os.path.join(folder_path, new_filename)
        os.rename(old_path, new_path)
        print(f"Renamed '{file}' to '{new_filename}'")

        

def resize_images_for_print(folder_path, paper_size="A4", orientation="portrait", dpi=300):
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

    # Retrieve image files from the folder based on valid extensions
    image_files = get_image_files_from_folder(folder_path)

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

def convert_images_to_pdf(folder_path, output_filename=None, title='Untitled', author='Unknown', publisher='Unknown', page_size=A4, orientation='portrait', margins=(50, 50), upscale=False, header_text='Header', footer_text='Footer', background_color=""):
    # If no specific output_filename is provided, use the folder name
    if not output_filename:
        output_filename = os.path.basename(folder_path) + '.pdf'
    
    output_filename = os.path.join(folder_path, output_filename)
    
    image_files = [os.path.join(folder_path, f) for f in get_image_files_from_folder(folder_path)]
    # image_files.sort()

    # Find the cover image and move it to the beginning of the list, if it exists
    image_files = find_and_move_cover_to_front(image_files)

    width, height = page_size # Default page size (8.5 * 11 inches)
    page_size = landscape(page_size) if orientation == 'landscape' else portrait(page_size)
    # Convert the background color from hex to ReportLab color
    bg_color = HexColor(background_color)

    c = canvas.Canvas(output_filename, pagesize=page_size)
    # Set the background color
    c.setFillColor(bg_color)
    c.rect(0, 0, width, height, fill=1)

    page_number = 1


    # Title Page
    c.setFillColorRGB(0.784, 0.784, 0.784)  # light Grey
    c.setFont("Helvetica", 16)
    c.drawCentredString(page_size[0] / 2, page_size[1] / 2, title)
    c.setFont("Helvetica", 12)
    c.drawCentredString(page_size[0] / 2, page_size[1] / 2 - 30, author)  # Adjusting position for author below title
    c.showPage()

    # Blank page after title
    c.showPage()
    
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
        c.setFillColor(bg_color)
        c.setFillColorRGB(0.784, 0.784, 0.784)  # light Grey
        c.setFont("Helvetica", 16)
        c.drawCentredString(header_x, header_y, header_text)
        c.line(margins[0], header_y - 15, page_size[0] - margins[0], header_y - 15)
        c.drawString(margins[0], margins[1] - 15, footer_text)
        c.drawRightString(page_size[0] - margins[0], margins[1] - 15, f"Page {page_number}")
        
        c.showPage()
        page_number += 1

    # Blank page after images
    c.showPage()

    # Back Cover
    c.setFillColor(bg_color)
    c.rect(0, 0, width, height, fill=1)  # Set the background
    c.setFillColorRGB(0.784, 0.784, 0.784)  # Set the text color to light grey
    # Set the font size for the title
    c.setFont("Helvetica", 16)
    c.drawCentredString(page_size[0] / 2, page_size[1] / 2 + 30, title)  # Position the title higher
    # Set the font size for author and publisher
    c.setFont("Helvetica", 12)
    c.drawCentredString(page_size[0] / 2, page_size[1] / 2, author)  # Center position for author
    c.drawCentredString(page_size[0] / 2, page_size[1] / 2 - 30, publisher)  # Position publisher below author
    # Draw footer text below the publisher
    c.drawCentredString(page_size[0] / 2, page_size[1] / 2 - 60, footer_text)  # Position footer text further down
    c.showPage()  # Add a new page or end this page 


    # Setting PDF properties
    c.setTitle(title)
    c.setAuthor(author)
    c.setCreator(publisher)
    # c.setLicense(footer_text)
    # c.setPermissions()
    c.setProducer("makepdf.py with reportlab")
    c.setSubject("Catalogue of Images")
    c.setKeywords(["Images","Catalogue", "Art Book" ,"GAI content", "NSFW", title, author, publisher])
    c.save()

# Create cbz file

def create_cbz_file(folder_path, title_text=None):
# Extract folder name if title_text is not provided
    if not title_text:
        title_text = os.path.basename(folder_path)
    
    # Construct the full path for the temporary ZIP file
    temp_zip_path = os.path.join(os.path.dirname(folder_path), f"{title_text}.zip")
    
    # Create ZIP archive
    with zipfile.ZipFile(temp_zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in sorted(os.listdir(folder_path)):
            # Only add image files to the archive
            if file.lower().endswith(('.jpeg', '.jpg')):
                file_path = os.path.join(folder_path, file)
                zf.write(file_path, arcname=file)
                print(f"Added '{file}' to ZIP archive")
    
    # Construct the full path for the final CBR file
    cbr_path = os.path.join(os.path.dirname(folder_path), f"{title_text}.cbz")
    
    # Rename ZIP file to CBR
    shutil.move(temp_zip_path, cbr_path)
    print(f"Created CBR file: {cbr_path}")

def select_license(commercial_use, allow_derivatives, share_alike):
    if not commercial_use and not allow_derivatives:
        return "CC BY-NC-ND (Attribution-NonCommercial-NoDerivs)"
    elif not commercial_use and allow_derivatives and share_alike:
        return "CC BY-NC-SA (Attribution-NonCommercial-ShareAlike)"
    elif not commercial_use and allow_derivatives and not share_alike:
        return "CC BY-NC (Attribution-NonCommercial)"
    elif commercial_use and not allow_derivatives:
        return "CC BY-ND (Attribution-NoDerivs)"
    elif commercial_use and allow_derivatives and share_alike:
        return "CC BY-SA (Attribution-ShareAlike)"
    elif commercial_use and allow_derivatives and not share_alike:
        return "CC BY (Attribution)"
    else:
        return "Public Domain (CC0)"

def select_copyright_statement(year_of_publication, Author_text, License):
    # Define the two copyright statements
    copyright_statement_0 = f"(CC0 1.0 Universal) {year_of_publication} {Author_text}"
    copyright_statement_1 = f"© {year_of_publication} {Author_text} {License}"
    copyright_statement_2 = f"Copyright {year_of_publication} by {Author_text}. All Rights Reserved"

    # Condition to choose the copyright statement
    if License == "Public Domain (CC0)":
        selected_statement = copyright_statement_0
    # choose statement 2 if the publication year is after 2020, else choose statement 1
    elif year_of_publication > 2020:
        selected_statement = copyright_statement_1
    else:
        selected_statement = copyright_statement_2

    return selected_statement        

# Example usage:
if __name__ == "__main__":
    folder_path = 'C:\\WorkArea\\ProjectX'
    title_text = "MyBook"
    background_color = "#000000"
    prefix_text="PAGE_"
    Publisher_text="My Publisher" 
    Author_text = "My Name"
    year_of_publication = 2024
    License = (select_license(commercial_use=True, allow_derivatives=True, share_alike=True))
    copyright_statement = select_copyright_statement(year_of_publication, Author_text, License)
    Copyright_text = copyright_statement

    output_pdf_name = title_text + '.pdf'

convert_png_to_jpeg(folder_path)

# convert_jpeg_to_png(folder_path) 

rename_files_in_folder(folder_path)

# rename_and_add_metadata(folder_path, Author_text, Copyright_text,prefix_text)

resize_images_for_print(folder_path, paper_size="A4", orientation="portrait")

convert_images_to_pdf(folder_path, output_pdf_name, title_text, Author_text, Publisher_text, page_size=A4, orientation='portrait', margins=(50, 50), upscale=True, header_text=title_text, footer_text=Copyright_text, background_color="#000000")

# rename_files_in_numerical_order(folder_path)

create_cbz_file(folder_path, title_text)