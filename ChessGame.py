import pygame as p
import ChessEngine
import MinMax as mm

WIDTH = 700
HEIGHT = 700
DIMENSION = 8  # The dimension of a chess board is 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    # Loading the images into IMAGES
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("chess_images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    firstTurn = True
    aiWhite = False
    while True:
        playerchoice = input("Do you want white to be ai or human?\n")
        if playerchoice == "ai":
            aiWhite = True
            break
        elif playerchoice == "human":
            break
        else:
            pass
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves(True)
    moveMade = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gameWon = False
    while running:
        if not gameWon:
            if gs.checkMate:
                gameWon = True
                if not gs.whiteToMove:
                    print("White has won the game")
                else:
                    print("Black has won the game")
            elif (gs.whiteToMove and aiWhite) or (not gs.whiteToMove and not aiWhite):
                print("AI turn")
                ai = mm.MinMax(gs, firstTurn)
                ai.makeMove()
                print("Player Turn")
                if firstTurn:
                    firstTurn = False
                validMoves = gs.getValidMoves(True)
            else:
                for e in p.event.get():
                    if e.type == p.QUIT:
                        running = False
                    elif e.type == p.MOUSEBUTTONDOWN:
                        location = p.mouse.get_pos()
                        col = location[0] // SQ_SIZE
                        row = location[1] // SQ_SIZE
                        if sqSelected == (row, col):
                            # Clears both selected and playerClicks to make sure we move the correct piece if people clicks on the same location twice.
                            sqSelected = ()
                            playerClicks = []
                        else:
                            sqSelected = (row, col)
                            playerClicks.append(sqSelected)  # both first and second click
                        if len(playerClicks) == 2:  # Makes a brick a move is being made
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    gs.makeMove(validMoves[i], True)
                                    moveMade = True
                                    sqSelected = ()
                                    playerClicks = []
                                    break
                            if not moveMade:
                                print("Not valid move")
                                playerClicks = [sqSelected]
                    elif e.type == p.KEYDOWN:
                        if e.key == p.K_z:
                            gs.undoMove()
                            moveMade = True
            if moveMade:
                validMoves = gs.getValidMoves(True)
                moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


'''
Draws he board from the current game state
'''


def drawGameState(screen, gs):
    drawBoard(screen)  # creates the board
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # checks if it's not an empty square
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
