import math
from packers import PackersGame
import random
from abc import ABC, abstractmethod


class PackersAI(ABC):
    def __init__(self, initialBoard):
        self.initialBoard = initialBoard
        self.trainAI()

    def trainAI(self):
        pass

    @abstractmethod
    def selectMove(self, currentBoard, targetCoord, startCoord):
        pass


class RandomAI(PackersAI):
    def __init__(self, initialBoard):
        super().__init__(initialBoard)

    def selectMove(self, currentBoard, _, startCoord):
        return random.choice(PackersGame.availableActions(currentBoard, startCoord))


class ManhattanDistanceAI(PackersAI):
    def __init__(self, initialBoard):
        super().__init__(initialBoard)

    def selectMove(self, currentBoard, targetCoord, startCoord):
        actionableCoordinates = PackersGame.availableActions(currentBoard, startCoord)
        shortestDistance = math.inf
        shortestDistanceACs = []

        for ac in actionableCoordinates:
            currentDistance = ac.distance(targetCoord)

            if currentDistance < shortestDistance:
                shortestDistance = currentDistance
                shortestDistanceACs.clear()
                shortestDistanceACs.append(ac)
            elif currentDistance == shortestDistance:
                shortestDistanceACs.append(ac)

        return random.choice(shortestDistanceACs)


class BreadthFirstSearchAI(PackersAI):
    def __init__(self, initialBoard):
        #super().__init__(initialBoard)
        raise NotImplementedError

    def selectMove(self, currentBoard, targetCoord, startCoord):
        pass


class MiniMaxAI(PackersAI):
    def __init__(self, initialBoard):
        #super().__init__(initialBoard)
        raise NotImplementedError

    def selectMove(self, currentBoard, targetCoord, startCoord):
        pass


class MachineLearningAI(PackersAI):
    def __init__(self, initialBoard):
        #super().__init__(initialBoard)
        raise NotImplementedError

    def selectMove(self, currentBoard, targetCoord, startCoord):
        pass


PACKER_AI_CLASSES = [
    RandomAI,
    ManhattanDistanceAI,
    BreadthFirstSearchAI,
    MiniMaxAI,
    MachineLearningAI
]
