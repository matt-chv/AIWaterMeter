""" Validating that labeling is OK as much as posisble:
* images (.jpg) file format should be 
%Y-%m-%d-%H-%M-%S_Volumeinm3.volume.jpg
* volume increase over time should be positive or null
"""

from os import walk
from datetime import datetime

import pandas as pd

readings = []
for root, dirs, files in walk("."):
   for f in files:
      if f.find(".jpg")>=0:
         try:
            datetimestamp, volume = f.split("_")
            dt = datetime.strptime(datetimestamp,"%Y-%m-%d-%H-%M-%S")
            volume_m3, volume_dl, _ = volume.split(".")
            volume = float(volume_m3)+float(volume_dl)/10000
         except:
            print("Filename badly formated",f)
            raise
         else:
            readings.append((dt,volume))
df = pd.DataFrame(readings,columns =["dt","Volume"])
df = df.sort_values(by="dt",ascending=True)
df["Vol_delta"]= df['Volume']-df['Volume'].shift(1)
df = df[df["Vol_delta"]<0]

if df.empty:
   print("no obvious labelling issues found !")
else:
   print("Volume did decrease at those timestamps, likely a labelling issue")
   print(df)
