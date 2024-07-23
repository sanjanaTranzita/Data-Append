from rembg import remove
import requests
from PIL import Image
import requests
import cv2
import numpy as np

def download_image(url, output_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Error downloading image: {response.status_code}")

def remove_background(image_path, output_path):
    with open(image_path, 'rb') as f:
        image_data = f.read()
    output = remove(image_data)
    with open(output_path, 'wb') as f:
        f.write(output)

image_url =  'https://assets.myntassets.com/h_1440,q_90,w_1080/v1/assets/images/26954450/2024/1/17/bd4cf5cc-12bd-461c-90ab-dd93330760821705466757828BindigasmsAdviWoven-DesignCottonSareeBlouse1.jpg'
download_path = "downloaded_image/downloaded_image.jpg"
output_path = "remove_background/image_no_background.png"

download_image(image_url, download_path)
remove_background(download_path, output_path)

print("Background removed! Check", output_path)

#Brightness
def increase_brightness(image_path, brightness_value):
  """
  Increases the brightness of a PNG image.

  Args:
      image_path: Path to the PNG image file.
      brightness_value: A positive value to add to the image pixel intensities.

  Returns:
      A new image with increased brightness. Raises an error if the image is not loaded successfully.
  """

  # Load the image (adjust for grayscale if needed)
  image = cv2.imread(image_path)

  # Check if image is loaded successfully
  if image is None:
    raise Exception("Failed to read image from path: {}".format(image_path))

  # Create a constant array with the same dimensions as the image and filled with the brightness value
  # This ensures correct broadcasting for element-wise addition
  const_brightness = np.ones_like(image, dtype="uint8") * brightness_value

  # Increase the brightness by adding the constant array
  brightened_image = cv2.add(image, const_brightness)

  # Return the brightened image
  return brightened_image

# Example usage
image_path =  'remove_background/image_no_background.png'
brightness_value = 30  # Adjust this value to control brightness increase

try:
  brightened_image = increase_brightness(image_path, brightness_value)
  # Use cv2.imwrite to save the brightened image with proper extension
  cv2.imwrite('remove_background/brightened_image.png', brightened_image)  
  print("Done Brightness - Image saved as brightened_image.png")
except Exception as e:
  print("Error:", e)








# Get Color
def get_dominant_color(image_path, tolerance=10):

  img = Image.open(image_path).convert('RGBA')
  width, height = img.size

  # Create a dictionary to store pixel frequencies
  color_counts = {}
  background_color = img.getpixel((0, 0))

  # Iterate through each pixel
  for x in range(width):
    for y in range(height):
      pixel = img.getpixel((x, y))

      # Check if pixel is transparent (background)
      if pixel[3] <= tolerance:
        continue

      # Check for color similarity to background (within tolerance)
      if abs(pixel[0] - background_color[0]) <= tolerance and \
         abs(pixel[1] - background_color[1]) <= tolerance and \
         abs(pixel[2] - background_color[2]) <= tolerance:
        continue

      # Increment count for this color
      if pixel in color_counts:
        color_counts[pixel] += 1
      else:
        color_counts[pixel] = 1

  # Find the most frequent color (excluding background)
  dominant_color = max(color_counts, key=color_counts.get)

  # Convert RGB to hex code
  return f"#{dominant_color[0]:02x}{dominant_color[1]:02x}{dominant_color[2]:02x}"

# Example usage
image_path = "remove_background/image_no_background.png"
dominant_color_hex = get_dominant_color(image_path)
print(f"Dominant color (excluding background): {dominant_color_hex}")

color_code = dominant_color_hex[1:]

response = requests.get(f"https://www.thecolorapi.com/id?hex={color_code}&format=json")
data = response.json()

print(f"Name: {data['name']['value']}")