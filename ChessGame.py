"""
This class will maintain the state of the game by keeping track of where the pieces are on the board.
It will keep track of whos turn it is.
It will aslo keep a move log of the game.
"""



class GameState():

    def __init__ (self):

        # 2d array to represent the board
        self.board = [
            ['bR', 'bK', 'bB', 'bQ', 'bK', 'bB', 'bK', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wK', 'wB', 'wQ', 'wK', 'wB', 'wK', 'wR']
        ]

        self.whiteToMove = True
        self.gameLog = []