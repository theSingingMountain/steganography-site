# Importing libraries opencv and numpy
import cv2
import numpy as np
import random
from pathlib import Path
from PIL import Image as im
import os
from django.contrib.auth.models import User
from django.http import HttpResponse
# Converting to binary
def messageToBinary(message):
    # Validating the type of instance of message to be string, byte or int, otherwise type not supported
    if type(message) == str:
        return ''.join([format(ord(i), "08b") for i in message])
    elif type(message) == bytes or type(message) == np.ndarray:
        return [ format(i, "08b") for i in message ]
    elif type(message) == int or type(message) == np.uint8:
        return format(message, "08b")
    else:
        return TypeError("Input type not supported.")

def hide(image_name, username, secret_message):
    print("--------------------- Encoding Data ---------------------")
    print("Encoding Image: ", image_name)
    # Using opencv library to read the bytes of the image

    image = cv2.imread(image_name, cv2.IMREAD_UNCHANGED)

    image_name = str(os.path.basename(image_name))
    height, width, channel = image.shape
    n_bytes = height * width * channel

    if len(secret_message) > n_bytes:
        raise ValueError("Insufficient Bytes in image, need a bigger image or lesser data.")

    secret_message += "####"
    data_index = 0

    binary_secret_message = messageToBinary(secret_message)

    data_len = len(binary_secret_message)

    binary_secret_message = messageToBinary(secret_message)
    data_len = len(binary_secret_message)
    max_length_message = 1200
    height, width, channel = image.shape        
    n_bytes = height * width * channel        

    random.seed(str(username + image_name))
    indexList = list()
    
    while len(indexList) < max_length_message:
        index = random.randint(0, n_bytes)
        if index not in indexList:
            indexList.append(index)
            random.seed(index)
        else:
            random.seed(index)
    print(indexList)
    for i in indexList:
        f_row = int(i / (width * channel))
        f_col1 = i % (width * channel)
        f_col2 = int(f_col1 / channel)
        f_channel = f_col1 % channel
        currChannel = image[f_row][f_col2][f_channel]
        currChannelBinary = messageToBinary(currChannel)
        if data_index < data_len:
            image[f_row][f_col2][f_channel] = int(currChannelBinary[:-1] + binary_secret_message[data_index], 2)
            data_index+=1
        if data_index >= data_len:
            break
    print(image)
    print(image_name)
    return image, image_name

def reveal(image_name, username):
    print("--------------------- Decoding data ---------------------")
    # Read the image with the opencv library
    print("Decoding Image: ", image_name)
    image = cv2.imread( image_name, cv2.IMREAD_UNCHANGED)
    binary_data = ""
    height, width, channel = image.shape

    print("Height, Width, Channel: ", height,width,channel)

    n_bytes = height * width * channel
    max_length_message = 1200
    image_name = str(os.path.basename(image_name))
    random.seed(str(username + image_name))

    indexList = list()
    
    while len(indexList) < max_length_message:
        index = random.randint(0, n_bytes)
        if index not in indexList:
            indexList.append(index)
            random.seed(index)
        else:
            random.seed(index)

    for i in indexList:
        f_row = int(i / (width * channel))
        f_col1 = i % (width * channel)
        f_col2 = int(f_col1 / channel)
        f_channel = f_col1 % channel
        currChannel = image[f_row][f_col2][f_channel]
        currChannelBinary = messageToBinary(currChannel)
        binary_data += currChannelBinary[-1]

    all_bytes = [ binary_data[i:i+8] for i in range(0, len(binary_data), 8) ]
    decoded_data = ""

    # Converting from binary to human readable data
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-4:] == "####":
            break
    print(str(decoded_data[:-4]))
    return decoded_data[:-4]