import requests

# Replace 'https://...' with the actual Dropbox image URL
image_url = "https://www.dropbox.com/s/ki4knkaa2x1k40v/N02A8778.JPG?dl=0"

# Set the filename (optional)
filename = "downloaded_image.jpg"

# Send GET request to download the image
response = requests.get(image_url, stream=True)

if response.status_code == 200:
    # Check for content-type header to ensure it's an image
    if response.headers.get('content-type', '').startswith('image/'):
        # Set decode_content to True to handle potential encoding issues
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Image downloaded successfully as {filename}")
    else:
        print("Error: The URL doesn't point to an image file.")
else:
    print(f"Error: Failed to download image. Status code: {response.status_code}")
