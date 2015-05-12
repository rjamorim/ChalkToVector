# Visual Interfaces final project
# Professor John R Kender
# Marcello Salomao - mrs2278
# Roberto Amorim - rja2139

import numpy as np
import cv2
import cv
from cursorParser import *
import strokeSplitter as ss


startingFrame = 200
currFrameIdx = startingFrame

videofile = "../resources/test.mp4"

# Get the videoCapture object and set it a bit ahead, so we don't have to wait a lot to start debugging
cap = cv2.VideoCapture(videofile)
cap2 = cv2.VideoCapture(videofile)
cap.set(cv.CV_CAP_PROP_POS_FRAMES, startingFrame)

# Read the first frame to obtain the video dimension
ret, lastFrame = cap.read()

cursorPosL = getCursorPosList()

cv2.namedWindow('frameDiff')
cv2.moveWindow('frameDiff', 50, 50)

cv2.namedWindow('original frame')
cv2.moveWindow('original frame', 800, 50)

cv2.namedWindow('result')
cv2.moveWindow('result', 50, 600)

frameDiff = None
frameSpacing = 10

ss.StrokeSpliter.start(cap2, frameSpacing, cursorPosL)

detectionStart = 0
detectionEnd = 0
detecting = False
detectionWindowR = 7


while cap.isOpened() and cv2.waitKey(80) != 27:
    ret, frame = cap.read()

    cursorCoord = cursorPosL[currFrameIdx]

    frameDiff = ss.StrokeSpliter.getFrameDiff(currFrameIdx)

    if cursorCoord[0] != -1:

        pixelsDetected = 0

        for i in range(-detectionWindowR+1, detectionWindowR):
            for j in range(-detectionWindowR+1, detectionWindowR):
                pixel = frame[cursorCoord[1]+i, cursorCoord[0]+j]
                if 40 < pixel[0] or 40 < pixel[1] or 40 < pixel[2]:
                    pixelsDetected += 1

        if pixelsDetected > 3:
            detecting = True
            detectionStart = currFrameIdx

        if not pixelsDetected and detecting:
            detecting = False
            detectionEnd = currFrameIdx

        if detecting:
            cv2.circle(frameDiff, cursorCoord, 3, (0, 0, 255), 1)
            cv2.rectangle(frameDiff, (-detectionWindowR+1, detectionWindowR), (-detectionWindowR+1, detectionWindowR)),



    currFrameIdx += 1
    cv2.imshow('frameDiff', frameDiff)
    cv2.imshow('original frame', frame)

cap.release()
cv2.destroyAllWindows()

