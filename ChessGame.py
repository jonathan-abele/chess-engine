"""
This class will maintain the state of the game by keeping track of where the pieces are on the board.
It will keep track of whos turn it is.
It will aslo keep a move log of the game.
"""


KING_WEIGHT = 200
QUEEN_WEIGHT = 9
ROOK_WEIGHT = 5
BISHOP_WEIGHT = 3
KNIGHT_WEIGHT = 3
PAWN_WEIGHT = 1

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

    # Dictionaries that change row to rank and col to file
    row_to_rank = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}
    col_to_file = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

    rank_to_row = {'8': 0, '7': 1, '6': 2,'5': 3, '4': 4, '3': 5, '2': 6, '1': 7}
    file_to_col = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

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

        self.white_king_loc = (7, 4)
        self.black_king_loc = (0, 4)

        self.white_can_castle_short = True
        self.white_can_castle_long = True
        self.black_can_castle_short = True
        self.black_can_castle_long = True


        self.piece_count = {'wp': 8, 'wR': 2, 'wN': 2, 'wB': 2, 'wQ': 1, 'wK': 1, 'bp': 8, 'bR': 2, 'bN': 2, 'bB': 2, 'bQ': 1, 'bK': 1}

        self.whiteToMove = True
        self.gameLog = []
        self.game_over = False

    def make_move (self, first_square, second_square):
        notation = self.Move(first_square, second_square)
        
        r1 = first_square[0]
        c1 = first_square[1]
        r2 = second_square[0]
        c2 = second_square[1]

        # For move undo
        before_castle_situation = [self.white_can_castle_short, self.white_can_castle_long, self.black_can_castle_short, self.black_can_castle_long]
        second_piece = self.board[r2][c2]
        was_pawn_promotion = False

        # Handle Castling
        if notation == 'O-O':
            if self.whiteToMove:
                self.board[7][6] = 'wK'
                self.board[7][5] = 'wR'
                self.board[7][4] = '--'
                self.board[7][7] = '--'
                self.white_king_loc = (7, 6)
                self.white_can_castle_short = False
                self.white_can_castle_long = False
            else:
                self.board[0][6] = 'bK'
                self.board[0][5] = 'bR'
                self.board[0][4] = '--'
                self.board[0][7] = '--'
                self.black_king_loc = (0, 6)
                self.black_can_castle_short = False
                self.black_can_castle_long = False
        elif notation == 'O-O-O':
            if self.whiteToMove:
                self.board[7][2] = 'wK'
                self.board[7][3] = 'wR'
                self.board[7][4] = '--'
                self.board[7][0] = '--'
                self.white_king_loc = (7, 2)
                self.white_can_castle_short = False
                self.white_can_castle_long = False
            else:
                self.board[0][2] = 'bK'
                self.board[0][3] = 'bR'
                self.board[0][4] = '--'
                self.board[0][0] = '--'
                self.black_king_loc = (0, 2)
                self.black_can_castle_short = False
                self.black_can_castle_long = False
        else:
            # Handle captures
            square_landed_on = self.board[r2][c2]
            if square_landed_on != '--':
                self.piece_count[square_landed_on] -= 1

            if self.board[r1][c1] == 'wK':
                self.white_king_loc = (r2, c2)
                self.white_can_castle_short = False
                self.white_can_castle_long = False
            if self.board[r1][c1] == 'bK':
                self.black_king_loc = (r2, c2)
                self.black_can_castle_short = False
                self.black_can_castle_long = False

            if self.board[r1][c1] == 'wR':
                if r1 == 7 and c1 == 7:
                    self.white_can_castle_short = False
                if r1 == 7 and c1 == 0:
                    self.white_can_castle_long = False
            if self.board[r1][c1] == 'bR':
                if r1 == 0 and c1 == 7:
                    self.black_can_castle_short = False
                if r1 == 0 and c1 == 0:
                    self.black_can_castle_long = False

            if self.board[r1][c1] == 'wp' and r2 == 0: # White pawn Promotion
                self.board[r2][c2] = 'wQ'
                was_pawn_promotion = True
            elif self.board[r1][c1] == 'bp' and r2 == 7: # Black pawn Promotion
                self.board[r2][c2] = 'bQ'
                was_pawn_promotion = True
            else:
                self.board[r2][c2] = self.board[r1][c1]
            
            self.board[r1][c1] = '--'

        self.gameLog.append(notation)
        self.whiteToMove = not self.whiteToMove

        next_moves = self.get_all_possible_moves()
        if len(next_moves) == 0:
            self.game_over = True


        return (second_piece, before_castle_situation, was_pawn_promotion, self.game_over)

    """"
    before_castling: 
    before_castle_situation = [self.white_can_castle_short, self.white_can_castle_long, self.black_can_castle_short, self.black_can_castle_long]

    second_piece: The piece that was on the second square before the chosen piece moved there. Could just be '--' for empty
    """
    def undo_move(self, first_square, second_square, second_piece, before_castling_situation, was_pawn_promotion, ended_game):
         # Flip who's move it is
        self.whiteToMove = not self.whiteToMove

        notation = self.gameLog.pop()
        # Handle Castling
        if notation == 'O-O':
            if self.whiteToMove:
                self.board[7][6] = '--'
                self.board[7][5] = '--'
                self.board[7][4] = 'wK'
                self.board[7][7] = 'wR'
                self.white_king_loc = (7, 4)
                self.white_can_castle_short = True
                self.white_can_castle_long = True
            else:
                self.board[0][6] = '--'
                self.board[0][5] = '--'
                self.board[0][4] = 'bK'
                self.board[0][7] = 'bR'
                self.black_king_loc = (0, 4)
                self.black_can_castle_short = True
                self.black_can_castle_long = True
        elif notation == 'O-O-O':
            if self.whiteToMove:
                self.board[7][2] = '--'
                self.board[7][3] = '--'
                self.board[7][4] = 'wK'
                self.board[7][0] = 'wR'
                self.white_king_loc = (7, 4)
                self.white_can_castle_short = True
                self.white_can_castle_long = True
            else:
                self.board[0][2] = '--'
                self.board[0][3] = '--'
                self.board[0][4] = 'bK'
                self.board[0][0] = 'bR'
                self.black_king_loc = (0, 4)
                self.black_can_castle_short = True
                self.black_can_castle_long = True
        
        else:
            r1 = first_square[0]
            c1 = first_square[1]
            r2 = second_square[0]
            c2 = second_square[1]

            if second_piece != '--':
                self.piece_count[second_piece] += 1

            # Handle king moves and castling permissions
            if self.board[r2][c2] == 'wK':
                self.white_king_loc = (r1, c1)
                if before_castling_situation[0]:
                    self.white_can_castle_short = True
                elif before_castling_situation[1]:
                    self.white_can_castle_long = True
            if self.board[r2][c2] == 'bK':
                self.black_king_loc = (r1, c1)
                if before_castling_situation[2]:
                    self.black_can_castle_short = True
                elif before_castling_situation[3]:
                    self.black_can_castle_long = True

            # Handle rook moves and castling permissions
            if self.board[r2][c2] == 'wR':
                if before_castling_situation[0]:
                    self.white_can_castle_short = True
                if before_castling_situation[1]:
                    self.white_can_castle_long = True
            if self.board[r2][c2] == 'bR':
                if before_castling_situation[2]:
                    self.black_can_castle_short = True
                if before_castling_situation[3]:
                    self.black_can_castle_long = True

            if was_pawn_promotion:
                self.board[r2][c2] = second_piece
                if self.whiteToMove:
                    self.board[r1][c1] = 'wp'
                else:
                    self.board[r1][c1] = 'bp'

            else: 
                self.board[r1][c1] = self.board[r2][c2]
                self.board[r2][c2] = second_piece
            
            if ended_game:
                self.game_over = False

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

        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c] != "--":
                    color = self.board[r][c][0]
                    if (color == 'w' and self.whiteToMove) or (color == 'b' and not self.whiteToMove):
                        piece = self.board[r][c][1]

                        if piece == 'p':
                            self.get_pawn_moves(r, c, moves)
                        if piece == 'R':
                            self.get_rook_moves(r, c, moves)
                        if piece == 'B':
                            self.get_bishop_moves(r, c, moves)
                        if piece == 'N':
                            self.get_knight_moves(r, c, moves)
                        if piece == 'Q':
                            self.get_queen_moves(r, c, moves)
                        if piece == 'K':
                            self.get_king_moves(r, c, moves)

        self.get_castle_moves(moves)

        if len(moves) == 0:
            self.game_over = True

        return moves

    # Appends castleing moves to moves if legal
    def get_castle_moves(self, moves):
        is_white = self.whiteToMove

        if is_white:
            if self.white_can_castle_short:
                if self.board[7][5] == '--' and self.board[7][6] == '--': # No pieces between
                    if not self.is_king_attacked_after_move(7,4,7,5) and not self.is_king_attacked_after_move(7,4,7,6):
                        moves.append('O-O')

            if self.white_can_castle_long:
                if self.board[7][3] == '--' and self.board[7][2] == '--' and self.board[7][1] == '--': # No pieces between
                    if not self.is_king_attacked_after_move(7,4,7,3) and not self.is_king_attacked_after_move(7,4,7,2):
                        moves.append('O-O-O')
        else:
            if self.black_can_castle_short:
                if self.board[0][5] == '--' and self.board[0][6] == '--': # No pieces between
                    if not self.is_king_attacked_after_move(0,4,0,5) and not self.is_king_attacked_after_move(0,4,0,6):
                        moves.append('O-O')

            if self.black_can_castle_long:
                if self.board[0][3] == '--' and self.board[0][2] == '--' and self.board[0][1] == '--': # No pieces between
                    if not self.is_king_attacked_after_move(0,4,0,3) and not self.is_king_attacked_after_move(0,4,0,2):
                        moves.append('O-O-O')



    # Adds all valid moves from the pawn at location (r,c)
    def get_pawn_moves(self, r, c, moves):
        is_white = self.whiteToMove

        # White Pawn
        if is_white:
            # Is on starting square
            if r == 6:
                if self.board[r - 1][c] == '--' and self.board[r - 2][c] == '--':
                    if not self.is_king_attacked_after_move(r, c, r - 2, c):
                        moves.append(self.Move((r, c), (r - 2, c)))

            # Forward 1 square
            if self.board[r - 1][c] == '--':
                if not self.is_king_attacked_after_move(r, c, r - 1, c):
                    moves.append(self.Move((r, c), (r - 1, c)))

            # Capture Diagonally
            if c != 7 and self.board[r - 1][c + 1][0] == 'b':
                if not self.is_king_attacked_after_move(r, c, r - 1, c + 1):
                    moves.append(self.Move((r, c), (r - 1, c + 1)))
            
            if c != 0 and self.board[r - 1][c - 1][0] == 'b':
                if not self.is_king_attacked_after_move(r, c, r - 1, c - 1):
                    moves.append(self.Move((r, c), (r - 1, c - 1)))

        # Black Pawn
        else:
            # Is on starting square
            if r == 1:
                if self.board[r + 1][c] == '--' and self.board[r + 2][c] == '--':
                    if not self.is_king_attacked_after_move(r, c, r + 2, c):
                        moves.append(self.Move((r, c), (r + 2, c)))

            # Forward one square
            if self.board[r + 1][c] == '--':
                if not self.is_king_attacked_after_move(r, c, r + 1, c):
                    moves.append(self.Move((r, c), (r + 1, c)))

            # Capture diagonally
            if c != 7 and self.board[r + 1][c + 1][0] == 'w':
                if not self.is_king_attacked_after_move(r, c, r + 1, c + 1):
                    moves.append(self.Move((r, c), (r + 1, c + 1)))
            
            if c != 0 and self.board[r + 1][c - 1][0] == 'w':
                if not self.is_king_attacked_after_move(r, c, r + 1, c - 1):
                    moves.append(self.Move((r, c), (r + 1, c - 1)))
 
    # Adds all valid moves from the rook at location (r,c)
    def get_rook_moves(self, r, c, moves):
        other_color = 'b' if self.whiteToMove else 'w'
        
        # Check all four directions

        # Left 
        check = c - 1 
        while check >= 0:
            if self.board[r][check] == '--':
                if not self.is_king_attacked_after_move(r, c, r, check):
                    moves.append(self.Move((r, c), (r, check)))
            elif self.board[r][check][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, r, check):
                    moves.append(self.Move((r, c), (r, check)))
                break
            else:
                break
            check = check - 1

        # Right
        check = c + 1 
        while check <= 7:
            if self.board[r][check] == '--':
                if not self.is_king_attacked_after_move(r, c, r, check):
                    moves.append(self.Move((r, c), (r, check)))
            elif self.board[r][check][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, r, check):
                    moves.append(self.Move((r, c), (r, check)))
                break
            else:
                break
            check = check + 1

        # Up 
        check = r - 1 
        while check >= 0:
            if self.board[check][c] == '--':
                if not self.is_king_attacked_after_move(r, c, check, c):
                    moves.append(self.Move((r, c), (check, c)))
            elif self.board[check][c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check, c):
                    moves.append(self.Move((r, c), (check, c)))
                break
            else:
                break
            check = check - 1

        # Down
        check = r + 1 
        while check <= 7:
            if self.board[check][c] == '--':
                if not self.is_king_attacked_after_move(r, c, check, c):
                    moves.append(self.Move((r, c), (check, c)))
            elif self.board[check][c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check, c):
                    moves.append(self.Move((r, c), (check, c)))
                break
            else:
                break
            check = check + 1
        
    # Adds all valid moves from the bisop at location (r,c)
    def get_bishop_moves(self, r, c, moves):
        other_color = 'b' if self.whiteToMove else 'w'
        
        # Check all four directions

        # Up left 
        check_r = r - 1
        check_c = c - 1 
        while check_r >= 0 and check_c >= 0:
            if self.board[check_r][check_c] == '--':
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(self.Move((r, c), (check_r, check_c)))
            elif self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(self.Move((r, c), (check_r, check_c)))
                break
            else:
                break
            check_r = check_r - 1
            check_c = check_c - 1

        # Bottom Right 
        check_r = r + 1
        check_c = c + 1 
        while check_r <= 7 and check_c <= 7:
            if self.board[check_r][check_c] == '--':
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(self.Move((r, c), (check_r, check_c)))
            elif self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(self.Move((r, c), (check_r, check_c)))
                break
            else:
                break
            check_r = check_r + 1
            check_c = check_c + 1

        # Up Right 
        check_r = r - 1
        check_c = c + 1 
        while check_r >= 0 and check_c <= 7:
            if self.board[check_r][check_c] == '--':
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(self.Move((r, c), (check_r, check_c)))
            elif self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(self.Move((r, c), (check_r, check_c)))
                break
            else:
                break
            check_r = check_r - 1
            check_c = check_c + 1

        # Bottom Left 
        check_r = r + 1
        check_c = c - 1 
        while check_r <= 7 and check_c >= 0:
            if self.board[check_r][check_c] == '--':
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(self.Move((r, c), (check_r, check_c)))
            elif self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(self.Move((r, c), (check_r, check_c)))
                break
            else:
                break
            check_r = check_r + 1
            check_c = check_c - 1

    # Adds all valid moves from the knight at location (r,c)
    def get_knight_moves(self, r, c, moves):
        other_color = 'b' if self.whiteToMove else 'w'

        # Up left 
        check_r = r - 1
        check_c = c - 2 
        if check_r >= 0 and check_c >= 0:
            if self.board[check_r][check_c] == '--' or self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(self.Move((r, c), (check_r, check_c)))

        check_r = r - 2
        check_c = c - 1 
        if check_r >= 0 and check_c >= 0:
            if self.board[check_r][check_c] == '--' or self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(self.Move((r, c), (check_r, check_c)))


        # Bottom Right
        check_r = r + 1
        check_c = c + 2 
        if check_r <= 7 and check_c <= 7:
            if self.board[check_r][check_c] == '--' or self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(self.Move((r, c), (check_r, check_c)))

        check_r = r + 2
        check_c = c + 1 
        if check_r <= 7 and check_c <= 7:
            if self.board[check_r][check_c] == '--' or self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(self.Move((r, c), (check_r, check_c)))

        # Up Right 
        check_r = r - 1
        check_c = c + 2 
        if check_r >= 0 and check_c <= 7:
            if self.board[check_r][check_c] == '--' or self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(self.Move((r, c), (check_r, check_c)))

        check_r = r - 2
        check_c = c + 1 
        if check_r >= 0 and check_c <= 7:
            if self.board[check_r][check_c] == '--' or self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(self.Move((r, c), (check_r, check_c)))

        # Bottom Left
        check_r = r + 1
        check_c = c - 2 
        if check_r <= 7 and check_c >= 0:
            if self.board[check_r][check_c] == '--' or self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(self.Move((r, c), (check_r, check_c)))

        check_r = r + 2
        check_c = c - 1 
        if check_r <= 7 and check_c >= 0:
            if self.board[check_r][check_c] == '--' or self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(self.Move((r, c), (check_r, check_c)))
        
    # Adds all valid moves from the queen at location (r,c)
    def get_queen_moves(self, r, c, moves):
        self.get_rook_moves(r, c, moves)
        self.get_bishop_moves(r, c, moves)

    # Adds all valid moves from the queen at location (r,c)
    def get_king_moves(self, r, c, moves):
        other_color = 'b' if self.whiteToMove else 'w'
        
        # Check all four directions

        # Left 
        check = c - 1 
        if check >= 0:
            if self.board[r][check] == '--' or self.board[r][check][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, r, check):
                    moves.append(self.Move((r, c), (r, check)))

        # Right
        check = c + 1 
        if check <= 7:
            if self.board[r][check] == '--' or self.board[r][check][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, r, check):
                    moves.append(self.Move((r, c), (r, check)))

        # Up 
        check = r - 1 
        if check >= 0:
            if self.board[check][c] == '--' or self.board[check][c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check, c):
                    moves.append(self.Move((r, c), (check, c)))
            
        # Down
        check = r + 1 
        if check <= 7:
            if self.board[check][c] == '--' or self.board[check][c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check, c):
                    moves.append(self.Move((r, c), (check, c)))

        # Up left 
        check_r = r - 1
        check_c = c - 1 
        if check_r >= 0 and check_c >= 0:
            if self.board[check_r][check_c] == '--' or self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(self.Move((r, c), (check_r, check_c)))

        # Bottom Right 
        check_r = r + 1
        check_c = c + 1 
        if check_r <= 7 and check_c <= 7:
            if self.board[check_r][check_c] == '--' or self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(self.Move((r, c), (check_r, check_c)))

        # Up Right 
        check_r = r - 1
        check_c = c + 1 
        if check_r >= 0 and check_c <= 7:
            if self.board[check_r][check_c] == '--' or self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(self.Move((r, c), (check_r, check_c)))

        # Bottom Left 
        check_r = r + 1
        check_c = c - 1 
        if check_r <= 7 and check_c >= 0:
            if self.board[check_r][check_c] == '--' or self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(self.Move((r, c), (check_r, check_c)))

    # Makes the offered move and tests to see if the king is attacked after making that move
    def is_king_attacked_after_move(self, first_r, first_c, second_r, second_c):
        is_white = self.whiteToMove
        other_color = 'b' if is_white else 'w'


        # Save squares previous pieces
        first_square_piece = self.board[first_r][first_c]
        second_square_piece = self.board[second_r][second_c]
        
        # If the king is the piece moved
        if first_square_piece[1] == 'K':
            if is_white:
                self.white_king_loc = (second_r, second_c)
            else:
                self.black_king_loc = (second_r, second_c)
                
        king_r = self.white_king_loc[0] if is_white else self.black_king_loc[0]
        king_c = self.white_king_loc[1] if is_white else self.black_king_loc[1]

        # Make move
        self.board[second_r][second_c] = self.board[first_r][first_c]
        self.board[first_r][first_c] = '--'

        # Revert Move
        def revert_move():
            self.board[first_r][first_c] = first_square_piece
            self.board[second_r][second_c] = second_square_piece

            if first_square_piece[1] == 'K':
                if is_white:
                    self.white_king_loc = (first_r, first_c)
                else:
                    self.black_king_loc = (first_r, first_c)

        ## Start Row Check ##

        check_r = king_r + 1
        while check_r <= 7:
            check_piece = self.board[check_r][king_c]
            if check_piece[0] == other_color and (check_piece[1] == 'Q' or check_piece[1] == 'R'):
                revert_move()
                return True
            if check_piece != '--':
                break
            check_r = check_r + 1

        check_r = king_r - 1
        while check_r >= 0:
            check_piece = self.board[check_r][king_c]
            if check_piece[0] == other_color and (check_piece[1] == 'Q' or check_piece[1] == 'R'):
                revert_move()
                return True
            if check_piece != '--':
                break
            check_r = check_r - 1

        ## End Row Check ##

        ## Start Column Check ##
        
        check_c = king_c + 1
        while check_c <= 7:
            check_piece = self.board[king_r][check_c]
            if check_piece[0] == other_color and (check_piece[1] == 'Q' or check_piece[1] == 'R'):
                revert_move()
                return True
            if check_piece != '--':
                break
            check_c = check_c + 1

        check_c = king_c - 1
        while check_c >= 0:
            check_piece = self.board[king_r][check_c]
            if check_piece[0] == other_color and (check_piece[1] == 'Q' or check_piece[1] == 'R'):
                revert_move()
                return True
            if check_piece != '--':
                break
            check_c = check_c - 1

        ## End Column Check ##

        ## Start Diagonal Check ##

        # Up left 
        check_r = king_r - 1
        check_c = king_c - 1 
        pawn_check = False
        while check_r >= 0 and check_c >= 0:
            check_piece = self.board[check_r][check_c]
            if check_piece[0] == other_color and (check_piece[1] == 'Q' or check_piece[1] == 'B'):
                revert_move()
                return True
            if check_piece != '--':
                break
            check_r = check_r - 1
            check_c = check_c - 1

        # Bottom Right 
        check_r = king_r + 1
        check_c = king_c + 1 
        while check_r <= 7 and check_c <= 7:
            check_piece = self.board[check_r][check_c]
            if check_piece[0] == other_color and (check_piece[1] == 'Q' or check_piece[1] == 'B'):
                revert_move()
                return True
            if check_piece != '--':
                break
            check_r = check_r + 1
            check_c = check_c + 1

        # Up Right 
        check_r = king_r - 1
        check_c = king_c + 1 
        while check_r >= 0 and check_c <= 7:
            check_piece = self.board[check_r][check_c]
            if check_piece[0] == other_color and (check_piece[1] == 'Q' or check_piece[1] == 'B'):
                revert_move()
                return True
            if check_piece != '--':
                break
            check_r = check_r - 1
            check_c = check_c + 1

        # Bottom Left 
        check_r = king_r + 1
        check_c = king_c - 1 
        while check_r <= 7 and check_c >= 0:
            check_piece = self.board[check_r][check_c]
            if check_piece[0] == other_color and (check_piece[1] == 'Q' or check_piece[1] == 'B'):
                revert_move()
                return True
            if check_piece != '--':
                break
            check_r = check_r + 1
            check_c = check_c - 1

        ## End Diagonal Check ##

        ## Start Knight Moves Check ##

        # Up left 
        check_r = king_r - 1
        check_c = king_c - 2 
        if check_r >= 0 and check_c >= 0:
            if self.board[check_r][check_c][0] == other_color and self.board[check_r][check_c][1] == 'N':
                revert_move()
                return True

        check_r = king_r - 2
        check_c = king_c - 1 
        if check_r >= 0 and check_c >= 0:
            if self.board[check_r][check_c][0] == other_color and self.board[check_r][check_c][1] == 'N':
                revert_move()
                return True


        # Bottom Right
        check_r = king_r + 1
        check_c = king_c + 2 
        if check_r <= 7 and check_c <= 7:
            if self.board[check_r][check_c][0] == other_color and self.board[check_r][check_c][1] == 'N':
                revert_move()
                return True

        check_r = king_r + 2
        check_c = king_c + 1 
        if check_r <= 7 and check_c <= 7:
            if self.board[check_r][check_c][0] == other_color and self.board[check_r][check_c][1] == 'N':
                revert_move()
                return True

        # Up Right 
        check_r = king_r - 1
        check_c = king_c + 2 
        if check_r >= 0 and check_c <= 7:
            if self.board[check_r][check_c][0] == other_color and self.board[check_r][check_c][1] == 'N':
                revert_move()
                return True

        check_r = king_r - 2
        check_c = king_c + 1 
        if check_r >= 0 and check_c <= 7:
            if self.board[check_r][check_c][0] == other_color and self.board[check_r][check_c][1] == 'N':
                revert_move()
                return True

        # Bottom Left
        check_r = king_r + 1
        check_c = king_c - 2 
        if check_r <= 7 and check_c >= 0:
            if self.board[check_r][check_c][0] == other_color and self.board[check_r][check_c][1] == 'N':
                revert_move()
                return True

        check_r = king_r + 2
        check_c = king_c - 1 
        if check_r <= 7 and check_c >= 0:
            if self.board[check_r][check_c][0] == other_color and self.board[check_r][check_c][1] == 'N':
                revert_move()
                return True

        ## End Knight Moves ## 


        ## Start pawn check ##

        if is_white:
            # Up left 
            check_r = king_r - 1
            check_c = king_c - 1 
            if check_r >= 0 and check_c >= 0:
                check_piece = self.board[check_r][check_c]
                if check_piece[0] == other_color and check_piece[1] == 'p':
                    revert_move()
                    return True
                
            # Up Right 
            check_r = king_r - 1
            check_c = king_c + 1 
            if check_r >= 0 and check_c <= 7:
                check_piece = self.board[check_r][check_c]
                if check_piece[0] == other_color and check_piece[1] == 'p':
                    revert_move()
                    return True
        else:
            # Bottom Right 
            check_r = king_r + 1
            check_c = king_c + 1 
            if check_r <= 7 and check_c <= 7:
                check_piece = self.board[check_r][check_c]
                if check_piece[0] == other_color and check_piece[1] == 'p':
                    revert_move()
                    return True

            # Bottom Left 
            check_r = king_r + 1
            check_c = king_c - 1 
            if check_r <= 7 and check_c >= 0:
                check_piece = self.board[check_r][check_c]
                if check_piece[0] == other_color and check_piece[1] == 'p':
                    revert_move()
                    return True

        ## End pawn check ##

        ## Start King check # 

        check_r = king_r + 1
        if check_r <= 7:
            check_piece = self.board[check_r][king_c]
            if check_piece[0] == other_color and check_piece[1] == 'K':
                revert_move()
                return True

        check_r = king_r - 1
        if check_r >= 0:
            check_piece = self.board[check_r][king_c]
            if check_piece[0] == other_color and check_piece[1] == 'K':
                revert_move()
                return True
        
        check_c = king_c + 1
        if check_c <= 7:
            check_piece = self.board[king_r][check_c]
            if check_piece[0] == other_color and check_piece[1] == 'K':
                revert_move()
                return True

        check_c = king_c - 1
        if check_c >= 0:
            check_piece = self.board[king_r][check_c]
            if check_piece[0] == other_color and check_piece[1] == 'K':
                revert_move()
                return True
        
        # Up left 
        check_r = king_r - 1
        check_c = king_c - 1 
        if check_r >= 0 and check_c >= 0:
            check_piece = self.board[check_r][check_c]
            if check_piece[0] == other_color and check_piece[1] == 'K':
                revert_move()
                return True
            
        # Up Right 
        check_r = king_r - 1
        check_c = king_c + 1 
        if check_r >= 0 and check_c <= 7:
            check_piece = self.board[check_r][check_c]
            if check_piece[0] == other_color and check_piece[1] == 'K':
                revert_move()
                return True
    
        # Bottom Right 
        check_r = king_r + 1
        check_c = king_c + 1 
        if check_r <= 7 and check_c <= 7:
            check_piece = self.board[check_r][check_c]
            if check_piece[0] == other_color and check_piece[1] == 'K':
                revert_move()
                return True

        # Bottom Left 
        check_r = king_r + 1
        check_c = king_c - 1 
        if check_r <= 7 and check_c >= 0:
            check_piece = self.board[check_r][check_c]
            if check_piece[0] == other_color and check_piece[1] == 'K':
                revert_move()
                return True

        ## End King check ## 

        revert_move()
        return False
    
    # Returns the chess notation for the move being made
    def Move(self, start_square, end_square):
        # Castling moves
        if self.board[start_square[0]][start_square[1]] == 'wK' and start_square == (7,4):
            if end_square[0] == 7 and end_square[1] in [6, 7]:
                return 'O-O'
            elif end_square[0] == 7 and end_square[1] in [0, 1, 2]:
                return 'O-O-O' 
        elif self.board[start_square[0]][start_square[1]] == 'bK' and start_square == (0,4):
            if end_square[0] == 0 and end_square[1] in [6, 7]:
                return 'O-O'
            elif end_square[0] == 0 and end_square[1] in [0, 1, 2]:
                return 'O-O-O'

        start = self.col_to_file[start_square[1]] + self.row_to_rank[start_square[0]]
        end = self.col_to_file[end_square[1]] + self.row_to_rank[end_square[0]]
        
        return start + end
    
    def notation_to_squares(self, notation):
        is_white = self.whiteToMove
        if notation == 'O-O':
            if is_white:
                return (7, 4), (7,6)
            else:
                return (0,4), (0, 6)
        elif notation == 'O-O-O':
            if is_white:
                return (7, 4), (7,2)
            else:
                return (0,4), (0, 2)
            
        return (self.rank_to_row[notation[1]], self.file_to_col[notation[0]],), (self.rank_to_row[notation[3]], self.file_to_col[notation[2]])



    def evaluate(self):

        kings = KING_WEIGHT * (self.piece_count['wK'] - self.piece_count['bK'])
        queens = QUEEN_WEIGHT * (self.piece_count['wQ'] - self.piece_count['bQ'])
        rooks = ROOK_WEIGHT * (self.piece_count['wR'] - self.piece_count['bR'])
        bishops = BISHOP_WEIGHT * (self.piece_count['wB'] - self.piece_count['bB'])
        knights = KNIGHT_WEIGHT * (self.piece_count['wN'] - self.piece_count['bN'])
        pawns = PAWN_WEIGHT * (self.piece_count['wp'] - self.piece_count['bp'])


        return kings + queens + rooks + bishops + knights + pawns 

    def alpha_beta_max (self, alpha, beta, depth):
    
        if depth == 0:
            return self.evaluate(), '--'
        
        best_score = float('-inf')
        best_move = None
        moves = self.get_all_possible_moves()

        for move in moves:
            first_square, second_square = self.notation_to_squares(move)
            second_piece, before_castling, was_pawn_promoted, ended_game = self.make_move(first_square, second_square)
            score, next_best_move = self.alpha_beta_min(alpha, beta, depth - 1)
            self.undo_move(first_square, second_square, second_piece, before_castling, was_pawn_promoted, ended_game)
            if score > best_score:
                best_score = score
                best_move = move
                if score > alpha:
                    alpha = score # Works as the global max
            if score >= beta:
                return score, move
            
        return best_score, best_move

    def alpha_beta_min (self, alpha, beta, depth):

        if depth == 0:
            return self.evaluate(), '--'
        
        best_score = float('inf')
        best_move = None
        moves = self.get_all_possible_moves()

        for move in moves:
            first_square, second_square = self.notation_to_squares(move)
            second_piece, before_castling, was_pawn_promoted, ended_game = self.make_move(first_square, second_square)
            score, next_best_move = self.alpha_beta_max(alpha, beta, depth - 1)
            self.undo_move(first_square, second_square, second_piece, before_castling, was_pawn_promoted, ended_game)
            if score < best_score:
                best_score = score
                best_move = move

                if score < beta:
                    beta = score

            if score <= alpha:
                return score, move
            
        return best_score, best_move


"""
class Move():
    # Dictionaries that change row to rank and col to file
    row_to_rank = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}
    col_to_file = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

    # Inializes a move object
    def __init__ (self, start_square, end_square):
        self.start = self.col_to_file[start_square[1]] + self.row_to_rank[start_square[0]]
        self.end = self.col_to_file[end_square[1]] + self.row_to_rank[end_square[0]]
        self.notation = self.start + self.end

    # Gets the chess notation from the starting square and ending
    def get_chess_notation(self):
        return self.notation
"""
