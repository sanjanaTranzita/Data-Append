import requests

def download_image(image_url, filename="image.jpg"):

  try:
    response = requests.get(image_url, stream=True)
    response.raise_for_status()  # Raise an exception for any unsuccessful response

    with open(filename, 'wb') as f:
      for chunk in response.iter_content(1024):
        f.write(chunk)

    print(f"Image downloaded successfully and saved as {filename}")
  except requests.exceptions.RequestException as e:
    print(f"Error downloading image: {e}")

# Example usage
image_url = "https://rukminim2.flixcart.com/image/832/832/xif0q/dress/x/u/6/m-yellow-dress-madhurima-collection-original-imagpzkfecycqcdm.jpeg?q=70&crop=false"
download_image(image_url)
