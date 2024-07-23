import fitz  # PyMuPDF
import zipfile
import os
import shutil

def extract_pdf_pages_to_images(pdf_path, output_folder):
    """
    Extracts each page of a PDF and saves it as a JPEG image in the specified folder.
    Args:
    pdf_path (str): Path to the PDF file.
    output_folder (str): Directory to save the JPEG images.
    """
    try:
        os.makedirs(output_folder, exist_ok=True)
        document = fitz.open(pdf_path)
        for page_number in range(document.page_count):
            page = document.load_page(page_number)
            pix = page.get_pixmap()
            img_path = os.path.join(output_folder, f"page_{page_number + 1}.jpg")
            pix.save(img_path)
        document.close()
    except Exception as e:
        print(f"An error occurred: {e}")

def create_cbr_from_images(output_folder, pdf_folder, pdf_name):
    """
    Creates a CBR file from all JPEG images in the specified folder and clears the folder afterwards.
    Args:
    output_folder (str): Folder containing the JPEG images.
    pdf_folder (str): Folder containing the original PDF.
    pdf_name (str): Base name of the PDF file used to name the CBR file.
    """
    try:
        jpeg_files = sorted([f for f in os.listdir(output_folder) if f.endswith('.jpg')])
        if not jpeg_files:
            print("No JPEG files found in the folder.")
            return
        cbr_filename = os.path.join(pdf_folder, f"{pdf_name}.cbr")
        with zipfile.ZipFile(cbr_filename, 'w') as cbr_archive:
            for file in jpeg_files:
                cbr_archive.write(os.path.join(output_folder, file), arcname=file)
        print(f"CBR file created: {cbr_filename}")
        # Clear the dump folder after creating the CBR
        for file in jpeg_files:
            os.remove(os.path.join(output_folder, file))
    except Exception as e:
        print(f"An error occurred: {e}")

# Usage
pdf_name = "test"
pdf_folder = 'D:\\Process\\Project43'
pdf_file_path = os.path.join(pdf_folder, f"{pdf_name}.pdf")
output_directory = 'D:\\dump'

extract_pdf_pages_to_images(pdf_file_path, output_directory)
create_cbr_from_images(output_directory, pdf_folder, pdf_name)
