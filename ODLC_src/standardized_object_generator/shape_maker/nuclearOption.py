import os
import glob

files = glob.glob(r"C:\Users\jcmis\Downloads\School\UAV Lab\testImages\*")


for file in files:
    os.remove(f"{file}")



#print(os.path.basename(file))
