import numpy as np
import cv2
import cv

pixelThreshold = 80
imgScaling = 16

# add neighbors of the pixel at location 'pt' to the BFS queue
def addNB(img, pt, queue, level):
    if pt[0] + 1 < len(img):
        queue.append((pt[0], pt[1] + 1, level))
    if pt[1] + 1 < len(img[0]):
        queue.append((pt[0] + 1, pt[1], level))
    if pt[0] - 1 > -1:
        queue.append((pt[0], pt[1] - 1, level))
    if pt[1] - 1 > -1:
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

BFSexploredPixelLevels = []

# add first neighbors to the BFS queue
addNB(testImg, startX, BFSqueue, 1)

while BFSqueue:
    pixelToExplore = BFSqueue[0][0:2]
    level = BFSqueue[0][2]
    BFSqueue.pop(0)

    if pixelToExplore in BFSexploredPixels:
        continue

    if testImg[pixelToExplore[1], pixelToExplore[0]] < pixelThreshold:
        continue

    level += 1
    addNB(testImg, pixelToExplore, BFSqueue, level)

    BFSexploredPixels.append(pixelToExplore)

    if len(BFSexploredPixelLevels) < level:
        BFSexploredPixelLevels.append([(pixelToExplore[0], pixelToExplore[1],level)])
    else:
        BFSexploredPixelLevels[-1].append((pixelToExplore[0], pixelToExplore[1],level))

    drawPt = (pixelToExplore[0], pixelToExplore[1])
    cv2.ellipse(result, drawPt, (1, 1), 0, 0, 0, (12, 100, 9*level))


# display the point where we start our BFS from using a bright pixel
# cv2.circle(testImg, startX, 1, (255,255,255))

newSize = (int(testImg.shape[1] * imgScaling), int(testImg.shape[0] * imgScaling))
# testImg = cv2.resize(testImg, newSize, interpolation=cv2.INTER_NEAREST)
result = cv2.resize(result, newSize, interpolation=cv2.INTER_NEAREST)


for pts in BFSexploredPixelLevels:
    centerOfMass = [0,0]
    w = 0.0
    for pt in pts:
        w += testImg[pt[1], pt[0]]
        centerOfMass[0] += pt[0] * testImg[pt[1], pt[0]]
        centerOfMass[1] += pt[1] * testImg[pt[1], pt[0]]
    print w
    centerOfMass[0] /= w
    centerOfMass[1] /= w
    centerOfMass[0] = centerOfMass[0] * imgScaling + imgScaling * 1.5
    centerOfMass[1] = centerOfMass[1] * imgScaling + imgScaling * 0.5

    cv2.circle(result, ( int(centerOfMass[0]), int(centerOfMass[1]) ), 1, (255, 255, 255), 3, cv.CV_AA)


while cv2.waitKey(100) != 27:
    cv2.imshow("x image", testImg)
    cv2.imshow("BFS result", result)
