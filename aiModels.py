
from aiModelsHeader import *


class PackersAI(ABC):
    def __init__(self, packersGame):
        self.game = packersGame
        self.gameBoard = self.game.board
        self.game.setAI(self)
        self.trainAI()

    def trainAI(self):
        pass

    @abstractmethod
    def selectMove(self, targetCoord, startCoord):
        pass


class RandomAI(PackersAI):
    def __init__(self, game):
        super().__init__(game)

    def selectMove(self, _, startCoord):
        return random.choice(self.game.availableActions(startCoord))


class ManhattanDistanceAI(PackersAI):
    def __init__(self, game):
        super().__init__(game)

    def selectMove(self, targetCoord, startCoord):
        actionableCoordinates = self.game.availableActions(startCoord)
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
    def __init__(self, game):
        super().__init__(game)
        self.lastTargetCoord = None
        self.lastTargetCoordNode = None

    def commenceSearch(self, targetCoord, startCoord, FrontierClass):
        startNode = Node(parent=None, action=startCoord)
        frontier = FrontierClass()
        frontier.add(startNode)
        explored = set()

        # if the player hasn't moved, the lastTargetCoord and current targetCoord will equal.
        # therefore, do not re-search. Use what's already been done
        if self.lastTargetCoord and self.lastTargetCoord == targetCoord:
            currentNode = self.lastTargetCoordNode

            while True:
                if currentNode.getParent().getAction() == startCoord:
                    return currentNode.getAction()
                else:
                    currentNode = currentNode.getParent()

        self.lastTargetCoord = targetCoord

        while True:
            if frontier.empty():
                return startCoord  # If no path is possible, stay still
            
            currentNode = frontier.remove()

            if currentNode.getAction() == targetCoord:
                self.lastTargetCoordNode = currentNode

                while True:
                    if currentNode.getParent().getAction() == startCoord:
                        return currentNode.getAction()
                    else:
                        currentNode = currentNode.getParent()

            explored.add(currentNode.getAction())
            
            actionableCoordinates = list(self.game.availableActions(currentNode.getAction()))
            random.shuffle(actionableCoordinates)

            for ac in actionableCoordinates:
                if ac not in explored and not frontier.containsAction(ac):
                    frontier.add(Node(currentNode, ac))


class BreadthFirstSearchAI(SearchAI):
    def __init__(self, game):
        super().__init__(game)

    def selectMove(self, targetCoord, startCoord):
        return self.commenceSearch(targetCoord, startCoord, QueueFrontier)
    

class DepthFirstSearchAI(SearchAI):
    def __init__(self, game):
        super().__init__(game)

    def selectMove(self, targetCoord, startCoord):
        return self.commenceSearch(targetCoord, startCoord, StackFrontier)


class AStarSearchAI(PackersAI):
    def __init__(self, game):
        #super().__init__(game)
        raise NotImplementedError

    def selectMove(self, targetCoord, startCoord):
        pass


class MiniMaxAI(PackersAI):
    def __init__(self, game):
        #super().__init__(game)
        raise NotImplementedError

    def selectMove(self, targetCoord, startCoord):
        pass


class QLearningManualAI(PackersAI):
    def __init__(self, game):
        #super().__init__(game)
        raise NotImplementedError

    def selectMove(self, targetCoord, startCoord):
        pass

class QLearningTensorFlowKerasAI(PackersAI):
    def __init__(self, game):
        #super().__init__(game)
        raise NotImplementedError

    def selectMove(self, targetCoord, startCoord):
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
