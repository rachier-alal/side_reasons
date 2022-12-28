require "mini_magick"

def is_blurry(filepath)
  # Open the image file
  img = MiniMagick::Image.open(filepath)

  # Check the image size and resolution
  width = img.width
  height = img.height
  dpi = img.density

  # Calculate the image size in inches
  inches_width = width / dpi
  inches_height = height / dpi

  # Calculate the total number of pixels in the image
  pixels = width * height

  # Calculate the number of pixels per inch
  pixels_per_inch = pixels / (inches_width * inches_height)

  # Check if the image is blurry
  if pixels_per_inch < 100
    puts "The image is blurry."
  else
    puts "The image is not blurry."
  end
end

# Check if the image is blurry
is_blurry("path/to/image.pdf")
