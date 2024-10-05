import random




KING_WEIGHT = 200
QUEEN_WEIGHT = 9
ROOK_WEIGHT = 5
BISHOP_WEIGHT = 3
KNIGHT_WEIGHT = 3
PAWN_WEIGHT = 1

# Choses one random move from all possible moves
def get_random_move(possible_moves):
    return random.choice(possible_moves)



"""
Board example: 

['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
['--', '--', '--', '--', '--', '--', '--', '--'],
['--', '--', '--', '--', '--', '--', '--', '--'],
['--', '--', '--', '--', '--', '--', '--', '--'],
['--', '--', '--', '--', '--', '--', '--', '--'],
['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']

piece_count example:

self.whites_piece_count = {'p': 8, 'R': 2, 'N': 2, 'B': 2, 'Q': 1, 'K': 1}
self.black_piece_count = {'p': 8, 'R': 2, 'N': 2, 'B': 2, 'Q': 1, 'K': 1}


"""
def evaluate(piece_count):

    kings = KING_WEIGHT * (piece_count['wK'] - piece_count['bK'])
    queens = QUEEN_WEIGHT * (piece_count['wQ'] - piece_count['bQ'])
    rooks = ROOK_WEIGHT * (piece_count['wR'] - piece_count['bR'])
    bishops = BISHOP_WEIGHT * (piece_count['wB'] - piece_count['bB'])
    knights = KNIGHT_WEIGHT * (piece_count['wN'] - piece_count['bN'])
    pawns = PAWN_WEIGHT * (piece_count['wp'] - piece_count['bp'])


    return kings + queens + rooks + bishops + knights + pawns 



def alpha_beta_max (game_state, alpha, beta, depth, pieces):
    
    if depth == 0:
        return evaluate(game_state.piece_count)