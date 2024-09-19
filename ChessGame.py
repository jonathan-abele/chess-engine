"""
This class will maintain the state of the game by keeping track of where the pieces are on the board.
It will keep track of whos turn it is.
It will aslo keep a move log of the game.
"""

def isPieceWhite (piece):
        if (piece[0] == 'w'):
            return True
        else:
            return False
        
def isPieceBlack (piece):
    if (piece[0] == 'b'):
        return True
    else:
        return False


class GameState():

    def __init__ (self):

        # 2d array to represent the board
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]

        self.whiteToMove = True
        self.gameLog = []

    def move (self, first_square, second_square):
        self.board[second_square[0]][second_square[1]] = self.board[first_square[0]][first_square[1]]
        self.board[first_square[0]][first_square[1]] = '--'


        self.whiteToMove = not self.whiteToMove

    def checkIfCanSelect (self, square):
        piece = self.board[square[0]][square[1]]

        if self.whiteToMove and isPieceWhite(piece):
            return True
        elif not self.whiteToMove and isPieceBlack(piece):
            return True
        else:
            return False
        

    def get_all_possible_moves (self):
        
        moves = []

        for r in range(self.board):
            for c in range(self.board[r]):
                if self.board[r][c] is not "--":
                    color = self.board[r][c][0]
                    if (color == 'w' and self.whiteToMove) or (color == 'w' and self.whiteToMove):
                        piece = self.board[r][c][1]

                        if piece == 'P':
                            moves.append(self.get_pawn_moves(r, c))
                        if piece == 'R':
                            moves.append(self.get_rook_moves(r, c))
                        if piece == 'B':
                            moves.append(self.get_bishop_moves(r, c))
                        if piece == 'N':
                            moves.append(self.get_knight_moves(r, c))
                        if piece == 'Q':
                            moves.append(self.get_queen_moves(r, c))
                        if piece == 'K':
                            moves.append(self.get_king_moves(r, c))




    def get_pawn_moves(self, r, c):
        pass

    def get_rook_moves(self, r, c):
        pass

    def get_bishop_moves(self, r, c):
        pass

    def get_knight_moves(self, r, c):
        pass

    def get_queen_moves(self, r, c):
        pass

    def get_king_moves(self, r, c):
        pass


        


class Move():

    # Dictionaries that change row to 

    # Inializes a move object
    def __init__ (self, start_square, end_square, board):
        pass


    # Gets the chess notation from the starting square and ending
    def get_chess_notation():
        pass