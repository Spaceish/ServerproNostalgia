import os
import shutil
import time
import pymongo
import os

import cv2
import numpy as np
import pytesseract
import imutils
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator

IMAGE_WIDTH = 160
IMAGE_HEIGHT = 60
BATCH_SIZE = 16
EPOCHS = 10



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

def preprocess_image(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply some thresholding to the image
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # Dilate the image to make the characters more readable
    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)

    # Resize the image to the desired size
    resized = cv2.resize(dilated, (IMAGE_WIDTH, IMAGE_HEIGHT))

    # Normalize the pixel values to be between 0 and 1
    normalized = resized / 255.0

    # Add an extra dimension to the image to match the input shape expected by the model
    return np.expand_dims(normalized, axis=-1)

model = Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMAGE_HEIGHT, IMAGE_WIDTH, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

data_generator = ImageDataGenerator(preprocessing_function=preprocess_image)


dataset_dir = 'captcha dataset'

train_dataset = data_generator.flow_from_directory(
    dataset_dir,
    target_size=(IMAGE_HEIGHT, IMAGE_WIDTH),
    batch_size=BATCH_SIZE,
    color_mode='grayscale',
    class_mode='categorical',
    shuffle=True
)

history = model.fit(
    train_dataset,
    epochs=EPOCHS,
    verbose=1
)


def solve_captcha(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Preprocess the image
    preprocessed = preprocess_image(image)

    # Make a prediction using the model
    predictions = model.predict(preprocessed)

    # Convert the predictions to characters
    captcha_text = ''
    for prediction in predictions:
        captcha_text += chr(np.argmax(prediction) + 48)

    return captcha_text