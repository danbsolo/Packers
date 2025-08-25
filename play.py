import sys
from packers import PackersGame
from packersAI import *


def playTerminal(levelFileName):
    pg = PackersGame(levelFileName)
    pgAI = RandomAI(pg.board)  # change AI here
    pg.setAI(pgAI)

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
