import numpy as np
import cv2
import cv
from datastructs import *

pixelThreshold = 100
imgScaling = 16

# add neighbors of the pixel at location 'pt' to the BFS queue
def addNB(img, pt, queue, level):
    if pt[0] + 1 < len(img):
        queue.append([pt[0], pt[1] + 1, level])
    if pt[1] + 1 < len(img[0]):
        queue.append([pt[0] + 1, pt[1], level])
    if pt[0] - 1 > -1:
        queue.append([pt[0], pt[1] - 1, level])
    if pt[1] - 1 > -1:
        queue.append([pt[0] - 1, pt[1], level])

# paths of the images we will use for testing
pathX = "resources/x.png"
pathM = "resources/m.png"
path2 = "resources/2.png"

# hardcoded BFS starting pixel locations
startX = (39,27)
startM = (0,0)
start2 = (0,0)

# hardcoded cursor paths
cursorPathX = [(39,27), (39,25), (44,28), (45,37), (48,40), (48,28), (49,25)]
cursorPath2 = [(39,27), (39,25), (44,28), (45,37), (48,40), (48,28), (49,25)]

cursorPath = cursorPath2
start = start2
testImg = cv2.imread(path2)
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

    BFSexploredPixels.append(pixelToExplore)

    if len(BFSexploredPixelLevels) < level:
        BFSexploredPixelLevels.append([[pixelToExplore[0], pixelToExplore[1], level]])
    else:
        BFSexploredPixelLevels[-1].append([pixelToExplore[0], pixelToExplore[1], level])

    level += 1
    addNB(testImg, pixelToExplore, BFSqueue, level)

    drawPt = (pixelToExplore[0], pixelToExplore[1])
    cv2.ellipse(result, drawPt, (1, 1), 0, 0, 0, (12, 100, 9*level))


newSize = (int(testImg.shape[1] * imgScaling), int(testImg.shape[0] * imgScaling))
testImg = cv2.resize(testImg, newSize, interpolation=cv2.INTER_NEAREST)
result = cv2.resize(result, newSize, interpolation=cv2.INTER_NEAREST)

# display the point where we start our BFS from using a bright pixel
cv2.circle(testImg, (start[0]*imgScaling, start[1]*imgScaling), 1, (255,255,255))
# lastPt = cursorPath[0]
# for pt in cursorPath[1:]:
#     cv2.line(result, (int(lastPt[0] * imgScaling + imgScaling * 1.5), int(lastPt[1] * imgScaling + imgScaling * 0.5)),
#              (int(pt[0] * imgScaling + imgScaling * 1.5), int(pt[1] * imgScaling + imgScaling * 0.5)), (255,0,0), 2, cv.CV_AA)
#     lastPt = pt

# centersOfMass = []
# group = 0
# cmClusters = [[[startX[0], startX[1], 0, group]]]
# # pixelClusters = cmClusters[:]
#
# strokeGraph = StrokeGraph(StrokeNode(cmClusters[0], cmClusters[0], 0))
#
# # print BFSexploredPixelLevels
# for pts in BFSexploredPixelLevels:
#     clusters = [[pt + [group]] for pt in pts]
#     for cluster in clusters:
#         otherClusters = clusters[:]
#         otherClusters.remove(cluster)
#         for otherCluster in otherClusters:
#             shouldJoin = False
#             for pt1 in cluster:
#                 for pt2 in otherCluster:
#                     if pixelSqDist(pt1, pt2) < 3:
#                         shouldJoin = True
#                         break
#                 if shouldJoin: break
#
#             if shouldJoin:
#                 cluster.extend(otherCluster)
#                 clusters.remove(otherCluster)
#
#     # done generating this level's clusters
#     # now join them with those from the previous level
#
#     levelCentersOfMass = []
#
#     # print len(clusters), clusters
#     for pathPtIdx in range(len(clusters)):
#         cluster = clusters[pathPtIdx]
#         # print cluster
#
#         centerOfMass = [0, 0]
#         w = 0.0
#
#         for pt in cluster:
#             w += testImg[pt[1], pt[0]]
#             centerOfMass[0] += pt[0] * testImg[pt[1], pt[0]]
#             centerOfMass[1] += pt[1] * testImg[pt[1], pt[0]]
#
#         centerOfMass[0] /= w
#         centerOfMass[1] /= w
#
#         levelCentersOfMass.append( [centerOfMass[0], centerOfMass[1], cluster[0][2]] )
#         centersOfMass.append( [centerOfMass[0], centerOfMass[1], cluster[0][2]] )
#
#         centerOfMass[0] = centerOfMass[0] * imgScaling + imgScaling * 1.5
#         centerOfMass[1] = centerOfMass[1] * imgScaling + imgScaling * 0.5
#
#         # cv2.circle(result, (int(centerOfMass[0]), int(centerOfMass[1])), 1, (9 * pts[0][2], 9 * pts[0][2], 9 * pts[0][2]), 4, cv.CV_AA)
#
#     strokeGraph.addClusters(clusters, levelCentersOfMass)
#
#     cmClusters.append(levelCentersOfMass)
#
# strokeGraph.root.printMe()
# strokeGraph.root.drawMe(result)
# # print len(centersOfMass)
#
# closestMatches = [[10000,0] for pathPtIdx in cursorPath]
# for ptIdx in range(len(centersOfMass)):
#     pt = centersOfMass[ptIdx]
#     for pathPtIdx in range(len(cursorPath)):
#         pathPt = cursorPath[pathPtIdx]
#         dist = pixelSqDist(pathPt, pt)
#         if dist < closestMatches[pathPtIdx][0]:
#             closestMatches[pathPtIdx][1] = ptIdx
#             closestMatches[pathPtIdx][0] = dist
#
# finalPath = strokeGraph.root.centersOfMass[:]
# pathNodes = [strokeGraph.root]
#
# for cMatch in closestMatches[:]:
#     cMatch = centersOfMass[cMatch[1]]
#     if cMatch in pathNodes[-1].centersOfMass:
#         continue
#
#     if not pathNodes[-1].children:
#         found = False
#         for child in pathNodes[-1].parent.children:
#             if cMatch in child.centersOfMass:
#                 finalPath.extend(reversed(pathNodes[-1].centersOfMass))
#                 finalPath.extend(child.centersOfMass)
#                 pathNodes.append(child)
#                 found = True
#                 break
#
#         if not found:
#             for child in pathNodes[-1].parent.parent.children:
#                 if cMatch in child.centersOfMass:
#                     finalPath.extend(reversed(pathNodes[-1].centersOfMass))
#                     finalPath.extend(reversed(pathNodes[-1].parent.centersOfMass))
#                     finalPath.extend(child.centersOfMass)
#                     pathNodes.append(child)
#                     found = True
#                     break
#
#
#     found = False
#     for child in pathNodes[-1].children:
#         if cMatch in child.centersOfMass:
#             pathNodes.append(child)
#             finalPath.append(child.centersOfMass)
#             found = True
#             break
#
#     if not found:
#         for child in pathNodes[-1].children:
#             for cchild in child.children:
#                 if cMatch in cchild.centersOfMass:
#                     pathNodes.append(child)
#                     pathNodes.append(cchild)
#                     finalPath.extend(child.centersOfMass)
#                     finalPath.extend(cchild.centersOfMass)
#                     found = True
#                     break
#             if found: break
#
# nodesMissing = []
#
# for node in strokeGraph.nodes:
#     if not (node in pathNodes):
#         nodesMissing.append(node)
#
# for missingNode in nodesMissing:
#     insertionPoint = pathNodes.index(missingNode.parent) + 1
#
#     pathNodes.insert(insertionPoint, missingNode)
#
#     insertionIdx = 0
#
#     for i in range(insertionPoint):
#         insertionIdx += len(pathNodes[i].centersOfMass)
#
#     finalPath[insertionIdx:insertionIdx] = missingNode.centersOfMass + missingNode.centersOfMass[::-1]
#
#
#
# for m in closestMatches:
#     cv2.circle(result, (int(centersOfMass[m[1]][0] * imgScaling + imgScaling * 1.5), int(centersOfMass[m[1]][1] * imgScaling + imgScaling * 0.5)), 8, (255,255,255), 1, cv.CV_AA)
#
# # currentGoal = 1
# # finalGoal = len(cursorPath) - 1
# # pathSegments = [cmClusters[0][0]]
# # pathsTree = [pathSegments, None]
# # pathSplit = []
#
# shiftX = 0
#
# lastPt = finalPath[0]
# for pt in finalPath[1:]:
#     cv2.line(result, (int(lastPt[0] * imgScaling + imgScaling * 1.5) - shiftX, int(lastPt[1] * imgScaling + imgScaling * 0.5)),
#              (int(pt[0] * imgScaling + imgScaling * 1.5) - shiftX, int(pt[1] * imgScaling + imgScaling * 0.5)), (255,255,0), 1, cv.CV_AA)
#     lastPt = pt

while cv2.waitKey(100) != 27:
    cv2.imshow("x image", testImg)
    cv2.imshow("BFS result", result)
