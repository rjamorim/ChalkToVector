# Visual Interfaces final project
# Professor John R Kender
# Marcello Salomao - mrs2278
# Roberto Amorim - rja2139

import numpy as np
import cv2
import cv

# Get the videoCapture object and set it a bit ahead, so we don't have to wait a lot to start debugging
cap = cv2.VideoCapture("../resources/test.mp4")
cap2 = cv2.VideoCapture("../resources/test.mp4")
# startingFrame = 265
startingFrame = 300
cap.set(cv.CV_CAP_PROP_POS_FRAMES, startingFrame)

# Read the first frame to obtain the video dimension
ret, lastFrame = cap.read()

# Buffers we will use throughout our application
# lastFrame = np.zeros(frame.shape, np.uint32)

# List of cursor positions
cursorPosL = []

# List of attributes per frame posL[2] >> -2 >> posL[2-2] == posL[0]
# posL = [ [STROKE_BEGIN/END/HOLD/UNKNOWN,dsfh], -1 , -2 ]
posL = []
colorL = []
frameSpacing = 1 # needs more descriptive name

# currFrame = cap.get(cv.CV_CAP_PROP_POS_FRAMES) + 1

cv2.namedWindow('frameDiff')
cv2.moveWindow('frameDiff', 50, 50)

cv2.namedWindow('frame')
cv2.moveWindow('frame', 800, 50)

#cv2.namedWindow('result')
#cv2.moveWindow('result', 50, 600)

points = []

def vectorize(cIdx, frameDiff):
    if cIdx > 0:
        res = np.zeros(frameDiff.shape)

        x0 = cursorPosL[cIdx-1][0]
        y0 = cursorPosL[cIdx-1][1]

        x1 = cursorPosL[cIdx][0]
        y1 = cursorPosL[cIdx][1]

        moveVec = (x1 - x0, y1 - y0)

        pixelsMatched = []

        for i in range(3):
            for j in range(3):
                sampleX = x0 + i
                sampleY = y0 + j
                if res.shape[1] <= sampleX < 0 or frameDiff.shape[0] <= sampleY < 0:
                    continue
                # Is RGB above (30,30,30) threshold?
                if [a for a,b in zip(frameDiff[sampleY][sampleX], [30, 30, 30]) if a > b]:
                    pixelsMatched.append((sampleX, sampleY))
                    cv2.circle(frameDiff, pixelsMatched[-1], 3, (0, 0, 255), 1)

        if len(pixelsMatched) != 0:
            points.append(pixelsMatched[-1])
        else:
            points.append( (-1,-1) )

        cv2.line(frameDiff, (cursorPosL[cIdx-1][0], cursorPosL[cIdx-1][1]), (cursorPosL[cIdx][0], cursorPosL[cIdx][1]), (255, 250, 150), 1, cv.CV_AA)

        lastVert = points[0]
        for vert in points:  # draw points and connections
            if vert[0] != -1 and lastVert[0] != -1:
                cv2.line(res, lastVert, vert, (255, 150, 150), 1, cv.CV_AA)
            lastVert = vert

        # cv2.imshow('result', res)

# Main loop
while cap.isOpened() and cv2.waitKey(1500) != 27:
    ret, frame = cap.read()

    # Identifies positions within the frame with color values between 230 and 255 to locate the cursor
    frameThresh = cv2.inRange(frame, (230, 230, 230), (255, 255, 255))
    contours, hierarchy = cv2.findContours(frameThresh, cv.CV_RETR_EXTERNAL, cv.CV_CHAIN_APPROX_NONE)

    # Getting cursor position from its contour
    if contours:
        maxArea = 0
        maxCnt = None
        cursorCoord = (float("inf"), float("inf"))  # Just a number much larger than any video dimension
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > maxArea:
                maxArea = area
                maxCnt = cnt

        for vert in cnt:
            if vert[0][0] <= cursorCoord[0] and vert[0][1] <= cursorCoord[1]:
                cursorCoord = (vert[0][0]-1, vert[0][1]-3)

        cursorPosL.append(cursorCoord)

        cursorStart = (cursorCoord[0] - 0, cursorCoord[1] - 0)
        cursorEnd = (cursorCoord[0] + 6, cursorCoord[1] + 13)
        cv2.rectangle(frame, cursorStart, cursorEnd, (0, 0, 0), cv.CV_FILLED)

    else:
        cursorPosL.append((-1,-1))

    currFrameIdx = cap.get(cv.CV_CAP_PROP_POS_FRAMES)
    cap2.set(cv.CV_CAP_PROP_POS_FRAMES, currFrameIdx + frameSpacing)
    ret, frameAhead = cap2.read()
    cap2.set(cv.CV_CAP_PROP_POS_FRAMES, currFrameIdx - frameSpacing)
    ret, frameBefore = cap2.read()
    frameDiff = cv2.absdiff(frameAhead, frameBefore)

    #vectorize(int(currFrameIdx)-startingFrame-2, frameDiff)

    lastFrame = frame.copy()

    # DEBUG DRAW of inferred cursor path
    overlay = frame.copy()  # create a copy of frame
    lastVert = cursorPosL[0]
    for vert in cursorPosL:  # draw points and connections
        if vert[0] != -1 and lastVert[0] != -1:
            # Draws in blue the line made by the cursor movement
            cv2.line(frame, lastVert, vert, (255, 150, 150), 1, cv.CV_AA)
        lastVert = vert

    # Draws vertices for the vectors
    for vert in cursorPosL:
        if vert[0] != -1:
            cv2.line(frame, vert, vert, (0, 0, 255), 1)

######################## MEN AT WORK
    for i in range(-2, 3):
        for j in range(-2, 3):
            pixel = frame[cursorCoord[1]+i, cursorCoord[0]+j]
            if 10 < pixel[0] < 230 or 10 < pixel[1] < 230 or 10 < pixel[2] < 230:
                frameDiff[cursorCoord[1]+i, cursorCoord[0]+j] = (255,255,255)
                print "Detected point: " + str(pixel)
########################

    print str(frame[cursorCoord[0], cursorCoord[1]]) + "   "  + str(cursorCoord)

    opacity = 0.4 # blend the cursor blue line with original image
    cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)

    newSize = (int(frame.shape[1] * 2), int(frame.shape[0] * 2))
    frameDiff = cv2.resize(frameDiff, newSize, interpolation=cv2.INTER_NEAREST)
    frame = cv2.resize(frame, newSize, interpolation=cv2.INTER_NEAREST)

    cv2.imshow('frameDiff', frameDiff)
    cv2.imshow('frame', frame)

    # cv2.imshow('frameThresh', frameThresh) # Debug purposes only

cap.release()
cv2.destroyAllWindows()

