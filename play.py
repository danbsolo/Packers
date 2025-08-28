import sys
from game import PackersGame
import aiModels



def playTerminal(levelFileName, selectedAIIndex=None):
    pg = PackersGame(levelFileName)

    # if command-line argument was not specified, ask for one
    if not selectedAIIndex:
        print("Packer AIs:")
        for i in range(len(aiModels.PACKER_AI_CLASSES)):
            print(f"\t{i} - {aiModels.PACKER_AI_CLASSES[i].__name__}")
        selectedAIIndex = input("Select an AI: ")

    # check for proper input
    try: selectedAIIndex = int(selectedAIIndex)
    except: return  # i.e. Quit
    if not (0 <= selectedAIIndex and selectedAIIndex < len(aiModels.PACKER_AI_CLASSES)): return

    aiModels.PACKER_AI_CLASSES[selectedAIIndex](pg)  # change AI here

    print(f"Using {aiModels.PACKER_AI_CLASSES[selectedAIIndex].__name__}")
    pg.displayBoard()
    while True:
        playerMove = input("Next move?: ").lower()

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
