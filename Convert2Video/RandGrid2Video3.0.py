""""
Title: Random Video Generation Script
Description: This script generates random binary grid images, creates title and credit images, and compiles them into a video.
Author: 334 Digital 
Date: 2024-05-15
Version: 3.0

Dependencies:
    - numpy
    - pillow (PIL)
    - opencv-python
    - uuid
    - shutil
    - datetime
    - os

Usage:
    RandGrid2Video3.0.py

License:
    MIT License

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
import numpy as np
from PIL import Image
# import itertools
import cv2
import os
import uuid
from datetime import datetime

# Function to generate an image from a binary grid
def generate_image(grid, filename):
    img = Image.fromarray(np.uint8(grid * 255), 'L')
    img = img.resize((64, 64), Image.NEAREST)  # Upscale for better visibility
    img.save(filename)
    print(f'Saved image: {filename}')  # Debug print to confirm image saving

# Function to generate random binary grids and images
def generate_random_images(num_images, grid_size=(256, 256), image_dir='output_images'):
    os.makedirs(image_dir, exist_ok=True)
    print(f'Output directory: {image_dir}')  # Debug print to confirm directory creation
    for i in range(num_images):
        grid = np.random.randint(0, 2, size=grid_size)
        filename = os.path.join(image_dir, f'image_{i}.jpg')
        generate_image(grid, filename)
    print(f'Generated {num_images} images in {image_dir}')

def rename_files_in_folder(image_dir):
    """Rename all files in the specified folder with UUID names."""
    for filename in os.listdir(image_dir):
        # Check if it's a file and not a folder
        if os.path.isfile(os.path.join(image_dir, filename)):
            # Split the filename into name and extension
            name, ext = os.path.splitext(filename)
            # Generate a new UUID name and add the original extension
            new_name = str(uuid.uuid4()) + ext
            # Construct full file paths
            old_file = os.path.join(image_dir, filename)
            new_file = os.path.join(image_dir, new_name)
            # Rename the file
            os.rename(old_file, new_file)
            print(f'Renamed {filename} to {new_name}')

def images_to_video(image_dir, output_file, frame_rate):
    # Get all image files in the input directory
    image_files = [f for f in sorted(os.listdir(image_dir)) if f.endswith(('.png', '.jpg', '.jpeg', '.JPG'))]

    # Check if there are any images
    if not image_files:
        print("No images found in the directory.")
        return

    # Read the first image to get the dimensions
    first_image_path = os.path.join(image_dir, image_files[0])
    frame = cv2.imread(first_image_path)
    if frame is None:
        print("Failed to read the first image.")
        return

    height, width, layers = frame.shape
    size = (width, height)

    # Initialize the video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Specify the codec
    video = cv2.VideoWriter(output_file, fourcc, frame_rate, size)

    # Iterate over each image file
    for image_file in image_files:
        image_path = os.path.join(image_dir, image_file)
        frame = cv2.imread(image_path)
        if frame is not None:
            video.write(frame)
        else:
            print(f"Failed to read image: {image_path}")

    # Release the video writer
    video.release()
    print(f"Video saved as {output_file}")

def clear_image_dir(image_dir):
    """Clear all files in the specified folder."""
    for filename in os.listdir(image_dir):
        file_path = os.path.join(image_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print(f'Deleted file: {file_path}')
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

if __name__ == "__main__":
# Parameters
    work_dir = 'D:\\process\\project54\\'
    image_dir = os.path.join(work_dir, 'test\\')  # Directory containing the images
    output_video_file = os.path.join(work_dir, f"vid_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")  # Output video file path with datetime stamp

    # Generate a sample of images
    generate_random_images(100, image_dir=image_dir)

    # Randomize filename of images (option)
    rename_files_in_folder(image_dir)

    # Create the video
    frame_rate = 30  # Frames per second
    images_to_video(image_dir, output_video_file, frame_rate)

    # Clear the image directory
    clear_image_dir(image_dir)
