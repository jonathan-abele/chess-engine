"""
Responsible for user import and displaying the game
"""


import pygame
from ChessGame import GameState

HEIGHT = 512
WIDTH = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15

IMAGES = {}



def main():

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color('white'))

    game = GameState()

    running = True

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        drawGameState(screen, game)
        clock.tick(MAX_FPS)
        pygame.display.flip()

def drawGameState(screen, game):
    drawBoard(screen) # draw squares on the board


"""
Draw the squares on the board
"""
def drawBoard(screen):
    colors = [pygame.Color('white'), pygame.Color('gray')]

    for r in range (DIMENSION):
        for c in range (DIMENSION):
            color = colors[(r+c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()