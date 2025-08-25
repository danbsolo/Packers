import sys
from packers import PackersGame
from packersAI import *



def playTerminal(levelFileName, selectedAI=None):
    pg = PackersGame(levelFileName)

    # if command-line argument was not specified, ask for one
    if not selectedAI:
        print("Packer AIs:")        
        for i in range(len(PACKER_AI_CLASSES)):
            print(f"\t{i} - {PACKER_AI_CLASSES[i].__name__}")
        selectedAI = input("Select an AI:")

    # check for proper input
    try: selectedAI = int(selectedAI)
    except: return  # i.e. Quit
    if not (0 <= selectedAI and selectedAI < len(PACKER_AI_CLASSES)): return

    pgAI = PACKER_AI_CLASSES[selectedAI](pg.board)  # change AI here
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
    if len(sys.argv) < 2:
        sys.exit("Usage: python packers.py <<filepath>> <<ai index (optional)>>")
    elif len(sys.argv) == 2:
        playTerminal(sys.argv[1])
    else:
        playTerminal(sys.argv[1], sys.argv[2])
    

if __name__ == "__main__":
    main()
