import json

payload = {
  "step1": {
    "super_category": "Women Fashion",
    "category": "Ethnic Wear",
    "sub_category": "Suits & Dress Material",
    "sub_sub_category": "Unstiched Suit",
    "sub_sub_category_id": "ZW8xNSHF5ijeMI07PcPM",
    "ondc_category": "Dress Materials",
    "ondc_category_id": "rtgu5qxh5rjl",
    "inventory": [],
    "images": [
      "https://storage.googleapis.com/shop-circuit-catalog-images/Bhavani Shanker Saini-8y0BKUwtl2MzQwqOKu9y/Screenshot 2023-10-04 164403.png"
    ],
    "featuredImage": "h"
  },
  "step2": {
    "sku_id": "Testing1",
    "prod_code": "Testing1",
    "short_desc": "Testing1",
    "long_desc": "Testing1",
    "manuf_detail": "Testing1",
    "packer_detail": "Testing1",
    "cancellable": "Yes",
    "cod": "Yes",
    "replaceable": "Yes",
    "returnable": "Yes",
    "time_to_ship": "P2D",
    "ondc_price": 666,
    "mrp": 566,
    "order_min_value": 500,
    "location_id": "c7a27d49b25c4a0eb9cb60061859ac03",
    "ondc_status": "pending",
    "status": "QC_IN_PROGRESS"
  },
  "step3": {
    "transparency": "Not Available",
    "butttom_color": "Aqua Blue",
    "pattern": "alpha",
    "Dupatta Length": 1.5,
    "Brand": "Not Available",
    "top_fabric": "Art Silk",
    "color": [
      "1B1404",
      "7CB0A1",
      "C9FFE5"
    ],
    "type": "Dhoti Suit",
    "GST": 12,
    "gender": "female",
    "Bottom Length": "0-2.00",
    "print_and_pattern_type": "Ajrak Print",
    "net_quantity": "2 Top",
    "country": "Albania",
    "neck": "boat",
    "Ocassion": "Party",
    "fabric": "acrylic",
    "dupatta_fabric": "Art Silk",
    "bottom_fabric": "Acrylic",
    "HSN_ID": "520811",
    "Top Length": "2 Meters"
  },
  "step4": {
    "variatn_overwrite": []
  }
}

with open("sample.json", "w") as write_file:
    json.dump(payload, write_file)
    print('Done')