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

        self.white_king_loc = (7, 4)
        self.black_king_loc = (0, 4)

        self.whiteToMove = True
        self.gameLog = []
        self.game_over = False

    def make_move (self, first_square, second_square):
        r1 = first_square[0]
        c1 = first_square[1]
        r2 = second_square[0]
        c2 = second_square[1]

        if self.board[r1][c1] == 'wK':
            self.white_king_loc = (r2, c2)

        if self.board[r1][c1] == 'bK':
            self.black_king_loc = (r2, c2)

        self.board[r2][c2] = self.board[r1][c1]
        self.board[r1][c1] = '--'

        self.gameLog.append(Move(first_square, second_square))

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

        if len(moves) == 0:
            self.game_over = True

        return moves



    # Adds all valid moves from the pawn at location (r,c)
    def get_pawn_moves(self, r, c, moves):
        is_white = self.whiteToMove

        # White Pawn
        if is_white:
            # Is on starting square
            if r == 6:
                if self.board[r - 1][c] == '--' and self.board[r - 2][c] == '--':
                    if not self.is_king_attacked_after_move(r, c, r - 2, c):
                        moves.append(Move((r, c), (r - 2, c)))

            # Forward 1 square
            if self.board[r - 1][c] == '--':
                if not self.is_king_attacked_after_move(r, c, r - 1, c):
                    moves.append(Move((r, c), (r - 1, c)))

            # Capture Diagonally
            if c != 7 and self.board[r - 1][c + 1][0] == 'b':
                if not self.is_king_attacked_after_move(r, c, r - 1, c + 1):
                    moves.append(Move((r, c), (r - 1, c + 1)))
            
            if c != 0 and self.board[r - 1][c - 1][0] == 'b':
                if not self.is_king_attacked_after_move(r, c, r - 1, c - 1):
                    moves.append(Move((r, c), (r - 1, c - 1)))

        # Black Pawn
        else:
            # Is on starting square
            if r == 1:
                if self.board[r + 1][c] == '--' and self.board[r + 2][c] == '--':
                    if not self.is_king_attacked_after_move(r, c, r + 2, c):
                        moves.append(Move((r, c), (r + 2, c)))

            # Forward one square
            if self.board[r + 1][c] == '--':
                if not self.is_king_attacked_after_move(r, c, r + 1, c):
                    moves.append(Move((r, c), (r + 1, c)))

            # Capture diagonally
            if c != 7 and self.board[r + 1][c + 1][0] == 'w':
                if not self.is_king_attacked_after_move(r, c, r + 1, c + 1):
                    moves.append(Move((r, c), (r + 1, c + 1)))
            
            if c != 0 and self.board[r + 1][c - 1][0] == 'w':
                if not self.is_king_attacked_after_move(r, c, r + 1, c - 1):
                    moves.append(Move((r, c), (r + 1, c - 1)))
 
    # Adds all valid moves from the rook at location (r,c)
    def get_rook_moves(self, r, c, moves):
        other_color = 'b' if self.whiteToMove else 'w'
        
        # Check all four directions

        # Left 
        check = c - 1 
        while check >= 0:
            if self.board[r][check] == '--':
                if not self.is_king_attacked_after_move(r, c, r, check):
                    moves.append(Move((r, c), (r, check)))
            elif self.board[r][check][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, r, check):
                    moves.append(Move((r, c), (r, check)))
                break
            else:
                break
            check = check - 1

        # Right
        check = c + 1 
        while check <= 7:
            if self.board[r][check] == '--':
                if not self.is_king_attacked_after_move(r, c, r, check):
                    moves.append(Move((r, c), (r, check)))
            elif self.board[r][check][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, r, check):
                    moves.append(Move((r, c), (r, check)))
                break
            else:
                break
            check = check + 1

        # Up 
        check = r - 1 
        while check >= 0:
            if self.board[check][c] == '--':
                if not self.is_king_attacked_after_move(r, c, check, c):
                    moves.append(Move((r, c), (check, c)))
            elif self.board[check][c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check, c):
                    moves.append(Move((r, c), (check, c)))
                break
            else:
                break
            check = check - 1

        # Down
        check = r + 1 
        while check <= 7:
            if self.board[check][c] == '--':
                if not self.is_king_attacked_after_move(r, c, check, c):
                    moves.append(Move((r, c), (check, c)))
            elif self.board[check][c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check, c):
                    moves.append(Move((r, c), (check, c)))
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
                    moves.append(Move((r, c), (check_r, check_c)))
            elif self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(Move((r, c), (check_r, check_c)))
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
                    moves.append(Move((r, c), (check_r, check_c)))
            elif self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(Move((r, c), (check_r, check_c)))
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
                    moves.append(Move((r, c), (check_r, check_c)))
            elif self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(Move((r, c), (check_r, check_c)))
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
                    moves.append(Move((r, c), (check_r, check_c)))
            elif self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(Move((r, c), (check_r, check_c)))
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
                    moves.append(Move((r, c), (check_r, check_c)))

        check_r = r - 2
        check_c = c - 1 
        if check_r >= 0 and check_c >= 0:
            if self.board[check_r][check_c] == '--' or self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(Move((r, c), (check_r, check_c)))


        # Bottom Right
        check_r = r + 1
        check_c = c + 2 
        if check_r <= 7 and check_c <= 7:
            if self.board[check_r][check_c] == '--' or self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(Move((r, c), (check_r, check_c)))

        check_r = r + 2
        check_c = c + 1 
        if check_r <= 7 and check_c <= 7:
            if self.board[check_r][check_c] == '--' or self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(Move((r, c), (check_r, check_c)))

        # Up Right 
        check_r = r - 1
        check_c = c + 2 
        if check_r >= 0 and check_c <= 7:
            if self.board[check_r][check_c] == '--' or self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(Move((r, c), (check_r, check_c)))

        check_r = r - 2
        check_c = c + 1 
        if check_r >= 0 and check_c <= 7:
            if self.board[check_r][check_c] == '--' or self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(Move((r, c), (check_r, check_c)))

        # Bottom Left
        check_r = r + 1
        check_c = c - 2 
        if check_r <= 7 and check_c >= 0:
            if self.board[check_r][check_c] == '--' or self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(Move((r, c), (check_r, check_c)))

        check_r = r + 2
        check_c = c - 1 
        if check_r <= 7 and check_c >= 0:
            if self.board[check_r][check_c] == '--' or self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(Move((r, c), (check_r, check_c)))
        
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
                    moves.append(Move((r, c), (r, check)))

        # Right
        check = c + 1 
        if check <= 7:
            if self.board[r][check] == '--' or self.board[r][check][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, r, check):
                    moves.append(Move((r, c), (r, check)))

        # Up 
        check = r - 1 
        if check >= 0:
            if self.board[check][c] == '--' or self.board[check][c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check, c):
                    moves.append(Move((r, c), (check, c)))
            
        # Down
        check = r + 1 
        if check <= 7:
            if self.board[check][c] == '--' or self.board[check][c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check, c):
                    moves.append(Move((r, c), (check, c)))

        # Up left 
        check_r = r - 1
        check_c = c - 1 
        if check_r >= 0 and check_c >= 0:
            if self.board[check_r][check_c] == '--' or self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(Move((r, c), (check_r, check_c)))

        # Bottom Right 
        check_r = r + 1
        check_c = c + 1 
        if check_r <= 7 and check_c <= 7:
            if self.board[check_r][check_c] == '--' or self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(Move((r, c), (check_r, check_c)))

        # Up Right 
        check_r = r - 1
        check_c = c + 1 
        if check_r >= 0 and check_c <= 7:
            if self.board[check_r][check_c] == '--' or self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(Move((r, c), (check_r, check_c)))

        # Bottom Left 
        check_r = r + 1
        check_c = c - 1 
        if check_r <= 7 and check_c >= 0:
            if self.board[check_r][check_c] == '--' or self.board[check_r][check_c][0] == other_color:
                if not self.is_king_attacked_after_move(r, c, check_r, check_c):
                    moves.append(Move((r, c), (check_r, check_c)))


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

        revert_move()
        return False
        
def Move(start_square, end_square):
    # Dictionaries that change row to rank and col to file
    row_to_rank = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}
    col_to_file = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

    start = col_to_file[start_square[1]] + row_to_rank[start_square[0]]
    end = col_to_file[end_square[1]] + row_to_rank[end_square[0]]

    return start + end


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
