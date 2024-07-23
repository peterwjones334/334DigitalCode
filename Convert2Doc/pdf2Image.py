import fitz  # PyMuPDF
import logging
import multiprocessing
import os
import shutil
import zipfile
import psutil
import time

# Setup logging configuration
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("processing_log.log"),
                        logging.StreamHandler()
                    ])

def process_single_pdf(pdf_file_path, pdf_folder):
    """
    Processes a single PDF file: extracts images and creates a CBZ archive.
    Args:
    pdf_file_path (str): Full path to the PDF file.
    pdf_folder (str): Directory where the PDF resides and output will be stored.
    """
    # Create a unique temporary directory for each process using the base name and a timestamp
    pdf_name = os.path.splitext(os.path.basename(pdf_file_path))[0]
    temp_dir_name = f"{pdf_name}_{int(time.time())}"
    output_directory = os.path.join(pdf_folder, temp_dir_name)  # Unique temporary folder for images
    os.makedirs(output_directory)  # Ensure the output directory is created

    extract_pdf_pages_to_images(pdf_file_path, output_directory)
    create_cbz_from_images(output_directory, pdf_folder, pdf_name)
    shutil.rmtree(output_directory)  # Clean up after CBZ creation

def extract_pdf_pages_to_images(pdf_path, output_folder, resolution=150):
    initial_memory = psutil.virtual_memory().used  # Memory usage before processing
    try:
        with fitz.open(pdf_path) as document:
            for page_number in range(document.page_count):
                page = document.load_page(page_number)
                mat = fitz.Matrix(resolution / 72, resolution / 72)
                pix = page.get_pixmap(matrix=mat, colorspace='RGB')
                img_path = os.path.join(output_folder, f"page_{page_number + 1:04d}.jpg")
                pix.save(img_path)
        logging.info(f"Extracted and saved images from {pdf_path}")
    except Exception as e:
        logging.error(f"An error occurred while processing {pdf_path}: {e}")
    final_memory = psutil.virtual_memory().used
    logging.debug(f"Memory used for processing {pdf_path}: {final_memory - initial_memory} bytes")

def create_cbz_from_images(output_folder, pdf_folder, pdf_name):
    try:
        jpeg_files = sorted([f for f in os.listdir(output_folder) if f.lower().endswith(('.jpg', '.jpeg'))])
        if not jpeg_files:
            logging.warning(f"No JPEG files found in the folder {output_folder}")
            return
        cbz_filename = os.path.join(pdf_folder, f"{pdf_name}.cbz")
        with zipfile.ZipFile(cbz_filename, 'w') as cbz_archive:
            for file in jpeg_files:
                cbz_archive.write(os.path.join(output_folder, file), arcname=file)
        logging.info(f"CBZ file created: {cbz_filename}")
    except Exception as e:
        logging.error(f"An error occurred while creating CBZ file {pdf_name}: {e}")

def process_pdf_directory(pdf_folder):
    pdf_files = [os.path.join(pdf_folder, f) for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    pool.starmap(process_single_pdf, [(pdf_path, pdf_folder) for pdf_path in pdf_files])
    pool.close()
    pool.join()

if __name__ == '__main__':
    # This block ensures that the script can be safely imported and run as a standalone script.
    pdf_folder = 'D:\\Process\\Project44'  # Folder containing PDF files
    process_pdf_directory(pdf_folder)
