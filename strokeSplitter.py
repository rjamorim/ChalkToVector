# Visual Interfaces final project
# Professor John R Kender
# Marcello Salomao - mrs2278
# Roberto Amorim - rja2139

import numpy as np
import cv2
import cv

from cursorParser import *


videofile = "../resources/test.mp4"


class StrokeSpliter:

    # debug only: start after the video's actual start
    startingFrame = 230
    currFrameIdx = startingFrame

    # creating capture objects
    cap = cv2.VideoCapture(videofile)
    cap2 = cv2.VideoCapture(videofile)
    cap.set(cv.CV_CAP_PROP_POS_FRAMES, startingFrame)

    # getting frame dimensions
    frame = cap2.read()[1]
    w = len(frame[0])
    h = len(frame)

    # frameDiff attributes - frameDiff is essential for our stroke segmentation
    frameDiff = None
    frameSpacing = 20

    # a precomputed list of cursor positions for each frame of the video
    cursorPosL = getCursorPosList()

    # stroke detection variables
    detectionStart = 0
    detectionEnd = 0
    detecting = False
    detectionWindowR = 5

    @classmethod
    def start(cls):
        cls.createWindows()


    @classmethod
    def createWindows(cls):
        cv2.namedWindow('frameDiff')
        cv2.moveWindow('frameDiff', 50, 50)

        cv2.namedWindow('original frame')
        cv2.moveWindow('original frame', 800, 50)

        #cv2.namedWindow('result')
        #cv2.moveWindow('result', 50, 600)


    @classmethod
    def mainLoop(cls):
        while cls.cap.isOpened() and cv2.waitKey(80) != 27:
            cls.frame = cls.cap.read()[1]

            cursorCoord = cls.cursorPosL[cls.currFrameIdx]

            cls.frameDiff = cls.getFrameDiff(cls.currFrameIdx)

            if cursorCoord[0] != -1:

                pixelsDetected = 0

                for i in range(-cls.detectionWindowR+1, cls.detectionWindowR):
                    for j in range(-cls.detectionWindowR+1, cls.detectionWindowR):
                        pixel = cls.frameDiff[cursorCoord[1]+i, cursorCoord[0]+j]
                        if int(pixel[0]) + int(pixel[1]) + int(pixel[2]) > 90:
                            pixelsDetected += 1

                if pixelsDetected > 5:
                    cls.detecting = True
                    cls.detectionStart = cls.currFrameIdx - cls.frameSpacing

                if not pixelsDetected and cls.detecting:
                    cls.detecting = False
                    cls.detectionEnd = cls.currFrameIdx

                if cls.detecting:
                    p1 = (cursorCoord[0] - cls.detectionWindowR, cursorCoord[1] + cls.detectionWindowR)
                    p2 = (cursorCoord[0] + cls.detectionWindowR, cursorCoord[1] - cls.detectionWindowR)

                    cv2.rectangle(cls.frame, p1, p2, (0, 0, 255), 1)
                    cv2.rectangle(cls.frameDiff, p1, p2, (0, 0, 255), 1)

            cls.updateFrames()


    @classmethod
    def isolateStroke(cls):
        pass
    

    @classmethod
    def updateFrames(cls):
        cls.currFrameIdx += 1

        cv2.imshow('frameDiff', cls.frameDiff)
        cv2.imshow('original frame', cls.frame)


    @classmethod
    def getFrameDiff(cls, currentFrame):
        ret, frame = cls.cap2.read()

        cls.cap2.set(cv.CV_CAP_PROP_POS_FRAMES, currentFrame + cls.frameSpacing)
        ret, frameAhead = cls.cap2.read()

        cls.cap2.set(cv.CV_CAP_PROP_POS_FRAMES, currentFrame - cls.frameSpacing)
        ret, frameBefore = cls.cap2.read()

        frameDiff = cv2.absdiff(frameAhead, frameBefore)


        cursorCoord = cls.cursorPosL[currentFrame + cls.frameSpacing]

        cursorStart = (cursorCoord[0] - 0, cursorCoord[1] - 0)
        cursorEnd = (cursorCoord[0] + 6, cursorCoord[1] + 13)

        cv2.rectangle(frameDiff, cursorStart, cursorEnd, (0, 0, 0), cv.CV_FILLED)


        cursorCoord = cls.cursorPosL[currentFrame - cls.frameSpacing]

        cursorStart = (cursorCoord[0] - 0, cursorCoord[1] - 0)
        cursorEnd = (cursorCoord[0] + 6, cursorCoord[1] + 13)

        cv2.rectangle(frameDiff, cursorStart, cursorEnd, (0, 0, 0), cv.CV_FILLED)

        return frameDiff


    @classmethod
    def finish(cls):
        cls.cap.release()
        cls.cap2.release()
        cv2.destroyAllWindows()