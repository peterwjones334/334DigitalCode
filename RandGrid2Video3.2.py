""""
Title: Random Video Generation Script
Description: This script generates random binary grid images, creates title and credit images, and compiles them into a video and uploads therm to Youtube.
Author: 334 Digital 
Date: 2024-05-17
Version: 3.2

Dependencies:
    - numpy
    - pillow (PIL)
    - opencv-python
    - uuid
    - shutil
    - datetime
    - os
    - google.auth
    - googleapiclient

Usage:
    RandGrid2Video3.2.py

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

import google.auth
import google.auth.transport.requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

# Path to your client_secret.json file
CLIENT_SECRET_FILE = 'client_secret.json' # co-locate this in in teh script directory, o call form a path.
# This OAuth 2.0 access scope allows for full read/write access to the authenticated user's account.
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# Function to generate an image from a binary grid or text
def generate_image(content, filename, scaler, aspect_ratio, is_text=False, text=""):
    width, height = content.shape if not is_text else content
    img = Image.new('L', (width, height), color=0) if not is_text else Image.new('RGB', (width, height), color='black')
    
    if is_text:
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 8)
        except IOError:
            font = ImageFont.load_default()
        textbbox = draw.textbbox((0, 0), text, font=font)
        textwidth = textbbox[2] - textbbox[0]
        textheight = textbbox[3] - textbbox[1]
        x = (width - textwidth) / 2
        y = (height - textheight) / 2
        draw.text((x, y), text, font=font, fill="white")
    else:
        img = Image.fromarray(np.uint8(content * 255), 'L')
    
    img = img.resize((width * scaler, height * scaler), Image.NEAREST)
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


def authenticate_youtube():
    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    youtube = googleapiclient.discovery.build('youtube', 'v3', credentials=credentials)
    return youtube

def upload_video(youtube, video_title, video_description, video_tags, video_category, video_status, output_video_file):
    request_body = {
        'snippet': {
            'title': video_title,
            'description': video_description,
            'tags': video_tags,
            'categoryId': video_category,
        },
        'status': {
            'privacyStatus': video_status,  # Set video privacy status (public, private, unlisted)
            'madeForKids': '1',
            'selfDeclaredMadeForKids': '1',
        }
    }

    media_file = MediaFileUpload(output_video_file, chunksize=-1, resumable=True)

    # Perform the request
    request = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media_file
    )

    response = request.execute()
    print(f"Video uploaded successfully: https://www.youtube.com/watch?v={response['id']}")


if __name__ == '__main__':

    # Parameters
    work_dir = 'D:\\process\\project54\\'
    image_dir = os.path.join(work_dir, 'temp\\')
    vidname = f"vid_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    output_video_file = os.path.join(work_dir, vidname)

    # Grid size, scaler, and aspect ratio
    grid_size = (128, 128)
    scaler = 2
    aspect_ratio = 1.0

    # Video duration and frame rate
    duration = 10
    frame_rate = 30

    # Title and credits duration
    title_text = vidname
    credits_text ='334Digital'
    title_duration = 2
    credits_duration = 1

    # Calculate the number of images needed based on duration and frame rate
    num_images = duration * frame_rate

    ## Youtube Data
    video_title = vidname
    video_description= 'A video generated by 334Digital'
    video_tags = ['Animation', 'Computer Generated']
    video_category = '1' # 1 = File & Animation' See https://developers.google.com/youtube/v3/docs/videoCategories/list for category IDs
    video_status = 'private'  # Set video privacy status (public, private, unlisted)

    # Generate random images
    generate_random_images(num_images, grid_size=grid_size, image_dir=image_dir, scaler=scaler, aspect_ratio=aspect_ratio)

    # Create title and credits images
    create_title_and_credits(image_dir, grid_size, scaler, aspect_ratio, title_text, credits_text, title_duration, credits_duration, frame_rate)

    # Rename image files
    rename_files_in_folder(image_dir)

    # Create video from images
    images_to_video(image_dir, output_video_file, frame_rate)

    # Clear the image directory
    clear_image_dir(image_dir)

    # Upload to Youtube
    youtube = authenticate_youtube()
    upload_video(youtube, video_title, video_description, video_tags, video_category, video_status, output_video_file)
