import math
from packers import PackersGame
import random
from abc import ABC, abstractmethod


class PackersAI(ABC):
    def __init__(self, board):
        self.originalBoard = board
        self.width = len(board[0])
        self.height = len(board)
        self.trainAI()

    def trainAI(self):
        return

    @abstractmethod
    def selectMove(self, targetCoord, startCoord):
        return


class RandomAI(PackersAI):
    def __init__(self, board):
        super().__init__(board)

    def selectMove(self, targetCoord, startCoord):
        return random.choice(PackersGame.availableActionsClassMethod(startCoord, self.width, self.height))


class ManhattanDistanceAI(PackersAI):
    def __init__(self, board):
        super().__init__(board)

    def selectMove(self, targetCoord, startCoord):
        actionableCoordinates = PackersGame.availableActionsClassMethod(startCoord, self.width, self.height)
        shortestDistance = math.inf
        shortestDistanceAC = None

        for ac in actionableCoordinates:
            currentDistance = ac.distance(targetCoord)

            if currentDistance < shortestDistance:
                shortestDistance = currentDistance
                shortestDistanceAC = ac
        
        return shortestDistanceAC
