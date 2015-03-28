# Visual Interfaces final project
# Professor John R Kender
# Marcello Salomao - mrs2278
# Roberto Amorim - rja2139

import numpy as np
import cv2
import cv

# Get the videoCapture object and set it a bit ahead, so we don't have to wait a lot to start debugging
cap = cv2.VideoCapture("../resources/test.mp4")
cap.set(cv.CV_CAP_PROP_POS_MSEC, 27500)

# Read the first frame to obtain the video dimension
ret, frame = cap.read()

# Buffers we will use throughout our application
# frameThresh = np.zeros(frame.shape, np.uint32)

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
                cursorCoord = (vert[0][0], vert[0][1])

        cv2.circle(frame, cursorCoord, 4, (0, 0, 255), 1) # Red debug circle
        cv2.circle(frame, cursorCoord, 1, (255, 0, 0), 1) # And its blue center

        print maxArea, maxCnt[0]

        # cv2.drawContours(frame, [maxCnt], 0, (0, 255, 0), 1) # Debug purposes only

    newS = (int(frame.shape[1] * 2), int(frame.shape[0] * 2))
    frame = cv2.resize(frame, newS, interpolation=cv2.INTER_NEAREST)
    cv2.imshow('frame', frame)
    # cv2.imshow('frameThresh', frameThresh) # Debug purposes only

cap.release()
cv2.destroyAllWindows()

