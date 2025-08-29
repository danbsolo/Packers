from game import PackersGame
import math
import random
from abc import ABC, abstractmethod
from queue import Queue


class Node():
    def __init__(self, parent, action):
        # For this problem, the "state" and the "action" are one and the same
        self.parent = parent
        self.action = action

    def getAction(self):
        return self.action
    
    def getParent(self):
        return self.parent


class QueueFrontier():
    def __init__(self):
        self.frontier = Queue(0)

    def add(self, node):
        self.frontier.put(node)

    def containsActionableCoordinate(self, actionableCoordinate): 
        # Imperfect way of checking membership because it accesses its structure under-the-hood
        for node in self.frontier.queue:
            if node.getAction() == actionableCoordinate:
                return True
        return False

    def empty(self):
        return self.frontier.empty()
    
    def remove(self):
        if self.empty():
            raise Exception("Empty frontier.")
        else:
            return self.frontier.get()


class StackFrontier(QueueFrontier):
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def containsActionableCoordinate(self, actionableCoordinate):
        for node in self.frontier:
            if node.getAction() == actionableCoordinate:
                return True
        return False

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("Empty frontier.")
        else:
            # or just >>> node = self.frontier.pop()
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class NodeStar(Node):
    def __init__(self, parent, action, gValue):
        super().__init__(parent, action)
        self.gValue = gValue
    
    def getGValue(self):
        return self.gValue

    def getHValue(self):
        return self.hValue

    def getFValue(self):
        return self.gValue + self.hValue

    def setHValue(self, hValue):
        self.hValue = hValue

    def setGValue(self, gValue):
        self.gValue = gValue
    
    def setParent(self, newParent):
        self.parent = newParent


class FrontierStar():
    def __init__(self, startNode, targetCoord):
        self.startNode = startNode
        self.targetCoord = targetCoord
        self.openList = []
        self.closedList = []
        self.addNodeStar(startNode)
    
    def addNodeStar(self, nodeStar):
        # set its hValue
        nodeStar.setHValue(nodeStar.getAction().distance(self.targetCoord))
        
        # TODO: add to openList in descending order **IN AN EFFICIENT MANNER**
        # TODO: For now, we're just appending it, and then sorting it by its fValue
        self.openList.append(nodeStar)
        self.openList = sorted(self.openList, key= lambda ns: ns.getFValue(), reverse=True)

    def getLowestFValueNodeStar(self):
        if not self.isOpenListEmpty():
            ns = self.openList.pop()
            self.closedList.append(ns)
            return ns

    def isOpenListEmpty(self):
        return len(self.openList) == 0
    
    # TODO: Optimize these two methods below to be less redundant with each other
    def openListContainsActionableCoordinate(self, actionableCoordinate):
        for ns in self.openList:
            if ns.getAction() == actionableCoordinate:
                return True
        return False
    
    def getNodeStarWithActionableCoordinateInOpenList(self, actionableCoordinate):
        for ns in self.openList:
            if ns.getAction() == actionableCoordinate:
                return ns
        return None

    def closedListContainsActionableCoordinate(self, actionableCoordinate):
        for ns in self.closedList:
            if ns.getAction() == actionableCoordinate:
                return True
        return False
        #return any(ns.getAction() == actionableCoordinate for ns in self.closedList)
    
    def updateNodeStarGValue(self, nodeStar, parent, gValue):
        self.openList.remove(nodeStar)
        nodeStar.setParent(parent)
        nodeStar.setGValue(gValue)
        self.addNodeStar(nodeStar)
