""""
Title: Image to Video Generation Script
Description: This script lists images in a directory and compiles them into a video.
Author: 334 Digital 
Date: 2024-05-15
Version: 1.0

Dependencies:
    - cv2
    - os

Usage:
    MakeImgtoVid1.py

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
# Makes a video form sequential Images
import cv2
import os

def images_to_video(input_dir, output_file, frame_rate):
    # Get all image files in the input directory
    image_files = [f for f in sorted(os.listdir(input_dir)) if f.endswith(('.png', '.jpg', '.jpeg', '.JPG'))]

    # Check if there are any images
    if not image_files:
        print("No images found in the directory.")
        return

    # Read the first image to get the dimensions
    first_image_path = os.path.join(input_dir, image_files[0])
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
        image_path = os.path.join(input_dir, image_file)
        frame = cv2.imread(image_path)
        if frame is not None:
            video.write(frame)
        else:
            print(f"Failed to read image: {image_path}")

    # Release the video writer
    video.release()
    print(f"Video saved as {output_file}")

# Parameters
input_directory = 'D:\\workplace\\projects\\bouncing_ball_frames1\\'  # Directory containing the images
output_video_file = 'D:\\workplace\\projects\\10mdrop.mp4'  # Output video file path
frame_rate = 30  # Frames per second

# Create the video
images_to_video(input_directory, output_video_file, frame_rate)
