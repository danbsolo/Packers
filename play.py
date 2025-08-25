import sys
from packers import PackersGame
from packersAI import *


def playTerminal(levelFileName):
    pg = PackersGame(levelFileName)
    pgAI = ManhattanDistanceAI(pg.board)  # change AI here
    pg.setAI(pgAI)

    pg.displayBoard()
    while True:
        playerMove = input("Next move?:").lower()

        if playerMove == "q":
            break
        elif (gameStatus := pg.incrementTimestep(playerMove)) is not None:
            pg.displayBoard()
            
            if gameStatus:
                print(">> YOU WIN. CONGRATS.")
            else:
                print(">> YOU LOSE. GAME OVER.")
            return
        pg.displayBoard()


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python packers.py <<filepath>>")
    playTerminal(sys.argv[1])

if __name__ == "__main__":
    main()
