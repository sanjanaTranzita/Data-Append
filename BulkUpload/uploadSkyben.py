import requests
import json
import pandas as pd
import jwt
import secrets 
import re
import os
import gdown
from google_drive_downloader import GoogleDriveDownloader as gdd

master_data=json.load(open('catalogs_with_attribute.json'))['data']

my_list = []

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlzX3Bob25lX3ZlcmlmaWVkIjp0cnVlLCJyb2xlIjoiVVNFUiIsInNpZ25hdHVyZSI6bnVsbCwiZGVzY3JpcHRpb24iOm51bGwsImNyZWF0ZWRfYXQiOiIyMDIzLTEwLTA1VDA2OjQ3OjM0LjUwNloiLCJnc3RpbiI6IjAzQVdZUEo1NjU5RzFaMCIsImJhbmsiOnsiaWZzY19jb2RlIjoiIiwiYWNjb3VudF9udW1iZXIiOiIiLCJiZW5lZmljaWFyeV9uYW1lIjoiIiwiYWNjb3VudF90eXBlIjoiIiwiYnJhbmNoX2FkZHJlc3MiOiIifSwiY29tcGFueV9sb2dvIjoiaHR0cHM6Ly9lbmNyeXB0ZWQtdGJuMC5nc3RhdGljLmNvbS9pbWFnZXM_cT10Ym46QU5kOUdjUkFIWFBsdXE2R3RUUlBESUhSdjVrSlB5ODZ1RmpwNXNPN2hnJnVzcXA9Q0FVIiwidXBkYXRlZF9hdCI6IjIwMjMtMTAtMDVUMDc6MTM6MTEuNDQ4WiIsImlzX2dzdGluX3ZlcmlmaWVkIjp0cnVlLCJjb21wYW55IjoiTS9zIFMgUyBBbmQgQ29tcGFueSIsImNvbXBhbnlfdXJsIjpudWxsLCJzdG9yZV90aW1pbmciOnsiY2xvc2UiOiIxODozMCIsIm9wZW4iOiI5OjMwIn0sImVtYWlsIjoic3NhbmRjb21wYW55bGRoQGdtYWlsLmNvbSIsImFncmVlbWVudCI6dHJ1ZSwibW9iaWxlIjo4MTQ2OTMzOTk5LCJncHMiOiIxMi45MTE5MDAsIDc3LjY0NDYwMCIsImF2YWlsYWJpbHR5Ijp7ImVuYWJsZSI6dHJ1ZSwidGltZXN0YW1wIjoiMjAyMy0xMC0wNVQwNjo0NzozNC41MDZaIn0sInByb2ZpbGVfaW1nIjoiaHR0cHM6Ly9zdGF0aWMudmVjdGVlenkuY29tL3N5c3RlbS9yZXNvdXJjZXMvcHJldmlld3MvMDAzLzI0MC8zODMvbm9uXzJ4L2Jlc3Qtc2VsbGVyLWdvbGRlbi1iYWRnZS1pc29sYXRlZC1pbGx1c3RyYXRpb24tdmVjdG9yLmpwZyIsIm5hbWUiOiJBcnVqICIsImFncmVlbWVudF90aW1lIjoiMjAyMy0xMC0wNVQwNjo0NzozNC41MDZaIiwibG9jYXRpb25zIjpbeyJhZGRyZXNzIjoiNTIuNzIwNjE1NDk5OTk5OTk0LDU4LjY2NTc0NjE4MTA4OTQzIiwicGlja3VwX2xvY2F0aW9uIjoiQXJ1aiAjIFBsb3QgTm8uIDIyICYgMjMsIHN0cmVldCBuby4gMTAoQmFjayBTaWRlIEdhdGUgV2FsaSBHYWxpKSMxNDEwMDc4MTQ2OTMzOTk5IiwidGltZSI6eyJzY2hlZHVsZSI6eyJob2xpZGF5cyI6W119LCJsYWJlbCI6dHJ1ZSwidGltZXN0YW1wIjoiMjAyMy0xMC0wNVQwNzoxMTo0MS4yOTBaIn0sImdwcyI6IjEyLjkxMTkwMCwgNzcuNjQ0NjAwIn1dLCJzdGF0dXMiOiJBQ1RJVkUiLCJ0YXQiOiJQNUQiLCJpZCI6IldaZG5ncFVFN1FCYkRzSWVoUXp4IiwiYXZhdGFyIjoiYXNzZXRzL2ltYWdlcy9hdmF0YXJzL21hbGUtMDcuanBnIn0sImlhdCI6MTcwNTY0NjgxNn0.-qAolhkc-ehzwelsVP_NVFTYphPOV7Alpb6_zRnvwF8'
def single_upload(super_category,category,sub_category,sub_sub_category,sub_sub_category_id,sku_id,prod_code,short_desc,long_desc,manuf_detail,packer_detail,cancellable,replaceable,returnable,time_to_ship,ondc_price,mrp,specifications,images):
    data3=pd.read_excel("ondc_category_mapping.xlsx")
    for index, row in data3.iterrows():
        sub_sub_categoryId2 =row['sub_sub_category_id'] if len(str(row['sub_sub_category_id']))>0 else "Not Founded"
        if sub_sub_categoryId2 == sub_sub_category_id:
            # sub_sub_category_id=row['sub_sub_category_id'] if len(str(row['sub_sub_category_id']))>0 else "Not Founded"
            Ondc_category_new=row['Ondc_category_new'] if len(str(row['Ondc_category_new']))>0 else "Not Founded"
            print("Ondc_category_new",Ondc_category_new)

    url = "https://asia-south1-prod-shopcircuit-seller-portal.cloudfunctions.net/api/catalog/create_single"
  
    data=jwt.decode(token, options={"verify_signature": False})
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
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlzX3Bob25lX3ZlcmlmaWVkIjp0cnVlLCJyb2xlIjoiVVNFUiIsInNpZ25hdHVyZSI6bnVsbCwiZGVzY3JpcHRpb24iOm51bGwsImNyZWF0ZWRfYXQiOiIyMDIzLTEwLTA1VDA2OjQ3OjM0LjUwNloiLCJnc3RpbiI6IjAzQVdZUEo1NjU5RzFaMCIsImJhbmsiOnsiaWZzY19jb2RlIjoiIiwiYWNjb3VudF9udW1iZXIiOiIiLCJiZW5lZmljaWFyeV9uYW1lIjoiIiwiYWNjb3VudF90eXBlIjoiIiwiYnJhbmNoX2FkZHJlc3MiOiIifSwiY29tcGFueV9sb2dvIjoiaHR0cHM6Ly9lbmNyeXB0ZWQtdGJuMC5nc3RhdGljLmNvbS9pbWFnZXM_cT10Ym46QU5kOUdjUkFIWFBsdXE2R3RUUlBESUhSdjVrSlB5ODZ1RmpwNXNPN2hnJnVzcXA9Q0FVIiwidXBkYXRlZF9hdCI6IjIwMjMtMTAtMDVUMDc6MTM6MTEuNDQ4WiIsImlzX2dzdGluX3ZlcmlmaWVkIjp0cnVlLCJjb21wYW55IjoiTS9zIFMgUyBBbmQgQ29tcGFueSIsImNvbXBhbnlfdXJsIjpudWxsLCJzdG9yZV90aW1pbmciOnsiY2xvc2UiOiIxODozMCIsIm9wZW4iOiI5OjMwIn0sImVtYWlsIjoic3NhbmRjb21wYW55bGRoQGdtYWlsLmNvbSIsImFncmVlbWVudCI6dHJ1ZSwibW9iaWxlIjo4MTQ2OTMzOTk5LCJncHMiOiIxMi45MTE5MDAsIDc3LjY0NDYwMCIsImF2YWlsYWJpbHR5Ijp7ImVuYWJsZSI6dHJ1ZSwidGltZXN0YW1wIjoiMjAyMy0xMC0wNVQwNjo0NzozNC41MDZaIn0sInByb2ZpbGVfaW1nIjoiaHR0cHM6Ly9zdGF0aWMudmVjdGVlenkuY29tL3N5c3RlbS9yZXNvdXJjZXMvcHJldmlld3MvMDAzLzI0MC8zODMvbm9uXzJ4L2Jlc3Qtc2VsbGVyLWdvbGRlbi1iYWRnZS1pc29sYXRlZC1pbGx1c3RyYXRpb24tdmVjdG9yLmpwZyIsIm5hbWUiOiJBcnVqICIsImFncmVlbWVudF90aW1lIjoiMjAyMy0xMC0wNVQwNjo0NzozNC41MDZaIiwibG9jYXRpb25zIjpbeyJhZGRyZXNzIjoiNTIuNzIwNjE1NDk5OTk5OTk0LDU4LjY2NTc0NjE4MTA4OTQzIiwicGlja3VwX2xvY2F0aW9uIjoiQXJ1aiAjIFBsb3QgTm8uIDIyICYgMjMsIHN0cmVldCBuby4gMTAoQmFjayBTaWRlIEdhdGUgV2FsaSBHYWxpKSMxNDEwMDc4MTQ2OTMzOTk5IiwidGltZSI6eyJzY2hlZHVsZSI6eyJob2xpZGF5cyI6W119LCJsYWJlbCI6dHJ1ZSwidGltZXN0YW1wIjoiMjAyMy0xMC0wNVQwNzoxMTo0MS4yOTBaIn0sImdwcyI6IjEyLjkxMTkwMCwgNzcuNjQ0NjAwIn1dLCJzdGF0dXMiOiJBQ1RJVkUiLCJ0YXQiOiJQNUQiLCJpZCI6IldaZG5ncFVFN1FCYkRzSWVoUXp4IiwiYXZhdGFyIjoiYXNzZXRzL2ltYWdlcy9hdmF0YXJzL21hbGUtMDcuanBnIn0sImlhdCI6MTcwNTY0NjgxNn0.-qAolhkc-ehzwelsVP_NVFTYphPOV7Alpb6_zRnvwF8',
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
                # print("line number 73 filtered_ids",filtered_ids)
                return filtered_ids[0]
            else:
                return "not founded"
            
def get_formated_specification(specfication,variants,brand,sub_sub_category_id):
    specfication=json.loads(specfication)
    variants=json.loads(variants)
    keys_to_remove = [key for key, value in variants.items() if value == "" or (isinstance(value, list) and not value)]
    for key in keys_to_remove:
         variants.pop(key)
    clothing_attributes = {}
    for item in master_data:
        if item["sub_sub_category_id"] == sub_sub_category_id:
            # Create a new attribute dictionary with all keys set to "Not Available"
            not_available_attributes = {key: "Not Available" for attribute_dict in item["attribute"] for key in attribute_dict.keys()}
            clothing_attributes.update(not_available_attributes)

    for attribute in specfication:
        key = list(attribute.keys())[0]  # Get the attribute name
        value = list(attribute.values())[0]  # Get the attribute value
        clothing_attributes[key.lower()] = value
    clothing_attributes.update({key.lower().replace(" ","_"): value for key, value in variants.items()})
    clothing_attributes["brand"]=brand
    if "size" in clothing_attributes:
        clothing_attributes["variation"] = clothing_attributes.pop("size")
    else:
        clothing_attributes["variation"] = ["Free Size"]
    if "color" in clothing_attributes:
        if isinstance(clothing_attributes["color"], str):
            clothing_attributes["color"] = ['Multicolor']
    # elif "Color" in clothing_attributes:
    #     if isinstance(clothing_attributes["Color"], str):
    #         clothing_attributes["color"] = [clothing_attributes["Color"]]
    else:
        clothing_attributes["variation"] = ["Free Size"]
    return clothing_attributes

def get_image_array(images):
    if images[-1] != "]" and images[0] != "[":
        image_urls = re.findall(r'https://[^\s]+', images)
        # Remove ?usp=sharing from each URL
        image_urls = [url.replace('?usp=sharing', '') for url in image_urls]
        return image_urls
    else:
        return json.loads(images)

def get_number(numData):
    
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
    id = url.split("/")[-2]
    try:
        url = f'https://drive.google.com/uc?id={id}'
        output = f'downloaded_image/{id}.jpg'
    
        gdd.download_file_from_google_drive(file_id=id,dest_path=output,unzip=False)
        print(f"Image downloaded successfully to {output}")
        upload_image(id)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the image: {e}") 

def upload_image(id):
    img = id+'.jpg'
    print("img -->",img)

    url = "http://127.0.0.1:5001/prod-shopcircuit-seller-portal/asia-south1/api/upload_catalog_img"

    payload = {'dir': 'null'}
    files=[
    ('file',(img,open(f'downloaded_image/{img}','rb'),'image/jpeg'))
    ]
    headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlzX3Bob25lX3ZlcmlmaWVkIjp0cnVlLCJyb2xlIjoiVVNFUiIsInNpZ25hdHVyZSI6bnVsbCwiZGVzY3JpcHRpb24iOm51bGwsImNyZWF0ZWRfYXQiOiIyMDIzLTEwLTA1VDA2OjQ3OjM0LjUwNloiLCJnc3RpbiI6IjAzQVdZUEo1NjU5RzFaMCIsImJhbmsiOnsiaWZzY19jb2RlIjoiIiwiYWNjb3VudF9udW1iZXIiOiIiLCJiZW5lZmljaWFyeV9uYW1lIjoiIiwiYWNjb3VudF90eXBlIjoiIiwiYnJhbmNoX2FkZHJlc3MiOiIifSwiY29tcGFueV9sb2dvIjoiaHR0cHM6Ly9lbmNyeXB0ZWQtdGJuMC5nc3RhdGljLmNvbS9pbWFnZXM_cT10Ym46QU5kOUdjUkFIWFBsdXE2R3RUUlBESUhSdjVrSlB5ODZ1RmpwNXNPN2hnJnVzcXA9Q0FVIiwidXBkYXRlZF9hdCI6IjIwMjMtMTAtMDVUMDc6MTM6MTEuNDQ4WiIsImlzX2dzdGluX3ZlcmlmaWVkIjp0cnVlLCJjb21wYW55IjoiTS9zIFMgUyBBbmQgQ29tcGFueSIsImNvbXBhbnlfdXJsIjpudWxsLCJzdG9yZV90aW1pbmciOnsiY2xvc2UiOiIxODozMCIsIm9wZW4iOiI5OjMwIn0sImVtYWlsIjoic3NhbmRjb21wYW55bGRoQGdtYWlsLmNvbSIsImFncmVlbWVudCI6dHJ1ZSwibW9iaWxlIjo4MTQ2OTMzOTk5LCJncHMiOiIxMi45MTE5MDAsIDc3LjY0NDYwMCIsImF2YWlsYWJpbHR5Ijp7ImVuYWJsZSI6dHJ1ZSwidGltZXN0YW1wIjoiMjAyMy0xMC0wNVQwNjo0NzozNC41MDZaIn0sInByb2ZpbGVfaW1nIjoiaHR0cHM6Ly9zdGF0aWMudmVjdGVlenkuY29tL3N5c3RlbS9yZXNvdXJjZXMvcHJldmlld3MvMDAzLzI0MC8zODMvbm9uXzJ4L2Jlc3Qtc2VsbGVyLWdvbGRlbi1iYWRnZS1pc29sYXRlZC1pbGx1c3RyYXRpb24tdmVjdG9yLmpwZyIsIm5hbWUiOiJBcnVqICIsImFncmVlbWVudF90aW1lIjoiMjAyMy0xMC0wNVQwNjo0NzozNC41MDZaIiwibG9jYXRpb25zIjpbeyJhZGRyZXNzIjoiNTIuNzIwNjE1NDk5OTk5OTk0LDU4LjY2NTc0NjE4MTA4OTQzIiwicGlja3VwX2xvY2F0aW9uIjoiQXJ1aiAjIFBsb3QgTm8uIDIyICYgMjMsIHN0cmVldCBuby4gMTAoQmFjayBTaWRlIEdhdGUgV2FsaSBHYWxpKSMxNDEwMDc4MTQ2OTMzOTk5IiwidGltZSI6eyJzY2hlZHVsZSI6eyJob2xpZGF5cyI6W119LCJsYWJlbCI6dHJ1ZSwidGltZXN0YW1wIjoiMjAyMy0xMC0wNVQwNzoxMTo0MS4yOTBaIn0sImdwcyI6IjEyLjkxMTkwMCwgNzcuNjQ0NjAwIn1dLCJzdGF0dXMiOiJBQ1RJVkUiLCJ0YXQiOiJQNUQiLCJpZCI6IldaZG5ncFVFN1FCYkRzSWVoUXp4IiwiYXZhdGFyIjoiYXNzZXRzL2ltYWdlcy9hdmF0YXJzL21hbGUtMDcuanBnIn0sImlhdCI6MTcwNTY0NjgxNn0.-qAolhkc-ehzwelsVP_NVFTYphPOV7Alpb6_zRnvwF8',
    'Connection': 'keep-alive',
    'Origin': 'http://localhost:4200',
    'Referer': 'http://localhost:4200/',
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
    
def upload_format_data(row):
    super_category="Men Fashion"
    category="Western Wear"
    sub_category="Top Wear"
    sub_sub_category="Tshirts"
    sub_sub_category_id=get_sub_sub_category_id(super_category,category,sub_category,sub_sub_category)
    sku_id=str(row['Item SKU']) if len(str(row['Item SKU']))>4 else row['Style Description'][:3]+"1234" 
    prod_code=row['StyleDescription'] if len(str(row['StyleDescription']))>4 else "Not Founded" 
    short_desc=row['Additional Information 2'] if len(str(row['Additional Information 2']))>4 else "Not Avilable" 
    long_desc=("<p>"+row['Additional Information 1']+"<br>"+row['Additional Information 2']+"<br>"+row['Additional Information 3']+"</p>")
    manuf_detail=row['Manufactured By']if len(str(row['Manufactured By']))>4 else "Not Avilable"
    packer_detail=row['Imported By'] if len(str(row['Imported By']))>4 else "Not Avilable"
    cancellable="Yes"
    replaceable="Yes"
    returnable="Yes"
    time_to_ship="P2D"
    brand=row['*Brand'] if len(str(row['*Brand']))>0 else "Not Avilable"
    ondc_price=get_number(row['*SELLING PRICE']) if get_number(row['*SELLING PRICE'])>0 else 0
    
    mrp=get_number(row['*MRP']) if get_number(row['*MRP'])>0 else 0
    color = row['*Color Family']
    if color=='Multi':
        color = "Multicolor"
    elif len(str(color))>0:
        color=color
    else:
        color = "Not Avilable"

    
    if row['*Sleeve'] == 'Short sleeve':
        sleeve = 'short'  
    if row['*Sleeve'] == 'Full-length sleeve' or row['*Sleeve'] == 'Full-length':
        sleeve = 'full'
    specifications = {
        "number_of_pockets": row['Pocket Description'],
        "neck": row['*Style Type'].lower(),
        "chest_size": "Not Available",
        "hemline": "Not Available",
        "net_quantity_(n)":"1",
        "sleeve_length": sleeve,
        "print_or_pattern_type": "Not Available",
        "fabric": row['*Fabric Type'].lower(),
        "character": row['Character'],
        "occasion": row['Mood'].lower(),
        "gender":  'male',
        "length_size": "Not Available",
        "brand":  brand,
        "pattern": row['*Pattern'].lower(),
        "color": [
        color
        ],
        "variation": [
        row['*StandardSize']
        ],
        "country_of_origin":row['*Country of Origin'].capitalize(),
        "length": "Not Available",
        "fit/_shape": row['*Size Group'].capitalize(),
        "gst": "12",
        "hsn_id": str(row['*HSN']),
        "sleeve_styling": "Not Available"
    }
    # print("specifications",specifications)
 
    image=get_image_array(row['*MODEL']+' '+','+row['MODEL2']+' '+','+row['MODEL3'])
    images = [row['*MODEL'],row['MODEL2'],row['MODEL3']]
    for item in image:
        print("Image is -->",item)
        download_image(item)
        
  
    images = my_list 




    print("images -->",images)
    # print(super_category," > ",category," > ",sub_category," > ",sub_sub_category," > ",sub_sub_category_id," >",sku_id," > ",prod_name," > ",manuf_detail," > ",packer_detail," > ",ondc_price," > ",mrp,)
    single_upload(super_category,category,sub_category,sub_sub_category,sub_sub_category_id,sku_id,prod_code,short_desc,long_desc,manuf_detail,packer_detail,cancellable,replaceable,returnable,time_to_ship,ondc_price,mrp,specifications,images)
# print(master_data)
data=pd.read_excel("tshirt.xlsx")
c=0
for index, row in data.iterrows():
    c=c+1
    print("--------------------------------------------------------")
    print("Count is -->",c)
    print("--------------------------------------------------------")
    my_list=[]
    upload_format_data(row)
    
    


