class GameState:
    def __init__(self):
        # Creates the board
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.functionForMOve = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                                'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        # White always start
        self.whiteToMove = True
        self.moveLog = []

        # Checks for the location of the black and white king
        self.whiteKingLoc = (7, 4)
        self.blackKingLoc = (0, 4)
        self.inCheck = False
        self.pins = []
        self.checks = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"  # Set the moved from postion empty
        self.board[move.endRow][move.endCol] = move.pieceMoved  # move the brick to the given position
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove  # Switches turn.
        # Checks for the position of the king
        if move.pieceMoved == "wK":
            self.whiteKingLoc = (move.startRow, move.startCol)
        elif move.pieceMoved == "bK":
            self.blackKingLoc = (move.startRow, move.startCol)

        if self.whiteToMove:
            print("White to move")
        else:
            print("Black to move")

    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForChecksAndPins
        if self.whiteToMove:
            kingRow = self.whiteKingLoc[0]
            kingCol = self.whiteKingLoc[1]
        else:
            kingRow = self.blackKingLoc[0]
            kingCol = self.blackKingLoc[1]
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []  # valid square to move to
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break

                # removes moves that doesn't block check, goes through backwards
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove((moves[i]))
            else:
                self.getKingMoves(kingRow, kingCol, moves)
        else:  # Not in Check do normal moves
            moves = self.getAllPossibleMoves()

        return moves

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of col in a row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.functionForMOve[piece](r, c, moves)  # instad of if/else statements
        return moves

    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, - 1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
            break

        # Has to think about which turn it is because pawns are only able to move one direction.
        if self.whiteToMove:
            if self.board[r - 1][c] == "--":
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((r, c), (r - 1, c), self.board))
                    if r == 6 and self.board[r - 2][c] == "--":  # 2 square move
                        moves.append(Move((r, c), (r - 2, c), self.board))

            if c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == 'b':
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r - 1][c + 1][0] == 'b':
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:
            if self.board[r + 1][c] == "--":
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    if r == 1 and self.board[r + 2][c] == "--":
                        moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == 'w':
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == 'w':
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':  # Doesn't remove pin for queen on rock moves
                    self.pins.remove(self.pins[i])
            break

        enemyColor = "b" if self.whiteToMove else "w"
        going = True
        i = 1
        goUp = True
        goDown = True
        goRight = True
        goLeft = True

        while going:

            # Checks for moves going up the board
            if r - i < 0:
                goUp = False
            # Checks for moves going up the board
            elif self.board[r - i][c] == "--" and goUp:
                if not piecePinned or pinDirection == (r - i, c):
                    moves.append(Move((r, c), (r - i, c), self.board))
            elif self.board[r - i][c][0] == enemyColor and goUp:
                if not piecePinned or pinDirection == (r - i, c):
                    moves.append(Move((r, c), (r - i, c), self.board))
                    goUp = False
            else:
                goUp = False

            # Checks for moves going down the board
            if r + i > len(self.board) - 1:
                goDown = False
            elif self.board[r + i][c] == "--" and goDown:
                if not piecePinned or pinDirection == (r + i, c):
                    moves.append(Move((r, c), (r + i, c), self.board))
            elif self.board[r + i][c][0] == enemyColor and goDown:
                if not piecePinned or pinDirection == (r + i, c):
                    moves.append(Move((r, c), (r + i, c), self.board))
                    goDown = False
            else:
                goDown = False

            # Checks for moves going right on the board
            if c + i > len(self.board) - 1:
                goRight = False
            elif self.board[r][c + i] == "--" and goRight:
                if not piecePinned or pinDirection == (r, c + 1):
                    moves.append(Move((r, c), (r, c + i), self.board))
            elif self.board[r][c + i][0] == enemyColor and goRight:
                if not piecePinned or pinDirection == (r, c + 1):
                    moves.append(Move((r, c), (r, c + i), self.board))
                    goRight = False
            else:
                goRight = False

            # Checks for moves going left on the board
            if c - i < 0:
                goLeft = False
            elif self.board[r][c - i] == "--" and goLeft:
                if not piecePinned or pinDirection == (r, c - 1):
                    moves.append(Move((r, c), (r, c - i), self.board))
            elif self.board[r][c - i][0] == enemyColor:
                if not piecePinned or pinDirection == (r, c - 1):
                    moves.append(Move((r, c), (r, c - i), self.board))
                    going = False
            else:
                goLeft = False

            if not goLeft and not goRight and not goUp and not goDown:
                going = False
            i += 1

    def getBishopMoves(self, r, c, moves):

        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        enemyColor = "b" if self.whiteToMove else "w"
        i = 1
        going = True
        topLeft = True
        topRight = True
        downLeft = True
        downRight = True

        while going:
            # Checks for possible topleft moves

            if r - i < 0 or c - i < 0:
                topLeft = False
            elif self.board[r - i][c - i] == "--" and topLeft:
                if not piecePinned:
                    moves.append(Move((r, c), (r - i, c - i), self.board))
            elif self.board[r - i][c - i][0] == enemyColor:
                if not piecePinned:
                    moves.append(Move((r, c), (r - i, c - i), self.board))
                    topLeft = False
            else:
                topLeft = False

            # Checks for possible down right moves
            if r + i > len(self.board) - 1 or c + i > len(self.board) - 1:
                downRight = False
            elif self.board[r + i][c + i] == "--" and downRight:
                if not piecePinned:
                    moves.append(Move((r, c), (r + i, c + i), self.board))
            elif self.board[r + i][c + i][0] == enemyColor and downRight:
                if not piecePinned:
                    moves.append(Move((r, c), (r + i, c + i), self.board))
                    downRight = False
            else:
                downRight = False

            # Checks for possible top right moves
            if r - i < 0 or c + i > len(self.board) - 1:
                topRight = False
            elif self.board[r - i][c + i] == "--" and topRight:
                if not piecePinned:
                    moves.append(Move((r, c), (r - i, c + i), self.board))
            elif self.board[r - i][c + i][0] == enemyColor and topRight:
                if not piecePinned:
                    moves.append(Move((r, c), (r - i, c + i), self.board))
                    topRight = False
            else:
                topRight = False

            # Checks for possible down left moves
            if r + i > len(self.board) - 1 or c - i < 0:
                downLeft = False
            elif self.board[r + i][c - i] == "--" and downLeft:
                if not piecePinned:
                    moves.append(Move((r, c), (r + i, c - i), self.board))
            elif self.board[r + i][c - i][0] == enemyColor and downLeft:
                if not piecePinned:
                    moves.append(Move((r, c), (r + i, c - i), self.board))
                    downLeft = False
            else:
                downLeft = False

            if not downLeft and not downRight and not topLeft and not topRight:
                going = False

            i += 1

    def getKnightMoves(self, r, c, moves):

        piecePinned = False
        pinDirections = ()

        for i in range(len(self.pins) - 1, -1, -1):
            piecePinned = True
            pinDirections = (self.pins[i][2], self.pins[i][3])
            self.pins.remove(self.pins[i])
            break

        enemyColor = "b" if self.whiteToMove else "w"

        if not piecePinned:
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
        allyColor = 'w' if self.whiteToMove else 'b'

        if r - 1 < 0 or c - 1 < 0:
            pass
        elif self.board[r - 1][c - 1] == "--" or self.board[r - 1][c - 1][0] == enemyColor:
            if allyColor == 'w':
                self.whiteKingLoc = (r - 1, c - 1)
            else:
                self.blackKingLoc = (r - 1, c - 1)
            inCheck, pins, checks = self.checkForChecksAndPins
            if not inCheck:
                moves.append(Move((r, c), (r - 1, c - 1), self.board))

        if r - 1 < 0:
            pass
        elif self.board[r - 1][c] == "--" or self.board[r - 1][c][0] == enemyColor:
            if allyColor == 'w':
                self.whiteKingLoc = (r - 1, c)
            else:
                self.blackKingLoc = (r - 1, c)
            inCheck, pins, checks = self.checkForChecksAndPins
            if not inCheck:
                moves.append(Move((r, c), (r - 1, c), self.board))

        if r - 1 < 0 or c + 1 > len(self.board) - 1:
            pass
        elif self.board[r - 1][c + 1] == "--" or self.board[r - 1][c + 1][0] == enemyColor:
            if allyColor == 'w':
                self.whiteKingLoc = (r - 1, c + 1)
            else:
                self.blackKingLoc = (r - 1, c + 1)
            inCheck, pins, checks = self.checkForChecksAndPins
            if not inCheck:
                moves.append(Move((r, c), (r - 1, c + 1), self.board))

        if c - 1 < 0:
            pass
        elif self.board[r][c - 1] == "--" or self.board[r][c - 1][0] == enemyColor:
            if allyColor == 'w':
                self.whiteKingLoc = (r, c - 1)
            else:
                self.blackKingLoc = (r, c - 1)
            inCheck, pins, checks = self.checkForChecksAndPins
            if not inCheck:
                moves.append(Move((r, c), (r, c - 1), self.board))

        if c + 1 > len(self.board) - 1:
            pass
        elif self.board[r][c + 1] == "--" or self.board[r][c + 1][0] == enemyColor:
            if allyColor == 'w':
                self.whiteKingLoc = (r, c + 1)
            else:
                self.blackKingLoc = (r, c + 1)
            inCheck, pins, checks = self.checkForChecksAndPins
            if not inCheck:
                moves.append(Move((r, c), (r, c + 1), self.board))

        if r + 1 > len(self.board) - 1 or c - 1 < 0:
            pass
        elif self.board[r + 1][c - 1] == "--" or self.board[r + 1][c - 1][0] == enemyColor:
            if allyColor == 'w':
                self.whiteKingLoc = (r + 1, c - 1)
            else:
                self.blackKingLoc = (r + 1, c - 1)
            inCheck, pins, checks = self.checkForChecksAndPins
            if not inCheck:
                moves.append(Move((r, c), (r + 1, c - 1), self.board))

        if r + 1 > len(self.board) - 1:
            pass
        elif self.board[r + 1][c] == "--" or self.board[r + 1][c][0] == enemyColor:
            if allyColor == 'w':
                self.whiteKingLoc = (r + 1, c)
            else:
                self.blackKingLoc = (r + 1, c)
            inCheck, pins, checks = self.checkForChecksAndPins
            if not inCheck:
                moves.append(Move((r, c), (r + 1, c), self.board))

        if r + 1 > len(self.board) - 1 or c + 2 > len(self.board) - 1:
            pass
        elif self.board[r + 1][c + 1] == "--" or self.board[r + 1][c + 1][0] == enemyColor:
            if allyColor == 'w':
                self.whiteKingLoc = (r + 1, c + 1)
            else:
                self.blackKingLoc = (r + 1, c + 1)
            inCheck, pins, checks = self.checkForChecksAndPins
            if not inCheck:
                moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switches the turn back

    @property
    def checkForChecksAndPins(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColor = "b"
            ally = "w"
            startRow = self.whiteKingLoc[0]
            startCol = self.whiteKingLoc[1]
        else:
            enemyColor = "w"
            ally = "b"
            startRow = self.blackKingLoc[0]
            startCol = self.blackKingLoc[1]
        possibleKingMoves = ((-1, 0), (0, -1), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for i in range(len(possibleKingMoves)):
            direction = possibleKingMoves[i]
            possiblePin = ()
            for j in range(1, 8):
                endRow = startRow + direction[0] * j
                endCol = startCol + direction[1] * j
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == ally:
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, direction[0], direction[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]

                        if (0 <= i <= 3 and type == 'R') or \
                                (4 <= i <= 7 and type == 'B') or \
                                (j == 1 and type == 'p' and ((enemyColor == 'w') and 6 <= i <= 7) or \
                                 (enemyColor == 'b' and 4 <= j <= 5)) or \
                                (type == 'Q') or (j == 1 and type == 'K'):
                            if possiblePin == ():  # Checks if any piece is blocking
                                inCheck = True
                                checks.append((endRow, endCol, direction[0], direction[1]))
                                break
                            else:  # A piece is blocking
                                pins.append((possiblePin))
                                break
                        else:  # No check
                            break
                    else:
                        break
        # Checks for knight check because of special move
        knightPossibleMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightPossibleMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))

        return inCheck, pins, checks


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
