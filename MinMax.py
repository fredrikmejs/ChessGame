import ChessEngine
import sys
import random
import threading
import time


class MinMax:
    def __init__(self, GameState, openingMove, isWhite):
        self.state = GameState
        self.openingMove = openingMove
        self.whiteOpeners = [ChessEngine.Move((6, 4), (4, 4), self.state.board),
                             ChessEngine.Move((6, 3), (4, 3), self.state.board),
                             ChessEngine.Move((7, 6), (5, 5), self.state.board),
                             ChessEngine.Move((6, 2), (4, 2), self.state.board)]
        self.isWhite = isWhite
        self.ztable = [[[random.randint(1, 2 ** 64 - 1) for i in range(12)] for j in range(8)] for k in range(8)]
        self.hashvalue = self.computeHash(self.state.board)
        self.hashtable = dict()
        self.timeUp = False
        self.timer = threading.Timer(17.0, self.changeTimer)
        self.timer.start()


    def changeTimer(self):
        self.timeUp = not self.timeUp

    # evaluation function, values taken from notes.
    def get_board_value(self, state, move):
        value = 0.0
        # checks if it's white's turn to move, and sets player.
        player = "w" if self.isWhite else "b"
        # field values, taken from slides.
        field_values = [
            [00.0, 00.0, 00.0, 00.0, 00.0, 00.0, 00.0, 00.0],
            [23.0, 30.0, 41.5, 44.0, 47.5, 33.5, 23.0, 23.0],
            [09.0, 14.0, 23.0, 26.0, 29.0, 17.0, 08.0, 08.0],
            [03.0, 07.0, 09.5, 12.0, 14.5, 04.5, -3.0, -3.0],
            [01.0, 03.0, 06.0, 08.0, 10.0, 02.0, -4.0, -4.0],
            [-4.0, -1.0, 04.5, 05.0, 06.5, 01.5, -4.0, -4.0],
            [-2.0, 00.0, 03.0, 04.0, 05.0, 01.0, -2.0, -2.0],
            [00.0, 00.0, 00.0, 00.0, 00.0, 00.0, 00.0, 00.0]]
        # reverses the field_values array
        rev_field_values = field_values[::-1]
        # reverses each row in the fied_values array
        for index, row in enumerate(rev_field_values):
            rev_field_values[index] = row[::-1]
        if player == 'w':
            for x, row in enumerate(state.board):
                for y, piece in enumerate(row):
                    if 'w' in piece:
                        if 'p' in piece:
                            if state.board[x - 1][y] == "wp":
                                value += -8.0
                            else:
                                value += 100.0 + field_values[x][y]
                        elif 'R' in piece:
                            value += 550.0 + 1.5 * self.protectedRook(x, y, state.board)
                        elif 'B' in piece:
                            value += 450.0 + 2.5 * self.protectedBishop(x, y, state.board)
                        elif 'Q' in piece:
                            mult = self.protectedBishop(x, y, state.board) + self.protectedRook(x, y, state.board) - 1
                            value += 1000.0 + 1.5 * mult
                        elif 'K' in piece:
                            value += 10000.0
                        elif 'N' in piece:
                            value += 300 + 3.0 * (4 - self.distanceToCenter(y))
                        if state.isAiMate:
                            value += 20000
                        if move.isCastleMove:
                            value += 35
                            state.castleLastTurnWhite = False

                    if 'b' in piece:
                        if 'p' in piece:
                            if state.board[x + 1][y] == 'bp':
                                value -= -8.0
                            else:
                                value -= 100.0 + rev_field_values[x][y]
                        elif 'R' in piece:
                            value -= 550.0 + 1.5 * self.protectedRook(x, y, state.board)
                        elif 'B' in piece:
                            value -= 450.0 + 2.5 * self.protectedBishop(x, y, state.board)
                        elif 'Q' in piece:
                            mult = self.protectedBishop(x, y, state.board) + self.protectedRook(x, y, state.board) - 1
                            value -= 1000.0 + 1.5 * mult
                        elif 'K' in piece:
                            value -= 10000.0
                        elif 'N' in piece:
                            value -= 300 + 3.0 * (4 - self.distanceToCenter(y))
                        if state.isAiMate:
                            value -= 20000
                        if move.isCastleMove:
                            value -= 35
                            state.castleLastTurnBlack = False
        else:
            for x, row in enumerate(state.board):
                for y, piece in enumerate(row):
                    if 'b' in piece:
                        if 'p' in piece:
                            if state.board[x - 1][y] == "bp":
                                value += -8.0
                            else:
                                value += 100.0 + rev_field_values[x][y]
                        elif 'R' in piece:
                            value += 550.0 + 1.5 * self.protectedRook(x, y, state.board)
                        elif 'B' in piece:
                            value += 450.0 + 2.5 * self.protectedBishop(x, y, state.board)
                        elif 'Q' in piece:
                            mult = self.protectedBishop(x, y, state.board) + self.protectedRook(x, y, state.board) - 1
                            value += 1000.0 + 1.5 * mult
                        elif 'K' in piece:
                            value += 10000.0
                        elif 'N' in piece:
                            value += 300 + 3.0 * (4 - self.distanceToCenter(y))
                        if state.isAiMate:
                            value += 20000
                        if move.isCastleMove:
                            value += 35
                            move.isCastleMove = False

                    if 'w' in piece:
                        if 'p' in piece:
                            if state.board[x + 1][y] == 'wp':
                                value -= -8.0
                            else:
                                value -= 100.0 + field_values[x][y]
                        elif 'R' in piece:
                            value -= 550.0 + 1.5 * self.protectedRook(x, y, state.board)
                        elif 'B' in piece:
                            value -= 450.0 + 2.5 * self.protectedBishop(x, y, state.board)
                        elif 'Q' in piece:
                            mult = self.protectedBishop(x, y, state.board) + self.protectedRook(x, y, state.board) - 1
                            value -= 1000.0 + 1.5 * mult
                        elif 'K' in piece:
                            value -= 10000.0
                        elif 'N' in piece:
                            value -= 300 + 3.0 * (4 - self.distanceToCenter(y))
                        if state.isAiMate:
                            value -= 20000
                        if move.isCastleMove:
                            value -= 35
                            state.castleLastTurnWhite = False
        return value

    def protectedRook(self, x, y, board):
        mult = 1.0
        tempX = x + 1
        tempY = y + 1
        if tempY <= 7:
            tempPiece = board[x][tempY]
            while tempPiece == '--' and tempY <= 7:
                mult += 1.0
                if tempY == 7:
                    break
                else:
                    tempY += 1
                    tempPiece = board[x][tempY]
        tempY = y - 1
        if tempY >= 0:
            tempPiece = board[x][tempY]
            while tempPiece == '--' and tempY >= 0:
                mult += 1.0
                if tempY == 0:
                    break
                else:
                    tempY -= 1
                    tempPiece = board[x][tempY]
        if tempX <= 7:
            tempPiece = board[tempX][y]
            while tempPiece == '--' and tempX <= 7:
                mult += 1.0
                if tempX == 7:
                    break
                else:
                    tempX += 1
                    tempPiece = board[tempX][y]
        tempX = x - 1
        if tempX >= 0:
            tempPiece = board[tempX][y]
            while tempPiece == '--' and tempX >= 0:
                mult += 1.0
                if tempX == 0:
                    break
                else:
                    tempX -= 1
                    tempPiece = board[tempX][y]
        return mult

    def protectedBishop(self, x, y, board):
        mult = 1.0
        tempX = x + 1
        tempY = y + 1
        if tempX <= 7 and tempY <= 7:
            tempPiece = board[tempX][tempY]
            while tempPiece == '--' and tempX <= 7 and tempY <= 7:
                mult += 1.0
                if tempX == 7 or tempY == 7:
                    break
                else:
                    tempX += 1
                    tempY += 1
                    tempPiece = board[tempX][tempY]
        tempX = x - 1
        tempY = y - 1
        if tempX >= 0 and tempY >= 0:
            tempPiece = board[tempX][tempY]
            while tempPiece == '--' and tempX >= 0 and tempY >= 0:
                mult += 1.0
                if tempX == 0 or tempY == 0:
                    break
                else:
                    tempX -= 1
                    tempY -= 1
                    tempPiece = board[tempX][tempY]
        return mult

    def distanceToCenter(self, y):
        distance = 0
        if y >= 4:
            distance = y - 4
        elif y < 4:
            distance = 3 - y
        return distance

    def minimaxRoot(self, state, depth, isMaximizing):
        possibleMoves = state.getValidMoves(True)
        bestMoveValue = -(sys.maxsize - 1)
        bestMove = None
        for move in possibleMoves:
            if self.timeUp:
                return None
            newHash = self.hashvalue
            piece = move.pieceMoved
            newHash ^= self.ztable[move.startRow][move.startCol][self.index(piece)]
            if newHash not in self.hashtable:
                state.makeMove(move, False)
                value = max(bestMoveValue,
                            self.minimax(state, depth - 1, -(sys.maxsize - 1), sys.maxsize, not isMaximizing, move))
                piece = state.board[move.endRow][move.endCol]
                newHash ^= self.ztable[move.endRow][move.endCol][self.index(piece)]
                self.hashtable[newHash] = (value, move)
                state.undoMove()
            else:
                value = self.hashtable.get(newHash)[0]
            if value > bestMoveValue:
                bestMoveValue = value
                bestMove = move
        if bestMove is None:
            value = self.hashtable.get(self.hashvalue)[0]
            bestMove = self.hashtable.get(self.hashvalue)[1]
        self.hashtable[self.hashvalue] = (value, bestMove)
        print("BestValue = " + str(value))
        return bestMove

    def minimax(self, state, depth, alpha, beta, isMaximizing, move):
        if depth == 0:
            return self.get_board_value(state, move)
        possibleMoves = state.getValidMoves(True)
        if isMaximizing:
            value = -(sys.maxsize - 1)
            for move in possibleMoves:
                if self.timeUp:
                    return -1
                newHash = self.hashvalue
                piece = move.pieceMoved
                newHash ^= self.ztable[move.startRow][move.startCol][self.index(piece)]
                if newHash not in self.hashtable:
                    state.makeMove(move, False)
                    value = max(value, self.minimax(state, depth - 1, alpha, beta, not isMaximizing, move))
                    piece = state.board[move.endRow][move.endCol]
                    newHash ^= self.ztable[move.endRow][move.endCol][self.index(piece)]
                    self.hashtable[newHash] = (value, move)
                    state.undoMove()
                else:
                    value = self.hashtable.get(newHash)[0]
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = sys.maxsize
            for move in possibleMoves:
                if self.timeUp:
                    return -1
                newHash = self.hashvalue
                piece = move.pieceMoved
                newHash ^= self.ztable[move.startRow][move.startCol][self.index(piece)]
                if newHash not in self.hashtable:
                    state.makeMove(move, False)
                    value = min(value, self.minimax(state, depth - 1, alpha, beta, not isMaximizing, move))
                    piece = state.board[move.endRow][move.endCol]
                    newHash ^= self.ztable[move.endRow][move.endCol][self.index(piece)]
                    self.hashtable[newHash] = (value, move)
                    state.undoMove()
                else:
                    value = self.hashtable.get(newHash)[0]
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value

    def makeMove(self):
        if not self.openingMove:
            chosenMove = None
            finalMove = None
            depth = 1
            while not self.timeUp:
                chosenMove = self.minimaxRoot(self.state, depth, True)
                if not self.timeUp:
                    finalMove = chosenMove
                depth += 1

            print("Depth = " + str(depth))
            self.state.makeMove(finalMove, True)
        elif self.openingMove and self.state.whiteToMove:
            self.state.makeMove(random.choice(self.whiteOpeners), True)
        elif self.openingMove and not self.state.whiteToMove:
            if self.state.board[4][4] == "wp":
                self.state.makeMove(ChessEngine.Move((1, 4), (3, 4), self.state.board), True)
            elif self.state.board[4][3] == "wp":
                self.state.makeMove(ChessEngine.Move((1, 3), (3, 3), self.state.board), True)

    def index(self, piece):
        if piece == 'wp':
            return 0
        if piece == 'wQ':
            return 1
        if piece == "wK":
            return 2
        if piece == "wB":
            return 3
        if piece == "wN":
            return 4
        if piece == "wR":
            return 5
        if piece == "bp":
            return 6
        if piece == "bQ":
            return 7
        if piece == "bK":
            return 8
        if piece == "bB":
            return 9
        if piece == "bN":
            return 10
        if piece == "bR":
            return 11
        else:
            return -1

    def computeHash(self, board):
        hash = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] != '--':
                    piece = self.index(board[i][j])
                    hash ^= self.ztable[i][j][piece]
        return hash
