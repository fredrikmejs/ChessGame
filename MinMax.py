import ChessEngine
import sys
import copy as c
import random


class MinMax:
    def __init__(self, GameState, openingMove):
        self.visitedStates = []
        self.state = GameState
        self.openingMove = openingMove
        self.whiteOpeners = [ChessEngine.Move((6, 4), (4, 4), self.state.board),
                             ChessEngine.Move((6, 3), (4, 3), self.state.board),
                             ChessEngine.Move((7, 6), (5, 5), self.state.board),
                             ChessEngine.Move((6, 2), (4, 2), self.state.board)]
        self.numberStates = 0
        self.knownBoards = []
        self.alpha = -sys.maxsize - 1

    def expandChildren(self, state):
        children = []
        possibleMoves = state.getValidMoves()
        for move in possibleMoves:
            tempState = ChessEngine.GameState()
            self.copyState(state, tempState)
            tempState.makeMove(move, False)
            if tempState.board not in self.knownBoards:
                children.append((tempState, move))
                self.knownBoards.append(tempState.board)
            elif len(possibleMoves) <= 9:
                children.append((tempState, move))

        return children

    # evaluation function, values taken from notes.
    def get_board_value(self, state):
        value = 0.0
        # checks if it's white's turn to move, and sets player.
        player = "w" if state.whiteToMove else "b"
        # field values, taken from slides.
        field_values = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [23.0, 30.0, 41.5, 44.0, 47.5, 33.5, 23.0, 23.0],
            [8.0, 14.0, 23.0, 26.0, 29.0, 17.0, 8.0, 8.0],
            [-3.0, 2.0, 9.5, 12.0, 14.5, 4.5, -3.0, -3.0],
            [-4.0, 0.0, 6.0, 8.0, 10.0, 2.0, -4.0, -4.0],
            [-4.0, -1.0, 3.5, 5.0, 6.5, 0.5, -4.0, -4.0],
            [-2.0, 0.0, 3.0, 4.0, 5.0, 1.0, -2.0, -2.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
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
                                value -= -8.0
                            else:
                                value -= 100.0 + field_values[x][y]
                        elif 'R' in piece:
                            value -= 500.0 + 1.5 * self.protectedRook(x, y, state.board)
                        elif 'B' in piece:
                            value -= 300.0 + 2.0 * self.protectedBishop(x, y, state.board)
                        elif 'Q' in piece:
                            mult = self.protectedBishop(x, y, state.board) + self.protectedRook(x, y, state.board) - 1
                            value -= 900.0 + 1.0 * mult
                        elif 'K' in piece:
                            value -= 10000.0
                        elif 'N' in piece:
                            value -= 300 + 3.0 * (4 - self.distanceToCenter(y))
                        elif state.checkMate:
                            value -= 2500

                    if 'b' in piece:
                        if 'p' in piece:
                            if state.board[x + 1][y] == 'bp':
                                value += -8.0
                            else:
                                value += 100.0 + rev_field_values[x][y]
                        elif 'R' in piece:
                            value += 500.0 + 1.5 * self.protectedRook(x, y, state.board)
                        elif 'B' in piece:
                            value += 300.0 + 2.0 * self.protectedBishop(x, y, state.board)
                        elif 'Q' in piece:
                            mult = self.protectedBishop(x, y, state.board) + self.protectedRook(x, y, state.board) - 1
                            value += 900 + 1.0 * mult
                        elif 'K' in piece:
                            value += 10000.0
                        elif 'N' in piece:
                            value += 300 + 3.0 * (4 - self.distanceToCenter(y))
                        elif state.checkMate:
                            value += 2500
        else:
            for x, row in enumerate(state.board):
                for y, piece in enumerate(row):
                    if 'b' in piece:
                        if 'p' in piece:
                            if state.board[x - 1][y] == "bp":
                                value -= -8.0
                            else:
                                value -= 100.0 + rev_field_values[x][y]
                        elif 'R' in piece:
                            value -= 500.0 + 1.5 * self.protectedRook(x, y, state.board)
                        elif 'B' in piece:
                            value -= 300.0 + 2.0 * self.protectedBishop(x, y, state.board)
                        elif 'Q' in piece:
                            mult = self.protectedBishop(x, y, state.board) + self.protectedRook(x, y, state.board) - 1
                            value -= 900.0 + 1.0 * mult
                        elif 'K' in piece:
                            value -= 10000.0
                        elif 'N' in piece:
                            value -= 300 + 3.0 * (4 - self.distanceToCenter(y))
                        elif state.checkMate:
                            value -= 2500
                    if 'w' in piece:
                        if 'p' in piece:
                            if state.board[x + 1][y] == 'wp':
                                value += -8.0
                            else:
                                value += 100.0 + field_values[x][y]
                        elif 'R' in piece:
                            value += 500.0 + 1.5 * self.protectedRook(x, y, state.board)
                        elif 'B' in piece:
                            value += 300.0 + 2.0 * self.protectedBishop(x, y, state.board)
                        elif 'Q' in piece:
                            mult = self.protectedBishop(x, y, state.board) + self.protectedRook(x, y, state.board) - 1
                            value += 900 + 1.0 * mult
                        elif 'K' in piece:
                            value += 10000.0
                        elif 'N' in piece:
                            value += 300 + 3.0 * (4 - self.distanceToCenter(y))
                        elif state.checkMate:
                            value += 2500
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

    def copyState(self, original, copy):
        copy.board = c.deepcopy(original.board)
        copy.whiteToMove = c.deepcopy(original.whiteToMove)
        copy.moveLog = c.deepcopy(original.moveLog)
        copy.whiteKingLoc = c.deepcopy(original.whiteKingLoc)
        copy.blackKingLoc = c.deepcopy(original.blackKingLoc)
        copy.staleMate = c.deepcopy(original.staleMate)
        copy.checkMate = c.deepcopy(original.checkMate)

    def minMax(self, state, depth, maximizingPlayer, beta=sys.maxsize):
        if depth == 0:
            return self.get_board_value(state)
        elif maximizingPlayer:
            value = -sys.maxsize - 1
            children = self.expandChildren(state)
            for child in children:
                value = max(value, self.minMax(child[0], depth - 1, False, beta))
                self.alpha = max(self.alpha, value)
                self.numberStates += 1
                if beta <= self.alpha:
                    break
            if len(children) == 0:
                return -1000
            return value
        else:
            value = sys.maxsize
            children = self.expandChildren(state)
            for child in children:
                value = min(value, self.minMax(child[0], depth - 1, False, beta))
                beta = min(beta, value)
                self.numberStates += 1
                if beta <= self.alpha:
                    break
            if len(children) == 0:
                return -1000
            return value

    def makeMove(self):
        if not self.openingMove:
            children = self.expandChildren(self.state)
            values = []
            for child in children:
                values.append(self.minMax(child[0], 3, True))
            print("number of states: " + str(self.numberStates))
            print("Max value " + str(values[values.index(max(values))]))
            self.numberStates = 0
            self.knownBoards = []
            self.alpha = -sys.maxsize - 1
            self.state.makeMove(children[values.index(max(values))][1], True)
        elif self.openingMove and self.state.whiteToMove:
            self.state.makeMove(random.choice(self.whiteOpeners), True)
        elif self.openingMove and not self.state.whiteToMove:
            if self.state.board[4][4] == "wp":
                self.state.makeMove(ChessEngine.Move((1, 4), (3, 4), self.state.board), True)
            elif self.state.board[4][3] == "wp":
                self.state.makeMove(ChessEngine.Move((1, 3), (3, 3), self.state.board), True)

