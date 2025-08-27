from packers import PackersGame
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

    def containsAction(self, action): 
        # Imperfect way of checking membership because it accesses its structure under-the-hood
        for node in self.frontier.queue:
            if node.getAction() == action:
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

    def containsAction(self, action):
        for node in self.frontier:
            if node.getAction() == action:
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
