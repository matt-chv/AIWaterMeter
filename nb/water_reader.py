# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import cv2
import numpy as np
import os
from keras import models
from datetime import datetime
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
from PIL import Image

model = models.load_model("watermeter.h5")

def ReadSingleDial(file):
    img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (200, 200), interpolation = cv2.INTER_AREA)
    img = np.reshape(img,(1,200,200,1))/255.
    result = model.predict(img)
    
    #print("Classified as: " + str(np.argmax(result)*0.5))
    #print(result)
    return (np.argmax(result)*0.5)


def Rotate(source, angle):
    h, w, ch = source.shape
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    target = cv2.warpAffine(source, M, (w, h))
    return target

def getAnalog(source, zeiger):
    if zeiger == 0:
        x = 361-10
        y = 705
    elif zeiger == 1:
        x = 638-20
        y = 825
    elif zeiger == 2:
        x = 902-20
        y = 725
    elif zeiger == 3:
        x = 992-20
        y = 456
            
    dx = 250
    dy = 250
    
    crop_img = source[y:y+dy, x:x+dx]
    return crop_img

def calculate_brightness(image):
    greyscale_image = image.convert('L')
    histogram = greyscale_image.histogram()
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for index in range(0, scale):
        ratio = histogram[index] / pixels
        brightness += ratio * (-scale + index)

    return 1 if brightness == 255 else brightness / scale

def on_message_print(client, userdata, message):
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d-%H:%M:%S")
    print(date_time)
    
    file = open('raw/' + date_time + '.jpg', 'wb')
    file.write(message.payload)
    file.close()
    img = Image.open('raw/' + date_time + '.jpg')
    brightness = calculate_brightness(img)
    print(brightness)
    if brightness > 0.3:
        imageIn = cv2.imread('raw/' + date_time + '.jpg', cv2.IMREAD_COLOR)
        imageRotated = Rotate(imageIn, 90)
        cv2.imwrite("rotated/"  + date_time +"_rot.jpg", imageRotated)
        imageAnalog = []
        reading = []
        for i in range(0, 4):
            imageAnalog.append(getAnalog(imageRotated, i))
            cv2.imwrite("dials/" + str(i) + "_" + date_time +"_aligned.jpg", imageAnalog[i])
            reading.append(ReadSingleDial("dials/" + str(i) + "_" + date_time +"_aligned.jpg"))
    
    #    if(reading[0] >= 5):
    #        reading[1] = np.ceil([reading[1]])
    #    else:
    #        reading[1] = np.floor([reading[1]])
    #        
    #    if(reading[1] >= 5):
    #        reading[2] = np.ceil([reading[2]])
    #    else:
    #        reading[2] = np.floor([reading[2]])
            
    #    if(reading[2] >= 5):
    #        reading[3] = np.ceil([reading[3]])
    #    else:
    #        reading[3] = np.floor([reading[3]])
        
        reading_int = int(reading[3])*1000 +int(reading[2])*100+int(reading[1])*10+int(reading[0])
        print(reading)
        print(reading_int)
    else:
        os.remove('raw/' + date_time + '.jpg')

client = mqtt.Client()
client.loop_start()
client.connect_async('192.168.11.254', keepalive=60)
subscribe.callback(on_message_print, "/ESP32_CAM/image", hostname="192.168.11.254")
