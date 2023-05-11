import os
import shutil
import time
import pymongo


def save_to_set(img, text):
    os.mkdir(f"captcha dataset/{text}")
    with open(f"captcha dataset/{text}/text.txt", "w") as txt:
        txt.write(text)
    ext = img.split(".")[-1]
    shutil.move(img, f"captcha dataset/{text}/{text}.{ext}")
    
def save_to_set_db(img, text):
    with open(img, "rb") as img:
        img_b = img.read()
    payload = {
        "ora in stampila" : int(time.time()),
        "captcha" : img_b,
        "solution" : text
    }
    lk = "mongodb+srv://alamicu:undeema@alamicu.pebemwy.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(lk)
    db = client["badaalamicuundeema"]
    col = db["captcha dataset"]
    col.insert_one(payload)
    print("Gata")
    print(img_b)
    print("text")
        