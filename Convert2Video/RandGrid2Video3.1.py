""""
Title: Random Video Generation Script
Description: This script generates random binary grid images, creates title and credit images, and compiles them into a video.
Author: 334 Digital 
Date: 2024-05-16
Version: 3.1

Dependencies:
    - numpy
    - pillow (PIL)
    - opencv-python
    - uuid
    - shutil
    - datetime
    - os

Usage:
    Random2Video3.1.py

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
from PIL import Image, ImageDraw, ImageFont
import cv2
import os
import uuid
import shutil
from datetime import datetime

# Function to generate an image from a binary grid or text
def generate_image(content, filename, scaler, aspect_ratio, is_text=False, text="", font_size=8):
    if is_text:
        width, height = content
        img = Image.new('RGB', (width, height), color='black')
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()
        textbbox = draw.textbbox((0, 0), text, font=font)
        textwidth = textbbox[2] - textbbox[0]
        textheight = textbbox[3] - textbbox[1]
        x = (width - textwidth) / 2
        y = (height - textheight) / 2
        draw.text((x, y), text, font=font, fill="white")
    else:
        width, height = content.shape
        img = Image.fromarray(np.uint8(content * 255), 'L')

    img = img.resize((int(width * scaler * aspect_ratio), int(height * scaler)), Image.NEAREST)
    img.save(filename)
    print(f'Saved image: {filename}')

# Function to generate random binary grids and images
def generate_random_images(num_images, grid_size=(64, 64), image_dir='output_images', scaler=4, aspect_ratio=1.0):
    os.makedirs(image_dir, exist_ok=True)
    print(f'Output directory: {image_dir}')
    for i in range(num_images):
        grid = np.random.randint(0, 2, size=grid_size)
        filename = os.path.join(image_dir, f'image_{i}.jpg')
        generate_image(grid, filename, scaler, aspect_ratio)
    print(f'Generated {num_images} images in {image_dir}')

# Function to rename files in folder
def rename_files_in_folder(image_dir):
    for filename in os.listdir(image_dir):
        if os.path.isfile(os.path.join(image_dir, filename)) and filename.startswith('image'):
            name, ext = os.path.splitext(filename)
            new_name = f'image-{uuid.uuid4()}{ext}'
            old_file = os.path.join(image_dir, filename)
            new_file = os.path.join(image_dir, new_name)
            os.rename(old_file, new_file)
            print(f'Renamed {filename} to {new_name}')

# Function to create title and credits images
def create_title_and_credits(image_dir, grid_size, scaler, aspect_ratio, title_text, credits_text, title_duration, credits_duration, frame_rate):
    title_image_path = os.path.join(image_dir, 'title.jpg')
    credits_image_path = os.path.join(image_dir, 'credits.jpg')

    create_image_from_text(title_text, grid_size, title_image_path, scaler, aspect_ratio)
    create_image_from_text(credits_text, grid_size, credits_image_path, scaler, aspect_ratio)

    if not os.path.exists(title_image_path) or not os.path.exists(credits_image_path):
        print(f'Error: Title or credits image not found.')
        return

    num_title_frames = int(title_duration * frame_rate)
    num_credits_frames = int(credits_duration * frame_rate)

    for i in range(num_title_frames):
        shutil.copyfile(title_image_path, os.path.join(image_dir, f'title_{i:04d}.jpg'))
    for i in range(num_credits_frames):
        shutil.copyfile(credits_image_path, os.path.join(image_dir, f'credits_{i:04d}.jpg'))

    os.remove(title_image_path)
    os.remove(credits_image_path)

# Function to create an image from text
def create_image_from_text(text, size, filename, scaler, aspect_ratio):
    generate_image(size, filename, scaler, aspect_ratio, is_text=True, text=text)

# Function to convert images to video
def images_to_video(image_dir, output_file, frame_rate):
    title_files = sorted([f for f in os.listdir(image_dir) if f.startswith('title') and f.endswith('.jpg')])
    main_files = sorted([f for f in os.listdir(image_dir) if f.startswith('image') and f.endswith('.jpg')])
    credits_files = sorted([f for f in os.listdir(image_dir) if f.startswith('credits') and f.endswith('.jpg')])

    image_files = title_files + main_files + credits_files
    if not image_files:
        print("No images found in the directory.")
        return

    first_image_path = os.path.join(image_dir, image_files[0])
    frame = cv2.imread(first_image_path)
    if frame is None:
        print("Failed to read the first image.")
        return

    height, width, _ = frame.shape
    video = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (width, height))

    for image_file in image_files:
        image_path = os.path.join(image_dir, image_file)
        frame = cv2.imread(image_path)
        if frame is not None:
            video.write(frame)
        else:
            print(f"Failed to read image: {image_path}")

    video.release()
    print(f"Video saved as {output_file}")

# Function to clear image directory
def clear_image_dir(image_dir):
    for filename in os.listdir(image_dir):
        file_path = os.path.join(image_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print(f'Deleted file: {file_path}')
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

# Parameters
work_dir = 'C:\\Workspace\\ProjectXX\\'
image_dir = os.path.join(work_dir, 'test\\')
vidname = f"vid_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
output_video_file = os.path.join(work_dir, vidname)

# Grid size, scaler, and aspect ratio
grid_size = (64, 64)
scaler = 2
aspect_ratio = 1.0

# Video duration and frame rate
duration = 10 # seconds
frame_rate = 30

# Calculate the number of images needed based on duration and frame rate
num_images = duration * frame_rate

# Generate random images
generate_random_images(num_images, grid_size=grid_size, image_dir=image_dir, scaler=scaler, aspect_ratio=aspect_ratio)

# Title and credits duration
title_duration = 2
credits_duration = 1
# Create title and credits images
title_text = vidname
credits_text = "334D"

create_title_and_credits(image_dir, grid_size, scaler, aspect_ratio, title_text, credits_text, title_duration, credits_duration, frame_rate)

# Rename image files
rename_files_in_folder(image_dir)

# Create video from images
images_to_video(image_dir, output_video_file, frame_rate)

# Clear the image directory
clear_image_dir(image_dir)
