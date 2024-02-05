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
        