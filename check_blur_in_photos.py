from PIL import Image

def is_blurry(filepath):
  # Open the image file
  img = Image.open(filepath)

  # Check the image size and resolution
  width, height = img.size
  dpi = img.info["dpi"]
  if dpi is None:
    dpi = (72, 72)

  # Calculate the image size in inches
  inches_width = width / dpi[0]
  inches_height = height / dpi[1]

  # Calculate the total number of pixels in the image
  pixels = width * height

  # Calculate the number of pixels per inch
  pixels_per_inch = pixels / (inches_width * inches_height)

  # Check if the image is blurry
  if pixels_per_inch < 100:
    print("The image is blurry.")
  else:
    print("The image is not blurry.")

# Check if the image is blurry
is_blurry("path/to/image.pdf")
