import cv2
import numpy as np
from colorLimits import get_limits

img = cv2.imread(r'C:\Users\jcmis\Downloads\School\UAV Lab\cropped.png', 1)
cv2.imshow('Image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

hsvImage = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

bgrVals ={

    "orange":[255,127,0],
    "black":[0,0,0],
    "yellow":[0,255,255],
    "red":[0,0,255],
    "blue":[255,0,0],
    "green":[0,255,0],
    "white":[255,255,255]

}

def main():
    
    h, w, c = hsvImage.shape

    print("here is the pixel" + str(hsvImage[148,50]))
    lowerLimit, upperLimit = get_limits(bgrVals['white'])

    redMask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
    redMaskPixC = cv2.countNonZero(redMask)

    print(redMaskPixC)
    cv2.imshow('Image',redMask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()





if __name__ == "__main__":
    main()

