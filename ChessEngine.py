class GameState:
    def __init__(self):
        # Creates the board
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "bB", "--", "--", "--", "--"],
            ["--", "--", "wB", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
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
                    self.functionForMOve[piece](r, c, moves) #instad of if/else statements
        return moves

    def getPawnMoves(self, r, c, moves):
        # Has to think about which turn it is because pawns are only able to move one direction.
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
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def getRookMoves(self, r, c, moves):
        enemyColor = "b" if self.whiteToMove else "w"
        going = True
        i = 1
        goUp = True
        goDown = True
        goRight = True
        goLeft = True

        while going:
            if r - i < 0:
                goUp = False
            #Checks for moves going up the board
            elif self.board[r - i][c] == "--" and goUp:
                moves.append(Move((r, c), (r - i, c), self.board))
            elif self.board[r - i][c][0] == enemyColor and goUp:
                moves.append(Move((r, c), (r - i, c), self.board))
                goUp = False
            else:
                goUp = False

            #Checks for moves going down the board
            if r + i > len(self.board) - 1:
                goDown = False
            elif self.board[r + i][c] == "--" and goDown:
                moves.append(Move((r, c), (r + i, c), self.board))
            elif self.board[r + i][c][0] == enemyColor and goDown:
                moves.append(Move((r, c), (r + i, c), self.board))
                goDown = False
            else:
                goDown = False

            #Checks for moves going right on the board
            if c + i > len(self.board) - 1:
                goRight = False
            elif self.board[r][c + i] == "--" and goRight:
                moves.append(Move((r, c), (r, c + i), self.board))
            elif self.board[r][c + i][0] == enemyColor and goRight:
                moves.append(Move((r, c), (r, c + i), self.board))
                goRight = False
            else:
                goRight = False

            #Checks for moves going left on the board
            if c - i < 0:
                goLeft = False
            elif self.board[r][c - i] == "--" and goLeft:
                moves.append(Move((r, c), (r, c - i), self.board))
            elif self.board[r][c - i][0] == enemyColor:
                moves.append(Move((r, c), (r, c - i), self.board))
                going = False
            else:
                goLeft = False

            if not goLeft and not goRight and not goUp and not goDown:
                going = False
            i += 1

    def getBishopMoves(self, r, c, moves):
        enemyColor = "b" if self.whiteToMove else "w"
        i = 1
        going = True
        topLeft = True
        topRight = True
        downLeft = True
        downRight = True

        while going:

            #Checks for possible topleft moves
            if r - i < 0 or c - i < 0:
                topLeft = False
            elif self.board[r - i][c - i] == "--" and topLeft:
                moves.append(Move((r, c), (r - i, c - i), self.board))
            elif self.board[r - i][c - i][0] == enemyColor:
                moves.append(Move((r, c), (r - i, c - i), self.board))
                topLeft = False
            else:
                topLeft = False

            #Checks for possible down right moves
            if r + i > len(self.board) - 1 or c + i > len(self.board) - 1:
                downRight = False
            elif self.board[r + i][c + i] == "--" and downRight:
                moves.append(Move((r, c), (r + i, c + i), self.board))
            elif self.board[r + i][c + i][0] == enemyColor and downRight:
                moves.append(Move((r, c), (r + i, c + i), self.board))
                downRight = False
            else:
                downRight = False


            #Checks for possible top right moves
            if r - i < 0 or c + i > len(self.board) - 1:
                topRight = False
            elif self.board[r - i][c + i] == "--" and topRight:
                moves.append(Move((r, c), (r - i, c + i), self.board))
            elif self.board[r - i][c + i][0] == enemyColor and topRight:
                moves.append(Move((r, c), (r - i, c + i), self.board))
                topRight = False
            else:
                topRight = False

            #Checks for possible down left moves
            if r + i > len(self.board) - 1 or c - i < 0:
                downLeft = False
            elif self.board[r + i][c - i] == "--" and downLeft:
                moves.append(Move((r, c), (r + i, c - i), self.board))
            elif self.board[r + i][c - i][0] == enemyColor and downLeft:
                moves.append(Move((r, c), (r + i, c - i), self.board))
                downLeft = False
            else:
                downLeft = False

            if not downLeft and not downRight and not topLeft and not topRight:
                going = False

            i += 1


    def getKnightMoves(self, r, c, moves):
        enemyColor = "b" if self.whiteToMove else "w"

        if r - 2 < 0 or c - 1 < 0:
            pass
        elif self.board[r - 2][c - 1] == "--" or self.board[r - 2][c - 1][0] == enemyColor:
            moves.append(Move((r, c), (r - 2, c - 1), self.board))

        if r - 2 < 0 or c + 1 > len(self.board) - 1:
            pass
        elif self.board[r - 2][c + 1] == "--" or self.board[r - 2][c + 1][0] == enemyColor:
            moves.append(Move((r, c), (r - 2, c + 1), self.board))

        if r + 2 > len(self.board) - 1 or c - 1 < 0:
            pass
        elif self.board[r + 2][c - 1] == "--" or self.board[r + 2][c - 1][0] == enemyColor:
            moves.append(Move((r, c), (r + 2, c - 1), self.board))

        if r + 2 > len(self.board) - 1 or c + 1 > len(self.board) - 1:
            pass
        elif self.board[r + 2][c + 1] == "--" or self.board[r + 2][c + 1][0] == enemyColor:
            moves.append(Move((r, c), (r + 2, c + 1), self.board))

        if r + 1 > len(self.board) - 1 or c - 2 < 0:
            pass
        elif self.board[r + 1][c - 2] == "--" or self.board[r + 1][c - 2][0] == enemyColor:
            moves.append(Move((r, c), (r + 1, c - 2), self.board))

        if r + 1 > len(self.board) - 1 or c + 2 > len(self.board) - 1:
            pass
        elif self.board[r + 1][c + 2] == "--" or self.board[r + 1][c + 2][0] == enemyColor:
            moves.append(Move((r, c), (r + 1, c + 2), self.board))

        if r - 1 < 0 or c - 2 < 0:
            pass
        elif self.board[r - 1][c - 2] == "--" or self.board[r - 1][c - 2][0] == enemyColor:
            moves.append(Move((r, c), (r - 1, c - 2), self.board))

        if r - 1 < 0 or c + 2 > len(self.board) - 1:
            pass
        elif self.board[r - 1][c + 2] == "--" or self.board[r - 1][c + 2][0] == enemyColor:
            moves.append(Move((r, c), (r - 1, c + 2), self.board))

    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        enemyColor = "b" if self.whiteToMove else "w"

        if r - 1 < 0 or c - 1 < 0:
            pass
        elif self.board[r - 1][c - 1] == "--" or self.board[r - 1][c - 1][0] == enemyColor:
            moves.append(Move((r, c), (r - 1, c - 1), self.board))

        if r - 1 < 0:
            pass
        elif self.board[r - 1][c] == "--" or self.board[r - 1][c][0] == enemyColor:
            moves.append(Move((r, c), (r - 1, c), self.board))

        if r - 1 < 0 or c + 1 > len(self.board) - 1:
            pass
        elif self.board[r - 1][c + 1] == "--" or self.board[r - 1][c + 1][0] == enemyColor:
            moves.append(Move((r, c), (r - 1, c + 1), self.board))

        if c - 1 < 0:
            pass
        elif self.board[r][c - 1] == "--" or self.board[r][c - 1][0] == enemyColor:
            moves.append(Move((r, c), (r, c - 1), self.board))

        if c + 1 > len(self.board) - 1:
            pass
        elif self.board[r][c + 1] == "--" or self.board[r][c + 1][0] == enemyColor:
            moves.append(Move((r, c), (r, c + 1), self.board))

        if r + 1 > len(self.board) - 1 or c - 1 < 0:
            pass
        elif self.board[r + 1][c - 1] == "--" or self.board[r + 1][c - 1][0] == enemyColor:
            moves.append(Move((r, c), (r + 1, c - 1), self.board))

        if r + 1 > len(self.board) - 1:
            pass
        elif self.board[r + 1][c] == "--" or self.board[r + 1][c][0] == enemyColor:
            moves.append(Move((r, c), (r + 1, c), self.board))

        if r + 1 > len(self.board) - 1 or c + 2 > len(self.board) - 1:
            pass
        elif self.board[r + 1][c + 1] == "--" or self.board[r + 1][c + 1][0] == enemyColor:
            moves.append(Move((r, c), (r + 1, c + 1), self.board))

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