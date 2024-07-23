from io import BytesIO
from PIL import Image
from requests import get

def convert_webp_to_jpg(webp_url, output_filename):

  response = get(webp_url)
  if not response.status_code == 200:
    raise Exception(f"Error downloading image: {response.status_code}")

  with BytesIO(response.content) as image_data:
    image = Image.open(image_data).convert("RGB")  
    image.save(output_filename, "JPEG")

# Example usage
webp_url = "https://storage.googleapis.com/shop-circuit-catalog-images/Kalpana%20Singh-i5tq2u6p6tvmp5QGYIIX/s-ku632blu-mokshi-original-imag4nmvnbwcyth5.webp"  
output_filename = "converted_image.jpg"

convert_webp_to_jpg(webp_url, output_filename)

print(f"WebP image converted to JPG and saved as {output_filename}")
