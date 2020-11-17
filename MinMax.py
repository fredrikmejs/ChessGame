import ChessEngine

class MinMax:
    def __init__(self, GameState):
        self.state = ChessEngine.GameState()
        print(self.state.board)
        self.state.board = GameState.board
        print(self.state.board)
    
    def switchturn(self):
        if self.player == "w":
            self.player = "b"
        elif self.player == "b":
            self.player = "w"
   
    #evaluation function, values taken from notes.
    def get_board_value(self, board):
        value = 0.0
        #checks if it's white's turn to move, and sets player.
        player = self.player
        #field values, taken from slides.
        field_values = [
            [0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 ],
            [23.0, 30.0, 41.5, 44.0, 47.5, 33.5, 23.0, 23.0],
            [8.0 , 14.0, 23.0, 26.0, 29.0, 17.0, 8.0 , 8.0 ],
            [-3.0, 2.0 , 9.5 , 12.0, 14.5, 4.5 , -3.0, -3.0],
            [-4.0, 0.0 , 6.0 , 8.0 , 10.0, 2.0 , -4.0, -4.0],
            [-4.0, -1.0, 3.5 , 5.0 , 6.5 , 0.5 , -4.0, -4.0],
            [-2.0, 0.0 , 3.0 , 4.0 , 5.0 , 1.0 , -2.0, -2.0],
            [0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 ]]
        #reverses the field_values array
        rev_field_values = field_values[::-1]
        #reverses each row in the fied_values array
        for index, row in enumerate(rev_field_values):
            rev_field_values[index] = row[::-1]
        if player == 'w':
            for x, row in enumerate(board):
                for y, piece in enumerate(row):
                    if 'w' in piece:
                        if 'p' in piece:
                            if board[x-1][y] == "wp":
                                value += -8.0
                            else:
                                value += 100.0 + field_values[x][y]
                        if 'R' in piece:
                            value += 500.0 + 1.5 * self.protectedRook(x, y, board)
                        if 'B' in piece:
                            value += 300.0 + 2.0 * self.protectedBishop(x, y, board)
                        if 'Q' in piece:
                            mult = self.protectedBishop(x, y, board) + self.protectedRook(x, y, board) - 1
                            value += 900.0 + 1.0 * mult
                        if 'K' in piece:
                            value += 10000.0
                        if 'N' in piece:
                            value += 300 + 3.0 * (4 - self.distanceToCenter(y))
                    if 'b' in piece:
                        if 'p' in piece:
                            if board[x+1][y] == 'bp':
                                value -= -8.0
                            else:
                                value -= 100.0 + rev_field_values[x][y]
                        if 'R' in piece:
                            value -= 500.0 + 1.5 * self.protectedRook(x, y, board)
                        if 'B' in piece:
                            value -= 300.0 + 2.0 * self.protectedBishop(x, y, board)
                        if 'Q' in piece:
                            mult = self.protectedBishop(x, y, board) + self.protectedRook(x, y, board) - 1
                            value -= 900 + 1.0 * mult
                        if 'K' in piece:
                            value -= 10000.0
                        if 'N' in piece:
                            value -= 300 + 3.0 * (4 - self.distanceToCenter(y))
        elif player == 'b':
            for x, row in enumerate(board):
                for y, piece in enumerate(row):
                    if 'b' in piece:
                        if 'p' in piece:
                            if board[x-1][y] == "bp":
                                value += -8.0
                            else:
                                value += 100.0 + rev_field_values[x][y]
                        if 'R' in piece:
                            value += 500.0 + 1.5 * self.protectedRook(x, y, board)
                        if 'B' in piece:
                            value += 300.0 + 2.0 * self.protectedBishop(x, y, board)
                        if 'Q' in piece:
                            mult = self.protectedBishop(x, y, board) + self.protectedRook(x, y, board) - 1
                            value += 900.0 + 1.0 * mult
                        if 'K' in piece:
                            value += 10000.0
                        if 'N' in piece:
                            value += 300 + 3.0 * (4 - self.distanceToCenter(y))
                    if 'w' in piece:
                        if 'p' in piece:
                            if board[x+1][y] == 'wp':
                                value -= -8.0
                            else:
                                value -= 100.0 + field_values[x][y]
                        if 'R' in piece:
                            value -= 500.0 + 1.5 * self.protectedRook(x, y, board)
                        if 'B' in piece:
                            value -= 300.0 + 2.0 * self.protectedBishop(x, y, board)
                        if 'Q' in piece:
                            mult = self.protectedBishop(x, y, board) + self.protectedRook(x, y, board) - 1
                            value -= 900 + 1.0 * mult
                        if 'K' in piece:
                            value -= 10000.0
                        if 'N' in piece:
                            value -= 300 + 3.0 * (4 - self.distanceToCenter(y))
        return value
        
    def protectedRook(self, x , y, board):
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