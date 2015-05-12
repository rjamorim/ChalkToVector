# Visual Interfaces final project
# Professor John R Kender
# Marcello Salomao - mrs2278
# Roberto Amorim - rja2139

import cv2
import cv


# Method to store in a file a list of all cursor positions in the video file
def updateCursorPosList(videofile):
    cap = cv2.VideoCapture(videofile)
    cursorFile = open("./resources/cursor.txt", 'w')

    while cap.isOpened():

        ret, frame = cap.read()
        if frame == None: break

        # Identifies positions within the frame with color values between 230 and 255 to locate the cursor
        frameThresh = cv2.inRange(frame, (230, 230, 230), (255, 255, 255))
        contours = cv2.findContours(frameThresh, cv.CV_RETR_EXTERNAL, cv.CV_CHAIN_APPROX_NONE)[0]
        maxArea = 0
        maxCnt = None

        # Getting cursor position from its contour
        if contours:

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > maxArea:
                    maxArea = area
                    maxCnt = cnt

            if maxArea:
                cursorCoord = (100000, 100000)  # Just a number much larger than any video dimension
                for vert in maxCnt:
                    if vert[0][0] <= cursorCoord[0] and vert[0][1] <= cursorCoord[1]:
                        cursorCoord = (vert[0][0]-1, vert[0][1]-3)
                cursorFile.write(str(cursorCoord[0]) + " " + str(cursorCoord[1]) + "\n")

        if not maxArea or not contours:
            cursorFile.write("-1 -1\n")

    cursorFile.close()


# Returns an array of tuples with the list of all cursor positions in the video
def getCursorPosList():
    cursorPosList = []

    with open("./resources/cursor.txt", "r") as cursorFile:
        line = cursorFile.readline()
        while line:
            tmp = line.split(' ')
            cursorPosList.append( (int(tmp[0]), int(tmp[1])) )
            line = cursorFile.readline()

    return cursorPosList
