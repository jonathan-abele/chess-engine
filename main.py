"""
Responsible for user import and displaying the game
"""

import pygame as p
from ChessGame import GameState

HEIGHT = 512
WIDTH = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15

IMAGES = {}

"""
Initialize a global dictionary of images. Called once at the beginning of the program.
"""
def loadImages():
    pieces = ['wp', 'wK', 'wQ', 'wN', 'wR', 'wB', 'bp', 'bK', 'bQ', 'bN', 'bR', 'bB']

    for piece in pieces:
        IMAGES[piece] = p.image.load("images/" + piece + ".png")

"""
The main driver for program. Handle user input and updating the graphics.
"""
def main():

    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))

    loadImages()

    game = GameState()
    running = True

    square_selected = () # keep track of the last square selected
    first_click = False

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:

                first_click = not first_click 

                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                clicked_square = (row, col)

                if first_click:
                    if game.checkIfCanSelect(clicked_square):
                        square_selected = clicked_square
                    else:
                        first_click = False
                else:
                    game.move(square_selected, clicked_square)
                    square_selected = ()
             

        drawGameState(screen, game, square_selected)
        clock.tick(MAX_FPS)
        p.display.flip()



def drawGameState(screen, game, square_selected):
    drawBoard(screen, square_selected) # draw squares on the board
    drawPieces(screen, game.board)

"""
Draw the squares on the board
"""
def drawBoard(screen, square_selected):
    colors = [p.Color('white'), p.Color('gray')]


    for r in range (DIMENSION):
        for c in range (DIMENSION):
            color = colors[(r+c) % 2]
        
            if len(square_selected) != 0 and r == square_selected[0] and c == square_selected[1]:
                p.draw.rect(screen, p.Color(173, 216, 230), p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            else:
                p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
          

"""
Draw the pieces on the board using the current GameState.board
"""
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))



if __name__ == "__main__":
    main()