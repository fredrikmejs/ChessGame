class GameState:
    def __init__(self):
        # Creates the board
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["--", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["bp", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.functionForMOve = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                                'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves }

        # White always start
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"  # Set the moved from postion empty
        self.board[move.endRow][move.endCol] = move.pieceMoved  # move the brick to the given position
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove  # Switches turn.

        if self.whiteToMove:
            print("White-- to move")
        else:
            print("Black to move")

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of col in a row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]

                    self.functionForMOve[piece](r,c,moves) #instad of if/else statements
        return moves

    def getPawnMoves(self, r, c, moves):
        # Has to think about which turn it is.
        if self.whiteToMove:
            if self.board[r - 1][c] == "--":
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r - 1][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

        if not self.whiteToMove:
            if self.board[r + 1][c] == "--":
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == 'w':
                    print("venstre " + self.board[r + 1][c - 1][0])
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == 'w':
                    print("højre " + self.board[r + 1][c + 1][0])
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def getRookMoves(self, r, c, moves):
            enemyColor = "b" if self.whiteToMove else "w"
            going = True
            i = 1
            while going:
                if r - i < 0:
                    break
                if self.board[r - i][c] == "--":
                    moves.append(Move((r, c), (r - i, c), self.board))
                else:
                    going = False
                if self.board[r - i][c][0] == enemyColor:
                    moves.append(Move((r, c), (r - i, c), self.board))
                    going = False
                i += 1
            i = 1
            going = True
            while going:
                if r + i > len(self.board)-1:
                    break
                if self.board[r + i][c] == "--":
                    moves.append(Move((r, c), (r + i, c), self.board))
                else:
                    going = False

                if self.board[r + i][c][0] == enemyColor:
                    moves.append(Move((r, c), (r + i, c), self.board))
                    going = False
                i += 1

            i = 1
            going = True
            while going:
                if c + i > len(self.board) - 1:
                    break
                if self.board[r][c + i] == "--":
                    moves.append(Move((r, c), (r, c + i), self.board))
                else:
                    going = False

                if self.board[r][c + i][0] == enemyColor:
                    moves.append(Move((r, c), (r, c + i), self.board))
                    going = False
                i += 1

            going = True
            i = 1
            while going:
                if c - i < 0:
                    break
                if self.board[r][c - i] == "--":
                    moves.append(Move((r, c), (r, c - i), self.board))
                else:
                    going = False

                if self.board[r][c - i][0] == enemyColor:
                    moves.append(Move((r, c), (r, c - i), self.board))
                    going = False
                i += 1

    def getBishopMoves(self, r, c, moves):
        pass

    def getKnightMoves(self, r, c, moves):
        pass

    def getQueenMoves(self, r, c, moves):
        pass

    def getKingMoves(self, r, c, moves):
        pass

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switches the turn back


class Move:

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
