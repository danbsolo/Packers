import sys

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
        LEFT: (-1, 0),
        RIGHT: (1, 0),
        UP: (0, -1),
        DOWN: (0, 1)
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
                            self.playerCoord = (i, j)
                            itemToAdd = self.PLAYER
                        case self.ENEMY:
                            self.enemyCoord = (i, j)
                            itemToAdd = self.ENEMY
                        case _:
                            itemToAdd = self.BLANK

                    currentRow.append(itemToAdd)
    
    def availableActions(self, coordinate):
        x, y = coordinate
        actions = set()

        # can move in the four cardinal directions, assuming there's space
        for actionableX in (x-1, x+1):
            if not (0 <= actionableX and actionableX < self.height):
                continue
            actions.add((actionableX, y))

        for actionableY in (y-1, y+1):
            if not (0 <= actionableY and actionableY < self.width):
                continue
            actions.add((x, actionableY))
                
        return actions
    
    def availablePlayerActions(self):
        return self.availableActions(self.playerCoord)
    

    def move(self, cardinalDirection):
        yModifier, xModifier = self.CARDINAL_DIRECTION_MODIFIERS[cardinalDirection]
        newCoord = (self.playerCoord[0] + xModifier, self.playerCoord[1] + yModifier)

        if newCoord not in self.availablePlayerActions():
            return False # i.e. Don't move.
        
        oldCoord = self.playerCoord
        self.playerCoord = newCoord

        self.board[oldCoord[0]][oldCoord[1]] = self.BLANK
        self.board[newCoord[0]][newCoord[1]] = self.PLAYER
        
        # TODO: Have AI make a move from here

        return True


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
            pg.move(playerMove)
            pg.displayBoard()


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python packers.py <<filepath>>")
    playTerminal(sys.argv[1])

if __name__ == "__main__":
    main()