import cv2
import numpy as np
from colorLimits import get_limits

img = cv2.imread(r'C:\Users\jcmis\Downloads\School\UAV Lab\images\red_triangle.png', 1)

hsvImage = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

bgrVals ={

    "orange":[255,127,0],
    "black":[0,0,0],
    "yellow":[0,255,255],
    "red":[0,0,255]

}

def main():
    
    h, w, c = hsvImage.shape


    lowerLimit, upperLimit = get_limits(bgrVals['red'])

    pixelColor = hsvImage[w//2,h//2]

    print("Pixels: " + str(pixelColor))
    print(f"{lowerLimit} {upperLimit}")

    if np.all(lowerLimit <= pixelColor) and np.all(pixelColor <= upperLimit):
        print("it is in range")
    else:
        print("it is not in range")

    cv2.imshow('Image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()





if __name__ == "__main__":
    main()

