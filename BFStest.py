import numpy as np
import cv2
import cv

pathX = "resources/x.png"
pathM = "resources/m.png"
path2 = "resources/2.png"

xImg = cv2.imread(pathX)

xImg = cv2.cvtColor(xImg,cv.CV_RGB2GRAY)

cv2.ellipse(xImg, startX, )

newSize = (int(xImg.shape[1] * 16), int(xImg.shape[0] * 16))
xImg = cv2.resize(xImg, newSize, interpolation=cv2.INTER_NEAREST)

while cv2.waitKey(250) != 27:
    cv2.imshow("x image", xImg)
