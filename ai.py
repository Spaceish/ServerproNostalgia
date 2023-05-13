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
from io import StringIO

IMAGE_WIDTH = 200
IMAGE_HEIGHT = 70
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

def retrieve_training_data():
    # Connect to the database
    client = pymongo.MongoClient("mongodb+srv://alamicu:undeema@alamicu.pebemwy.mongodb.net/?retryWrites=true&w=majority")
    db = client["badaalamicuundeema"]
    col = db["captcha dataset"]
    
    # Create the "captcha dataset" folder if it doesn't exist
    os.makedirs("captcha dataset", exist_ok=True)
    
    # Loop through each document in the collection
    for doc in col.find():
        # Get the binary data and solution from the document
        captcha = doc["captcha"]
        solution = doc["solution"]
        
        os.mkdir(f"captcha dataset/{solution}")
        # Write the binary data to a file
        with open(f"captcha dataset/{solution}/{solution}.png", "wb") as f:
            f.write(captcha)
            
        # Write the solution to a text file
        with open(f"captcha dataset/{solution}/text.txt", "w") as f:
            f.write(solution)

# def preprocess_image(image):
#     # pylint: disable=no-member
#     # Convert the image to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Apply some thresholding to the image
#     thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

#     # Dilate the image to make the characters more readable
#     kernel = np.ones((3,3), np.uint8)
#     dilated = cv2.dilate(thresh, kernel, iterations=1)

#     # Get the width and height of the image
#     height, width = dilated.shape[:2]

#     # Resize the image to the desired size
#     resized = cv2.resize(dilated, (width, height))

#     # Normalize the pixel values to be between 0 and 1
#     normalized = resized / 255.0

#     # Add an extra dimension to the image to match the input shape expected by the model
#     return np.expand_dims(normalized, axis=-1)

# def preprocess_dataset():
#     # create directories for processed images
#     os.makedirs("processed_captcha_dataset", exist_ok=True)
#     for label in os.listdir("captcha dataset"):
#         if os.path.isdir(f"captcha dataset/{label}"):
#             os.makedirs(f"processed_captcha_dataset/{label}", exist_ok=True)
#             for filename in os.listdir(f"captcha dataset/{label}"):
#                 if filename.endswith(".png"):
#                     image_path = f"captcha dataset/{label}/{filename}"
#                     print(f"Processing image: {image_path}")
#                     # pylint: disable=no-member
#                     image = cv2.imread(image_path)
#                     if image is not None and not image.size == 0:
#                         processed_image = preprocess_image(image)
#                         cv2.imwrite(f"processed_captcha_dataset/{label}/{filename}", processed_image)

# preprocess_dataset()

# model = Sequential([
#     layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMAGE_HEIGHT, IMAGE_WIDTH, 1)),
#     layers.MaxPooling2D((2, 2)),
#     layers.Conv2D(64, (3, 3), activation='relu'),
#     layers.MaxPooling2D((2, 2)),
#     layers.Flatten(),
#     layers.Dense(128, activation='relu'),
#     layers.Dense(10, activation='softmax')
# ])

# model.compile(optimizer='adam',
#               loss='categorical_crossentropy',
#               metrics=['accuracy'])

# data_generator = ImageDataGenerator(preprocessing_function=preprocess_image)


# dataset_dir = 'captcha dataset'

# train_dataset = data_generator.flow_from_directory(
#     dataset_dir,
#     target_size=(IMAGE_HEIGHT, IMAGE_WIDTH),
#     batch_size=BATCH_SIZE,
#     color_mode='grayscale',
#     class_mode='categorical',
#     shuffle=True
# )

# history = model.fit(
#     train_dataset,
#     epochs=EPOCHS,
#     verbose=1
# )


# def solve_captcha(image_path, model):
#     # Load the image
#     # pylint: disable=no-member
#     image = cv2.imread(image_path)

#     # Preprocess the image
#     preprocessed = preprocess_image(image)

#     # Make a prediction using the model
#     predictions = model.predict(preprocessed)

#     # Convert the predictions to characters
#     captcha_text = ''
#     for prediction in predictions:
#         captcha_text += chr(np.argmax(prediction) + 48)

#     return captcha_text

# # retrieve_training_data()