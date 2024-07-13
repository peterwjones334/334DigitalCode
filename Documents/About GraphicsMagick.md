## About GraphicsMagick

GraphicsMagick is a fork of ImageMagick and offers similar capabilities but focuses on performance and stability. 

Below are some basic examples of using GraphicsMagick to manipulate images:

### 1. **Convert Image Formats:**
   ```shell
   gm convert image.jpg image.png
   ```
   Converts an image from JPEG format to PNG format.

### 2. **Resize Image:**
   ```shell
   gm convert image.jpg -resize 800x600 resized_image.jpg
   ```
   Resizes an image to the specified dimensions.

### 3. **Crop Image:**
   ```shell
   gm convert image.jpg -crop 800x600+100+150 cropped_image.jpg
   ```
   Crops an image to 800x600 pixels size starting from the point (100,150).

### 4. **Rotate Image:**
   ```shell
   gm convert image.jpg -rotate 90 rotated_image.jpg
   ```
   Rotates an image 90 degrees clockwise.

### 5. **Add Text to Image:**
   ```shell
   gm convert image.jpg -font Arial -pointsize 40 -draw "text 100,150 'Hello'" text_image.jpg
   ```
   Adds the text "Hello" to an image at the position (100,150).

### 6. **Adjust Brightness and Contrast:**
   ```shell
   gm convert image.jpg -brightness-contrast 10x5 adjusted_image.jpg
   ```
   Adjusts the brightness by 10 and contrast by 5.

### Documentation:
- For a detailed list of commands and usage, refer to the official [GraphicsMagick Command-line Options](http://www.graphicsmagick.org/GraphicsMagick.html) documentation.

## Converting multiple JPEG images into a single PDF file

GraphicsMagick can convert multiple JPEG images into a single PDF file, and you can center the image on each page using the `-gravity center` option along with `-extent` to specify the page size. 

Here is a basic example where the page size is set to A4:

```shell
gm convert -page A4 -gravity center -extent 595x842 *.jpg output.pdf
```

- The `-page A4` option sets the page size (in this case, A4 is 595x842 points).
- The `-gravity center` centers the image.
- The `-extent 595x842` sets the output canvas (page) size, so if the image is smaller than this, it will be centered with a white background filling the rest of the page.
- The `*.jpg` denotes that all JPEG images in the current directory will be included.
- The `output.pdf` is the name of the resulting PDF file.

### Notes
1. Make sure all the jpg files are sorted in the desired order, as the command will process them in alphanumeric order.
2. If the images are of different sizes and you want to maintain their aspect ratio, you might need to process each image individually to resize them proportionally before combining them into a PDF.

### Example with Resizing
If your images have varying sizes and you wish to maintain their aspect ratio while fitting them to the A4 page, you can first resize them and then convert them to PDF. 

```shell
# Resize images while maintaining aspect ratio
for img in *.jpg; do
  gm convert "$img" -resize 595x842 -gravity center -extent 595x842 "resized_$img"
done

# Convert resized images to PDF
gm convert -page A4 resized_*.jpg output.pdf
```

This will process each image individually, resize it while maintaining its aspect ratio, center it on an A4 page, and then convert all the processed images to a single PDF file.