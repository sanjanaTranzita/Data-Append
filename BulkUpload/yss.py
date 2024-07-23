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

token='Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlzX3Bob25lX3ZlcmlmaWVkIjp0cnVlLCJyb2xlIjoiVVNFUiIsInNpZ25hdHVyZSI6bnVsbCwiZGVzY3JpcHRpb24iOm51bGwsImNyZWF0ZWRfYXQiOiIyMDI0LTAzLTI3VDA5OjEwOjAxLjIxOVoiLCJnc3RpbiI6IjA5QUdTUFk4OTY4TTFaUCIsImJhbmsiOnsiaWZzY19jb2RlIjoiIiwiYWNjb3VudF9udW1iZXIiOiIiLCJiZW5lZmljaWFyeV9uYW1lIjoiIiwiYWNjb3VudF90eXBlIjoiIiwiYnJhbmNoX2FkZHJlc3MiOiIifSwiY29tcGFueV9sb2dvIjoiaHR0cHM6Ly9lbmNyeXB0ZWQtdGJuMC5nc3RhdGljLmNvbS9pbWFnZXM_cT10Ym46QU5kOUdjUkFIWFBsdXE2R3RUUlBESUhSdjVrSlB5ODZ1RmpwNXNPN2hnJnVzcXA9Q0FVIiwiaXNfZ3N0aW5fdmVyaWZpZWQiOnRydWUsImNvbXBhbnkiOiJZU1MgR2VhcnMiLCJjb21wYW55X3VybCI6bnVsbCwic3RvcmVfdGltaW5nIjp7ImNsb3NlIjoiMTg6MzAiLCJvcGVuIjoiOTozMCJ9LCJlbWFpbCI6InlhZHVzcG9ydHNzb2x1dGlvbnNAZ21haWwuY29tIiwiYWdyZWVtZW50Ijp0cnVlLCJ0YXQiOiJQNUQiLCJtb2JpbGUiOjc4MTc5MzY5NjQsIm9yZGVyX21pbl92YWx1ZSI6NTAwLCJzdG9yZSI6W10sImdwcyI6IjI4LjgwMjAwNjQ1MTYxMjksIDc3LjkyOTc2NDUxNjEyOTA0IiwiYXZhaWxhYmlsdHkiOnsiZW5hYmxlIjp0cnVlLCJ0aW1lc3RhbXAiOiIyMDI0LTAzLTI3VDA5OjEwOjAxLjIxOVoifSwicHJvZmlsZV9pbWciOiJodHRwczovL3N0YXRpYy52ZWN0ZWV6eS5jb20vc3lzdGVtL3Jlc291cmNlcy9wcmV2aWV3cy8wMDMvMjQwLzM4My9ub25fMngvYmVzdC1zZWxsZXItZ29sZGVuLWJhZGdlLWlzb2xhdGVkLWlsbHVzdHJhdGlvbi12ZWN0b3IuanBnIiwibmFtZSI6Ik0vUyBZQURVIFNQT1JUUyBTT0xVVElPTlMiLCJhZ3JlZW1lbnRfdGltZSI6IjIwMjQtMDMtMjdUMDk6MTA6MDEuMjE5WiIsImxvY2F0aW9ucyI6W3siYWRkcmVzcyI6eyJwaW5jb2RlIjoyNTAwMDEsImNvdW50cnkiOiJJbmRpYSIsInN0ZF9jb2RlIjoiMDEyMSIsImNpdHkiOiJNZWVydXQiLCJzdHJlZXQiOiJuZXcgbW9oYW5wdXJpIiwiZGlzdHJpY3QiOiJNZWVydXQiLCJsb2NhbGl0eSI6Ijc0LGJ1ZGggdmloYXIsIiwic3RhdGUiOiJVdHRhciBQcmFkZXNoIn0sInBpY2t1cF9sb2NhdGlvbiI6Ik0vUyBZQURVIFNQT1JUUyBTT0xVVElPTlMjNzQsYnVkaCB2aWhhciwjMjUwMDAxNzgxNzkzNjk2NCIsInRpbWUiOnsic2NoZWR1bGUiOnsiaG9saWRheXMiOltdfSwibGFiZWwiOiJlbmFibGUiLCJ0aW1lc3RhbXAiOiIyMDI0LTAzLTI3VDA5OjE0OjU2LjkzMFoifSwiZ3BzIjoiMjguODAyMDA2NDUxNjEyOSwgNzcuOTI5NzY0NTE2MTI5MDQiLCJsb2NhdGlvbl9pZCI6Ijc0YmJkYjEzOTBkODQ4MjE5MmJkNWE1NzM4Y2ZmZDM4In1dLCJ1cGRhdGVkX2F0IjoiMjAyNC0wMy0yN1QwOToxNToyNy43OTVaIiwic3RhdHVzIjoiQUNUSVZFIiwiaWQiOiI2bFhaMmFHZEFlN0FFMlRKR25KRSIsImF2YXRhciI6ImFzc2V0cy9pbWFnZXMvYXZhdGFycy9tYWxlLTA3LmpwZyJ9LCJpYXQiOjE3MTE2Mzk1NDh9.YsCZ72P0asCNbxpFAhYIPl4G1Db87WZRL5y1CqFFOCc'
token2= token.split('Bearer ')[1]
def single_upload(super_category,category,sub_category,sub_sub_category,sub_sub_category_id,sku_id,prod_code,short_desc,long_desc,manuf_detail,packer_detail,cancellable,replaceable,returnable,time_to_ship,ondc_price,mrp,specifications,images):
    data3=pd.read_excel("ondc_category_mapping.xlsx")
    for index, row in data3.iterrows():
        sub_sub_category2 =row['sub_sub_category'] if len(str(row['sub_sub_category']))>0 else "Not Founded"
        if sub_sub_category2 == sub_sub_category:
            # sub_sub_category_id=row['sub_sub_category_id'] if len(str(row['sub_sub_category_id']))>0 else "Not Founded"
            Ondc_category_new=row['Ondc_category_new'] if len(str(row['Ondc_category_new']))>0 else "Not Founded"
            

    url = "http://127.0.0.1:5001/prod-shopcircuit-seller-portal/asia-south1/api/catalog/create_single"
  
    data=jwt.decode(token2, options={"verify_signature": False})
    address=data['user']['locations'][0]['address']
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
        "address": [],
        "ondc_status": "pending",
        "status": "draft"
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
        'origin': 'http://localhost:4200',
        'referer': 'http://localhost:4200/',
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
            for attribute1 in item["attribute"]:
                for attribute in specfication:
                    key = list(attribute.keys())[0]  # Get the attribute name
                    value = list(attribute.values())[0]  # Get the attribute value
                    if  type(value) is list:
                        if 'Color' == key:
                            value  = colors_array
                            # value = value[0].split(",")
                            if value[0] == 'NA':
                                value=getImageColor(imageUrl)            
                            newColor=[]
                            # print("The Value Changed --> ",value)
                            for colr in value:
                                newValue = matchColorName(colr)
                                # print("The Value Changed --> ",newValue)
                                if newValue != None:
                                 colorCode = newValue[1:]
                                 newColor.append(colorCode)    
                            if newColor != []:
                                value = newColor
                            value=  value
                            clothing_attributes['color'] = value
                            print("Total color is --> ",value)   
                        elif 'variation' == key:
                            value =value
                        else:
                            # print("Not Valid -->",sub2Item)
                            
                            my_string = " ".join(str(item4) for item4 in value)  # Convert items to strings first
                            # print(my_string) 
                            value = my_string
                # print(subItem," : ",sub2Item)
                    # print("key:",key,",","value:",value)
                    key1 = key.replace(' ','_')
                    key = key1.lower()
                    # print("The key 1 == > ",key)
                            
                    if key in attribute1:
                        # print("The key 2 == > ",key)
                        dt = attribute1[key]
                        if key == 'gender':
                            if value.lower() == 'women':
                                value='female'
                            if value.lower() == 'men':
                                value='male'
                            clothing_attributes[key] = value
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
                                    # # print('Completed',key,'=-->',item2)
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
    
    clothing_attributes["brand"]='yss gears'
    if "size" in clothing_attributes:
        clothing_attributes["variation"] = clothing_attributes.pop("size")
    else:
        clothing_attributes["variation"] = ["Free Size"]
    if "color" in clothing_attributes:
        print("Ranjet-------Singh-----------------------------")
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
        print("Ranjet------------------------------------")
        value=getImageColor(imageUrl)
        clothing_attributes["color"] = [value]
        # clothing_attributes["variation"] = ["Free Size"]
    print("clothing_attributes",clothing_attributes)    
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
    sub_sub_category_id=get_sub_sub_category_id(row['super_category'],str(row['category']),str(row['sub_category']),str(row['sub_sub_category'])) if len(get_sub_sub_category_id(str(row['super_category']),str(row['category']),str(row['sub_category']),str(row['sub_sub_category'])))>4 else "Not Founded"
    sku_id=str(row['prod_code']) if len(str(row['prod_code']))>4 else row['product_name'][:3]+"1234" 
    prod_code=row['product_name'] if len(str(row['product_name']))>4 else "Not Founded" 
    short_desc=row['short_desc'] if len(str(row['short_desc']))>4 else "Not Avilable" 
    long_desc=row['long_desc']if len(str(row['long_desc']))>4 else "Not Avilable"
    manuf_detail=row['manuf_detail']if len(str(row['manuf_detail']))>4 else "Not Avilable"
    packer_detail=row['packer_detail'] if len(str(row['packer_detail']))>4 else "Not Avilable"
    cancellable="Yes"
    replaceable="Yes"
    returnable="Yes"
    time_to_ship="P2D"
    brand=row['brand'] if len(str(row['brand']))>0 else "Not Avilable"
    ondc_price=get_number(row['price']) if get_number(row['price'])>0 else 0
    mrp=get_number(row['mrp']) if get_number(row['mrp'])>0 else 0
    
    image=get_image_array(row['images'])
    for item in image:
        print("IMAge is -->",item)
        download_image(item)
        
    images = my_list    
   
    for item in image:
        imageUrl = item
        break

    size = row['size']
    size_list = size.split(",")
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
    # print("varients -- > ",variants)
    print("sub_sub_category_id -> ",sub_sub_category_id)
    specifications=get_formated_specification(row['specification'],variants,brand,sub_sub_category_id,imageUrl,colors_array)
    # print("specifications --> ",specifications)
    # print("Specification -->",specifications)
    # print(super_category," > ",category," > ",sub_category," > ",sub_sub_category," > ",sub_sub_category_id," >",sku_id," > ",prod_name," > ",manuf_detail," > ",packer_detail," > ",ondc_price," > ",mrp,)
    single_upload(super_category,category,sub_category,sub_sub_category,sub_sub_category_id,sku_id,prod_code,short_desc,long_desc,manuf_detail,packer_detail,cancellable,replaceable,returnable,time_to_ship,ondc_price,mrp,specifications,images)
# print(master_data)
data=pd.read_excel("yssGears.xlsx")
c=0
for index, row in data.iterrows():
    c=c+1
    print("--------------------------------------------------------")
    print("Count is -->",c)
    my_list=[]
    ran = 1
    if c > 0:
        upload_format_data(row)
    
    
    
    
    
    
    
    
    
    


