
# squared eclidian distance between two points
def pixelSqDist(pt1, pt2):
    return (pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2

class StrokeNode:
    def __init__(self, initialCluster, ID, type=0):
        self.clusters = [initialCluster]
        self.coms = []
        self.children = []
        self.ID = ID
        self.type = type
        self.expansionIntention = []

    def addCluster(self, cluster):
        self.clusters.append(cluster)

    def printMe(self):
        print self.ID, self.clusters
        for child in self.children:
            child.printMe()

class StrokeGraph:
    def __init__(self, firstNode):
        self.root = firstNode
        self.frontier = [firstNode]
        self.nNodes = 1

    def addClusters(self, clusters):

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

        for frontierNode in self.frontier:
            nIntentions = len(frontierNode.expansionIntention)

            if nIntentions == 0:
                self.frontier.remove(frontierNode)

            elif nIntentions == 1:
                frontierNode.addCluster(frontierNode.expansionIntention[0])

            else:
                for cluster in frontierNode.expansionIntention:
                    newNode = StrokeNode(cluster, self.nNodes)
                    self.nNodes += 1
                    frontierNode.children.append(newNode)
                    self.frontier.append(newNode)

                self.frontier.remove(frontierNode)


