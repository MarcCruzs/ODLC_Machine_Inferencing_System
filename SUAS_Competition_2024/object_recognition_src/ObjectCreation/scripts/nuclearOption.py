import os
import glob

files = glob.glob(r"C:\Users\jcmis\Downloads\School\UAV Lab\GitRepo\SUAS_Competiton\SUAS_Competition_2024\object_recognition_src\ObjectCreation\testImages*")


for file in files:
    os.remove(f"{file}")



#print(os.path.basename(file))
