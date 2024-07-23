# ==================================================import liberary============================================================================
import traceback
import sys
import requests
import json
import pandas as pd
import jwt
import secrets 
import re
import os
import numpy as np
from rembg import remove
import requests
from PIL import Image
import requests
import math
import uuid
import cv2
import ast
from itertools import product as cartesian_product
from datetime import datetime
# ==========================================================import data ======================================================================
master_data = json.load(open('./data/catalog-full.json'))["data"]
colorName = json.load(open('./data/color.json'))["color_list"]
# ==============================================================function define===============================================================

# ----------------------------------------------------------------------------create single catelog from validated data -----------------------------------------------------------

def single_upload(token, domain, Ondc_category_new, super_category,category,sub_category,sub_sub_category,sub_sub_category_id,sku_id,prod_code,short_desc,long_desc,manuf_detail,packer_detail,cancellable,replaceable,returnable,time_to_ship,ondc_price,mrp,specifications,images,variatn_overwrite,ondc_status,status):
        

    # url = "https://asia-south1-prod-shopcircuit-seller-portal.cloudfunctions.net/api/catalog/create_single"
    url = "http://127.0.0.1:5001/prod-shopcircuit-seller-portal/asia-south1/api/catalog/create_single"

  
    data=jwt.decode(token, options={"verify_signature": False})
    address=data['user']['locations'][0]['location_id']
    print("address --> ",address)
    pickup_location  = data['user']['locations'][0]['pickup_location']
    ondc_category_id = secrets.token_hex(6) 

    payload = json.dumps({
    "step1": {
        "super_category": super_category ,
        "category": category,
        "sub_category": sub_category,
        "sub_sub_category":sub_sub_category,
        "sub_sub_category_id": sub_sub_category_id,
        "ondc_category": Ondc_category_new,
        "ondc_category_id": ondc_category_id,
        "ondc_domain": domain,
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
        "ondc_status": ondc_status,
        "status": status
    },
    "step3": specifications, 
    "step4": {"variatn_overwrite":variatn_overwrite}
    
    })
    headers = {
        'authority': 'asia-south1-prod-shopcircuit-seller-portal.cloudfunctions.net',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'authorization': f"Bearer {token}",
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
    print("payload : ",payload)
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


# ---------------------------------------------------------------------------get sub sub category ---------------------------------------------------------------------------------

def get_sub_sub_category_id(super_categories,categories, sub_categories, sub_sub_categories):
    print("get_sub_sub_category_id called",super_categories,categories, sub_categories, sub_sub_categories)
    filtered_ids = []
    for item in master_data:
        if (
            item["super_category"].strip()  == super_categories and
            item["category"].strip() == categories and
            item["sub_category"].strip() == sub_categories and
            item["sub_sub_category"].strip() == sub_sub_categories
        ):
            filtered_ids.append(item["sub_sub_category_id"])
            if len(filtered_ids)>0:
                print("line number 73 filtered_ids",filtered_ids)
                return filtered_ids[0]
            else:
                print("Getting None from function get_sub_sub_category_id")
                return None

# ------------------------------------------------------------------------------- get ondc domain and madetory field using sub_sub_category_id --------------------------------------------   

def get_ONDC_parameter(sub_sub_category_id):
    print("get_ONDC_parameter called",sub_sub_category_id)
    for item in master_data:
        if item["sub_sub_category_id"].strip()  == sub_sub_category_id :
                print("result from function get_ONDC_parameter",item)
                return item
    else:
        print("Getting None from function get_ONDC_parameter")
        return None

# --------------------------------------------------------------------------------get dominating color code from images------------------------------------------------------------------------------------
def getColorCode():
    # download_path = "temp.png"
    # output_path = "temp.png"
    # download_image(url, download_path)
    imgArr = get_all_files("./data/temp")
    hexArray = []
    delete_files_in_folder("./data/segmented_img")
    for img in imgArr:
        remove_background_and_save(img)
    segmentedImgArr = get_all_files("./data/segmented_img")

    for img in segmentedImgArr:
        dominant_color_hex = get_dominant_color(img)
        hexArray.append(dominant_color_hex)
        
    delete_files_in_folder("./data/segmented_img")

    print("Color_Hex_Code --> ", hexArray)
    domHex = dominant_hex(hexArray)
    hex_ =  find_nearest_color(domHex)
    return [hex_]
    # return "getColorCode function called"

def dominant_hex(hex_codes):
    def hex_to_rgb(hex_code):
        hex_code = hex_code.lstrip('#')
        return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

    def rgb_distance(rgb1, rgb2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)))

    hex_codes_rgb = [hex_to_rgb(hex_code) for hex_code in hex_codes]
    dominant_rgb = min(hex_codes_rgb, key=lambda rgb: sum(rgb_distance(rgb, other_rgb) for other_rgb in hex_codes_rgb))
    dominant_hex = '#{:02x}{:02x}{:02x}'.format(*dominant_rgb)
    return dominant_hex

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


def getTrueColor(color_list, hex_color):
    for item in color_list:
        if item[1] == hex_color:
            color = item[1]
            print("If worked ", item[1])
            return color


def getRanColor(color_list, hex_color):
    for item in color_list:
        if item[1] == hex_color:
            ran = 0
            return ran


def matchColorName(color):
    for item in colorName.color_list:
        if item[0] == color:
            color = item[1]
            return color


def getRan2ColorName(color):
    for item in colorName.color_list:
        if item[0] == color:
            ran2 = 0
            return ran2





def remove_background_and_save(image_path):
    # Read the image
    img = cv2.imread(image_path)

    # Create a mask initialized with zeros, same size as the image
    mask = np.zeros(img.shape[:2], np.uint8)

    # Initialize background and foreground models
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)

    # Define the rectangular ROI around the object you want to keep
    rect = (50, 50, img.shape[1]-50, img.shape[0]-50)  # (x, y, width, height)

    # Apply GrabCut algorithm to extract foreground
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

    # Create a mask where the background is 0, the probable background is 2,
    # and the probable foreground and foreground are both set to 1
    mask2 = np.where((mask==2)|(mask==0), 0, 1).astype('uint8')

    # Multiply the image with the mask to get the segmented image
    segmented_image = img * mask2[:, :, np.newaxis]

    # Get the directory and filename of the original image
    directory, filename = os.path.split(image_path)

    # Save the segmented image in the same directory with '_segmented' appended to the filename
    cv2.imwrite(os.path.join("./data/segmented_img/", filename), segmented_image)
def get_all_files(folder_path):
    files = []
    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

# -----------------------------------------------------------------------------------------------get ondc color name from color code ----------------------------------------------------------------- 
def find_nearest_color(hex_color):
    color_list = colorName
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

# --------------------------------------------------------------------------------- generate uuid ----------------------------------------------
def generate_uuid():
    return str(uuid.uuid4())

# ------------------------------------------------------------download image from url--------------------------------------------------------------------------------
def download_image(url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        # base_url="downloaded_image/"+generate_uuid()+".png"
        name = "./data/temp/"+generate_uuid()+".png"
        with open(name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
       
        print(f"Image downloaded successfully to {name}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading the image: {e}")  
# ------------------------------------------------------------------upload images to shopcircuit db ------------------------------------------------------------
def upload_images(token):
    # url = "https://asia-south1-prod-shopcircuit-seller-portal.cloudfunctions.net/api/upload_catalog_img"
    url = "http://127.0.0.1:5001/prod-shopcircuit-seller-portal/asia-south1/api/upload_catalog_img"


    payload = {'dir': 'null'}
    files=[]
    imgArr = get_all_files("./data/temp")
    # print(imgArr)
    for img in  imgArr:
        print(f"{img} appended")
        files.append(('file',(img.split("/")[-1],open(f'{img}','rb'),'image/png')))
    # print(files)
    headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Authorization': f"Bearer {token}"
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)

    json_data = response.text
    data = json.loads(json_data)
    return data["url"]
    
# ------------------------------------------------------------------------------ delete all image from any folder path ------------------------
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
# ------------------------------------------------------------AI--------------------------------------------------------------------------------------
def gemini_text_modal(prompt):
    data = json.dumps({"prompt": prompt})

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImFkZHJlc3MiOiJMdWNraG5vdyIsInJvbGUiOiJBRE1JTiIsInRhdCI6IlA1RCIsIm1vYmlsZSI6IjAwMDAwMDAwIiwiYWdyZWVtZW50cyI6dHJ1ZSwib3JkZXJfbWluX3ZhbHVlIjo1MDAsImdwcyI6IjEyLjkxMTkwMCwgNzcuNjQ0NjAwIiwiZ3N0aW4iOiJBRE1JTiIsImF2YWlsYWJpbHR5Ijp7ImVuYWJsZSI6dHJ1ZSwidGltZXN0YW1wIjoiMjAyMy0wOS0yMlQxMDoxNzozNi4xNzRaIn0sIm5hbWUiOiJBZG1pbiIsImNvbXBhbnkiOiJBZG1pbiIsImVtYWlsIjoiYWRtaW5AdmlkeWFudC5jb20iLCJzdGF0dXMiOiJBQ1RJVkUiLCJpZCI6IndrdHpxeGQzS285cFB0TjVMYTNxIiwiYXZhdGFyIjoiYXNzZXRzL2ltYWdlcy9hdmF0YXJzL21hbGUtMDcuanBnIn0sImlhdCI6MTcxNzczNDMxM30.TzSijueJyH-r_PVaNU0I3WNVhHnNiSLvxRvFt3vN45k"
    }

    try:
        response = requests.post(
            url="https://asia-south1-prod-shopcircuit-seller-portal.cloudfunctions.net/api/bot/help_me_write",
            headers=headers,
            data=data
        )
        response.raise_for_status()
        print("response : ",response.json()["data"])
        return response.json()["data"]
    except requests.RequestException as e:
        print(f"Error: {e}")
        raise e 
# ------------------------------------------------------------get possible attribute-----------------------------------------------------------------------------

def get_possible_attribute(sub_sub_category_id,token):
  
    url = f"http://127.0.0.1:5001/prod-shopcircuit-seller-portal/asia-south1/api/master-data/form?sub_sub_category_id={sub_sub_category_id}"

    payload = {}
    headers = {
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'http://localhost:4200/',
    'sec-ch-ua-mobile': '?0',
    'Authorization': f'Bearer {token}',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'sec-ch-ua-platform': '"Linux"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)
    json_data = response.text
    data = json.loads(json_data)
    if data["message"] == "success":
        return data["data"]
    else:
        return []

# ---------------------------------------------------------------create formated data-----------------------------------------------------------
def create_formated_data(row,token,brand,index,ondc_status,status):
    try:
        super_category=row['super_category'] if len(str(row['super_category']))>0 else "Not Founded" 
        category=row['category'] if len(str(row['category']))>0 else "Not Founded" 
        sub_category=row['sub_category'] if len(str(row['sub_category']))>0 else "Not Founded" 
        sub_sub_category=row['sub_sub_category'] if len(str(row['sub_sub_category']))>0 else "Not Founded" 
        sub_sub_category_id=get_sub_sub_category_id(row['super_category'],str(row['category']),str(row['sub_category']),str(row['sub_sub_category']))
        ondc_parameter = get_ONDC_parameter(sub_sub_category_id)
        domain = ondc_parameter["ondc_domain"] if ondc_parameter != None else "NA"
        ondc_category_new = ondc_parameter["ondc_category"] if ondc_parameter != None else "NA"
        sku_id=str(row['prod_code']) if len(str(row['prod_code']))>4 else row['product_name'][:3]+"1234" 
        prod_code=row['product_name'] if len(str(row['product_name']))>4 else "Not Founded" 
        short_desc=row['short_desc'] if len(str(row['short_desc']))>4 else "Not Available" 
        long_desc=row['long_desc']if len(str(row['long_desc']))>4 else "Not Available"
        manuf_detail = str(row['manuf_detail']).split(": ")[1].strip() if len(str(row['manuf_detail']).split(":"))>1 else "Self"
        packer_detail = str(row['packer_detail']).split(": ")[1].strip() if len(str(row['packer_detail']).split(":"))>1 else "Self"
        cancellable="Yes"
        replaceable="Yes"
        returnable="Yes"
        time_to_ship="P2D"
        brand=row['brand'] if len(str(row['brand']))>0 else "Not Available"
        ondc_price=get_number(row['price']) if get_number(row['price'])>0 else 0
        mrp=get_number(row['mrp']) if get_number(row['mrp'])>0 else 0
        images = row["images"]
    
        print(type(images))
        for tempImg in ast.literal_eval(images) :
            if tempImg != None :
                download_image(tempImg)
        long_desc = gemini_text_modal(f"Write 5 line short description of {prod_code} for selling purpose. provide only description do not write unwanted things.")
        
    
        possible_attr = get_possible_attribute(sub_sub_category_id,token)
        # print("possible_attr : ",possible_attr)
        tempValues = get_values_by_name(possible_attr,"variation")
        size = row['size'].strip('[]').replace('"', '')
        print("size :",size ,type(size))
        images = upload_images(token)
        if size == 'NA' or size == 'NAN' or size == 'nan' or type(size) == float or size == '':
            size_list = ['Free Size']
        else:
            size_list = size.split(",")
            size_list = [item.strip() for item in size_list]
            size_list = filter_list(tempValues,size_list)

        colors=row['color']
        print("=====",colors)
        if type(colors) == float:
            if math.isnan(float(colors)):
                print("The value is NaN")
                colors_array = getColorCode()
        elif str(colors) == 'NA':
            print("The value is Na")
            colors_array = getColorCode()
        elif str(colors) == '[]':
            print("The value is Na")
            colors_array = getColorCode()
        elif colors == []:
            print("The value is []")
            colors_array = getColorCode()
        elif colors == None or colors == "":
            print("The value is None")
            colors_array = getColorCode()
        elif not colors:
            print("The value is []")
            colors_array = getColorCode()
        else:  
            print("The value is [some data]",type(colors),colors)  
            
            colors_array = gemini_text_modal(f"provide only hex code  array in text form  of colors {colors} in format of hex1,hex2,hex3 .Make sure solution length same as provided color array.").strip().replace("```\n","").replace("\n```","").split(",")
            
            colors_array = [find_nearest_color(s.strip()) for s in colors_array]
            colors_array = [s.replace("#","") for s in colors_array]
            colorNameAndCodeMap = dict(zip(ast.literal_eval(colors), colors_array))
            print("colorNameAndCodeMap : ",colorNameAndCodeMap)
            
            
            
        # Create the dictionary with the size list and an empty color list
        colors_array = [s.replace("#","") for s in colors_array]
        variants = {"size": size_list, "color": colors_array}
        
        specifications = get_formated_specification(possible_attr,row["specification"],variants,brand,super_category,sub_sub_category_id,token)
        if row["variation_image_map"] != '{}':
            print("getting variation_image_map {}",row["variation_image_map"])
            variation_override = createVariationOverride(ast.literal_eval(row["variation_image_map"]),colorNameAndCodeMap,variants,token)
        else:
            variation_override = []  
    
        # specifications=get_formated_specification(row['specification'],variants,brand,sub_sub_category_id,"gfhdgf",colors_array)
        # print("specifications --> ",specifications)
        # print("Specification -->",specifications)
        # single_upload(super_category,category,sub_category,sub_sub_category,sub_sub_category_id,sku_id,prod_code,short_desc,long_desc,manuf_detail,packer_detail,cancellable,replaceable,returnable,time_to_ship,ondc_price,mrp,specifications,images)
        print("=============================================================All print start ============================================================")
        print("### Sub Sub Category ID: ", sub_sub_category_id)
        print("### SKU ID: ", sku_id)
        print("### Product Code: ", prod_code)
        print("### Short Description: ", short_desc)
        print("### Long Description: ", long_desc)
        print("### Manufacturer Details: ", manuf_detail)
        print("### Packer Details: ", packer_detail)
        print("### Cancellable: ", cancellable)
        print("### Replaceable: ", replaceable)
        print("### Returnable: ", returnable)
        print("### Time to Ship: ", time_to_ship)
        print("### Brand: ", brand)
        print("### ONDC Price: ", ondc_price)
        print("### MRP: ", mrp)
        print("### Size: ", size_list)
        print("### Colors: ", colors_array)
        print("### Variants: ", variants)
        print("### Images: ", images)
        print("### ondc domain: ", domain)
        print("### ondc category: ", ondc_category_new)
        print("### specifications: ", specifications)
        print("### variation override: ", variation_override)
        print("### Category Hierarchy: ")
        print("  * Super Category: ", super_category)
        print("  * Category: ", category)
        print("  * Sub Category: ", sub_category)
        print("  * Sub Sub Category: ", sub_sub_category)
        print("  * Sub Sub Category ID: ", sub_sub_category_id)
        print("=============================================================All print end ============================================================")
        single_upload(token, domain,ondc_category_new, super_category,category,sub_category,sub_sub_category,sub_sub_category_id,sku_id,prod_code,short_desc,long_desc,manuf_detail,packer_detail,cancellable,replaceable,returnable,time_to_ship,ondc_price,mrp,specifications,images,variation_override,ondc_status,status)
    except Exception as e:
        print("Error in uploading product ",index)
        exc_type, exc_value, exc_traceback = sys.exc_info()
    print(f"Exception type: {exc_type}")
    print(f"Exception value: {exc_value}")
    print(f"Traceback: {exc_traceback}")

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
def get_formated_specification(possible_attr,rawSpec,varient,brand,super_category,sub_sub_category_id,token):
    rawSpec = ast.literal_eval(rawSpec)
    print("rawSpec --> ",rawSpec)
    print("type ---->", type(rawSpec))
    data = possible_attr
    # print("data --> ",data,type(data))
    required_fields = {d['name']: d['values'][0] for d in data if d['validators']['required']}
    print("required_fields : ",required_fields)
    result = {}

    for key, value in required_fields.items():
        found = False
        for d in rawSpec:
            for k, v in d.items():
                if key.replace(' ', '_').lower() == k.replace(' ', '_').lower():
                    result[key] = str(v[0])
                    found = True
                    break
            if found:
                break
        if not found:
            result[key] = value

    result['variation'] = varient["size"]
    result['color'] = varient["color"]
    if "gender" in result:
        result['gender'] = "female" if "women" in super_category else "male" if "men" in super_category else "unisex"
    result['country_of_origin'] = "India"
    result['brand'] = brand
    print(required_fields)
    print("results : ",result)
    return result
def createVariationOverride(variation_img, colormap,variants,token):
    for k,v in variation_img.items():
        delete_files_in_folder("./data/temp")
        for i in v:
            download_image(i)
        variation_img[k] = upload_images(token)
    cartesian_payload = []
    if "color" in variants:
        print(f"color: {variants['color']}")
        cartesian_payload.append(variants['color'])
        for attr in variants:
            if attr != "color":
                print(f"{attr}: {variants[attr]}")
                cartesian_payload.append(variants[attr])
    else:
        for attr in variants:
            print(f"{attr}: {variants[attr]}")
            cartesian_payload.append(variants[attr])
    cross_product_dict_result = cross_product_dict(cartesian_payload)
    print("cross_product_dict_result : ",cross_product_dict_result)
    print(type(variation_img),variation_img)
    dict1 = colormap
    dict2 = variation_img
    dict3 = cross_product_dict_result

    result = {}
    for key, value in dict1.items():
        for k, v in dict3.items():
            if value in k:
                result[k] = dict2[key.strip()]
    
    print("result---variation: ",result)
    finalArray = []
    for key, value in result.items():
        finalResult = {}
        finalResult["updated_at"] = datetime.now().isoformat()
        finalResult[key] = {"images": value}
        finalArray.append(finalResult)
    return finalArray
def get_values_by_name(data, name):
    for item in data:
        if item["name"] == name:
            return item["values"]
    return None
def filter_list(list1, list2):
    result = [element for element in list2 if element in list1]
    if not result:
        result = [list1[1]]
    return result
def cross_product_dict(list_of_lists):
    keys = ['#'.join(p) for p in cartesian_product(*list_of_lists)]
    return {key: "---" for key in keys}

# ================================================================testing code =================================================================
# print(master_data)

# super_categories = "Consumer Electronics"
# categories = "Computers & Accessories"
# sub_categories = "Hard Drive Accessories"
# sub_sub_categories = "Caddies"

# result = get_sub_sub_category_id(super_categories, categories, sub_categories, sub_sub_categories)
# print("Result:", result)

# print(get_ONDC_parameter("REUYyruDYAIookCkGThW"))    # working

# print(generate_uuid())   # working
# download_image("https://4.imimg.com/data4/UE/DH/MY-11759647/cloth-fabric-500x500.jpg")   # working
# delete_files_in_folder("./data/temp")   # working

# print(colorName) # working

# print(get_all_files("./data/temp")) # working
# print(getColorCode()) # working

# hex_codes = [ '#0000F7','#FF0000', '#00FF09', '#00FF00', '#0000FF']   # working
# dominant_hex = dominant_hex(hex_codes)
# print(dominant_hex)


# print(find_nearest_color("#000742".upper()))   # working

# print(upload_images("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlzX3Bob25lX3ZlcmlmaWVkIjp0cnVlLCJyb2xlIjoiVVNFUiIsInNpZ25hdHVyZSI6Imh0dHBzOi8vc3RvcmFnZS5nb29nbGVhcGlzLmNvbS92YWFuaWotdXNlci1zaWduYXR1cmUvUGFua2FqIFNpbmdoLWZMQmtoVlFVZEVaRWpWRUJaUllYL0lNR18yMDIzMTAxMF8yMTE5NDAuanBnIiwiY3JlYXRlZF9hdCI6eyJfc2Vjb25kcyI6MTY5NDg1MzYwOCwiX25hbm9zZWNvbmRzIjo0NDgwMDAwMDB9LCJiYW5rIjp7Imlmc2NfY29kZSI6IkNOUkIyMzQ1IiwiYWNjb3VudF9udW1iZXIiOjQ1Nzg0NzM0NzM5NDgzOSwiYmVuZWZpY2lhcnlfbmFtZSI6IlBhbmthaiIsImFjY291bnRfdHlwZSI6IlNhdmluZ3MiLCJicmFuY2hfYWRkcmVzcyI6IkJhbmsgUm9hZCJ9LCJjb21wYW55X2xvZ28iOiJodHRwczovL2VuY3J5cHRlZC10Ym4wLmdzdGF0aWMuY29tL2ltYWdlcz9xPXRibjpBTmQ5R2NSQUhYUGx1cTZHdFRSUERJSFJ2NWtKUHk4NnVGanA1c083aGcmdXNxcD1DQVUiLCJpc19nc3Rpbl92ZXJpZmllZCI6dHJ1ZSwiY29tcGFueSI6IklNIFRlY2ggUHZ0IEx0ZC4iLCJjb21wYW55X3VybCI6Imh0dHBzOi8vY29zbWljLXNlbGtpZS05M2ZhNTUubmV0bGlmeS5hcHAiLCJzdG9yZV90aW1pbmciOnsiY2xvc2UiOiIxODozMCIsIm9wZW4iOiI5OjMwIn0sImVtYWlsIjoic2luZ2hwYW5rYWo3MDU3QGdtYWlsLmNvbSIsImFncmVlbWVudCI6dHJ1ZSwibW9iaWxlIjo5NTMyNjk2NDYxLCJncHMiOiIxMi45MTE5MDAsIDc3LjY0NDYwMCIsIm5hbWUiOiJQYW5rYWogU2luZ2giLCJhZ3JlZW1lbnRfdGltZSI6IjIwMjMtMDktMjJUMTA6MTc6MzYuMTc0WiIsImF2YWlsYWJpbHR5Ijp7ImVuYWJsZSI6ZmFsc2UsInRpbWVzdGFtcCI6IjIwMjMtMTEtMDhUMDY6MDE6MTMuMjUxWiJ9LCJ0YXQiOiJQMTBEIiwicHJvZmlsZV9pbWciOiJodHRwczovL3N0b3JhZ2UuZ29vZ2xlYXBpcy5jb20vc2hvcC1jaXJjdWl0LXVzZXItZGF0YS9pbWFnZS9wcm9maWxlLXBpY3R1cmUvUGFua2FqIFNpbmdoLWZMQmtoVlFVZEVaRWpWRUJaUllYL21hbGUtdXNlci1hdmF0YXItaWNvbi1pbi1mbGF0LWRlc2lnbi1zdHlsZS1wZXJzb24tc2lnbnMtaWxsdXN0cmF0aW9uLXBuZy53ZWJwIiwiZ3N0aW4iOiJndmRmbmdkZmtnaGRjIiwibG9jYXRpb25zIjpbeyJhZGRyZXNzIjp7ImNvdW50cnkiOiJJbmRpYSIsInBpbmNvZGUiOjI3MzIwOSwiY2l0eSI6IkJhcmllcGFyIiwic3RyZWV0IjoieXl5IiwiZGlzdHJpY3QiOiJHb3Jha2hwdXIiLCJsb2NhbGl0eSI6Inh4eCIsInN0YXRlIjoiVXR0YXIgUHJhZGVzaCJ9LCJwaWNrdXBfbG9jYXRpb24iOiJIb21lIDEiLCJncHMiOiIyNi42ODAwNTIsIDgzLjEyODczMjUiLCJ0aW1lIjp7InNjaGVkdWxlIjp7ImhvbGlkYXlzIjpbXX0sInJhbmdlIjp7InN0YXJ0IjoiIiwiZW5kIjoiIn0sImxhYmVsIjoiIiwidGltZXN0YW1wIjoiMjAyNC0wMS0xNVQwOToyOTozMC4zMjJaIn0sImxvY2F0aW9uX2lkIjoiYTAxZGRjMTBjN2I5NGExYmE0ZDU0YjJhYzZmOTJjYTEifSx7ImFkZHJlc3MiOnsiY291bnRyeSI6IkluZGlhIiwicGluY29kZSI6MjczMjA5LCJjaXR5IjoiQmFyaWVwYXIiLCJzdHJlZXQiOiJhYWEiLCJkaXN0cmljdCI6IkdvcmFraHB1ciIsImxvY2FsaXR5Ijoienp6Iiwic3RhdGUiOiJVdHRhciBQcmFkZXNoIn0sInBpY2t1cF9sb2NhdGlvbiI6IkhvbWUgMiIsImdwcyI6IjI2LjY4MDA1MiwgODMuMTI4NzMyNSIsInRpbWUiOnsic2NoZWR1bGUiOnsiaG9saWRheXMiOltdfSwicmFuZ2UiOnsic3RhcnQiOiIiLCJlbmQiOiIifSwibGFiZWwiOiIiLCJ0aW1lc3RhbXAiOiIyMDI0LTAxLTE1VDA5OjI5OjU3LjExMFoifSwibG9jYXRpb25faWQiOiJlZTcxMjI3ZTgwNzk0MmM1OTY5MWI2MTVmNjNjNmMxZSJ9LHsiYWRkcmVzcyI6eyJjb3VudHJ5IjoiSW5kaWEiLCJwaW5jb2RlIjoyMjYwMTAsImNpdHkiOiJHb210aW5hZ2FyIiwic3RyZWV0IjoiSW5kcmEgcHJhaXN0aGFuIG1hcmciLCJkaXN0cmljdCI6Ikx1Y2tub3ciLCJsb2NhbGl0eSI6IkxldmFuIGN5YmVyIGhlaWdodCIsInN0YXRlIjoiVXR0YXIgUHJhZGVzaCJ9LCJwaWNrdXBfbG9jYXRpb24iOiJPZmZpY2UiLCJncHMiOiIyNi44NTU4NjYwNzkxNjY2NywgODAuOTk5MjI3NjU5NzIyMjIiLCJ0aW1lIjp7InNjaGVkdWxlIjp7ImhvbGlkYXlzIjpbXX0sInJhbmdlIjp7InN0YXJ0IjoiIiwiZW5kIjoiIn0sImxhYmVsIjoiIiwidGltZXN0YW1wIjoiMjAyNC0wMS0xNVQwOTo0MDo1Ny43OTdaIn0sImxvY2F0aW9uX2lkIjoiYTZiOTQyY2FkM2MyNDJiYzkzYzk4NDk0YjAwODIxMWUifSx7ImFkZHJlc3MiOnsiY291bnRyeSI6IkluZGlhIiwicGluY29kZSI6MjI2MDEwLCJjaXR5IjoiR29tdGluYWdhciIsInN0cmVldCI6ImFiYyIsImRpc3RyaWN0IjoiTHVja25vdyIsImxvY2FsaXR5IjoieHl6Iiwic3RhdGUiOiJVdHRhciBQcmFkZXNoIn0sInBpY2t1cF9sb2NhdGlvbiI6Ik9mZmljZSAxIiwiZ3BzIjoiMjYuODU1ODY2MDc5MTY2NjcsIDgwLjk5OTIyNzY1OTcyMjIyIiwidGltZSI6eyJzY2hlZHVsZSI6eyJob2xpZGF5cyI6W119LCJyYW5nZSI6eyJzdGFydCI6IiIsImVuZCI6IiJ9LCJsYWJlbCI6IiIsInRpbWVzdGFtcCI6IjIwMjQtMDEtMTVUMDk6NDE6NDMuMjE3WiJ9LCJsb2NhdGlvbl9pZCI6IjkzNTBiMTJjZDRlZDQ5NTI5OTVmZmVlMjRmZmU4MzE3In1dLCJkZXNjcmlwdGlvbiI6IlRoaXMgaXMgZGVzY3JpcHRpb24uLi4uIiwidXBkYXRlZF9hdCI6IjIwMjQtMDYtMjBUMDk6MDQ6NTIuNTc0WiIsInN0YXR1cyI6IkFDVElWRSIsIm9yZGVyX21pbl92YWx1ZSI6Ijk5IiwiaWQiOiJmTEJraFZRVWRFWkVqVkVCWlJZWCIsImF2YXRhciI6ImFzc2V0cy9pbWFnZXMvYXZhdGFycy9tYWxlLTA3LmpwZyJ9LCJpYXQiOjE3MjAxNjc3NTR9.iL-dKRMILQtjN32lXWhLlB6-rOhU_7aRJggzAKF9AHU"))

# print(get_possible_attribute("20IIhmgp5I6t4rNC2nh0","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlzX3Bob25lX3ZlcmlmaWVkIjp0cnVlLCJyb2xlIjoiVVNFUiIsInNpZ25hdHVyZSI6Imh0dHBzOi8vc3RvcmFnZS5nb29nbGVhcGlzLmNvbS92YWFuaWotdXNlci1zaWduYXR1cmUvUGFua2FqIFNpbmdoLWZMQmtoVlFVZEVaRWpWRUJaUllYL0lNR18yMDIzMTAxMF8yMTE5NDAuanBnIiwiY3JlYXRlZF9hdCI6eyJfc2Vjb25kcyI6MTY5NDg1MzYwOCwiX25hbm9zZWNvbmRzIjo0NDgwMDAwMDB9LCJiYW5rIjp7Imlmc2NfY29kZSI6IkNOUkIyMzQ1IiwiYWNjb3VudF9udW1iZXIiOjQ1Nzg0NzM0NzM5NDgzOSwiYmVuZWZpY2lhcnlfbmFtZSI6IlBhbmthaiIsImFjY291bnRfdHlwZSI6IlNhdmluZ3MiLCJicmFuY2hfYWRkcmVzcyI6IkJhbmsgUm9hZCJ9LCJjb21wYW55X2xvZ28iOiJodHRwczovL2VuY3J5cHRlZC10Ym4wLmdzdGF0aWMuY29tL2ltYWdlcz9xPXRibjpBTmQ5R2NSQUhYUGx1cTZHdFRSUERJSFJ2NWtKUHk4NnVGanA1c083aGcmdXNxcD1DQVUiLCJpc19nc3Rpbl92ZXJpZmllZCI6dHJ1ZSwiY29tcGFueSI6IklNIFRlY2ggUHZ0IEx0ZC4iLCJjb21wYW55X3VybCI6Imh0dHBzOi8vY29zbWljLXNlbGtpZS05M2ZhNTUubmV0bGlmeS5hcHAiLCJzdG9yZV90aW1pbmciOnsiY2xvc2UiOiIxODozMCIsIm9wZW4iOiI5OjMwIn0sImVtYWlsIjoic2luZ2hwYW5rYWo3MDU3QGdtYWlsLmNvbSIsImFncmVlbWVudCI6dHJ1ZSwibW9iaWxlIjo5NTMyNjk2NDYxLCJncHMiOiIxMi45MTE5MDAsIDc3LjY0NDYwMCIsIm5hbWUiOiJQYW5rYWogU2luZ2giLCJhZ3JlZW1lbnRfdGltZSI6IjIwMjMtMDktMjJUMTA6MTc6MzYuMTc0WiIsImF2YWlsYWJpbHR5Ijp7ImVuYWJsZSI6ZmFsc2UsInRpbWVzdGFtcCI6IjIwMjMtMTEtMDhUMDY6MDE6MTMuMjUxWiJ9LCJ0YXQiOiJQMTBEIiwicHJvZmlsZV9pbWciOiJodHRwczovL3N0b3JhZ2UuZ29vZ2xlYXBpcy5jb20vc2hvcC1jaXJjdWl0LXVzZXItZGF0YS9pbWFnZS9wcm9maWxlLXBpY3R1cmUvUGFua2FqIFNpbmdoLWZMQmtoVlFVZEVaRWpWRUJaUllYL21hbGUtdXNlci1hdmF0YXItaWNvbi1pbi1mbGF0LWRlc2lnbi1zdHlsZS1wZXJzb24tc2lnbnMtaWxsdXN0cmF0aW9uLXBuZy53ZWJwIiwiZ3N0aW4iOiJndmRmbmdkZmtnaGRjIiwibG9jYXRpb25zIjpbeyJhZGRyZXNzIjp7ImNvdW50cnkiOiJJbmRpYSIsInBpbmNvZGUiOjI3MzIwOSwiY2l0eSI6IkJhcmllcGFyIiwic3RyZWV0IjoieXl5IiwiZGlzdHJpY3QiOiJHb3Jha2hwdXIiLCJsb2NhbGl0eSI6Inh4eCIsInN0YXRlIjoiVXR0YXIgUHJhZGVzaCJ9LCJwaWNrdXBfbG9jYXRpb24iOiJIb21lIDEiLCJncHMiOiIyNi42ODAwNTIsIDgzLjEyODczMjUiLCJ0aW1lIjp7InNjaGVkdWxlIjp7ImhvbGlkYXlzIjpbXX0sInJhbmdlIjp7InN0YXJ0IjoiIiwiZW5kIjoiIn0sImxhYmVsIjoiIiwidGltZXN0YW1wIjoiMjAyNC0wMS0xNVQwOToyOTozMC4zMjJaIn0sImxvY2F0aW9uX2lkIjoiYTAxZGRjMTBjN2I5NGExYmE0ZDU0YjJhYzZmOTJjYTEifSx7ImFkZHJlc3MiOnsiY291bnRyeSI6IkluZGlhIiwicGluY29kZSI6MjczMjA5LCJjaXR5IjoiQmFyaWVwYXIiLCJzdHJlZXQiOiJhYWEiLCJkaXN0cmljdCI6IkdvcmFraHB1ciIsImxvY2FsaXR5Ijoienp6Iiwic3RhdGUiOiJVdHRhciBQcmFkZXNoIn0sInBpY2t1cF9sb2NhdGlvbiI6IkhvbWUgMiIsImdwcyI6IjI2LjY4MDA1MiwgODMuMTI4NzMyNSIsInRpbWUiOnsic2NoZWR1bGUiOnsiaG9saWRheXMiOltdfSwicmFuZ2UiOnsic3RhcnQiOiIiLCJlbmQiOiIifSwibGFiZWwiOiIiLCJ0aW1lc3RhbXAiOiIyMDI0LTAxLTE1VDA5OjI5OjU3LjExMFoifSwibG9jYXRpb25faWQiOiJlZTcxMjI3ZTgwNzk0MmM1OTY5MWI2MTVmNjNjNmMxZSJ9LHsiYWRkcmVzcyI6eyJjb3VudHJ5IjoiSW5kaWEiLCJwaW5jb2RlIjoyMjYwMTAsImNpdHkiOiJHb210aW5hZ2FyIiwic3RyZWV0IjoiSW5kcmEgcHJhaXN0aGFuIG1hcmciLCJkaXN0cmljdCI6Ikx1Y2tub3ciLCJsb2NhbGl0eSI6IkxldmFuIGN5YmVyIGhlaWdodCIsInN0YXRlIjoiVXR0YXIgUHJhZGVzaCJ9LCJwaWNrdXBfbG9jYXRpb24iOiJPZmZpY2UiLCJncHMiOiIyNi44NTU4NjYwNzkxNjY2NywgODAuOTk5MjI3NjU5NzIyMjIiLCJ0aW1lIjp7InNjaGVkdWxlIjp7ImhvbGlkYXlzIjpbXX0sInJhbmdlIjp7InN0YXJ0IjoiIiwiZW5kIjoiIn0sImxhYmVsIjoiIiwidGltZXN0YW1wIjoiMjAyNC0wMS0xNVQwOTo0MDo1Ny43OTdaIn0sImxvY2F0aW9uX2lkIjoiYTZiOTQyY2FkM2MyNDJiYzkzYzk4NDk0YjAwODIxMWUifSx7ImFkZHJlc3MiOnsiY291bnRyeSI6IkluZGlhIiwicGluY29kZSI6MjI2MDEwLCJjaXR5IjoiR29tdGluYWdhciIsInN0cmVldCI6ImFiYyIsImRpc3RyaWN0IjoiTHVja25vdyIsImxvY2FsaXR5IjoieHl6Iiwic3RhdGUiOiJVdHRhciBQcmFkZXNoIn0sInBpY2t1cF9sb2NhdGlvbiI6Ik9mZmljZSAxIiwiZ3BzIjoiMjYuODU1ODY2MDc5MTY2NjcsIDgwLjk5OTIyNzY1OTcyMjIyIiwidGltZSI6eyJzY2hlZHVsZSI6eyJob2xpZGF5cyI6W119LCJyYW5nZSI6eyJzdGFydCI6IiIsImVuZCI6IiJ9LCJsYWJlbCI6IiIsInRpbWVzdGFtcCI6IjIwMjQtMDEtMTVUMDk6NDE6NDMuMjE3WiJ9LCJsb2NhdGlvbl9pZCI6IjkzNTBiMTJjZDRlZDQ5NTI5OTVmZmVlMjRmZmU4MzE3In1dLCJkZXNjcmlwdGlvbiI6IlRoaXMgaXMgZGVzY3JpcHRpb24uLi4uIiwidXBkYXRlZF9hdCI6IjIwMjQtMDYtMjBUMDk6MDQ6NTIuNTc0WiIsInN0YXR1cyI6IkFDVElWRSIsIm9yZGVyX21pbl92YWx1ZSI6Ijk5IiwiaWQiOiJmTEJraFZRVWRFWkVqVkVCWlJZWCIsImF2YXRhciI6ImFzc2V0cy9pbWFnZXMvYXZhdGFycy9tYWxlLTA3LmpwZyJ9LCJpYXQiOjE3MjAxNjc3NTR9.iL-dKRMILQtjN32lXWhLlB6-rOhU_7aRJggzAKF9AHU"))