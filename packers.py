from coordinate import Coordinate

class PackersGame():
    BORDER = "#"
    POINT = "o"
    PLAYER = "P"
    ENEMY = "E"
    BLANK = "-"
    DEATH = "X"
    LEFT = "a"
    RIGHT = "d"
    UP = "w"
    DOWN = "s"
    CARDINAL_DIRECTIONS = {LEFT, RIGHT, UP, DOWN}
    CARDINAL_DIRECTION_MODIFIERS = {
        LEFT: Coordinate(-1, 0),
        RIGHT: Coordinate(1, 0),
        UP: Coordinate(0, -1),
        DOWN: Coordinate(0, 1)
    }


    def __init__(self, levelFileName, enemyTimestepMove=2):
        self.enemyTimestepMove = enemyTimestepMove
        self.playerCoordinate = None
        self.enemyCoordinate = None # TODO: for now, only one enemy may exist
        self.pointCoordinates = set()
        self.borderCoordinates = set()
        # self.width = None
        # self.height = None
        # self.packersAI = None
        self.timestep = 0
        self.board = []
        self.initializeState(levelFileName)

    def setAI(self, packersAI):
        self.packersAI = packersAI

    def initializeState(self, levelFileName):
        with open(levelFileName) as f:
            lines = f.readlines()
            self.width = len(lines[0].rstrip())  # assume all rows are the same length as the first
            self.height = len(lines)

            for i in range(len(lines)):
                currentRow = []
                self.board.append(currentRow)

                for j in range(self.width):
                    itemToAdd = None
                    
                    match lines[i][j]:
                        case PackersGame.PLAYER if not self.playerCoordinate:  # can only have one player
                            self.playerCoordinate = Coordinate(j, i)
                            itemToAdd = PackersGame.PLAYER
                        case PackersGame.ENEMY if not self.enemyCoordinate:  # TODO: can only have one enemy for now
                            self.enemyCoordinate = Coordinate(j, i)
                            itemToAdd = PackersGame.ENEMY
                        case PackersGame.POINT:
                            self.pointCoordinates.add(Coordinate(j, i))
                            itemToAdd = PackersGame.POINT
                        case PackersGame.BORDER:
                            self.borderCoordinates.add(Coordinate(j, i))
                            itemToAdd = PackersGame.BORDER
                        case _:
                            itemToAdd = PackersGame.BLANK

                    currentRow.append(itemToAdd)

    @classmethod
    def availableActions(cls, board, coordinate):
        width = len(board[0])
        height = len(board)

        actionableCoordinates = coordinate.getCoordinatesInProximity()
        actionsToRemove = set()

        for ac in actionableCoordinates:
            x = ac.getX()
            y = ac.getY()

            # NOTE: this last clause here is bad encapsulation. This whole method is bad encapsulation.
            if not (0 <= x and x < width) or not (0 <= y and y < height) or (board[y][x] == PackersGame.BORDER):
                actionsToRemove.add(ac)
        
        for ac in actionsToRemove:
            actionableCoordinates.remove(ac)
        
        return actionableCoordinates

    def availablePlayerActions(self):
        return self.availableActions(self.board, self.playerCoordinate)
    
    def incrementTimestep(self, cardinalDirection):
        self.timestep += 1
        self.move(cardinalDirection)
        return self.gameOver()

    def move(self, cardinalDirection):
        oldPlayerCoord = self.playerCoordinate
        
        if cardinalDirection in PackersGame.CARDINAL_DIRECTIONS:
            newPlayerCoord = oldPlayerCoord + self.CARDINAL_DIRECTION_MODIFIERS[cardinalDirection]

            # if the action is valid, move. Otherwise, do nothing.
            if newPlayerCoord in self.availablePlayerActions():
                self.updateBoardPlayerMove(oldPlayerCoord, newPlayerCoord, PackersGame.PLAYER)
                self.playerCoordinate = newPlayerCoord

        # enemyTimestepMove determines how often the enemy gets to move
        if (self.timestep % self.enemyTimestepMove) == 0:

            # first, check if player went on this space
            if self.isPlayerDead():
                return

            # Enemy only chases coordination of player one timestep ago, not where they just moved
            newEnemyCoord = self.packersAI.selectMove(self.board, oldPlayerCoord, self.enemyCoordinate)
            self.updateBoardEnemyMove(self.enemyCoordinate, newEnemyCoord, self.ENEMY)
            self.enemyCoordinate = newEnemyCoord

    def isPlayerDead(self):
        if self.playerCoordinate == self.enemyCoordinate:
            self.updateSpot(self.playerCoordinate, PackersGame.DEATH)
            return True
        return False

    def gameOver(self):
        # Check if player's dead
        if self.isPlayerDead():
            return False

        # Otherwise, check if player got a point
        if self.playerCoordinate in self.pointCoordinates:
            self.pointCoordinates.remove(self.playerCoordinate)
            
            # Check if player got all points
            if not self.pointCoordinates:
                return True
            
        return None # explicitly return None if game is ongoing

    def updateBoardPlayerMove(self, oldCoord, newCoord, item):
        self.updateSpot(oldCoord, PackersGame.BLANK)
        self.updateSpot(newCoord, item)

    def updateBoardEnemyMove(self, oldCoord, newCoord, item):
        if oldCoord in self.pointCoordinates:
            self.updateSpot(oldCoord, PackersGame.POINT)
        else:
            self.updateSpot(oldCoord, PackersGame.BLANK)
        self.updateSpot(newCoord, item)

    def updateSpot(self, coord, item):
        zeroIndex, oneIndex = coord.get2DMatrixEquivalent()
        self.board[zeroIndex][oneIndex] = item

    def displayBoard(self):
        print()
        for row in self.board:
            for item in row:
                print(item, end=" ")
            print()
