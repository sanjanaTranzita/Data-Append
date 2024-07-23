import math
import requests
import json
import pandas as pd
import re
master_data=json.load(open('catalogs_with_attribute.json'))['data']


def single_upload(super_category,category,sub_category,sub_sub_category,sub_sub_category_id,sku_id,prod_name,short_desc,long_desc,manuf_detail,packer_detail,cancellable,replaceable,returnable,time_to_ship,ondc_price,mrp,specifications,images):

    url = "https://us-central1-vaanij.cloudfunctions.net/api/catalog/create_single"

    payload = json.dumps({
    "step1": {
        "super_category": super_category,
        "category": category,
        "sub_category": sub_category,
        "sub_sub_category": sub_sub_category,
        "sub_sub_category_id": sub_sub_category_id,
        "images": images
    },
    "step2": {
        "sku_id": sku_id,
        "prod_code": prod_name,
        "short_desc": short_desc,
        "long_desc": long_desc,
        "manuf_detail": manuf_detail,
        "packer_detail": packer_detail,
        "cancellable": cancellable,
        "replaceable": replaceable,
        "returnable": returnable,
        "time_to_ship": time_to_ship,
        "ondc_price": ondc_price,
        "mrp": mrp
    },
    "step3": specifications,
    "step4":[]
   
    })
    testingToken='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7InJvbGUiOiJVU0VSIiwiYWdyZWVtZW50cyI6dHJ1ZSwiZ3BzIjoiMTIuOTExOTAwLCA3Ny42NDQ2MDAiLCJjb21wYW55IjoidHJhbnppdGEiLCJuYW1lIjoiUGFua2FqIFNpbmdoIiwibW9iaWxlIjoiOTUzMjY5NjQ2MSIsImdzdGluIjoiWFhYWFhYWFhYWFhYWCIsImFkZHJlc3MiOiJMdWNraG5vdyxVUCIsInRhdCI6IlBUMkgiLCJzdGF0dXMiOiJBQ1RJVkUiLCJlbWFpbCI6InBhbmthakB0cmFueml0YS5jb20iLCJpZCI6InVLejFqZHlsNHVjMmNUN1NXRDF1IiwiYXZhdGFyIjoiYXNzZXRzL2ltYWdlcy9hdmF0YXJzL21hbGUtMDcuanBnIn0sImlhdCI6MTY5Mzk4Njk4Nn0.KNxwyy-2nzhFId--AaXmvqmcWggFmvCw3Nsxgx0JzA4'
    token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImFkZHJlc3MiOiJMdWNrbm93Iiwicm9sZSI6IlVTRVIiLCJ0YXQiOiJQVDVEIiwibW9iaWxlIjoiOTUzMjY5NjQ2MSIsImFncmVlbWVudHMiOnRydWUsImNyZWF0ZWRfYXQiOnsiX3NlY29uZHMiOjE2OTM5Nzk2MDEsIl9uYW5vc2Vjb25kcyI6OTU2MDAwMDAwfSwiZ3BzIjoiMTIuOTExOTAwLCA3Ny42NDQ2MDAiLCJnc3RpbiI6IjI5Q0lCUFM0NzE1WFlaUiIsInVwZGF0ZWRfYXQiOnsiX3NlY29uZHMiOjE2OTM5Nzk2MDEsIl9uYW5vc2Vjb25kcyI6OTU2MDAwMDAwfSwibmFtZSI6IkgmTSIsImNvbXBhbnkiOiJIJk0iLCJlbWFpbCI6IkhNQGdtYWlsLmNvbSIsInN0YXR1cyI6IkFDVElWRSIsImlkIjoiS3E5aVNMblY0RUttNGpDNDVzT3EiLCJhdmF0YXIiOiJhc3NldHMvaW1hZ2VzL2F2YXRhcnMvbWFsZS0wNy5qcGcifSwiaWF0IjoxNjkzOTg2NTI3fQ.sQ0cq_MwcVB9qKwUJf0ZlXlwyBET-Klli7eOjPAQuCk'
    headers = {
    'authority': 'us-central1-vaanij.cloudfunctions.net',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': f'Bearer {testingToken}',
    'content-type': 'application/json',
    'origin': 'https://dashboard.vidyant.com',
    'referer': 'https://dashboard.vidyant.com/',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
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
def get_formated_specification(specfication,brand,sub_sub_category_id):
    specfication=json.loads(specfication)
   # varients=json.loads(varients)
   # keys_to_remove = [key for key, value in varients.items() if value == "" or (isinstance(value, list) and not value)]
   # for key in keys_to_remove:
      #  varients.pop(key)
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
   # clothing_attributes.update({key.lower().replace(" ","_"): value for key, value in varients.items()})
    clothing_attributes["brand"]=brand
    if "size" in clothing_attributes:
        clothing_attributes["variation"] = clothing_attributes.pop("size")
    else:
        clothing_attributes["variation"] = ["Free Size"]
    if "color" in clothing_attributes:
        if isinstance(clothing_attributes["color"], str):
            clothing_attributes["color"] = [clothing_attributes["color"]]
    # elif "Color" in clothing_attributes:
    #     if isinstance(clothing_attributes["Color"], str):
    #         clothing_attributes["color"] = [clothing_attributes["Color"]]
    else:
        clothing_attributes["variation"] = ["Free Size"]
    return clothing_attributes
def get_image_array(images):
    if images[-1]!="]" and images[0]!= "[":
        return re.findall(r'https://.*?\.jpg', images)
    else:
        # print("line number 112 images",json.loads(images) ,type(json.loads(images)))
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
def upload_format_data(row):
    super_category=row['super_category'] if len(str(row['super_category']))>0 else "Not Founded" 
    category=row['category'] if len(str(row['category']))>0 else "Not Founded" 
    sub_category=row['sub_category'] if len(str(row['sub_category']))>0 else "Not Founded" 
    sub_sub_category=row['sub_sub_category'] if len(str(row['sub_sub_category']))>0 else "Not Founded" 
    sub_sub_category_id=get_sub_sub_category_id(row['super_category'],str(row['category']),str(row['sub_category']),str(row['sub_sub_category'])) if len(get_sub_sub_category_id(str(row['super_category']),str(row['category']),str(row['sub_category']),str(row['sub_sub_category'])))>4 else "Not Founded"
    sku_id=str(row['prod_code']) if len(str(row['prod_code']))>4 else row['product_name'][:3]+"1234" 
    prod_name=row['product_name'] if len(str(row['product_name']))>4 else "Not Founded" 
    short_desc=row['short_desc'] if len(str(row['short_desc']))>4 else "Not Avilable" 
    long_desc=row['long_desc']if len(str(row['long_desc']))>4 else "Not Avilable"
    manuf_detail=row['manuf_detail']if len(str(row['manuf_detail']))>4 else "Not Avilable"
    packer_detail=row['packer_detail'] if len(str(row['packer_detail']))>4 else "Not Avilable"
    cancellable="Yes"
    replaceable="Yes"
    returnable="Yes"
    time_to_ship="2 Days"
    brand=row['brand'] if len(str(row['brand']))>0 else "Not Avilable"
    ondc_price=get_number(row['price']) if get_number(row['price'])>0 else 0
    mrp=get_number(row['mrp']) if get_number(row['mrp'])>0 else 0
    specifications=get_formated_specification(row['specification'],row['variants'],brand,sub_sub_category_id)
    images=get_image_array(row['images'])
    # print(super_category," > ",category," > ",sub_category," > ",sub_sub_category," > ",sub_sub_category_id," >",sku_id," > ",prod_name," > ",manuf_detail," > ",packer_detail," > ",ondc_price," > ",mrp,)
    single_upload(super_category,category,sub_category,sub_sub_category,sub_sub_category_id,sku_id,prod_name,short_desc,long_desc,manuf_detail,packer_detail,cancellable,replaceable,returnable,time_to_ship,ondc_price,mrp,specifications,images)
# print(master_data)
data=pd.read_excel("FlipkartDumpTesting.xlsx")
for index, row in data.iterrows():
    upload_format_data(row)


