import math
from packers import PackersGame
import random
from abc import ABC, abstractmethod


class PackersAI(ABC):
    def __init__(self, board):
        self.board = board
        self.width = len(self.board[0])
        self.height = len(self.board)
        self.trainAI()

    def trainAI(self):
        pass

    @abstractmethod
    def selectMove(self, targetCoord, startCoord):
        pass


class RandomAI(PackersAI):
    def __init__(self, board):
        super().__init__(board)

    def selectMove(self, _, startCoord):
        return random.choice(PackersGame.availableActions(startCoord, self.width, self.height))


class ManhattanDistanceAI(PackersAI):
    def __init__(self, board):
        super().__init__(board)

    def selectMove(self, targetCoord, startCoord):
        actionableCoordinates = PackersGame.availableActions(startCoord, self.width, self.height)
        shortestDistance = math.inf
        shortestDistanceAC = None

        # TODO: Pick a random action from the best ones, if there are multiple ones with shortest distance
        for ac in actionableCoordinates:
            currentDistance = ac.distance(targetCoord)

            if currentDistance < shortestDistance:
                shortestDistance = currentDistance
                shortestDistanceAC = ac
        
        return shortestDistanceAC
