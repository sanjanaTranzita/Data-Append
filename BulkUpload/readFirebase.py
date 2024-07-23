import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter,Or
cred = credentials.Certificate("/media/ranjeet/Files/Tranzita/seller_dashboard/backend/functions/src/environments/pre-prod-shopcircuit-seller-firebase-adminsdk-8ywnn-009b24736d.json")
firebase_admin.initialize_app(cred)
import json
import os
from io import BytesIO
from PIL import Image
from requests import get
import requests

token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlzX3Bob25lX3ZlcmlmaWVkIjp0cnVlLCJyb2xlIjoiVVNFUiIsInNpZ25hdHVyZSI6bnVsbCwiZGVzY3JpcHRpb24iOm51bGwsImNyZWF0ZWRfYXQiOiIyMDIzLTA5LTIyVDA2OjAyOjE0LjM0OVoiLCJnc3RpbiI6IkFTREZHSEpLTFExMjM0NSIsImJhbmsiOnsiaWZzY19jb2RlIjoiQ1NFMjMxMyIsImFjY291bnRfbnVtYmVyIjoyMTQ1Njc4OTEyMywiYmVuZWZpY2lhcnlfbmFtZSI6IkthbHBhbmEiLCJhY2NvdW50X3R5cGUiOiJDdXJyZW50IiwiYnJhbmNoX2FkZHJlc3MiOiJQYWRyaSBCYXphYXIifSwiY29tcGFueV9sb2dvIjoiaHR0cHM6Ly9lbmNyeXB0ZWQtdGJuMC5nc3RhdGljLmNvbS9pbWFnZXM_cT10Ym46QU5kOUdjUkFIWFBsdXE2R3RUUlBESUhSdjVrSlB5ODZ1RmpwNXNPN2hnJnVzcXA9Q0FVIiwiaXNfZ3N0aW5fdmVyaWZpZWQiOnRydWUsImNvbXBhbnlfdXJsIjpudWxsLCJjb21wYW55IjoiSCZNIiwic3RvcmVfdGltaW5nIjp7ImNsb3NlIjoiMTg6MzAiLCJvcGVuIjoiOTozMCJ9LCJlbWFpbCI6ImhtQGdtYWlsLmNvbSIsImFncmVlbWVudCI6dHJ1ZSwicHJvZmlsZV9pbWciOiJodHRwczovL3N0b3JhZ2UuZ29vZ2xlYXBpcy5jb20vdmFhbmlqLXByb2ZpbGUtcGljdHVyZS9IJk0tNGQ5U1doZ1JpaXlkWk05Z3RqcjAvaG0tbG9nby1icmFuZC1zeW1ib2wtcmVkLWRlc2lnbi1oZW5uZXMtYW5kLW1hdXJpdHotY2xvdGhlcy1mYXNoaW9uLWlsbHVzdHJhdGlvbi13aXRoLWJsYWNrLWJhY2tncm91bmQtZnJlZS12ZWN0b3IuanBnIiwibmFtZSI6IkgmTSIsImFncmVlbWVudF90aW1lIjoiMjAyMy0wOS0yMlQwNjowMjoxNC4zNDlaIiwic3RhdHVzIjoiQUNUSVZFIiwidGF0IjoiUDVEIiwibW9iaWxlIjo5MzM2MzU2MTMyLCJncHMiOiIyNi43NTAxNTE0ODg3NjQwNTQsIDgzLjM3NTM5ODk3MjE4OTg0IiwibG9jYXRpb25zIjpbeyJhZGRyZXNzIjp7ImNvdW50cnkiOiJJbmRpYSIsInBpbmNvZGUiOjIyNjAyOCwiY2l0eSI6IkFtcmFpZ2FvbiIsInN0cmVldCI6IlNlbXJhIiwiZGlzdHJpY3QiOiJMdWNrbm93IiwibG9jYWxpdHkiOiJBbmFuZCBMb2sgQ29sb255Iiwic3RhdGUiOiJVdHRhciBQcmFkZXNoIn0sInBpY2t1cF9sb2NhdGlvbiI6IkhvbWUiLCJncHMiOiIyNi44ODQ0Mzc4LCA4MS4wNTkwNjIxMzMzMzMzNCIsInRpbWUiOnsic2NoZWR1bGUiOnsiaG9saWRheXMiOltdfSwicmFuZ2UiOnsic3RhcnQiOiIiLCJlbmQiOiIifSwibGFiZWwiOiJlbmFibGUiLCJ0aW1lc3RhbXAiOiIyMDI0LTAxLTIwVDExOjExOjUyLjU3MloifSwibG9jYXRpb25faWQiOiI3Njg3ZmU1Yi0wMzJhLTRjMGMtOTZlMS03ZTBlNjAxNGIzNTUifV0sIm9yZGVyX21pbl92YWx1ZSI6NTAwLCJhdmFpbGFiaWx0eSI6eyJlbmFibGUiOmZhbHNlLCJ0aW1lc3RhbXAiOiIyMDI0LTAyLTAyVDEwOjQwOjM3Ljc4MVoifSwidXBkYXRlZF9hdCI6IjIwMjQtMDItMDJUMTA6NDA6MzguMTU0WiIsImlkIjoiNGQ5U1doZ1JpaXlkWk05Z3RqcjAiLCJhdmF0YXIiOiJhc3NldHMvaW1hZ2VzL2F2YXRhcnMvbWFsZS0wNy5qcGcifSwiaWF0IjoxNzExNDUwNTU4fQ.626MK_zXgiDa6bFTtgyvCTC8cQHLzuPxQlmwrdY9Dog"

db = firestore.client()

# write the data
# doc_ref = db.collection('colllectionName').document()
# doc_ref.set(data)
# print('Documnet Id ->',doc_ref.id)

def convert_webp_to_jpg(webp_url,):
  url=webp_url.split('/')[-1]
  urlRemove = url.split('.')[-1]
  jpg_url = url.replace(urlRemove, "jpg")
  name="downloaded_image/"+jpg_url
  print("url -->",name)
  response = get(webp_url)
  if not response.status_code == 200:
    raise Exception(f"Error downloading image: {response.status_code}")
  with BytesIO(response.content) as image_data:
    image = Image.open(image_data).convert("RGB")  
    image.save(name, "JPEG")
    return upload_image(jpg_url)    

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
    direc = 'downloaded_image/'
    delete_files_in_folder(direc)
    return url_value

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


#READ DATA
def get_all_docs(collectionName):
    # doc_ref = (
    #     db.collection(collectionName)
    #     .stream()
    # )
    try:
        doc_ref = db.collection(collectionName)
        filter_todo = FieldFilter("ondc_status","==","LIVE_ON_ONDC")
        # filter_done = FieldFilter("status","==","QC_PASS")
        
        # Create the union filter of the two filters (queries)
        # or_filter = Or(filters=[filter_todo,filter_done])

        # Execute the Query
        docs = doc_ref.where(filter=filter_todo).stream()

        for doc in docs:
            doc_data = doc.to_dict()
            # print("DOC_Data is --> ",doc_data)
            imageArray=[]
            for item in doc_data:
                images_original = doc_data['images']
                # print('superItem --> ',doc_data['images'])
                for img in doc_data['images']:
                    filename = img.split('/')[-1]  
                    allowed_extensions = ('png', 'jpg', 'jpeg')
                    if any(filename.lower().endswith(ext) for ext in allowed_extensions):
                        # print("IF WORKED")
                        imageArray.append(img)
                    else:
                        print("Else Worked")
                        c=c+1
                        newImage = convert_webp_to_jpg(img)
                        imageArray.append(newImage)
                        # print("New Image is ",newImage)



                break
            break
    except Exception as e:
        print(f"Error Retrieving documents: {str(e)}")        
get_all_docs("catalogue")