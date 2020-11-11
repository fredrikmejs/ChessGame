class GameState():
    def __init__(self):
        #Creates the board
        self.board = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        #White always start
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self,move):
        a = move.pieceMoved
        b = self.board[move.startRow][move.startCol]
        c = self.board[move.endRow][move.endCol]

        self.board[move.startRow][move.startCol] = "--" #Set the moved from postion empty
        self.board[move.endRow][move.endCol] = move.pieceMoved #move the brick to the given position
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove #Switches turn.


class Move():

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
