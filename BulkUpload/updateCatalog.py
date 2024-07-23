import requests
import json


# skuid = kurta with pant04
url = "http://127.0.0.1:5001/prod-shopcircuit-seller-portal/asia-south1/api/catalog/fetch_all_catalog/8y0BKUwtl2MzQwqOKu9y"

payload = {}
headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlzX3Bob25lX3ZlcmlmaWVkIjp0cnVlLCJyb2xlIjoiVVNFUiIsInNpZ25hdHVyZSI6bnVsbCwiZGVzY3JpcHRpb24iOm51bGwsImNyZWF0ZWRfYXQiOiIyMDIzLTA5LTI3VDA3OjQ3OjQ3Ljg2OFoiLCJnc3RpbiI6IjA4TVpRUFMyNTc0QTFaUiIsImJhbmsiOnsiaWZzY19jb2RlIjoiIiwiYWNjb3VudF9udW1iZXIiOiIiLCJiZW5lZmljaWFyeV9uYW1lIjoiIiwiYWNjb3VudF90eXBlIjoiIiwiYnJhbmNoX2FkZHJlc3MiOiIifSwiY29tcGFueV9sb2dvIjoiaHR0cHM6Ly9lbmNyeXB0ZWQtdGJuMC5nc3RhdGljLmNvbS9pbWFnZXM_cT10Ym46QU5kOUdjUkFIWFBsdXE2R3RUUlBESUhSdjVrSlB5ODZ1RmpwNXNPN2hnJnVzcXA9Q0FVIiwiaXNfZ3N0aW5fdmVyaWZpZWQiOnRydWUsImNvbXBhbnkiOiJNYWRodXJpbWEgQ29sbGVjdGlvbiIsImNvbXBhbnlfdXJsIjpudWxsLCJzdG9yZV90aW1pbmciOnsiY2xvc2UiOiIxODozMCIsIm9wZW4iOiI5OjMwIn0sImVtYWlsIjoic2FpbmliaGF2YW5pMDI1QGdtYWlsLmNvbSIsImFncmVlbWVudCI6dHJ1ZSwibW9iaWxlIjo5Nzg1NzAyNDQyLCJncHMiOiIxMi45MTE5MDAsIDc3LjY0NDYwMCIsImF2YWlsYWJpbHR5Ijp7ImVuYWJsZSI6dHJ1ZSwidGltZXN0YW1wIjoiMjAyMy0wOS0yN1QwNzo0Nzo0Ny44NjhaIn0sInByb2ZpbGVfaW1nIjoiaHR0cHM6Ly9zdGF0aWMudmVjdGVlenkuY29tL3N5c3RlbS9yZXNvdXJjZXMvcHJldmlld3MvMDAzLzI0MC8zODMvbm9uXzJ4L2Jlc3Qtc2VsbGVyLWdvbGRlbi1iYWRnZS1pc29sYXRlZC1pbGx1c3RyYXRpb24tdmVjdG9yLmpwZyIsIm5hbWUiOiJCaGF2YW5pIFNoYW5rZXIgU2FpbmkiLCJhZ3JlZW1lbnRfdGltZSI6IjIwMjMtMDktMjdUMDc6NDc6NDcuODY4WiIsInN0YXR1cyI6IkFDVElWRSIsInRhdCI6IlA1RCIsIm9yZGVyX21pbl92YWx1ZSI6NTAwLCJsb2NhdGlvbnMiOlt7ImFkZHJlc3MiOnsiY291bnRyeSI6IkluZGlhIiwicGluY29kZSI6MzAyMDE5LCJzdGRfY29kZSI6IjAxNDEiLCJjaXR5IjoiU29kYWxhIiwic3RyZWV0IjoiUmFtIE5hZ2FyLCBOZXcgU2FuZ2FuZXIgcm9hZCBuZWFyYnkgQ2hhd2xhIHJlc3RhdXJhbnQgIiwiZGlzdHJpY3QiOiJKYWlwdXIiLCJsb2NhbGl0eSI6IlBsb3QgTm8uIGMtMTggU3VuZGFyIFZpaGFyIiwic3RhdGUiOiJSYWphc3RoYW4ifSwicGlja3VwX2xvY2F0aW9uIjoiV29yayIsImdwcyI6IjI2Ljc4NjUsIDc1LjU4MDkiLCJ0aW1lIjp7InNjaGVkdWxlIjp7ImhvbGlkYXlzIjpbXX0sInJhbmdlIjp7InN0YXJ0IjoiIiwiZW5kIjoiIn0sImxhYmVsIjoiZW5hYmxlIiwidGltZXN0YW1wIjoiMjAyNC0wMy0wN1QwODozODowMS41MzJaIn0sImxvY2F0aW9uX2lkIjoiYzdhMjdkNDliMjVjNGEwZWI5Y2I2MDA2MTg1OWFjMDMifV0sInVwZGF0ZWRfYXQiOiIyMDI0LTAzLTA3VDA4OjQwOjAwLjU0MVoiLCJpZCI6Ijh5MEJLVXd0bDJNelF3cU9LdTl5IiwiYXZhdGFyIjoiYXNzZXRzL2ltYWdlcy9hdmF0YXJzL21hbGUtMDcuanBnIn0sImlhdCI6MTcxMDQ5ODc4OH0.sNbCoRTCwJz2zc2Tn4_kPeW5M-p5v1RSJs_JVopbU10'
}

response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)



data = json.loads(response.text)  

# print(data["catalogs"][0]["data"]['sku_id'])

y=0

for superItem in data["catalogs"]:  
   
    if 'kurta with pant04' == superItem["data"]['sku_id']:
        print("worked")
        c=0
        z=0
        clothing_attributes = {}
        print("Id is --> ",superItem["id"])
        id = superItem["id"]

        break

        for subItem in superItem["data"]["specifications"]:
            sub2Item = superItem["data"]["specifications"][subItem]

            if  type(sub2Item) is list:
                if c == 0:
                    c=c+1
                    z=c
                # print("sub2Item -->",sub2Item)
                
                my_string = " ".join(str(item) for item in sub2Item)  # Convert items to strings first
                # print(my_string) 
                sub2Item = my_string
            # print(subItem," : ",sub2Item)

            clothing_attributes[subItem] = sub2Item
                        
                    
        if z== 1:
            y=y+1

        del superItem["data"]["specifications"]
        superItem["data"]["specifications"] = clothing_attributes
        # print("superItem -->> ",superItem["data"]["specifications"])  
        # print("superItem -->> ",superItem["data"])  

    
        break  
    
    data = superItem["data"]
    id = superItem["id"]
    url2 = "https://asia-south1-prod-shopcircuit-seller-portal.cloudfunctions.net/api/catalog/create_single"
    payloads = {
    "catalog_id" : id,
    "step1": {
        "super_category": data['super_category'] ,
        "category": data['category'],
        "sub_category": data['sub_category'],
        "sub_sub_category":data['sub_sub_category'],
        "sub_sub_category_id": data['sub_sub_category_id'],
        "ondc_category": data['ondc_category'],
        "ondc_category_id": data['ondc_category_id'],
        "inventory": data['inventory'],
        "images": data['images']
    },
    "step2": {
        "sku_id": data['sku_id'],
        "prod_code":data['prod_code'],
        "short_desc": data['short_desc'],
        "long_desc": data['long_desc'],
        "manuf_detail": data['manuf_detail'],
        "packer_detail": data['packer_detail'],
        "cancellable": data['cancellable'],
        "replaceable": "Yes",
        "returnable": data['returnable'],
        "time_to_ship":data['time_to_ship'],
        "ondc_price": data['ondc_price'],
        "mrp": data['mrp'],
        "address": [],
        "ondc_status": "pending",
        "status": "draft"
    },
    "step3": data['specifications'], 
    "step4": []
    }
    print("payloads",payloads)
    # headers = {
    #     'authority': 'asia-south1-prod-shopcircuit-seller-portal.cloudfunctions.net',
    #     'accept': 'application/json, text/plain, */*',
    #     'accept-language': 'en-US,en;q=0.9',
    #     'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlzX3Bob25lX3ZlcmlmaWVkIjp0cnVlLCJyb2xlIjoiVVNFUiIsInNpZ25hdHVyZSI6bnVsbCwiZGVzY3JpcHRpb24iOm51bGwsImNyZWF0ZWRfYXQiOiIyMDIzLTA5LTI3VDA3OjQ3OjQ3Ljg2OFoiLCJnc3RpbiI6IjA4TVpRUFMyNTc0QTFaUiIsImJhbmsiOnsiaWZzY19jb2RlIjoiIiwiYWNjb3VudF9udW1iZXIiOiIiLCJiZW5lZmljaWFyeV9uYW1lIjoiIiwiYWNjb3VudF90eXBlIjoiIiwiYnJhbmNoX2FkZHJlc3MiOiIifSwiY29tcGFueV9sb2dvIjoiaHR0cHM6Ly9lbmNyeXB0ZWQtdGJuMC5nc3RhdGljLmNvbS9pbWFnZXM_cT10Ym46QU5kOUdjUkFIWFBsdXE2R3RUUlBESUhSdjVrSlB5ODZ1RmpwNXNPN2hnJnVzcXA9Q0FVIiwiaXNfZ3N0aW5fdmVyaWZpZWQiOnRydWUsImNvbXBhbnkiOiJNYWRodXJpbWEgQ29sbGVjdGlvbiIsImNvbXBhbnlfdXJsIjpudWxsLCJzdG9yZV90aW1pbmciOnsiY2xvc2UiOiIxODozMCIsIm9wZW4iOiI5OjMwIn0sImVtYWlsIjoic2FpbmliaGF2YW5pMDI1QGdtYWlsLmNvbSIsImFncmVlbWVudCI6dHJ1ZSwibW9iaWxlIjo5Nzg1NzAyNDQyLCJncHMiOiIxMi45MTE5MDAsIDc3LjY0NDYwMCIsImF2YWlsYWJpbHR5Ijp7ImVuYWJsZSI6dHJ1ZSwidGltZXN0YW1wIjoiMjAyMy0wOS0yN1QwNzo0Nzo0Ny44NjhaIn0sInByb2ZpbGVfaW1nIjoiaHR0cHM6Ly9zdGF0aWMudmVjdGVlenkuY29tL3N5c3RlbS9yZXNvdXJjZXMvcHJldmlld3MvMDAzLzI0MC8zODMvbm9uXzJ4L2Jlc3Qtc2VsbGVyLWdvbGRlbi1iYWRnZS1pc29sYXRlZC1pbGx1c3RyYXRpb24tdmVjdG9yLmpwZyIsIm5hbWUiOiJCaGF2YW5pIFNoYW5rZXIgU2FpbmkiLCJhZ3JlZW1lbnRfdGltZSI6IjIwMjMtMDktMjdUMDc6NDc6NDcuODY4WiIsInN0YXR1cyI6IkFDVElWRSIsInRhdCI6IlA1RCIsIm9yZGVyX21pbl92YWx1ZSI6NTAwLCJsb2NhdGlvbnMiOlt7ImFkZHJlc3MiOnsiY291bnRyeSI6IkluZGlhIiwicGluY29kZSI6MzAyMDE5LCJzdGRfY29kZSI6IjAxNDEiLCJjaXR5IjoiU29kYWxhIiwic3RyZWV0IjoiUmFtIE5hZ2FyLCBOZXcgU2FuZ2FuZXIgcm9hZCBuZWFyYnkgQ2hhd2xhIHJlc3RhdXJhbnQgIiwiZGlzdHJpY3QiOiJKYWlwdXIiLCJsb2NhbGl0eSI6IlBsb3QgTm8uIGMtMTggU3VuZGFyIFZpaGFyIiwic3RhdGUiOiJSYWphc3RoYW4ifSwicGlja3VwX2xvY2F0aW9uIjoiV29yayIsImdwcyI6IjI2Ljc4NjUsIDc1LjU4MDkiLCJ0aW1lIjp7InNjaGVkdWxlIjp7ImhvbGlkYXlzIjpbXX0sInJhbmdlIjp7InN0YXJ0IjoiIiwiZW5kIjoiIn0sImxhYmVsIjoiZW5hYmxlIiwidGltZXN0YW1wIjoiMjAyNC0wMy0wN1QwODozODowMS41MzJaIn0sImxvY2F0aW9uX2lkIjoiYzdhMjdkNDliMjVjNGEwZWI5Y2I2MDA2MTg1OWFjMDMifV0sInVwZGF0ZWRfYXQiOiIyMDI0LTAzLTA3VDA4OjQwOjAwLjU0MVoiLCJpZCI6Ijh5MEJLVXd0bDJNelF3cU9LdTl5IiwiYXZhdGFyIjoiYXNzZXRzL2ltYWdlcy9hdmF0YXJzL21hbGUtMDcuanBnIn0sImlhdCI6MTcxMDQ5ODc4OH0.sNbCoRTCwJz2zc2Tn4_kPeW5M-p5v1RSJs_JVopbU10',
    #     'content-type': 'application/json',
    #     'origin': 'https://dashboard.shopcircuit.ai',
    #     'referer': 'https://dashboard.shopcircuit.ai/',
    #     'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    #     'sec-ch-ua-mobile': '?0',
    #     'sec-ch-ua-platform': '"Linux"',
    #     'sec-fetch-dest': 'empty',
    #     'sec-fetch-mode': 'cors',
    #     'sec-fetch-site': 'cross-site',
    #     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    # }

    # response2 = requests.request("POST", url2, headers=headers, data=payloads)
    # print(response2.text)
    # response2 = requests.request("POST", url2, headers=headers, data=payloads)
    # print(response2.text)
print("Count -->",y)   


