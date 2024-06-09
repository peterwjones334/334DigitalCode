# This code resizes images for filling standard page sizes

import os
from PIL import Image

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

# Example usage
if __name__ == "__main__":
    folder_path = 'c:\folder\images'
    resize_images_for_print(folder_path, paper_size="A4", orientation="portrait")
