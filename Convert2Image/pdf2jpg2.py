import fitz  # Import the PyMuPDF library, make sure to install it using pip
import os

def extract_pages_as_jpeg(pdf_path, base_output_folder):
    # Extract the base name of the PDF file without the extension
    pdf_name = os.path.basename(pdf_path)
    pdf_name_without_ext = os.path.splitext(pdf_name)[0]
    
    # Create a new folder for the output based on the PDF name
    output_folder = os.path.join(base_output_folder, pdf_name_without_ext)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Open the PDF file
    doc = fitz.open(pdf_path)
    
    # Iterate through each page
    for i in range(len(doc)):
        page = doc.load_page(i)  # Get the page
        pix = page.get_pixmap()  # Render page to an image
        
        # Define the output image file name
        output_image_path = f"{output_folder}/page_{i + 1:03d}.jpeg"
        
        # Save the image
        pix.save(output_image_path)
    
    print(f"All pages have been extracted as JPEG images into '{output_folder}'.")
    
    # Close the document
    doc.close()

# Specify the path to your PDF file
pdf_path = 'D:\\Process\\Project42\\Mass Transit.pdf'

# Specify the base path for the output folder where the JPEG images will be saved
base_output_folder = 'D:\\Process\\Project42\Convert'

# Call the function
extract_pages_as_jpeg(pdf_path, base_output_folder)
