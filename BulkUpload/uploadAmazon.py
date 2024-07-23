import requests
import json
import pandas as pd
import jwt
import secrets 
import re

master_data=json.load(open('catalogs_with_attribute.json'))['data']

token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlzX3Bob25lX3ZlcmlmaWVkIjp0cnVlLCJyb2xlIjoiVVNFUiIsInNpZ25hdHVyZSI6bnVsbCwiZGVzY3JpcHRpb24iOm51bGwsImNyZWF0ZWRfYXQiOiIyMDIzLTEyLTA1VDEwOjQ5OjIwLjk1MFoiLCJnc3RpbiI6IjI3QUFRQ0E5MjU4SDFaMiIsImJhbmsiOnsiaWZzY19jb2RlIjoiIiwiYWNjb3VudF9udW1iZXIiOiIiLCJiZW5lZmljaWFyeV9uYW1lIjoiIiwiYWNjb3VudF90eXBlIjoiIiwiYnJhbmNoX2FkZHJlc3MiOiIifSwiY29tcGFueV9sb2dvIjoiaHR0cHM6Ly9lbmNyeXB0ZWQtdGJuMC5nc3RhdGljLmNvbS9pbWFnZXM_cT10Ym46QU5kOUdjUkFIWFBsdXE2R3RUUlBESUhSdjVrSlB5ODZ1RmpwNXNPN2hnJnVzcXA9Q0FVIiwiaXNfZ3N0aW5fdmVyaWZpZWQiOnRydWUsImNvbXBhbnkiOiJQZXBwbGF5IiwiY29tcGFueV91cmwiOm51bGwsInN0b3JlX3RpbWluZyI6eyJjbG9zZSI6IjE4OjMwIiwib3BlbiI6Ijk6MzAifSwiZW1haWwiOiJzdXBwb3J0QHBlcHBsYXkuaW4iLCJhZ3JlZW1lbnQiOnRydWUsInRhdCI6IlA1RCIsIm1vYmlsZSI6OTE1NjcyNzQ5NCwiZ3BzIjoiNDYuNzYyNzQ2MzM2ODQyMTA2LCAyMy42MDI4NzQ5MzU1OTQ0MDciLCJhdmFpbGFiaWx0eSI6eyJlbmFibGUiOnRydWUsInRpbWVzdGFtcCI6IjIwMjMtMTItMDVUMTA6NDk6MjAuOTUwWiJ9LCJwcm9maWxlX2ltZyI6Imh0dHBzOi8vc3RhdGljLnZlY3RlZXp5LmNvbS9zeXN0ZW0vcmVzb3VyY2VzL3ByZXZpZXdzLzAwMy8yNDAvMzgzL25vbl8yeC9iZXN0LXNlbGxlci1nb2xkZW4tYmFkZ2UtaXNvbGF0ZWQtaWxsdXN0cmF0aW9uLXZlY3Rvci5qcGciLCJuYW1lIjoiTWluYWxpIEFnYXJ3YWwiLCJhZ3JlZW1lbnRfdGltZSI6IjIwMjMtMTItMDVUMTA6NDk6MjAuOTUwWiIsImxvY2F0aW9ucyI6W3siYWRkcmVzcyI6eyJwaW5jb2RlIjo0MDAwNjYsImNvdW50cnkiOiJJbmRpYSIsImNpdHkiOiJib3JpdmFsaSBlYXN0Iiwic3RyZWV0IjoiMTE0IGJsdWVyb3NlIGluZHVzdHJpYWwgZXN0YXRlIiwiZGlzdHJpY3QiOiJib3JpdmFsaSBlYXN0IiwibG9jYWxpdHkiOiIxMTQgYmx1ZXJvc2UgaW5kdXN0cmlhbCBlc3RhdGUgbmVhciBtZXRybyBtYWxsIG9wcCBtYWdhdGhhbmUgZGVwb3QgVyBFIGhpZ2h3YXkgYm9yaXZhbGkgZWFzdCA0MDAwNjYiLCJzdGF0ZSI6Ik1haGFyYXNodHJhIn0sInBpY2t1cF9sb2NhdGlvbiI6Ik1pbmFsaSBBZ2Fyd2FsIzExNCBibHVlcm9zZSBpbmR1c3RyaWFsIGVzdGF0ZSBuZWFyIG1ldHJvIG1hbGwgb3BwIG1hZ2F0aGFuZSBkZXBvdCBXIEUgaGlnaHdheSBib3JpdmFsaSBlYXN0IDQwMDA2NiM0MDAwNjY5MTU2NzI3NDk0IiwidGltZSI6eyJzY2hlZHVsZSI6eyJob2xpZGF5cyI6W119LCJsYWJlbCI6dHJ1ZSwidGltZXN0YW1wIjoiMjAyMy0xMi0wNVQxMToxNDowNi4yMTlaIn0sImdwcyI6IjQ2Ljc2Mjc0NjMzNjg0MjEwNiwgMjMuNjAyODc0OTM1NTk0NDA3In1dLCJ1cGRhdGVkX2F0IjoiMjAyMy0xMi0wNVQxMToxNjowOC40NzNaIiwic3RhdHVzIjoiQUNUSVZFIiwiaWQiOiJaVlF3RzlUSGl5djV5ZzhYdlpTOSIsImF2YXRhciI6ImFzc2V0cy9pbWFnZXMvYXZhdGFycy9tYWxlLTA3LmpwZyJ9LCJpYXQiOjE3MDI4ODQzNDB9.7oJJh7M6vZ25FZyW-mIaHEoN6UyZ7kGXhkuERm6lbyA'

def single_upload(super_category,category,sub_category,sub_sub_category,sub_sub_category_id,sku_id,prod_code,short_desc,long_desc,manuf_detail,packer_detail,cancellable,replaceable,returnable,time_to_ship,ondc_price,mrp,specifications,images):
    data3=pd.read_excel("ondc_category_mapping.xlsx")
    for index, row in data3.iterrows():
        sub_sub_category2 =row['sub_sub_category'] if len(str(row['sub_sub_category']))>0 else "Not Founded"
        if sub_sub_category2 == sub_sub_category:
            # sub_sub_category_id=row['sub_sub_category_id'] if len(str(row['sub_sub_category_id']))>0 else "Not Founded"
            Ondc_category_new=row['Ondc_category_new'] if len(str(row['Ondc_category_new']))>0 else "Not Founded"
            

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
        #  {
        #     "address": {
        #         "pincode": address['pincode'],
        #         "country": address['country'],
        #         "city":address['city'],
        #         "street": address['street'],
        #         "district": address['district'],
        #         "locality": address['locality'],
        #         "state":address['state']
        #     },
        #     "pickup_location": pickup_location,
        #     "time": {
        #         "schedule": {
        #             "holidays": []
        #         },
        #         "label": True,
        #         "timestamp": "2023-12-08T10:33:38.099Z"
        #     },
        #     "gps": "26.855821767945724, 80.99750570239284"
        #  }
        
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
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlzX3Bob25lX3ZlcmlmaWVkIjp0cnVlLCJyb2xlIjoiVVNFUiIsInNpZ25hdHVyZSI6bnVsbCwiZGVzY3JpcHRpb24iOm51bGwsImNyZWF0ZWRfYXQiOiIyMDIzLTEyLTA1VDEwOjQ5OjIwLjk1MFoiLCJnc3RpbiI6IjI3QUFRQ0E5MjU4SDFaMiIsImJhbmsiOnsiaWZzY19jb2RlIjoiIiwiYWNjb3VudF9udW1iZXIiOiIiLCJiZW5lZmljaWFyeV9uYW1lIjoiIiwiYWNjb3VudF90eXBlIjoiIiwiYnJhbmNoX2FkZHJlc3MiOiIifSwiY29tcGFueV9sb2dvIjoiaHR0cHM6Ly9lbmNyeXB0ZWQtdGJuMC5nc3RhdGljLmNvbS9pbWFnZXM_cT10Ym46QU5kOUdjUkFIWFBsdXE2R3RUUlBESUhSdjVrSlB5ODZ1RmpwNXNPN2hnJnVzcXA9Q0FVIiwiaXNfZ3N0aW5fdmVyaWZpZWQiOnRydWUsImNvbXBhbnkiOiJQZXBwbGF5IiwiY29tcGFueV91cmwiOm51bGwsInN0b3JlX3RpbWluZyI6eyJjbG9zZSI6IjE4OjMwIiwib3BlbiI6Ijk6MzAifSwiZW1haWwiOiJzdXBwb3J0QHBlcHBsYXkuaW4iLCJhZ3JlZW1lbnQiOnRydWUsInRhdCI6IlA1RCIsIm1vYmlsZSI6OTE1NjcyNzQ5NCwiZ3BzIjoiNDYuNzYyNzQ2MzM2ODQyMTA2LCAyMy42MDI4NzQ5MzU1OTQ0MDciLCJhdmFpbGFiaWx0eSI6eyJlbmFibGUiOnRydWUsInRpbWVzdGFtcCI6IjIwMjMtMTItMDVUMTA6NDk6MjAuOTUwWiJ9LCJwcm9maWxlX2ltZyI6Imh0dHBzOi8vc3RhdGljLnZlY3RlZXp5LmNvbS9zeXN0ZW0vcmVzb3VyY2VzL3ByZXZpZXdzLzAwMy8yNDAvMzgzL25vbl8yeC9iZXN0LXNlbGxlci1nb2xkZW4tYmFkZ2UtaXNvbGF0ZWQtaWxsdXN0cmF0aW9uLXZlY3Rvci5qcGciLCJuYW1lIjoiTWluYWxpIEFnYXJ3YWwiLCJhZ3JlZW1lbnRfdGltZSI6IjIwMjMtMTItMDVUMTA6NDk6MjAuOTUwWiIsImxvY2F0aW9ucyI6W3siYWRkcmVzcyI6eyJwaW5jb2RlIjo0MDAwNjYsImNvdW50cnkiOiJJbmRpYSIsImNpdHkiOiJib3JpdmFsaSBlYXN0Iiwic3RyZWV0IjoiMTE0IGJsdWVyb3NlIGluZHVzdHJpYWwgZXN0YXRlIiwiZGlzdHJpY3QiOiJib3JpdmFsaSBlYXN0IiwibG9jYWxpdHkiOiIxMTQgYmx1ZXJvc2UgaW5kdXN0cmlhbCBlc3RhdGUgbmVhciBtZXRybyBtYWxsIG9wcCBtYWdhdGhhbmUgZGVwb3QgVyBFIGhpZ2h3YXkgYm9yaXZhbGkgZWFzdCA0MDAwNjYiLCJzdGF0ZSI6Ik1haGFyYXNodHJhIn0sInBpY2t1cF9sb2NhdGlvbiI6Ik1pbmFsaSBBZ2Fyd2FsIzExNCBibHVlcm9zZSBpbmR1c3RyaWFsIGVzdGF0ZSBuZWFyIG1ldHJvIG1hbGwgb3BwIG1hZ2F0aGFuZSBkZXBvdCBXIEUgaGlnaHdheSBib3JpdmFsaSBlYXN0IDQwMDA2NiM0MDAwNjY5MTU2NzI3NDk0IiwidGltZSI6eyJzY2hlZHVsZSI6eyJob2xpZGF5cyI6W119LCJsYWJlbCI6dHJ1ZSwidGltZXN0YW1wIjoiMjAyMy0xMi0wNVQxMToxNDowNi4yMTlaIn0sImdwcyI6IjQ2Ljc2Mjc0NjMzNjg0MjEwNiwgMjMuNjAyODc0OTM1NTk0NDA3In1dLCJ1cGRhdGVkX2F0IjoiMjAyMy0xMi0wNVQxMToxNjowOC40NzNaIiwic3RhdHVzIjoiQUNUSVZFIiwiaWQiOiJaVlF3RzlUSGl5djV5ZzhYdlpTOSIsImF2YXRhciI6ImFzc2V0cy9pbWFnZXMvYXZhdGFycy9tYWxlLTA3LmpwZyJ9LCJpYXQiOjE3MDI4ODQzNDB9.7oJJh7M6vZ25FZyW-mIaHEoN6UyZ7kGXhkuERm6lbyA',
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
def get_formated_specification(specification,color,variants,brand,sub_sub_category_id):
    specification1 =json.loads(specification)
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
    
    for attribute in specification1:
        key = list(attribute.keys())[0]  # Get the attribute name
        value = list(attribute.values())[0]  # Get the attribute value
        clothing_attributes[key.lower()] = value
    clothing_attributes.update({key.lower().replace(" ","_"): value for key, value in variants.items()})
    bb = brand
    brd = bb.replace('\u200e','')
    clothing_attributes["brand"]= brd
    if "customer reviews" in clothing_attributes:
        clothing_attributes["customer reviews"] = 'Not Available'

    if "item model number" in clothing_attributes:
        cng = [clothing_attributes["item model number"]]
        cngg = cng[0].replace('\u200e','')
        clothing_attributes["item model number"] = cngg

    if "shape" in clothing_attributes:
        cng1 = [clothing_attributes["shape"]]
        cngg1 = cng1[0].replace('\u200e','')
        clothing_attributes["shape"] = cngg1 

    if "number of items" in clothing_attributes:
        cng2 = [clothing_attributes["number of items"]]
        cngg2 = cng2[0].replace('\u200e','')
        clothing_attributes["number of items"] = cngg2


    if "manufacturer" in clothing_attributes:
        cng3 = [clothing_attributes["manufacturer"]]
        cngg3 = cng3[0].replace('\u200e','')
        clothing_attributes["manufacturer"] = cngg3

    if "variation" in clothing_attributes:
        cng4= [clothing_attributes["variation"]]
        cngg4 = cng4[0].replace('\u200e','')
        clothing_attributes["variation"] = cngg4


    if "ink colour" in clothing_attributes:
        cng5 = [clothing_attributes["ink colour"]]
        cngg5 = cng5[0].replace('\u200e','')
        clothing_attributes["ink colour"] = cngg5                     

    if "point type" in clothing_attributes:
        cng6 = [clothing_attributes["point type"]]
        cngg6 = cng6[0].replace('\u200e','')
        clothing_attributes["point type"] = cngg6    

    if "item weight" in clothing_attributes:
        cng7 = [clothing_attributes["item weight"]]
        cngg7 = cng7[0].replace('\u200e','')
        clothing_attributes["item weight"] = cngg7    

    if "country of origin" in clothing_attributes:
        cng8 = [clothing_attributes["country of origin"]]
        cngg8 = cng8[0].replace('\u200e','')
        clothing_attributes["country of origin"] = cngg8



    if "model number" in clothing_attributes:
        cng9 = [clothing_attributes["model number"]]
        cngg9 = cng9[0].replace('\u200e','')
        clothing_attributes["model number"] = cngg9      


    if "manufacturer part number" in clothing_attributes:
        cng11 = [clothing_attributes["manufacturer part number"]]
        cngg11= cng11[0].replace('\u200e','')
        clothing_attributes["manufacturer part number"] = cngg11

    if "material" in clothing_attributes:
        cng12 = [clothing_attributes["material"]]
        cngg12 = cng12[0].replace('\u200e','')
        clothing_attributes["material"] = cngg12


    if "product dimensions" in clothing_attributes:
        cng13 = [clothing_attributes["product dimensions"]]
        cngg13 = cng13[0].replace('\u200e','')
        clothing_attributes["product dimensions"] = cngg13     

    if "package dimensions" in clothing_attributes:
        cng14= [clothing_attributes["package dimensions"]]
        cngg14 = cng14[0].replace('\u200e','')
        clothing_attributes["package dimensions"] = cngg14  

    if "closure" in clothing_attributes:
        cng15 = [clothing_attributes["closure"]]
        cngg15 = cng15[0].replace('\u200e','')
        clothing_attributes["closure"] = cngg15

    if "number of puzzle pieces" in clothing_attributes:
        cng16 = [clothing_attributes["number of puzzle pieces"]]
        cngg16 = cng16[0].replace('\u200e','')
        clothing_attributes["number of puzzle pieces"] = cngg16     

    if "asin" in clothing_attributes:
        cng17 = [clothing_attributes["asin"]]
        cngg17 = cng17[0].replace('\u200e','')
        clothing_attributes["asin"] = cngg17

    if "material type(s)" in clothing_attributes:
        cng18 = [clothing_attributes["material type(s)"]]
        cngg18 = cng18[0].replace('\u200e','')
        clothing_attributes["material type(s)"] = cngg18    

    if "item part number" in clothing_attributes:
        cng19 = [clothing_attributes["item part number"]]
        cngg19 = cng19[0].replace('\u200e','')
        clothing_attributes["item part number"] = cngg19                                              

    if "batteries required" in clothing_attributes:
        cng20 = [clothing_attributes["batteries required"]]
        cngg20 = cng20[0].replace('\u200e','')
        clothing_attributes["batteries required"] = cngg20 

    if "assembly required" in clothing_attributes:
        cng21 = [clothing_attributes["assembly required"]]
        cngg21 = cng21[0].replace('\u200e','')
        clothing_attributes["assembly required"] = cngg21   

    if "radio control suitability" in clothing_attributes:
        cng22 = [clothing_attributes["radio control suitability"]]
        cngg22 = cng22[0].replace('\u200e','')
        clothing_attributes["radio control suitability"] = cngg22  

    if "number of pieces" in clothing_attributes:
        cng23 = [clothing_attributes["number of pieces"]]
        cngg23 = cng23[0].replace('\u200e','')
        clothing_attributes["number of pieces"] = cngg23        

    if "product care instructions" in clothing_attributes:
        cng24 = [clothing_attributes["product care instructions"]]
        cngg24 = cng24[0].replace('\u200e','')
        clothing_attributes["product care instructions"] = cngg24                      
     

    if "colour" in clothing_attributes:
        if isinstance(clothing_attributes["colour"], str):
            ran = [clothing_attributes["colour"]]
            ran2 = ran[0].replace('\u200e','')

            clothing_attributes["colour"] = ran2
            clothing_attributes["color"] = [ran2]
    else:
        clothing_attributes["variation"] = ["Free Size"]
        
        clothing_attributes["colour"] = 'Not Available'

    # if "Color" in clothing_attributes:
    #     if isinstance(clothing_attributes["Color"], str):
    #         clothing_attributes["color"] = ran2
            

    # else:
    #     clothing_attributes["color"] = 'Not Available'

    if "size" in clothing_attributes:
        ran5= clothing_attributes.pop("size")
        ran6 = ran5[0].replace('\u200e','')
        clothing_attributes["variation"] = ran6
   
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
    specifications=get_formated_specification(row['specification'],row['color'],row['variants'],brand,sub_sub_category_id)
    images=get_image_array(row['images'])
    # print(super_category," > ",category," > ",sub_category," > ",sub_sub_category," > ",sub_sub_category_id," >",sku_id," > ",prod_name," > ",manuf_detail," > ",packer_detail," > ",ondc_price," > ",mrp,)
    single_upload(super_category,category,sub_category,sub_sub_category,sub_sub_category_id,sku_id,prod_code,short_desc,long_desc,manuf_detail,packer_detail,cancellable,replaceable,returnable,time_to_ship,ondc_price,mrp,specifications,images)
# print(master_data)
data=pd.read_excel("AmazonDump1.xlsx")
for index, row in data.iterrows():
    upload_format_data(row)


