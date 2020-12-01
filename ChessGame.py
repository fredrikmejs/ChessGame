import pygame as p
import ChessEngine
import MinMax as mm


class ChessGame:

    def __init__(self):
        self.WIDTH = 1920
        self.HEIGHT = 1920
        self.DIMENSION = 8  # The dimension of a chess board is 8x8
        self.SQ_SIZE = self.HEIGHT // self.DIMENSION
        self.MAX_FPS = 15
        self.IMAGES = {}
        self.aiWhite = False

    def loadImages(self):
        pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
        # Loading the images into IMAGES
        for piece in pieces:
            self.IMAGES[piece] = p.transform.scale(p.image.load("chess_images/" + piece + ".png"), (self.SQ_SIZE, self.SQ_SIZE))

    def main(self):
        firstTurn = True
        while True:
            playerchoice = input("Do you want white to be ai or human?\n")
            if playerchoice == "ai":
                self.aiWhite = True
                break
            elif playerchoice == "human":
                break
            else:
                pass
        p.init()
        screen = p.display.set_mode((self.WIDTH, self.HEIGHT))
        clock = p.time.Clock()
        screen.fill(p.Color("white"))
        gs = ChessEngine.GameState()
        validMoves = gs.getValidMoves(False)
        moveMade = False
        self.loadImages()
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
                elif (gs.whiteToMove and self.aiWhite) or (not gs.whiteToMove and not self.aiWhite):
                    print("AI turn")
                    ai = mm.MinMax(gs, firstTurn, gs.whiteToMove)
                    ai.makeMove()
                    print("Player Turn")
                    if firstTurn:
                        firstTurn = False
                    validMoves = gs.getValidMoves(False)
                else:
                    for e in p.event.get():
                        if e.type == p.QUIT:
                            running = False
                        elif e.type == p.MOUSEBUTTONDOWN:
                            location = p.mouse.get_pos()
                            col = location[0] // self.SQ_SIZE
                            row = location[1] // self.SQ_SIZE
                            if sqSelected == (row, col):
                                # Clears both selected and playerClicks to make sure we move the correct piece if people clicks on the same location twice.
                                sqSelected = ()
                                playerClicks = []
                            else:
                                validMoves = gs.getValidMoves(False)
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
                    moveMade = False

            self.drawGameState(screen, gs)
            clock.tick(self.MAX_FPS)
            p.display.flip()

    '''
    Draws he board from the current game state
    '''

    def drawGameState(self, screen, gs):
        self.drawBoard(screen)  # creates the board
        self.drawPieces(screen, gs.board)

    def drawBoard(self, screen):
        colors = [p.Color("white"), p.Color("gray")]
        for r in range(self.DIMENSION):
            for c in range(self.DIMENSION):
                color = colors[((r + c) % 2)]
                p.draw.rect(screen, color, p.Rect(c * self.SQ_SIZE, r * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))

    def drawPieces(self, screen, board):
        for r in range(self.DIMENSION):
            for c in range(self.DIMENSION):
                piece = board[r][c]
                if piece != "--":  # checks if it's not an empty square
                    screen.blit(self.IMAGES[piece],
                                p.Rect(c * self.SQ_SIZE, r * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))


if __name__ == "__main__":
    startGame = ChessGame()
    startGame.main()
