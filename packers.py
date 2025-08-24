import sys
from coordinate import Coordinate


class PackersGame():
    #BORDER = "#"
    #POINT = "•"
    PLAYER = "P"
    ENEMY = "E"
    BLANK = "-"

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
        self.enemyCoord = None # for now, only one enemy may exist

        self.width = None
        self.height = None
        
        self.ai = None

        self.board = []
        self.createBoard()
    

    def trainAI(self):
        """This is where the AI would get trained on the board.
        For now, we're just initialized the PackersAI object."""
        self.ai = PackersAI()


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
    
    def availableActions(self, coordinate):
        actionableCoordinates = coordinate.getSurroundingCoordinates()
        actionsToRemove = []

        for ac in actionableCoordinates:
            x = ac.getX()
            y = ac.getY()

            if not (0 <= x and x < self.width) or not (0 <= y and y < self.height):
                actionsToRemove.append(ac)
        
        for ac in actionsToRemove:
            actionableCoordinates.remove(ac)
                
        return actionableCoordinates


    def availablePlayerActions(self):
        return self.availableActions(self.playerCoord)


    def move(self, cardinalDirection):
        newCoord = self.playerCoord + self.CARDINAL_DIRECTION_MODIFIERS[cardinalDirection]

        if newCoord not in self.availablePlayerActions():
            return False # i.e. Don't move.
        
        oldCoord = self.playerCoord
        self.playerCoord = newCoord
        self.updateBoard(oldCoord, newCoord, self.PLAYER)
        
        # TODO: Have AI make a move from here

        return True

    def updateBoard(self, oldCoord, newCoord, item):
        zeroIndex, oneIndex = oldCoord.get2DMatrixEquivalent()
        self.board[zeroIndex][oneIndex] = self.BLANK

        zeroIndex, oneIndex = newCoord.get2DMatrixEquivalent()
        self.board[zeroIndex][oneIndex] = item

    def displayBoard(self):
        for row in self.board:
            for item in row:
                print(item, end=" ")
            print()
        print()

class PackersAI():
    def __init__(self):
        pass



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


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python packers.py <<filepath>>")
    playTerminal(sys.argv[1])

if __name__ == "__main__":
    main()