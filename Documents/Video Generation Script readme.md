# Video Generation Script

This script generates random binary grid images, creates title and credit images, and compiles them into a video.

## Table of Contents

- [Description](##description)
- [Dependencies](##dependencies)
- [Usage](##usage)
- [Functions](#f#unctions)
    - [generate_image](###generate_image)
    - [generate_random_images](###generate_random_images)
    - [rename_files_in_folder](#r##ename_files_in_folder)
    - [create_title_and_credits](###create_title_and_credits)
    - [create_image_from_text](###create_image_from_text)
    - [images_to_video](###images_to_video)
    - [clear_image_dir](###clear_image_dir)
- [Parameters](##parameters)
- [License](##license)

## Description

This script generates random binary grid images, creates title and credit images, and compiles them into a video.

## Dependencies

- `numpy`
- `pillow (PIL)`
- `opencv-python`
- `uuid`
- `shutil`
- `datetime`
- `os`

## Usage

Run the script using the following command:

```sh
python your_script_name.py
```

## Functions

### generate_image

```Python
def generate_image(content, filename, scaler, aspect_ratio, is_text=False, text="", font_size=8):
```

Generates an image from a binary grid or text.

Parameters:

- content: The content to be converted into an image (binary grid or text dimensions).
- filename: The name of the file to save the image.
- scaler: The scaling factor for the image.
- aspect_ratio: The aspect ratio of the image.
- is_text: Boolean indicating if the content is text.
- text: The text to be drawn on the image.
- font_size: The font size of the text.

### generate_random_images

```Python
def generate_random_images(num_images, grid_size=(64, 64), image_dir='output_images', scaler=4, aspect_ratio=1.0):
```

Generates random binary grid images.

Parameters:

- num_images: Number of images to generate.
- grid_size: The size of the binary grid.
- image_dir: Directory to save the generated images.
- scaler: The scaling factor for the images.
- aspect_ratio: The aspect ratio of the images.

### rename_files_in_folder

```Python
def rename_files_in_folder(image_dir):
```

Renames files in the specified folder with unique UUIDs.

Parameters:

image_dir: Directory containing the images to rename.

### create_title_and_credits

```Python
def create_title_and_credits(image_dir, grid_size, scaler, aspect_ratio, title_text, credits_text, title_duration, credits_duration, frame_rate):
```

Creates title and credits images and duplicates them based on the specified duration and frame rate.

Parameters:

- image_dir: Directory to save the title and credits images.
- grid_size: The size of the binary grid.
- scaler: The scaling factor for the images.
- aspect_ratio: The aspect ratio of the images.
- title_text: Text for the title image.
- credits_text: Text for the credits image.
- title_duration: Duration of the title in seconds.
- credits_duration: Duration of the credits in seconds.
- frame_rate: Frame rate of the video.

### create_image_from_text

```Python
def create_image_from_text(text, size, filename, scaler, aspect_ratio):
```

Creates an image from text.

Parameters:

- text: The text to be drawn on the image.
- size: The size of the image.
- filename: The name of the file to save the image.
- scaler: The scaling factor for the image.
- aspect_ratio: The aspect ratio of the image.

### images_to_video

```Python
def images_to_video(image_dir, output_file, frame_rate):
```

Converts a sequence of images to a video.

Parameters:

- image_dir: Directory containing the images.
- output_file: The output video file name.
- frame_rate: Frame rate of the video.

### clear_image_dir

```Python
def clear_image_dir(image_dir):
```

Clears the specified image directory.

Parameters:  
image_dir: Directory to clear.

## Parameters

- work_dir: Working directory for the script.
- image_dir: Directory to save the generated images.
- vidname: Name of the output video file.
- output_video_file: Full path to the output video file.
- grid_size: Size of the binary grid.
- scaler: Scaling factor for the images.
- aspect_ratio: Aspect ratio of the images.
- duration: Duration of the video in seconds.
- frame_rate: Frame rate of the video.
- num_images: Number of images to generate based on duration and frame rate.
- title_duration: Duration of the title in seconds.
- credits_duration: Duration of the credits in seconds.
- title_text: Text for the title image.
- credits_text: Text for the credits image.

## License

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.