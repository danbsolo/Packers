import sys
from coordinate import Coordinate
import random

class PackersGame():
    #BORDER = "#"
    #POINT = "•"
    PLAYER = "P"
    ENEMY = "E"
    BLANK = "-"
    DEAD = "X"
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


    def __init__(self, levelFileName):
        self.levelFileName = levelFileName

        self.playerCoord = None
        self.enemyCoord = None # TODO: for now, only one enemy may exist

        self.width = None
        self.height = None
        
        self.packAI = None

        self.timestep = 0

        self.board = []
        self.createBoard()
        self.initializeAI()


    def initializeAI(self):
        self.packAI = PackersAI(self.board)


    def createBoard(self):
        with open(self.levelFileName) as f:
            lines = f.readlines()
            # assume all rows are the same length as the first
            self.width = len(lines[0].rstrip())
            self.height = len(lines)

            for i in range(len(lines)):
                currentRow = []
                self.board.append(currentRow)

                for j in range(self.width):
                    itemToAdd = None
                    
                    match lines[i][j]:
                        case self.PLAYER if not self.playerCoord:  # can only have one player
                            self.playerCoord = Coordinate(j, i)
                            itemToAdd = self.PLAYER
                        case self.ENEMY:
                            self.enemyCoord = Coordinate(j, i)
                            itemToAdd = self.ENEMY
                        case _:
                            itemToAdd = self.BLANK

                    currentRow.append(itemToAdd)
    
    @classmethod
    def availableActionsClassMethod(cls, coordinate, width, height):
        actionableCoordinates = coordinate.getSurroundingCoordinates()
        # TODO: Add current spot as an available action (i.e. standing still)
        actionsToRemove = []

        for ac in actionableCoordinates:
            x = ac.getX()
            y = ac.getY()

            if not (0 <= x and x < width) or not (0 <= y and y < height):
                actionsToRemove.append(ac)
        
        for ac in actionsToRemove:
            actionableCoordinates.remove(ac)
                
        return actionableCoordinates

    def availableActions(self, coordinate):
        return PackersGame.availableActionsClassMethod(coordinate, self.width, self.height)

    def availablePlayerActions(self):
        return self.availableActions(self.playerCoord)



    def move(self, cardinalDirection):
        self.timestep += 1 # TODO: This should be somewhere else, but is okay for now
        
        newPlayerCoord = self.playerCoord + self.CARDINAL_DIRECTION_MODIFIERS[cardinalDirection]

        if newPlayerCoord not in self.availablePlayerActions():
            return False # i.e. Don't move as the action is invalid.
        
        self.updateBoard(self.playerCoord, newPlayerCoord, self.PLAYER)
        self.playerCoord = newPlayerCoord

        # TODO: It's hard-coded that the player is effectively twices as fast as the enemy
        # NOTE: Bug exists in that if a player moves to a space the enemy was just at, their coordinate will show as a blank, even though a player resides there
        if (self.timestep % 2) == 0:
            newEnemyCoord = self.packAI.selectMove(self.board, self.playerCoord, self.enemyCoord)
            self.updateBoard(self.enemyCoord, newEnemyCoord, self.ENEMY)
            self.enemyCoord = newEnemyCoord

        # TODO: Should be somewhere else. Check if game's over.
        if self.playerCoord == self.enemyCoord:
            self.updateSpot(self.playerCoord, PackersGame.DEAD)
            return True
        return False

    def updateBoard(self, oldCoord, newCoord, item):
        self.updateSpot(oldCoord, self.BLANK)
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



class PackersAI():
    def __init__(self, board):
        self.originalBoard = board
        self.width = len(board[0])
        self.height = len(board)
        self.trainAI()

    def trainAI(self):
        pass

    def selectMove(self, currentBoardState, playerCoord, enemyCoord):
        return random.choice(PackersGame.availableActionsClassMethod(enemyCoord, self.width, self.height))


def playTerminal(levelFileName):
    pg = PackersGame(levelFileName)

    pg.displayBoard()
    while True:
        playerMove = input("Next move?:").lower()

        if playerMove == "q":
            break
        elif playerMove in PackersGame.CARDINAL_DIRECTIONS:
            if pg.move(playerMove):
                pg.displayBoard()
                print(">> GAME OVER. YOU LOSE.")
                return
            pg.displayBoard()


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python packers.py <<filepath>>")
    playTerminal(sys.argv[1])

if __name__ == "__main__":
    main()