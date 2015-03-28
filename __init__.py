import numpy as np
import cv2
import cv

# Get the videoCapture object and set it a bit ahead, so we don't have to wait a lot to start debugging
cap = cv2.VideoCapture("../resources/test.mp4")
cap.set(cv.CV_CAP_PROP_POS_MSEC, 27500)

# Read the first frame to obtain the video dimension
ret, frame = cap.read()

# Buffers we will use throughout our application
frameThresh = np.zeros(frame.shape, np.uint8)

# Main loop
while ( cap.isOpened() and cv2.waitKey(50) != 27 ):
    ret, frame = cap.read()

    # Identifies positions within the frame with color values between 230 and 255 to locate the cursor
    frameThresh = cv2.inRange(frame, (230, 230, 230), (255, 255, 255))

    cv2.imshow('frame', frame)
    cv2.imshow('frameThresh', frameThresh)


cap.release()
cv2.destroyAllWindows()

