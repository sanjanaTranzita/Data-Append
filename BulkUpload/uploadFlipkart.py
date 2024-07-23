import requests
import json
import pandas as pd
import jwt
import secrets 
import re
import os
from color import colorName
import numpy as np
from rembg import remove
import requests
from PIL import Image
import requests
import math


master_data=json.load(open('catalogs_with_attribute.json'))['data']
my_list = []
ran = 1

token='Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlzX3Bob25lX3ZlcmlmaWVkIjp0cnVlLCJyb2xlIjoiVVNFUiIsInNpZ25hdHVyZSI6bnVsbCwiZGVzY3JpcHRpb24iOm51bGwsImNyZWF0ZWRfYXQiOiIyMDI0LTA1LTI3VDA3OjMwOjM4LjExNVoiLCJnc3RpbiI6IjI5QUFHQ0I0MDM4RTFaVCIsImJhbmsiOnsiaWZzY19jb2RlIjoiIiwiYWNjb3VudF9udW1iZXIiOiIiLCJiZW5lZmljaWFyeV9uYW1lIjoiIiwiYWNjb3VudF90eXBlIjoiIiwiYnJhbmNoX2FkZHJlc3MiOiIifSwiY29tcGFueV9sb2dvIjoiaHR0cHM6Ly9lbmNyeXB0ZWQtdGJuMC5nc3RhdGljLmNvbS9pbWFnZXM_cT10Ym46QU5kOUdjUkFIWFBsdXE2R3RUUlBESUhSdjVrSlB5ODZ1RmpwNXNPN2hnJnVzcXA9Q0FVIiwiaXNfZ3N0aW5fdmVyaWZpZWQiOnRydWUsImNvbXBhbnkiOiIgQURSTyIsImNvbXBhbnlfdXJsIjpudWxsLCJzdG9yZV90aW1pbmciOnsiY2xvc2UiOiIxODozMCIsIm9wZW4iOiI5OjMwIn0sImVtYWlsIjoiaW5mb0BhZHJvLmluIiwiYWdyZWVtZW50Ijp0cnVlLCJ0YXQiOiJQNUQiLCJtb2JpbGUiOjk3NDE0MzAwMzMsIm9yZGVyX21pbl92YWx1ZSI6NTAwLCJncHMiOiIxMy4yMjU3NzcsIDc3LjU3NTU1NSIsInN0b3JlIjpbeyJBbWF6b24iOiJodHRwczovL3d3dy5hbWF6b24uaW4vcz9rPWFkcm8mY3JpZD0yWUZCOFhMSFJCSUcyJnNwcmVmaXg9YWRyJTJDYXBzJTJDNjkwJnJlZj1uYl9zYl9ub3NzXzEifV0sImF2YWlsYWJpbHR5Ijp7ImVuYWJsZSI6dHJ1ZSwidGltZXN0YW1wIjoiMjAyNC0wNS0yN1QwNzozMDozOC4xMTVaIn0sInByb2ZpbGVfaW1nIjoiaHR0cHM6Ly9zdGF0aWMudmVjdGVlenkuY29tL3N5c3RlbS9yZXNvdXJjZXMvcHJldmlld3MvMDAzLzI0MC8zODMvbm9uXzJ4L2Jlc3Qtc2VsbGVyLWdvbGRlbi1iYWRnZS1pc29sYXRlZC1pbGx1c3RyYXRpb24tdmVjdG9yLmpwZyIsIm5hbWUiOiJBRFJPICAgICAgICAgICAgICAgICAgIiwiYWdyZWVtZW50X3RpbWUiOiIyMDI0LTA1LTI3VDA3OjMwOjM4LjExNVoiLCJsb2NhdGlvbnMiOlt7ImFkZHJlc3MiOnsicGluY29kZSI6NTYwMDY4LCJjb3VudHJ5IjoiSW5kaWEiLCJzdGRfY29kZSI6IjA4MCIsImNpdHkiOiJCYW5nYWxvcmUiLCJzdHJlZXQiOiJLcmlzaG5hIFJvYWQsIEtvZGljaGlra2FuYWhhbGxpIE1haW4sIEJvbW1hbmFoYWxsaSIsImRpc3RyaWN0IjoiQmFuZ2Fsb3JlIiwibG9jYWxpdHkiOiIgIyA5LCBSYWphIEJoYXZhbiwgMXN0IGFuZCAybmQgZmxvb3IsIDEydGggJ0EnIE1haW4iLCJzdGF0ZSI6Ikthcm5hdGFrYSJ9LCJwaWNrdXBfbG9jYXRpb24iOiJBRFJPICAgICAgICAgICAgICAgICAgIyAjIDksIFJhamEgQmhhdmFuLCAxc3QgYW5kIDJuZCBmbG9vciwgMTJ0aCAnQScgTWFpbiM1NjAwNjg5NzQxNDMwMDMzIiwidGltZSI6eyJzY2hlZHVsZSI6eyJob2xpZGF5cyI6W119LCJsYWJlbCI6ImVuYWJsZSIsInRpbWVzdGFtcCI6IjIwMjQtMDUtMjdUMDc6MzA6MzYuMzExWiJ9LCJncHMiOiIxMy4yMjU3NzcsIDc3LjU3NTU1NSIsImxvY2F0aW9uX2lkIjoiMWU3OTI0YzMyZTRlNDUxOTg4ZDlmOTY2Nzg5YjQ1MTAifV0sInVwZGF0ZWRfYXQiOiIyMDI0LTA1LTI3VDA3OjM3OjI5Ljk4MloiLCJzdGF0dXMiOiJBQ1RJVkUiLCJpZCI6IkhuaXBvSjg4bWR1aGJIRzNpRHJoIiwiYXZhdGFyIjoiYXNzZXRzL2ltYWdlcy9hdmF0YXJzL21hbGUtMDcuanBnIn0sImlhdCI6MTcxNjc5NTUwNX0.JS5YlsoERggTARH5gC_XHtzeMg_rJnQ8CYEYIDi3Oew'
token2= token.split('Bearer ')[1]
def single_upload(super_category,category,sub_category,sub_sub_category,sub_sub_category_id,sku_id,prod_code,short_desc,long_desc,manuf_detail,packer_detail,cancellable,replaceable,returnable,time_to_ship,ondc_price,mrp,specifications,images):
    data3=pd.read_excel("ondc_category_mapping.xlsx")
    for index, row in data3.iterrows():
        sub_sub_category2 =row['sub_sub_category'] if len(str(row['sub_sub_category']))>0 else "Not Founded"
        if sub_sub_category2 == sub_sub_category:
            # sub_sub_category_id=row['sub_sub_category_id'] if len(str(row['sub_sub_category_id']))>0 else "Not Founded"
            Ondc_category_new=row['Ondc_category_new'] if len(str(row['Ondc_category_new']))>0 else "Not Founded"
            

    url = "https://asia-south1-prod-shopcircuit-seller-portal.cloudfunctions.net/api/catalog/create_single"
  
    data=jwt.decode(token2, options={"verify_signature": False})
    address=data['user']['locations'][0]['location_id']
    print("address --> ",address)
    pickup_location  = data['user']['locations'][0]['pickup_location']
    token1 = secrets.token_hex(6) 

    payload = json.dumps({
    "step1": {
        "super_category": super_category ,
        "category": category,
        "sub_category": sub_category,
        "sub_sub_category":sub_sub_category,
        "sub_sub_category_id": sub_sub_category_id,
        "ondc_category": Ondc_category_new,
        "ondc_category_id": token1,
        "ondc_domain": "ONDC:RET12",
        "inventory": [],
        "images": images
    },
    "step2": {
        "sku_id": sku_id,
        "prod_code":prod_code,
        "short_desc": short_desc,
        "long_desc": long_desc,
        "manuf_detail": manuf_detail,
        "packer_detail": packer_detail,
        "cancellable": cancellable,
        "replaceable": replaceable,
        "returnable": returnable,
        "time_to_ship":time_to_ship,
        "ondc_price": ondc_price,
        "mrp": mrp,
        "location_id":address,
        "address": [],
        "ondc_status": "pending",
        "status": "QC_IN_PROGRESS"
    },
    "step3": specifications, 
    "step4": []
    })
    headers = {
        'authority': 'asia-south1-prod-shopcircuit-seller-portal.cloudfunctions.net',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'authorization': token,
        'content-type': 'application/json',
        'origin': 'https://dashboard.shopcircuit.ai',
        'referer': 'https://dashboard.shopcircuit.ai/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def get_sub_sub_category_id(super_categories,categories, sub_categories, sub_sub_categories):
    print("get_sub_sub_category_id called",super_categories,categories, sub_categories, sub_sub_categories)
    filtered_ids = []
    for item in master_data:
        if (
            item["super_category"].strip() in super_categories and
            item["category"].strip() in categories and
            item["sub_category"].strip() in sub_categories and
            item["sub_sub_category"].strip() in sub_sub_categories
        ):
            filtered_ids.append(item["sub_sub_category_id"])
            if len(filtered_ids)>0:
                print("line number 73 filtered_ids",filtered_ids)
                return filtered_ids[0]
            else:
                return "not founded"
            
def get_formated_specification(specfication,variants,brand,sub_sub_category_id,imageUrl,colors_array):
    specfication=json.loads(specfication)
    variants=variants
    keys_to_remove = [key for key, value in variants.items() if value == "" or (isinstance(value, list) and not value)]
    for key in keys_to_remove:
         variants.pop(key)
    clothing_attributes = {}
    for item in master_data:
        if item["sub_sub_category_id"] == sub_sub_category_id:
            # Create a new attribute dictionary with all keys set to "Not Available"
            not_available_attributes = {key: "Not Available" for attribute_dict in item["attribute"] for key in attribute_dict.keys()}
            # print("not_available_attributes",not_available_attributes)
            clothing_attributes.update(not_available_attributes)
            # print(clothing_attributes)

    for item in master_data:
        if item["sub_sub_category_id"] == sub_sub_category_id:
            specfication.append({"Color":colors_array})
            print("Specification --> ",specfication)
            for attribute1 in item["attribute"]:
                for attribute in specfication:
                    key = list(attribute.keys())[0]  # Get the attribute name
                    value = list(attribute.values())[0]  # Get the attribute value
                    key1 = key.replace(' ','_')
                    key = key1.lower()
                
                    # if  type(value) is list:
                    #     if 'Color' == key:
                    #         value  = colors_array
                    #         # value = value[0].split(",")
                    #         if value[0] == 'NA':
                    #             value=getImageColor(imageUrl)            
                    #         newColor=[]
                    #         # print("The Value Changed --> ",value)
                    #         for colr in value:
                    #             print("colr --> ", colr)
                    #             newValue = matchColorName(colr)
                    #             print("The Value Changed --> ",newValue)
                    #             if newValue != None:
                    #              colorCode = newValue[1:]
                    #              newColor.append(colorCode)    
                    #         if newColor != []:
                    #             value = newColor
                    #         else:
                    #             value=getImageColor(imageUrl) 
                    #         value=  value
                    #         clothing_attributes['color'] = value
                    #         print("Total color is --> ",value)   
                    #     elif 'variation' == key:
                    #         value =value
                    #     else:
                    #         my_string = " ".join(str(item4) for item4 in value)  # Convert items to strings first
                    #         value = my_string
        
                    # if key == 'Bottom Length' or key == 'Top Length' or key == 'Dupatta Length':
                    #     print(key)
                    # else:    
                    #     key1 = key.replace(' ','_')
                    #     key = key1.lower()
                    print("Key =====> ",key)
                    print("Value ===> ",value)
                    if 'color' == key:
                        value  = colors_array
                        # value = value[0].split(",")
                        if value[0] == 'NA':
                            value=getImageColor(imageUrl)            
                        newColor=[]
                        for colr in value:
                            newValue = matchColorName(colr)
                            if newValue != None:
                                colorCode = newValue[1:]
                                newColor.append(colorCode)    
                        if newColor != []:
                            value = newColor
                        else:
                            value=getImageColor(imageUrl) 
                        value=  value
                        clothing_attributes['color'] = value
                        print("Total color is --> ",value)   
                    elif 'variation' == key:
                        value =value
                    
                    elif 'GST' in attribute1:
                        dt = attribute1['GST']
                        for item2 in dt:
                            clothing_attributes['GST'] = item2 
                            break
                    elif 'gst' in attribute1:
                        dt = attribute1['gst']
                        for item2 in dt:
                            clothing_attributes['gst'] = item2 
                            break
                    # elif 'HSN_ID' in attribute1:
                    #     dt = attribute1['HSN_ID']
                    #     for item2 in dt:
                    #         clothing_attributes['HSN_ID'] = item2 
                    #         break
                    # elif 'hsn_id' in attribute1:
                    #     dt = attribute1['hsn_id']
                    #     for item2 in dt:
                    #         clothing_attributes['hsn_id'] = item2 
                    #         break
                    
                    elif key in attribute1:
                        print("The key fabric 2 == > ",key)
                        dt = attribute1[key]
                        if key == 'gender':
                            if value.lower() == 'women':
                                value='female'
                            if value.lower() == 'men':
                                value='male'
                            clothing_attributes[key] = value
                        elif key == 'country': 
                            clothing_attributes[key] = 'India'

                        elif key == 'color':
                            clothing_attributes[key] = value
                        elif key == 'Top Length':
                            w1 = str(value)
                            if len(w1) < 4:
                                value= value.replace('m', 'Meters')
                                clothing_attributes[key] = value
                            else:    
                                clothing_attributes[key] = '2.01-2.25'
                        elif key == 'Bottom Length':
                            w2 = str(value)
                            if len(w2) < 4:
                                value= value.replace('m', 'Meters')
                                clothing_attributes[key] = value
                            else:    
                                clothing_attributes[key] = '2.01-2.25'
                        elif key == 'Dupatta Length':
                            w3 = str(value)
                            if len(w3) < 6:
                                value= value.replace('m', '')
                                value= value.replace(' ', '')
                                clothing_attributes[key] = eval(value)
                            else:
                                clothing_attributes[key] = 2.2
                        elif key == 'varient':
                            clothing_attributes[key] = value
                        else:
                            print("Key -> ",key,"  Value -> ",value)
                            for item2 in dt:
                                dt1 = item2.lower()
                                dt2 = value.lower()                            
                                if dt1 in dt2:
                                    value = item2
                                    # if dt2 in dt1:
                                    # print('Completed',key,'=-->',item2)
                                    #     value = item2
                                    clothing_attributes[key] = value 
                        # print("clothing_attributes -----> ",clothing_attributes)


    # for attribute in specfication:
    #     key = list(attribute.keys())[0]  # Get the attribute name
    #     value = list(attribute.values())[0]  # Get the attribute value
    #     # print("key:",key,",","value:",value)
    #     key1 = key.replace(' ','_')
    #     # print("key1",key1)

    #     clothing_attributes[key1.lower()] = value
    #     # print("clothing_attributes",clothing_attributes)
        
    clothing_attributes.update({key.lower().replace(" ","_"): value for key, value in variants.items()})
    
    
    clothing_attributes["brand"]=brand

    if "size" in clothing_attributes:
        clothing_attributes["variation"] = clothing_attributes.pop("size")
    else:
        clothing_attributes["variation"] = ["Free Size"]
    if "color" in clothing_attributes:
        if isinstance(clothing_attributes["color"], str):
            if clothing_attributes["color"] == 'Not Available':
                value=getImageColor(imageUrl)
                clothing_attributes["color"] = [value]
            else:
                clothing_attributes["color"] = [clothing_attributes["color"]]
            print("clothing_attributes Color is -- > ",clothing_attributes["color"])
    # elif "Color" in clothing_attributes:
    #     if isinstance(clothing_attributes["Color"], str):
    #         clothing_attributes["color"] = [clothing_attributes["Color"]]
    else:
        value=getImageColor(imageUrl)
        clothing_attributes["color"] = [value]
        # clothing_attributes["variation"] = ["Free Size"]
    # print("clothing_attributes",clothing_attributes)   
    return clothing_attributes

def get_image_array(images):
    if images[-1]!="]" and images[0]!= "[":
        return re.findall(r'https://.*?\.jpg', images)
    else:
        # print("line number 112 images",json.loads(images) ,type(json.loads(images)))
        return json.loads(images)

def get_number(numData):
    numData = numData.replace(",", "")
    
    if numData!="" or not isinstance(float,numData) :
        numData=str(numData)
        result=[]
        result=[int(match) for match in re.findall(r'\b\d+\b', numData)]
        if len(result)>0:
            return result[0]
        else:
            return 0
    else:
        return 0

def download_image(url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        base_url="downloaded_image/"+url.split('/')[-1]
        name = base_url.split("?")[0]
        with open(name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
       
        print(f"Image downloaded successfully to {name}")
        url = str(name)
        img = url.split("/")[1]
        upload_image(img)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the image: {e}")  

def upload_image(img):
    print("img -->",img)

    url = "https://asia-south1-prod-shopcircuit-seller-portal.cloudfunctions.net/api/upload_catalog_img"

    payload = {'dir': 'null'}
    files=[
    ('file',(img,open(f'downloaded_image/{img}','rb'),'image/jpeg'))
    ]
    headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Authorization': token,
    'Connection': 'keep-alive',
    'Origin': 'https://dashboard.shopcircuit.ai',
    'Referer': 'https://dashboard.shopcircuit.ai/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)

    json_data = response.text
    data = json.loads(json_data)
    url_value = data.get('url')
    print("out url",url_value)
    my_list.append(url_value)
    direc = 'downloaded_image/'
    delete_files_in_folder(direc)

def delete_files_in_folder(folder_path):
    try:
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                os.remove(file_path)
                print(f"Deleted: {file_path}")

            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                os.rmdir(dir_path)
                print(f"Deleted directory: {dir_path}")

        print(f"All files and directories in {folder_path} deleted successfully.")
    except OSError as e:
        print(f"Error deleting files and directories: {e}")    

def download_image_url(url, output_path):
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



def find_nearest_color(hex_color,color_list):
    def validate_color_list(color_list):
        """Validates the color list and corrects any errors."""
        valid_colors = []
        for entry in color_list:
            if not isinstance(entry, list) or len(entry) != 2:
                print("Invalid entry:", entry)
                continue  # Skip invalid entries
            color_name, hex_value = entry
            if not isinstance(color_name, str) or not isinstance(hex_value, str):
                print("Invalid entry:", entry)
                continue  # Skip invalid entries
            if not hex_value.startswith('#') or len(hex_value) != 7:
                print("Invalid hex value in entry:", entry)
                continue  # Skip invalid entries
            try:
                int(hex_value[1:], 16)  # Attempt to convert the hex value to an integer
                valid_colors.append(entry)
            except ValueError:
                print("Invalid hex value in entry:", entry)
                continue  # Skip invalid entries
        return valid_colors

    def hex_to_rgb(hex_color):
        """Converts a hexadecimal color to RGB."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_distance(color1, color2):
        """Calculates the Euclidean distance between two RGB colors."""
        return sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)) ** 0.5

    def nearest_color(hex_color, color_list):
        """Finds the nearest color in a list based on Euclidean distance in RGB space."""
        target_rgb = hex_to_rgb(hex_color)
        nearest_name = None
        nearest_hex = None
        min_distance = float('inf')
        for color_name, hex_value in color_list:
            rgb_value = hex_to_rgb(hex_value)
            distance = rgb_distance(target_rgb, rgb_value)
            if distance < min_distance:
                min_distance = distance
                nearest_name = color_name
                nearest_hex = hex_value
        return nearest_hex, nearest_name

    color_list = validate_color_list(color_list)
    hex_color = hex_color.upper()  # Ensure uppercase hex color input
    nearest_hex, nearest_name = nearest_color(hex_color, color_list)
    return nearest_hex

# hex_color = "#1E93FF"  # Example hexadecimal color
# nearest_name, nearest_hex = find_nearest_color(hex_color, color_list)
# print("Nearest color to", hex_color, "is:", nearest_name, "with hexcode:", nearest_hex)


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

def getTrueColor(color_list,hex_color):
    for item in color_list:
        if item[1] == hex_color:
            color=item[1]
            return color
def getRanColor(color_list,hex_color):
    for item in color_list:
        if item[1] == hex_color:
            ran =0
            return ran
def matchColorName(color1):
    color = color1.lower()
    for item in colorName.color_list:
        if item[0] == color:
            color = item[1]
            return color
    else:
        color = color.replace(" ", "")
        if item[0] == color:
            color = item[1]
            return color

        
def getRan2ColorName(color):
    for item in colorName.color_list:
        if item[0] == color:
            ran2=0
            return ran2
def getImageColor(item):
    download_path = "downloaded_image/downloaded_image.jpg"
    output_path = "remove_background/image_no_background.png"
    download_image_url(item, download_path)
    remove_background(download_path, output_path)

    dominant_color_hex = get_dominant_color(output_path)
    print("Color_Hex_Code --> ",dominant_color_hex)
    color = getTrueColor(colorName.color_list,dominant_color_hex) 
    colorCode = color
    ran = getRanColor(colorName.color_list,dominant_color_hex) 
    print("color -->",color)   
    print("ran",ran)           
    if ran == None:
        color_code = dominant_color_hex[1:]
        response = requests.get(f"https://www.thecolorapi.com/id?hex={color_code}&format=json")
        data = response.json()
        color = data['name']['value']
        print("Else Worked Color_Name --> ",color)
        color = color.lower()
        dominant_color_hex = dominant_color_hex.upper()
        color2 = matchColorName(color)
        ran2 = getRan2ColorName(color)
        
        colorCode = dominant_color_hex
        newColor = [color,dominant_color_hex]
        if ran2 == None:
            with open('color/colorNewName.txt','a') as f:
                f.write(f"\n{newColor}")
        if color2 != None:
            colorCode = color2

    colorCode =find_nearest_color(colorCode,colorName.color_list)
    colorCode = colorCode[1:]      
    color= colorCode
    print("color --> ",color)
    direc = 'downloaded_image/'
    delete_files_in_folder(direc)
    return color


def upload_format_data(row):
    super_category=row['super_category'] if len(str(row['super_category']))>0 else "Not Founded" 
    category=row['category'] if len(str(row['category']))>0 else "Not Founded" 
    sub_category=row['sub_category'] if len(str(row['sub_category']))>0 else "Not Founded" 
    sub_sub_category=row['sub_sub_category'] if len(str(row['sub_sub_category']))>0 else "Not Founded" 
    # sub_sub_category_id=get_sub_sub_category_id(row['super_category'],str(row['category']),str(row['sub_category']),str(row['sub_sub_category'])) if len(get_sub_sub_category_id(str(row['super_category']),str(row['category']),str(row['sub_category']),str(row['sub_sub_category'])))>4 else "Not Founded"
    sub_sub_category_id = row['sub_sub_category_id'] if len(str(row['sub_sub_category_id']))>0 else "Not Founded" 
    print("sub_sub_category_id -->", sub_sub_category_id)
    sku_id=str(row['prod_code']) if len(str(row['prod_code']))>4 else row['product_name'][:3]+"1234" 
    prod_code=row['product_name'] if len(str(row['product_name']))>4 else "Not Founded" 
    short_desc=row['short_desc'] if len(str(row['short_desc']))>4 else "Not Available" 
    long_desc=row['long_desc']if len(str(row['long_desc']))>4 else "Not Available"
    manuf_detail=row['manuf_detail']if len(str(row['manuf_detail']))>4 else "Not Available"
    packer_detail=row['packer_detail'] if len(str(row['packer_detail']))>4 else "Not Available"
    cancellable="Yes"
    replaceable="Yes"
    returnable="Yes"
    time_to_ship="P2D"
    brand=row['brand'] if len(str(row['brand']))>0 else "Not Available"
    ondc_price=get_number(row['price']) if get_number(row['price'])>0 else 0
    mrp=get_number(row['mrp']) if get_number(row['mrp'])>0 else 0
    # mrp = ondc_price
    
    image=get_image_array(row['images'])
    for item in image:
        print("IMAge is -->",item)
        download_image(item)
        
    images = my_list    
   
    for item in image:
        imageUrl = item
        break

    size = row['size']
    
    if size == 'NA' or size == 'NAN' or size == 'nan' or type(size) == float:
        size_list = ['Free Size']
    else:
        size_list = size.split(",")
        size_list = [item.strip() for item in size_list]

    colors=row['color']
    print("=====",colors)
    if type(colors) == float:
        if math.isnan(float(colors)):
            print("The value is NaN")
            colors_array=['NA']
    elif str(colors) == 'NA':
        print("The value is NaN")
        colors_array=['NA']
    else:    
        colors_array = colors.split(',')

    print("Color is --> ",colors_array)

    # Create the dictionary with the size list and an empty color list
    variants = {"size": size_list, "color": []}
    print("varients -- > ",variants)
    brand = 'ADRO'
    specifications=get_formated_specification(row['specification'],variants,brand,sub_sub_category_id,imageUrl,colors_array)
    print("specifications --> ",specifications)
    # print("Specification -->",specifications)
    # print(super_category," > ",category," > ",sub_category," > ",sub_sub_category," > ",sub_sub_category_id," >",sku_id," > ",prod_name," > ",manuf_detail," > ",packer_detail," > ",ondc_price," > ",mrp,)
    single_upload(super_category,category,sub_category,sub_sub_category,sub_sub_category_id,sku_id,prod_code,short_desc,long_desc,manuf_detail,packer_detail,cancellable,replaceable,returnable,time_to_ship,ondc_price,mrp,specifications,images)
# print(master_data)
data=pd.read_excel("Adro2.xlsx")
c=0
for index, row in data.iterrows():
    c=c+1
    print("--------------------------------------------------------")
    print("Count is -->",c)
    my_list=[]
    ran = 1
    if c > 186:
        upload_format_data(row)
        
    
    
    
    
    
    
    
    
    
    


