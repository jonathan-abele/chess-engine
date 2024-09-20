"""
Responsible for user import and displaying the game
"""

import pygame as p
from ChessGame import GameState
from ChessGame import Move

HEIGHT = 600
WIDTH = 600
BOARD_HEIGHT = 512
BOARD_WIDTH = 512
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
WHITE = p.Color('white')
GRAY = p.Color('gray')
SELECTED_SQUARE_COLOR = p.Color(173, 216, 230)

# Calculate the offset for the board to be centered inside the black area
board_x_offset = (WIDTH - BOARD_WIDTH) // 2
board_y_offset = (HEIGHT - BOARD_HEIGHT) // 2

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
    screen.fill(p.Color('black'))

    loadImages()

    game = GameState()
    running = True

    

    square_selected = () # keep track of the last square selected
    first_click = True

    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:

                possible_moves = game.get_all_possible_moves()

                location = p.mouse.get_pos()
                clicked_square = getBoardSquare(location)

                # Clicked off of chess board
                if clicked_square is None:
                    first_click = True
                    square_selected = ()
                    continue
                
                if first_click:
                    if game.checkIfCanSelect(clicked_square): # selected piece of right color
                        square_selected = clicked_square
                        first_click = False
                    else:
                        first_click = True        
                else:
                    if Move(square_selected, clicked_square) in possible_moves: # chose a valid square to move to
                        game.make_move(square_selected, clicked_square)
                        square_selected = ()
                        first_click = True
                    elif game.checkIfCanSelect(clicked_square): # Choosing to move another piece
                        square_selected = clicked_square
                        firt_click = False
                    else: # not a valid square to move to
                        square_selected = ()
                        first_click = True
                        

        drawGameState(screen, game, square_selected)
        clock.tick(MAX_FPS)
        p.display.flip()

def getBoardSquare(mouse_pos):
    # Unpack mouse position
    mouse_x, mouse_y = mouse_pos

    # Adjust mouse position to be relative to the board
    adjusted_x = mouse_x - board_x_offset
    adjusted_y = mouse_y - board_y_offset

    # Check if the mouse is within the board area
    if 0 <= adjusted_x < BOARD_WIDTH and 0 <= adjusted_y < BOARD_HEIGHT:
        # Calculate the row and column based on the adjusted mouse position
        col = adjusted_x // SQ_SIZE
        row = adjusted_y // SQ_SIZE
        return (int(row), int(col))  # Return the clicked square as (row, col)
    else:
        # Mouse click is outside the board
        return None

def drawGameState(screen, game, square_selected):
    drawBoard(screen, square_selected) # draw squares on the board
    drawPieces(screen, game.board)

"""
Draw the squares on the board
"""
def drawBoard(screen, square_selected):
    colors = [WHITE, GRAY]

    for r in range (DIMENSION):
        for c in range (DIMENSION):
            color = colors[(r+c) % 2]

        
            if len(square_selected) != 0 and r == square_selected[0] and c == square_selected[1]:
                p.draw.rect(screen, SELECTED_SQUARE_COLOR, p.Rect(c*SQ_SIZE + board_x_offset, r*SQ_SIZE + board_y_offset, SQ_SIZE, SQ_SIZE))
            else:
                p.draw.rect(screen, color, p.Rect(c*SQ_SIZE + board_x_offset, r*SQ_SIZE + board_y_offset, SQ_SIZE, SQ_SIZE))
          

"""
Draw the pieces on the board using the current GameState.board
"""
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE + board_x_offset, r*SQ_SIZE + board_y_offset, SQ_SIZE, SQ_SIZE))



if __name__ == "__main__":
    main()