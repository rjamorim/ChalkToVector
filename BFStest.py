import numpy as np
import cv2
import cv

pixelThreshold = 30

# add neighbors of the pixel at location 'pt' to the BFS queue
def addNB(img, pt, queue, level):
    if pt[0] + 1 < len(img):
        if img[pt[1], pt[0] + 1] > pixelThreshold:
            queue.append((pt[0], pt[1] + 1, level))
    if pt[1] + 1 < len(img[0]):
        if img[pt[1] + 1, pt[0]] > pixelThreshold:
            queue.append((pt[0] + 1, pt[1], level))
    if pt[0] - 1 > -1:
        if img[pt[1], pt[0] - 1] > pixelThreshold:
            queue.append((pt[0], pt[1] - 1, level))
    if pt[1] - 1 > -1:
        if img[pt[1] - 1, pt[0]] > pixelThreshold:
            queue.append((pt[0] - 1, pt[1], level))

# paths of the images we will use for testing
pathX = "resources/x.png"
pathM = "resources/m.png"
path2 = "resources/2.png"

# hardcoded BFS starting pixel locations
startX = (39,27)
startM = (0,0)
start2 = (0,0)

start = startX

testImg = cv2.imread(pathX)

result = np.zeros(testImg.shape, testImg.dtype)

testImg = cv2.cvtColor(testImg,cv.CV_RGB2GRAY)

BFSqueue = []

BFSexploredPixels = []

BFSlevel = 1

# add first neighbors to the BFS queue
addNB(testImg, startX, BFSqueue, BFSlevel)

print len(BFSqueue)

while BFSqueue:
    pixelToExplore = BFSqueue[0][0:2]
    BFSqueue.pop(0)

    if pixelToExplore in BFSexploredPixels:
        continue
    else:
        BFSexploredPixels.append(pixelToExplore)
        BFSlevel += 1
        addNB(testImg, pixelToExplore, BFSqueue, BFSlevel)
        drawPt = (pixelToExplore[0], pixelToExplore[1])
        cv2.ellipse(result, drawPt, (1,1), 0, 0, 0, (12,57,255))


# display the point where we start our BFS from using a bright pixel
cv2.ellipse(testImg, startX, (1,1), 0, 0, 0, (255,255,255))

newSize = (int(testImg.shape[1] * 16), int(testImg.shape[0] * 16))
testImg = cv2.resize(testImg, newSize, interpolation=cv2.INTER_NEAREST)
result = cv2.resize(result, newSize, interpolation=cv2.INTER_NEAREST)

while cv2.waitKey(250) != 27:
    cv2.imshow("x image", testImg)
    cv2.imshow("BFS result", result)
