
from aiModelsHeader import *


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


class SearchAI(PackersAI):
    def commenceSearch(self, currentBoard, targetCoord, startCoord, FrontierClass):
        startNode = Node(parent=None, action=startCoord)
        frontier = FrontierClass()
        frontier.add(startNode)
        explored = set()

        while True:
            if frontier.empty():
                return startCoord  # If no path is possible, don't move
            
            currentNode = frontier.remove()

            if currentNode.getAction() == targetCoord:
                while True:
                    if currentNode.parent.getAction() == startCoord:
                        return currentNode.getAction()
                    # elif currentNode.parent is None: # this clause is likely unnecessary
                    #     return currentNode.getAction()
                    else:
                        currentNode = currentNode.parent

            explored.add(currentNode.getAction())

            for ac in PackersGame.availableActions(currentBoard, currentNode.getAction()):
                if ac not in explored and not frontier.containsAction(ac):
                    frontier.add(Node(currentNode, ac))


class BreadthFirstSearchAI(SearchAI):
    def __init__(self, initialBoard):
        super().__init__(initialBoard)

    def selectMove(self, currentBoard, targetCoord, startCoord):
        return self.commenceSearch(currentBoard, targetCoord, startCoord, QueueFrontier)
    

class DepthFirstSearchAI(SearchAI):
    def __init__(self, initialBoard):
        super().__init__(initialBoard)

    def selectMove(self, currentBoard, targetCoord, startCoord):
        return self.commenceSearch(currentBoard, targetCoord, startCoord, StackFrontier)



class AStarSearchAI(PackersAI):
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


class QLearningManualAI(PackersAI):
    def __init__(self, initialBoard):
        #super().__init__(initialBoard)
        raise NotImplementedError

    def selectMove(self, currentBoard, targetCoord, startCoord):
        pass

class QLearningTensorFlowKerasAI(PackersAI):
    def __init__(self, initialBoard):
        #super().__init__(initialBoard)
        raise NotImplementedError

    def selectMove(self, currentBoard, targetCoord, startCoord):
        pass


PACKER_AI_CLASSES = [
    RandomAI,
    ManhattanDistanceAI,
    DepthFirstSearchAI,
    BreadthFirstSearchAI,
    AStarSearchAI,
    MiniMaxAI,
    QLearningManualAI,
    QLearningTensorFlowKerasAI
]
