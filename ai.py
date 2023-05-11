import os
import shutil


def save_to_set(img, text):
    os.mkdir(f"captcha dataset/{text}")
    with open(f"captcha dataset/{text}/text.txt") as txt:
        txt.write(text)
    ext = img.split(".")[-1]
    shutil.move(img, f"captcha dataset/{text}.{ext}")
    os.remove(img)