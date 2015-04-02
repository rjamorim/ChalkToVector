# Visual Interfaces final project
# Professor John R Kender
# Marcello Salomao - mrs2278
# Roberto Amorim - rja2139

import numpy as np
import cv2
import cv


def vectorize(fromFrame, toFrame):
    pass


# Get the videoCapture object and set it a bit ahead, so we don't have to wait a lot to start debugging
cap = cv2.VideoCapture("../resources/test.mp4")
cap2 = cv2.VideoCapture("../resources/test.mp4")
cap.set(cv.CV_CAP_PROP_POS_MSEC, 27500)

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

# currFrame = cap.get(cv.CV_CAP_PROP_POS_FRAMES) + 1

cv2.namedWindow('frameDiff')
cv2.namedWindow('frame')
cv2.moveWindow('frameDiff', 20, 20)
cv2.moveWindow('frame', 700, 20)

# Main loop
while cap.isOpened() and cv2.waitKey(50) != 27:
    ret, frame = cap.read()

    # Identifies positions within the frame with color values between 230 and 255 to locate the cursor
    frameThresh = cv2.inRange(frame, (230, 230, 230), (255, 255, 255))
    # cv.CV_RETR_EXTERNAL
    contours, hierarchy = cv2.findContours(frameThresh, cv.CV_RETR_LIST, cv.CV_CHAIN_APPROX_NONE)

    if contours:
        maxArea = 0
        maxCnt = None
        cursorCoord = (100000, 100000)  # Just a number much larger than any video dimension
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

        # cv2.circle(frame, cursorCoord, 4, (0, 0, 255), 1)  # Red debug circle
        # cv2.circle(frame, cursorCoord, 1, (255, 0, 0), 1)  # And its blue center

        # print maxArea # Debug purposes only
        # cv2.drawContours(frame, [maxCnt], 0, (0, 255, 0), 1) # Debug purposes only
        # if maxArea <= 3.5: cv2.circle(frame, cursorCoord, 4, (255, 255, 255), 1) # Red debug circle
        # NOTE: inform in the report that even with very low values of area, we still achieve
        # pretty good precision. (area=3.5 for instance)

    currFrameIdx = cap.get(cv.CV_CAP_PROP_POS_FRAMES)
    cap2.set(cv.CV_CAP_PROP_POS_FRAMES, currFrameIdx + 40)
    ret, frameAhead = cap2.read()
    cap2.set(cv.CV_CAP_PROP_POS_FRAMES, currFrameIdx - 40)
    ret, frameBefore = cap2.read()
    frameDiff = cv2.absdiff(frameAhead, frameBefore)

    lastFrame = frame.copy()


    # DEBUG DRAW of inferred cursor path
    overlay = frame.copy() # create a copy of frame
    lastVert = cursorPosL[0]
    for vert in cursorPosL: # draw points and connections
        cv2.line(frame, lastVert, vert, (255, 150, 150),1, cv.CV_AA)
        lastVert = vert
    for vert in cursorPosL: cv2.line(frame, vert, vert, (0, 0, 255),1)
    opacity = 0.4 # blend with original image
    cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)


    newS = (int(frame.shape[1] * 2), int(frame.shape[0] * 2))
    frameDiff = cv2.resize(frameDiff, newS, interpolation=cv2.INTER_NEAREST)
    frame = cv2.resize(frame, newS, interpolation=cv2.INTER_NEAREST)


    cv2.imshow('frameDiff', frameDiff)
    cv2.imshow('frame', frame)

    # cv2.imshow('frameThresh', frameThresh) # Debug purposes only


cap.release()
cv2.destroyAllWindows()

