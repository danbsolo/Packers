
class PackersGame():
    #BORDER = "#"
    #POINT = "•"
    PLAYER = "P"
    ENEMY = "E"
    BLANK = "-"

    def __init__(self, levelFileName):
        self.levelFileName = levelFileName
        self.playerCoord = None
        self.enemyCoord = None # for now, only one enemy may exist

        self.board = []
        self.createBoard()
        
    def createBoard(self):
        with open(self.levelFileName) as f:
            lines = f.readlines()

            for i in range(len(lines)):
                currentRow = []
                self.board.append(currentRow)

                for j in range(len(lines[i].rstrip())):
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


    def displayBoard(self):
        for row in self.board:
            for item in row:
                print(item, end=" ")
            print()


class PackersAI():
    def __init__(self):
        pass



def main():
    pg = PackersGame("levels/level1.txt")
    pg.displayBoard()

if __name__ == "__main__":
    main()