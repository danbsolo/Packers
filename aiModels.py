
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


class BreadthFirstSearchAI(PackersAI):
    def __init__(self, initialBoard):
        super().__init__(initialBoard)

    def selectMove(self, currentBoard, targetCoord, startCoord):
        startNode = Node(parent=None, action=startCoord)
        frontier = QueueFrontier()
        frontier.add(startNode)
        explored = []

        while True:
            if frontier.empty():
                return startCoord  # If no path is possible, don't move
            
            node = frontier.remove()
            
            if node.getAction() == targetCoord:
                while True:
                    if node.parent.getAction() == startCoord:
                        return node.getAction()
                    elif node.parent is None: # this clause is likely unnecessary
                        return node.getAction()
                    else:
                        node = node.parent

            explored.append(node.getAction())

            for ac in PackersGame.availableActions(currentBoard, node.getAction()):
                if ac not in explored and not frontier.containsAction(ac):
                    frontier.add(Node(node, ac))



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
    BreadthFirstSearchAI,
    AStarSearchAI,
    MiniMaxAI,
    QLearningManualAI,
    QLearningTensorFlowKerasAI
]
