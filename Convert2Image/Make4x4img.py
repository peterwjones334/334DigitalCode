""""
Title: Make4x4Grid
Description: This script generates binary 4 x 4 grid to images.
Author: 334 Digital 
Date: 2024-05-16
Version: 1.0

Dependencies:
    - numpy
    - pillow (PIL)
    - os
    - itertools

Usage:
    Make4x4img.py

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
import os
import itertools

# Function to generate an image from a binary grid
def generate_image(grid, filename):
    img = Image.fromarray(np.uint8(grid * 255), 'L')
    img = img.resize((256, 246), Image.NEAREST)  # Upscale for better visibility
    img.save(filename)
    print(f'Saved image: {filename}')  # Debug print to confirm image saving

# Function to generate all possible binary grids and images
def generate_all_images(grid_size=(4, 4), output_dir='C:\\Workplace\\projectxxx\\output\\'):
    os.makedirs(output_dir, exist_ok=True)
    print(f'Output directory: {output_dir}')  # Debug print to confirm directory creation
    # Generate all possible combinations of binary values for the grid
    for idx, bits in enumerate(itertools.product([0, 1], repeat=grid_size[0] * grid_size[1])):
        grid = np.array(bits).reshape(grid_size)
        filename = os.path.join(output_dir, f'4X4image_{idx}.JPG')
        generate_image(grid, filename)
    print(f'Generated {2**(grid_size[0] * grid_size[1])} images in {output_dir}')

# Generate all images for a grid
generate_all_images()
