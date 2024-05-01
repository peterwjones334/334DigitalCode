from pdf2image import convert_from_path
import os

def convert_pdf_to_jpg(pdf_path, output_folder):
    # Ensure the output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Convert PDF to a list of images
    images = convert_from_path(pdf_path)

    # Save each page as a JPEG file
    for i, image in enumerate(images):
        output_file = os.path.join(output_folder, f"page_{i + 1:03d}.jpg")
        image.save(output_file, 'JPEG')
        print(f"Saved '{output_file}'")

    print("Finished extracting pages.")

# Specify the path to your PDF file
pdf_path = 'C:\\WorkArea\\ProjectX\\test.pdf'

# Specify the path to the output folder where the JPEG images will be saved
output_folder = 'C:\\WorkArea\\ProjectX\\Images'

# Run the function
convert_pdf_to_jpg(pdf_path, output_folder)
