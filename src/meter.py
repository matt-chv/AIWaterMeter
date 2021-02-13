"""
v0.1: reads decimal part of meter from image
"""

#Python modules
import logging
import os

#Pip imports
import cv2
from tensorflow import keras
import numpy as np
import matplotlib
import matplotlib.pylab as plt


# fix image rotation by 15.3
def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

def get_img(path, file):
   """
   Parameters:
   -----------
   path: str
   file: str
   Returns:
   --------
   image: cv2 image
   """
   image = cv2.imread(os.path.join(path,file), cv2.IMREAD_GRAYSCALE)
   image = rotate_image(image, 15.3)
   cv2.imwrite("rotated.jpg",image)
   return image 

def meter_reading(m3,dl):
   """
   Parameters:
   -----------
   m3: int
   dl: list of int
   Return:
   -------
   vol_m3: float
      volume in m3 from the dial and gauges values
      /!\ The nature of gauges means the gauge will show the next value early
      converting requires to take 1 away from digit if digit for smaller gauge is 9

       Example: reading gauges in order 2* 1/10 m3 + 9 *1/100 m3 = 0.19m3 
   """
   #see comments above for logic
   dl = [str(x[0] if x[1]<9 else x[0]-1) for x in zip(dl, dl[1:] + [0])]
   dl = int("".join(dl))/(10**len(dl))
   return m3+dl
            
   
def validate():
   """ add here code for non reg """
   assert meter_reading(0,[0,0,0,0,0])==0
   assert meter_reading(0,[1,2,3,4,5])==0.12345
   assert meter_reading(0,[1,2,3,4,9])==0.12339

def get_dials(meter_image):
   """
   Parameters:
   -----------
   meter_image: XXX
      image in open cv
   Returns:
   --------
   dial_imges: list of XXX
      list of images
   """
   dials = []
   cs = [(1250, 508),(1154,837),(843, 974),(520, 839)]
   r=140
   for i, center in enumerate(cs):
      cx, cy = center
      dial = meter_image[cy-r:cy+r, cx-r:cx+r]
      dial = cv2.resize(dial, (200, 200), interpolation = cv2.INTER_AREA)
      cv2.imwrite("dial%s.jpg"%(i),dial)
      dials.append(dial)
   return dials

   
def get_readings(dials):
   """
   Parameters:
   -----------
   dials: list of cv2 images
      images of each dial sorted in descending order of volume resolution
   Returns:
   --------
   readings: list of int
   """
   readings = []
   model = keras.models.load_model('ai_dial.h5')
   for dial in dials:
      dial = np.reshape(dial,(1,200,200,1))/255.
      predictions = model.predict(dial)
      res=np.argmax(predictions)*0.5
      readings.append(res)
   return readings
   
def get_meter_volume(folder,fn):
   """
   Parameters:
   -----------
   folder: str
      folder path
   fn: str
      filename
   Return:
   -------
   res: float
      the meter reading in m3
   FIXME:
   ------
   Hardcoded the integer part of the meter
   """
   img = get_img(folder,fp)
   dials = get_dials(img)
   readings = get_readings(dials)
   readings = [int(r) for r in readings]
   #@FIXME: below hard coded 157 value
   res = meter_reading(157,readings)
   return res
   
if __name__=="__main__":
   res = get_meter_volume("../data/labeled/","2020-07-07-22-23-27_00157.4673.jpg")
   print(f"Volume in m3: {res}")
