import numpy as np
import cv2
import cv

class StrokeSpliter:

    @classmethod
    def start(cls, cap, frameSpacing, cursorPosL):
        cls.cap = cap
        cls.frameSpacing = frameSpacing
        cls.cursorPosL = cursorPosL


    @classmethod
    def getFrameDiff(cls, currentFrame):
        ret, frame = cls.cap.read()

        cls.cap.set(cv.CV_CAP_PROP_POS_FRAMES, currentFrame + cls.frameSpacing)
        ret, frameAhead = cls.cap.read()

        cls.cap.set(cv.CV_CAP_PROP_POS_FRAMES, currentFrame - cls.frameSpacing)
        ret, frameBefore = cls.cap.read()

        frameDiff = cv2.absdiff(frameAhead, frameBefore)


        cursorCoord = cls.cursorPosL[currentFrame + cls.frameSpacing]

        cursorStart = (cursorCoord[0] - 0, cursorCoord[1] - 0)
        cursorEnd = (cursorCoord[0] + 6, cursorCoord[1] + 13)

        cv2.rectangle(frame, cursorStart, cursorEnd, (0, 0, 0), cv.CV_FILLED)


        cursorCoord = cls.cursorPosL[currentFrame - cls.frameSpacing]

        cursorStart = (cursorCoord[0] - 0, cursorCoord[1] - 0)
        cursorEnd = (cursorCoord[0] + 6, cursorCoord[1] + 13)

        cv2.rectangle(frame, cursorStart, cursorEnd, (0, 0, 0), cv.CV_FILLED)

        return frameDiff