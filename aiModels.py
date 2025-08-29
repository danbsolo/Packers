
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
        frontier = FrontierClass()
        frontier.add(Node(parent=None, action=startCoord)) # starting node
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
            
            # turn set into a list since sets aren't formally ordered
            actionableCoordinates = list(self.game.availableActions(currentNode.getAction()))
            
            # randomize order so if multiple items are optimal, one is randomly selected
            random.shuffle(actionableCoordinates)

            # sort in ascending order using the manhattan distance heuristic
            actionableCoordinates = self.sortActionableCoordinates(actionableCoordinates, targetCoord)

            for ac in actionableCoordinates:
                if ac not in explored and not frontier.containsActionableCoordinate(ac):
                    frontier.add(Node(currentNode, ac))

    @abstractmethod
    def sortActionableCoordinates(self, actionableCoordinatesList, targetCoord):
        pass


class DepthFirstSearchAI(SearchAI):
    def selectMove(self, targetCoord, startCoord):
        return self.commenceSearch(targetCoord, startCoord, StackFrontier)

    def sortActionableCoordinates(self, actionableCoordinatesList, targetCoord):
        # Sorts in reverse so the closest coord by distance is prioritized in the stack
        return sorted(actionableCoordinatesList, key=lambda ac: ac.distance(targetCoord), reverse=True)


class BreadthFirstSearchAI(SearchAI):
    def selectMove(self, targetCoord, startCoord):
        return self.commenceSearch(targetCoord, startCoord, QueueFrontier)
    
    def sortActionableCoordinates(self, actionableCoordinatesList, targetCoord):
        return sorted(actionableCoordinatesList, key=lambda ac: ac.distance(targetCoord))


# NOTE: Coding it on its own first so I have a good idea of what's going on
class AStarSearchAI(PackersAI):    
    def selectMove(self, targetCoord, startCoord):
        currentGValue = 0
        NodeStar(None, startCoord, currentGValue)
        frontier = FrontierStar(NodeStar(None, startCoord, currentGValue), targetCoord)

        while True:
            # TODO: This is correct, right?
            if frontier.isOpenListEmpty():
                return startCoord
            
            currentNodeStar = frontier.getLowestFValueNodeStar()

            if currentNodeStar.getAction() == targetCoord:
                while True:
                    if currentNodeStar.getParent().getAction() == startCoord:
                        return currentNodeStar.getAction()
                    else:
                        currentNodeStar = currentNodeStar.getParent()

            currentGValue += 1
            for ac in list(self.game.availableActions(currentNodeStar.getAction())):
                if frontier.closedListContainsActionableCoordinate(ac):
                    continue

                elif frontier.openListContainsActionableCoordinate(ac):
                    ns = frontier.getNodeStarWithActionableCoordinateInOpenList(ac)
                    
                    if ns.getGValue() > currentGValue:
                        frontier.updateNodeStar(ns, currentNodeStar, currentGValue)
                
                else:
                    ns = NodeStar(currentNodeStar, ac, currentGValue)
                    frontier.addNodeStar(ns)


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
