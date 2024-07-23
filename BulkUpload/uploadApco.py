import requests
import json
import pandas as pd
import jwt
import secrets 
import re

master_data=json.load(open('catalogs_with_attribute.json'))['data']

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlzX3Bob25lX3ZlcmlmaWVkIjp0cnVlLCJyb2xlIjoiVVNFUiIsInNpZ25hdHVyZSI6bnVsbCwiZGVzY3JpcHRpb24iOm51bGwsImNyZWF0ZWRfYXQiOiIyMDIzLTEyLTI5VDEwOjIxOjQ5LjAzOFoiLCJnc3RpbiI6IjM3QUFCQVQzNzgwQTJaTiIsImJhbmsiOnsiaWZzY19jb2RlIjoiQkFSQjBWSlZJS1IiLCJhY2NvdW50X251bWJlciI6NzU1MzAxMDAwMTAzMTMsImJlbmVmaWNpYXJ5X25hbWUiOiJUSEUgQVBTSFdDUyBMVEQgQVBDTyIsImFjY291bnRfdHlwZSI6IlNhdmluZ3MiLCJicmFuY2hfYWRkcmVzcyI6IkdPVkVSTkVSUEVUIEJSQU5DSCwgVklKQVlBV0FEQSJ9LCJjb21wYW55X2xvZ28iOiJodHRwczovL2VuY3J5cHRlZC10Ym4wLmdzdGF0aWMuY29tL2ltYWdlcz9xPXRibjpBTmQ5R2NSQUhYUGx1cTZHdFRSUERJSFJ2NWtKUHk4NnVGanA1c083aGcmdXNxcD1DQVUiLCJpc19nc3Rpbl92ZXJpZmllZCI6dHJ1ZSwiY29tcGFueSI6IlRIRSBBTkRIUkEgUFJBREVTSCBTVEFURSBIQU5ETE9PTSBXRUFWRVJTICBDT09QRVJBVElWRSBTT0NJRVRZIExJTUlURUQiLCJjb21wYW55X3VybCI6bnVsbCwic3RvcmVfdGltaW5nIjp7ImNsb3NlIjoiMTg6MzAiLCJvcGVuIjoiOTozMCJ9LCJlbWFpbCI6ImFwY29mYWJyaWNzYXBAZ21haWwuY29tIiwiYWdyZWVtZW50Ijp0cnVlLCJ0YXQiOiJQNUQiLCJtb2JpbGUiOjkwMDA1NTE1NzgsImdwcyI6IjE2LjI0NjM3NDQsIDgwLjY0ODYwMTYiLCJhdmFpbGFiaWx0eSI6eyJlbmFibGUiOnRydWUsInRpbWVzdGFtcCI6IjIwMjMtMTItMjlUMTA6MjE6NDkuMDM4WiJ9LCJwcm9maWxlX2ltZyI6Imh0dHBzOi8vc3RhdGljLnZlY3RlZXp5LmNvbS9zeXN0ZW0vcmVzb3VyY2VzL3ByZXZpZXdzLzAwMy8yNDAvMzgzL25vbl8yeC9iZXN0LXNlbGxlci1nb2xkZW4tYmFkZ2UtaXNvbGF0ZWQtaWxsdXN0cmF0aW9uLXZlY3Rvci5qcGciLCJuYW1lIjoiVGhlIEFuZGhyYSBQcmFkZXNoIFN0YXRlIEhhbmRsb29tIFdlYXZlcnMgQ28tb3BlcmF0aXZlIFNvY2lldHkgTHRkLiwgIFtBUENPXSIsImFncmVlbWVudF90aW1lIjoiMjAyMy0xMi0yOVQxMDoyMTo0OS4wMzhaIiwibG9jYXRpb25zIjpbeyJhZGRyZXNzIjp7InBpbmNvZGUiOjUyMDAwMiwiY291bnRyeSI6IkluZGlhIiwiY2l0eSI6IlZpamF5YXdhZGEiLCJzdHJlZXQiOiIgVmVua2F0ZXN3YXJhIFJhbyBSb2FkLCBOZWFyIFJhaG1hbiBQYXJrIiwiZGlzdHJpY3QiOiJOVFIgRGlzdHJpY3QiLCJsb2NhbGl0eSI6IkNlbnRyYWwgT2ZmaWNlLCBBUENPIEJoYXZhbiwgIDI5LTExLTkvMSIsInN0YXRlIjoiQW5kaHJhIFByYWRlc2gifSwicGlja3VwX2xvY2F0aW9uIjoiVGhlIEFuZGhyYSBQcmFkZXNoIFN0YXRlIEhhbmRsb29tIFdlYXZlcnMgQ28tb3BlcmF0aXZlIFNvY2lldHkgTHRkLiwgIFtBUENPXSNDZW50cmFsIE9mZmljZSwgQVBDTyBCaGF2YW4sICAyOS0xMS05LzEjNTIwMDAyOTAwMDU1MTU3OCIsInRpbWUiOnsic2NoZWR1bGUiOnsiaG9saWRheXMiOltdfSwibGFiZWwiOiJlbmFibGUiLCJ0aW1lc3RhbXAiOiIyMDIzLTEyLTI5VDEwOjI2OjM4LjgwMVoifSwiZ3BzIjoiMTYuMjQ2Mzc0NCwgODAuNjQ4NjAxNiIsImxvY2F0aW9uX2lkIjoiM2EyM2ExODJiMzBlNGNmMWJmMDI2MzdhZDQ1MTk3N2UifV0sInVwZGF0ZWRfYXQiOiIyMDI0LTAxLTEwVDA2OjE0OjU1LjMzOFoiLCJzdGF0dXMiOiJBQ1RJVkUiLCJpZCI6InlCbFliaVJ0NUw2OGVSMFVEd2JZIiwiYXZhdGFyIjoiYXNzZXRzL2ltYWdlcy9hdmF0YXJzL21hbGUtMDcuanBnIn0sImlhdCI6MTcwNTkxODU1Mn0.f8-dIIkWv4Gef9R2TyxYcjUiTlEns4pJJACAW47gjq0'


def single_upload(super_category,category,sub_category,sub_sub_category,sub_sub_category_id,sku_id,prod_code,short_desc,long_desc,manuf_detail,packer_detail,cancellable,replaceable,returnable,time_to_ship,ondc_price,mrp,specifications,images):
    data3=pd.read_excel("ondc_category_mapping.xlsx")
    for index, row in data3.iterrows():
        sub_sub_categoryId2 =row['sub_sub_category_id'] if len(str(row['sub_sub_category_id']))>0 else "Not Founded"
        if sub_sub_categoryId2 == sub_sub_category_id:
            # sub_sub_category_id=row['sub_sub_category_id'] if len(str(row['sub_sub_category_id']))>0 else "Not Founded"
            Ondc_category_new=row['Ondc_category_new'] if len(str(row['Ondc_category_new']))>0 else "Not Founded"
            print("Ondc_category_new",Ondc_category_new)

    data=jwt.decode(token, options={"verify_signature": False})
    address=data['user']['locations'][0]['address']
    pickup_location  = data['user']['locations'][0]['pickup_location']
    token1 = secrets.token_hex(6)             

    url = "https://asia-south1-prod-shopcircuit-seller-portal.cloudfunctions.net/api/catalog/create_single"
    # url = "http://127.0.0.1:5001/prod-shopcircuit-seller-portal/asia-south1/api/catalog/create_single"

    payload = json.dumps({
    "step1": {
        "super_category": super_category,
        "category": category,
        "sub_category": sub_category,
        "sub_sub_category": sub_sub_category,
        "sub_sub_category_id": sub_sub_category_id,
        "ondc_category": Ondc_category_new,
        "ondc_category_id": token1,
        "inventory": [],
        "images": images
    },
    "step2": {
        "sku_id": sku_id,
        "prod_code": prod_code,
        "short_desc": short_desc,
        "long_desc": long_desc,
        "manuf_detail": manuf_detail,
        "packer_detail": packer_detail,
        "cancellable": cancellable,
        "replaceable": replaceable,
        "returnable": returnable,
        "time_to_ship": time_to_ship,
        "ondc_price": ondc_price,
        "mrp": mrp,
        "location_id":'3a23a182b30e4cf1bf02637ad451977e',
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
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlzX3Bob25lX3ZlcmlmaWVkIjp0cnVlLCJyb2xlIjoiVVNFUiIsInNpZ25hdHVyZSI6bnVsbCwiZGVzY3JpcHRpb24iOm51bGwsImNyZWF0ZWRfYXQiOiIyMDIzLTEyLTI5VDEwOjIxOjQ5LjAzOFoiLCJnc3RpbiI6IjM3QUFCQVQzNzgwQTJaTiIsImJhbmsiOnsiaWZzY19jb2RlIjoiQkFSQjBWSlZJS1IiLCJhY2NvdW50X251bWJlciI6NzU1MzAxMDAwMTAzMTMsImJlbmVmaWNpYXJ5X25hbWUiOiJUSEUgQVBTSFdDUyBMVEQgQVBDTyIsImFjY291bnRfdHlwZSI6IlNhdmluZ3MiLCJicmFuY2hfYWRkcmVzcyI6IkdPVkVSTkVSUEVUIEJSQU5DSCwgVklKQVlBV0FEQSJ9LCJjb21wYW55X2xvZ28iOiJodHRwczovL2VuY3J5cHRlZC10Ym4wLmdzdGF0aWMuY29tL2ltYWdlcz9xPXRibjpBTmQ5R2NSQUhYUGx1cTZHdFRSUERJSFJ2NWtKUHk4NnVGanA1c083aGcmdXNxcD1DQVUiLCJpc19nc3Rpbl92ZXJpZmllZCI6dHJ1ZSwiY29tcGFueSI6IlRIRSBBTkRIUkEgUFJBREVTSCBTVEFURSBIQU5ETE9PTSBXRUFWRVJTICBDT09QRVJBVElWRSBTT0NJRVRZIExJTUlURUQiLCJjb21wYW55X3VybCI6bnVsbCwic3RvcmVfdGltaW5nIjp7ImNsb3NlIjoiMTg6MzAiLCJvcGVuIjoiOTozMCJ9LCJlbWFpbCI6ImFwY29mYWJyaWNzYXBAZ21haWwuY29tIiwiYWdyZWVtZW50Ijp0cnVlLCJ0YXQiOiJQNUQiLCJtb2JpbGUiOjkwMDA1NTE1NzgsImdwcyI6IjE2LjI0NjM3NDQsIDgwLjY0ODYwMTYiLCJhdmFpbGFiaWx0eSI6eyJlbmFibGUiOnRydWUsInRpbWVzdGFtcCI6IjIwMjMtMTItMjlUMTA6MjE6NDkuMDM4WiJ9LCJwcm9maWxlX2ltZyI6Imh0dHBzOi8vc3RhdGljLnZlY3RlZXp5LmNvbS9zeXN0ZW0vcmVzb3VyY2VzL3ByZXZpZXdzLzAwMy8yNDAvMzgzL25vbl8yeC9iZXN0LXNlbGxlci1nb2xkZW4tYmFkZ2UtaXNvbGF0ZWQtaWxsdXN0cmF0aW9uLXZlY3Rvci5qcGciLCJuYW1lIjoiVGhlIEFuZGhyYSBQcmFkZXNoIFN0YXRlIEhhbmRsb29tIFdlYXZlcnMgQ28tb3BlcmF0aXZlIFNvY2lldHkgTHRkLiwgIFtBUENPXSIsImFncmVlbWVudF90aW1lIjoiMjAyMy0xMi0yOVQxMDoyMTo0OS4wMzhaIiwibG9jYXRpb25zIjpbeyJhZGRyZXNzIjp7InBpbmNvZGUiOjUyMDAwMiwiY291bnRyeSI6IkluZGlhIiwiY2l0eSI6IlZpamF5YXdhZGEiLCJzdHJlZXQiOiIgVmVua2F0ZXN3YXJhIFJhbyBSb2FkLCBOZWFyIFJhaG1hbiBQYXJrIiwiZGlzdHJpY3QiOiJOVFIgRGlzdHJpY3QiLCJsb2NhbGl0eSI6IkNlbnRyYWwgT2ZmaWNlLCBBUENPIEJoYXZhbiwgIDI5LTExLTkvMSIsInN0YXRlIjoiQW5kaHJhIFByYWRlc2gifSwicGlja3VwX2xvY2F0aW9uIjoiVGhlIEFuZGhyYSBQcmFkZXNoIFN0YXRlIEhhbmRsb29tIFdlYXZlcnMgQ28tb3BlcmF0aXZlIFNvY2lldHkgTHRkLiwgIFtBUENPXSNDZW50cmFsIE9mZmljZSwgQVBDTyBCaGF2YW4sICAyOS0xMS05LzEjNTIwMDAyOTAwMDU1MTU3OCIsInRpbWUiOnsic2NoZWR1bGUiOnsiaG9saWRheXMiOltdfSwibGFiZWwiOiJlbmFibGUiLCJ0aW1lc3RhbXAiOiIyMDIzLTEyLTI5VDEwOjI2OjM4LjgwMVoifSwiZ3BzIjoiMTYuMjQ2Mzc0NCwgODAuNjQ4NjAxNiIsImxvY2F0aW9uX2lkIjoiM2EyM2ExODJiMzBlNGNmMWJmMDI2MzdhZDQ1MTk3N2UifV0sInVwZGF0ZWRfYXQiOiIyMDI0LTAxLTEwVDA2OjE0OjU1LjMzOFoiLCJzdGF0dXMiOiJBQ1RJVkUiLCJpZCI6InlCbFliaVJ0NUw2OGVSMFVEd2JZIiwiYXZhdGFyIjoiYXNzZXRzL2ltYWdlcy9hdmF0YXJzL21hbGUtMDcuanBnIn0sImlhdCI6MTcwNTkxODU1Mn0.f8-dIIkWv4Gef9R2TyxYcjUiTlEns4pJJACAW47gjq0',
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
            
def get_formated_specification(specfication,brand,sub_sub_category_id,color):
    specfication=json.loads(specfication)


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

    clothing_attributes["brand"]=brand
    
    if "size" in clothing_attributes:
        clothing_attributes["variation"] = ["Free Size"]
    else:
        clothing_attributes["variation"] = ["Free Size"]
    if "color" in clothing_attributes:
        if isinstance(clothing_attributes["color"], str):
            clothing_attributes["color"] = [color]
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
    if numData != "" and not isinstance(numData, float):
        numData = str(numData)
        numData = numData.replace(',', '')  # Remove commas
        result = [int(match) for match in re.findall(r'\b\d+\b', numData)]
        if len(result) > 0:
            return result[0]
        else:
            return 0
    else:
        return 0




def upload_format_data(row):
    super_category=row['super_category'] if len(str(row['super_category']))>0 else "Not Founded" 
    print("super_category",super_category)
    category=row['category'] if len(str(row['category']))>0 else "Not Founded" 
    print("category",category)
    sub_category=row['sub_category'] if len(str(row['sub_category']))>0 else "Not Founded" 
    print("sub_category",sub_category)
    sub_sub_category=row['sub_sub_category'] if len(str(row['sub_sub_category']))>0 else "Not Founded" 
    print("sub_sub_category",sub_sub_category)
    sub_sub_category_id=get_sub_sub_category_id(row['super_category'],str(row['category']),str(row['sub_category']),str(row['sub_sub_category'])) if len(get_sub_sub_category_id(str(row['super_category']),str(row['category']),str(row['sub_category']),str(row['sub_sub_category'])))>4 else "Not Founded"
    print("sub_sub_category_id",sub_sub_category_id)
    sku_id=str(row['skuId']) if len(str(row['skuId']))>4 else row['product_name'][:3]+"1234" 
    print("sku_id",sku_id)
    prod_code=row['product_name'] if len(str(row['product_name']))>4 else "Not Founded" 
    print("prod_code",prod_code)
    short_desc=row['short_desc'] if len(str(row['short_desc']))>4 else "Not Avilable" 
    print("short_desc",short_desc)
    long_desc=row['long_desc']if len(str(row['long_desc']))>4 else "Not Avilable"
    print("long_desc",long_desc)
    manuf_detail=row['manuf_detail']if len(str(row['manuf_detail']))>4 else "Not Avilable"
    print("manuf_detail",manuf_detail)
    packer_detail=row['packer_detail'] if len(str(row['packer_detail']))>4 else "Not Avilable"
    print("packer_detail",packer_detail)
    cancellable="Yes"
    replaceable="Yes"
    returnable="Yes"
    time_to_ship="P2D"
    brand=row['brand'] if len(str(row['brand']))>0 else "Not Avilable"
    print("brand",brand)
    ondc_price=get_number(row['price']) if get_number(row['price'])>0 else 0
    print("ondc_price",ondc_price)
    mrp=get_number(row['mrp']) if get_number(row['mrp'])>0 else 0
    print("mrp",mrp)
    color = row['color'] if len(str(row['color']))>4 else "Not Avilable"
    specifications=get_formated_specification(row['specification'],brand,sub_sub_category_id,color)
    print("specifications",specifications)
    images=get_image_array(row['images'])
    print("images",images)
    

    # print(super_category," > ",category," > ",sub_category," > ",sub_sub_category," > ",sub_sub_category_id," >",sku_id," > ",prod_name," > ",manuf_detail," > ",packer_detail," > ",ondc_price," > ",mrp,)
    single_upload(super_category,category,sub_category,sub_sub_category,sub_sub_category_id,sku_id,prod_code,short_desc,long_desc,manuf_detail,packer_detail,cancellable,replaceable,returnable,time_to_ship,ondc_price,mrp,specifications,images)
# print(master_data)
data=pd.read_excel("apco/TowelsApco.xlsx")
for index, row in data.iterrows():
    upload_format_data(row)
    
    

    

