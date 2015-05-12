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
    startingFrame = 250
    currFrameIdx = startingFrame

    # creating capture objects
    cap = cv2.VideoCapture(videofile)
    cap2 = cv2.VideoCapture(videofile)
    cap.set(cv.CV_CAP_PROP_POS_FRAMES, startingFrame)

    # getting frame dimensions
    frame = cap2.read()[1]
    w = len(frame[0])
    h = len(frame)
    parsedRegions = np.zeros(frame.shape, frame.dtype)

    # frameDiff attributes - frameDiff is essential for our stroke segmentation
    frameDiff = None
    frameSpacing = 7

    # a precomputed list of cursor positions for each frame of the video
    cursorPosL = getCursorPosList()

    # stroke detection variables
    detectionStart = 0
    detectionEnd = 0
    detecting = False
    detectionWindowR = 3

    dilationKernel = np.ones((3,3),np.uint8)

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

            cls.frameDiff = cls.getFrameDiff(cls.frameSpacing, cls.frameSpacing)

            detectionPos = [0,0]

            if cursorCoord[0] != -1:

                pixelsDetected = 0

                for i in range(-cls.detectionWindowR + 1, cls.detectionWindowR):
                    for j in range(-cls.detectionWindowR + 1, cls.detectionWindowR):
                        pixel = cls.frameDiff[cursorCoord[1] + i, cursorCoord[0] + j]
                        if int(pixel[0]) + int(pixel[1]) + int(pixel[2]) > 90:
                            pixelsDetected += 1
                            detectionPos[0] += cursorCoord[0] + i
                            detectionPos[1] += cursorCoord[1] + j

                if pixelsDetected > 5:
                    cls.detecting = True
                    cls.detectionStart = cls.currFrameIdx - cls.frameSpacing
                    detectionPos[0] = int( float(detectionPos[0]) / float(pixelsDetected) )
                    detectionPos[1] = int( float(detectionPos[1]) / float(pixelsDetected) )
                    cls.isolateStroke2(detectionPos)
                    # cls.isolateStroke(cursorCoord)

                if not pixelsDetected and cls.detecting:
                    cls.detecting = False
                    cls.detectionEnd = cls.currFrameIdx

                if cls.detecting:
                    p1 = (cursorCoord[0] - cls.detectionWindowR, cursorCoord[1] + cls.detectionWindowR)
                    p2 = (cursorCoord[0] + cls.detectionWindowR, cursorCoord[1] - cls.detectionWindowR)

                    # cv2.rectangle(cls.frame, p1, p2, (0, 0, 255), 1)
                    # cv2.rectangle(cls.frameDiff, p1, p2, (0, 0, 255), 1)
                    #
                    # cv2.circle(cls.frame, (detectionPos[0], detectionPos[1]), 2, (255,240,110))

            cls.updateFrames()


    # add neighbors of the pixel at location 'pt' to the BFS queue
    @classmethod
    def addNB(cls, img, pt, queue):
        if pt[0] + 1 < len(img[0]):
            queue.append([pt[0], pt[1] + 1])
        if pt[1] + 1 < len(img):
            queue.append([pt[0] + 1, pt[1]])
        if pt[0] - 1 > -1:
            queue.append([pt[0], pt[1] - 1])
        if pt[1] - 1 > -1:
            queue.append([pt[0] - 1, pt[1]])


    @classmethod
    def pixelBFS(cls, img, start):

        BFSqueue = []
        BFSexploredPixels = []

        # add first neighbors to the BFS queue
        cls.addNB(img, start, BFSqueue)

        while BFSqueue:
            pixelToExplore = BFSqueue[0][0:2]
            BFSqueue.pop(0)

            if pixelToExplore in BFSexploredPixels:
                continue

            if img[pixelToExplore[1], pixelToExplore[0]] < 10:
                continue

            BFSexploredPixels.append(pixelToExplore)

            cls.addNB(img, pixelToExplore, BFSqueue)

        return BFSexploredPixels


    currStartSpacing = 3
    currEndSpacing = 3
    expandingStart = True
    lastCntArea = 0
    uselessExpansions = 0
    maxUselessExpansions = 45

    @classmethod
    def isolateStroke2(cls, cursorCoord):

        expandingDone = False

        while (not expandingDone):
            cls.tmpFrameDiff = cls.getFrameDiff(cls.currStartSpacing, cls.currEndSpacing)
            cls.frameThresh = cv2.cvtColor(cls.tmpFrameDiff, cv.CV_RGB2GRAY)
            cls.frameThresh = cv2.inRange(cls.frameThresh, 40, 255)
            # cls.frameThresh = cv2.dilate(cls.frameThresh, cls.dilationKernel, 1)

            strokeArea = cls.pixelBFS(cls.frameThresh, cursorCoord)

            if cls.expandingStart: cls.currStartSpacing += 1
            else: cls.currEndSpacing += 1

            if len(strokeArea) > cls.lastCntArea:
                cls.lastCntArea = len(strokeArea)
                cls.uselessExpansions -= 1
                if cls.uselessExpansions < 0: cls.uselessExpansions = 0
            else:
                cls.uselessExpansions += 1

                if cls.uselessExpansions > cls.maxUselessExpansions:
                    if cls.expandingStart:
                        cls.expandingStart = False
                        cls.uselessExpansions = 0
                    else:
                        expandingDone = True

            # print cls.uselessExpansions

        print cls.currStartSpacing, cls.currEndSpacing

        cls.currStartSpacing = 3
        cls.currEndSpacing = 3
        cls.expandingStart = True
        cls.lastCntArea = 0
        cls.uselessExpansions = 0
        cls.maxUselessExpansions = 45

        print len(strokeArea)
        for p in strokeArea:
            cv2.circle(cls.parsedRegions, (p[0], p[1]), 1, (80,80,255))
            # cv2.circle(cls.tmpFrameDiff, (p[0], p[1]), 1, (80,80,255))

        cv2.circle(cls.tmpFrameDiff, (cursorCoord[0], cursorCoord[1]), 3, (180,180,255))

        cv2.imshow('tmpFrameDiff', cls.frameThresh)
        cv2.waitKey(70)



                # dist = cv2.pointPolygonTest(maxCnt, cursorCoord, True)
                #
                # if dist >= 0:
                #     frameThreshInv = cv2.bitwise_not(frameThresh)
                #
                #     # parsedRegion = cv2.bitwise_and(tmpFrameDiff, tmpFrameDiff, mask = frameThresh)
                #     # parsedRegionRest = cv2.bitwise_and(cls.parsedRegions, cls.parsedRegions, mask = frameThreshInv)
                #     # cls.parsedRegions = cv2.add(parsedRegionRest, parsedRegion)
                #
                #     cls.parsedRegions = tmpFrameDiff
                #
                #     # tmp = tmpFrameDiff.copy()
                #     # cv2.drawContours(tmp, [maxCnt], 0, (0,0,250), cv.CV_FILLED)
                #     # cv2.imshow('tmpFrameDiff', tmp)
                #     # cv2.waitKey(10000)


    @classmethod
    def updateFrames(cls):
        cls.currFrameIdx += 1

        cv2.imshow('frameDiff', cls.frameDiff)
        cv2.imshow('original frame', cls.frame)
        cv2.imshow('parsedRegions', cls.parsedRegions)



    @classmethod
    def getFrameDiff(cls, frameSpacingStart, frameSpacingEnd):
        ret, frame = cls.cap2.read()

        cls.cap2.set(cv.CV_CAP_PROP_POS_FRAMES, cls.currFrameIdx + frameSpacingEnd)
        ret, frameAhead = cls.cap2.read()

        cls.cap2.set(cv.CV_CAP_PROP_POS_FRAMES, cls.currFrameIdx - frameSpacingStart)
        ret, frameBefore = cls.cap2.read()

        frameDiff = cv2.absdiff(frameAhead, frameBefore)


        cursorCoord = cls.cursorPosL[cls.currFrameIdx + frameSpacingEnd]

        cursorStart = (cursorCoord[0] - 0, cursorCoord[1] - 0)
        cursorEnd = (cursorCoord[0] + 6, cursorCoord[1] + 13)

        cv2.rectangle(frameDiff, cursorStart, cursorEnd, (0, 0, 0), cv.CV_FILLED)


        cursorCoord = cls.cursorPosL[cls.currFrameIdx - frameSpacingStart]

        cursorStart = (cursorCoord[0] - 0, cursorCoord[1] - 0)
        cursorEnd = (cursorCoord[0] + 6, cursorCoord[1] + 13)

        cv2.rectangle(frameDiff, cursorStart, cursorEnd, (0, 0, 0), cv.CV_FILLED)

        return frameDiff


    @classmethod
    def finish(cls):
        cls.cap.release()
        cls.cap2.release()
        cv2.destroyAllWindows()