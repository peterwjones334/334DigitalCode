# This script renames images in folder and adds metadata

import os
from datetime import datetime
from PIL import Image, PngImagePlugin
import piexif

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

# Example usage:
folder_path = 'c:\folder\images'
prefix_text="_Image"
Author_text = "Your Name Here"
Copyright_text = f"Copyright © 2023 {Author_text}"
rename_and_add_metadata(folder_path, Author_text, Copyright_text,prefix_text)

