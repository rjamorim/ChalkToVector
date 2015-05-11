import cv2
import cv
import numpy as np

# squared eclidian distance between two points
def pixelSqDist(pt1, pt2):
    return (pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2

class StrokeNode:
    def __init__(self, initialCluster, initialCenterOfMass, ID, type=0):
        self.clusters = [initialCluster]
        self.centersOfMass = initialCenterOfMass
        self.coms = []
        self.children = []
        self.ID = ID
        self.type = type
        self.expansionIntention = []

    def addCluster(self, cluster, centerOfMass):
        self.clusters.append(cluster)
        self.centersOfMass.append(centerOfMass)

    def printMe(self):
        print '\n', self.ID, len(self.centersOfMass), '\n'
        for cm in self.centersOfMass:
            print cm
        for child in self.children:
            child.printMe()

    def drawMe(self, img):
        for cm in self.centersOfMass:
            cv2.waitKey(500)
            cv2.imshow("x image", img)
            cv2.circle(img, ( int(cm[0]*16+24), int(cm[1]*16+8) ), 1, (60*self.ID,60*self.ID,110), 4, cv.CV_AA)


        for child in self.children:
            child.drawMe(img)


class StrokeGraph:
    def __init__(self, firstNode):
        self.root = firstNode
        self.frontier = [firstNode]
        self.nNodes = 1

    def addClusters(self, clusters, centersOfMass):

        for cluster in clusters:
            for frontierNode in self.frontier:
                for pt1 in frontierNode.clusters[-1]: # once per point for every frontier node
                    foundGroup = False
                    for pt2 in cluster: # once per point for every new node
                        if pixelSqDist(pt1, pt2) < 3:
                            frontierNode.expansionIntention.append(cluster)
                            foundGroup = True
                            break
                    if foundGroup: break

        frontierCopy = self.frontier[:]

        for frontierNode in frontierCopy:
            nIntentions = len(frontierNode.expansionIntention)

            if nIntentions == 0:
                self.frontier.remove(frontierNode)

            elif nIntentions == 1:
                frontierNode.addCluster(frontierNode.expansionIntention[0], centersOfMass[clusters.index(frontierNode.expansionIntention[0])])

            else:
                for cluster in frontierNode.expansionIntention:
                    newNode = StrokeNode(cluster, [ centersOfMass[clusters.index(cluster)] ], self.nNodes)
                    self.nNodes += 1
                    frontierNode.children.append(newNode)
                    self.frontier.append(newNode)

                self.frontier.remove(frontierNode)

            frontierNode.expansionIntention = []
