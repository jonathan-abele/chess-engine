#include "engine.h"
#include <iostream>
#include <sstream>
#include <cctype>

using namespace std;

vector<string> ChessEngine::get_all_possible_moves()
{
    vector<string> moves;

    for (int r = 0; r < 8; ++r)
    {
        for (int c = 0; c < 8; ++c)
        {
            char piece = board[r][c];
            // Look for a piece of the color of who's turn it is
            if (piece == ' ')
                continue;

            if ((isupper(piece) && active_color == 'w') || (!isupper(piece) && active_color == 'b'))
            {
                if (tolower(piece) == 'p')
                    get_pawn_moves(r, c, moves);
                else if (tolower(piece) == 'r')
                    get_rook_moves(r, c, moves);
                else if (tolower(piece) == 'b')
                    get_bishop_moves(r, c, moves);
                else if (tolower(piece) == 'n')
                    get_knight_moves(r, c, moves);
                else if (tolower(piece) == 'k')
                    get_king_moves(r, c, moves);
                else if (tolower(piece) == 'q')
                    get_queen_moves(r, c, moves);
            }
        }
    }

    get_castling_moves(moves);

    return moves;
}

void ChessEngine::get_castling_moves(vector<string> &moves)
{
    // Check for white castling availability
    if (active_color == 'w')
    {
        // Kingside castling for white (K)
        if (castling_availability.find('K') != std::string::npos)
        {
            // Ensure the squares between the king and rook are empty and king is not in/going through check
            if (board[7][5] == ' ' && board[7][6] == ' ' &&
                !is_square_attacked(7, 4, 'b') && // Current king square
                !is_square_attacked(7, 5, 'b') && // Square the king moves through
                !is_square_attacked(7, 6, 'b'))   // Square the king ends up
            {
                moves.push_back("O-O"); // Kingside castling notation
            }
        }

        // Queenside castling for white (Q)
        if (castling_availability.find('Q') != std::string::npos)
        {
            // Ensure the squares between the king and rook are empty and king is not in/going through check
            if (board[7][1] == ' ' && board[7][2] == ' ' && board[7][3] == ' ' &&
                !is_square_attacked(7, 4, 'b') && // Current king square
                !is_square_attacked(7, 3, 'b') && // Square the king moves through
                !is_square_attacked(7, 2, 'b'))   // Square the king ends up
            {
                moves.push_back("O-O-O"); // Queenside castling notation
            }
        }
    }
    // Check for black castling availability
    else if (active_color == 'b')
    {
        // Kingside castling for black (k)
        if (castling_availability.find('k') != std::string::npos)
        {
            // Ensure the squares between the king and rook are empty and king is not in/going through check
            if (board[0][5] == ' ' && board[0][6] == ' ' &&
                !is_square_attacked(0, 4, 'w') && // Current king square
                !is_square_attacked(0, 5, 'w') && // Square the king moves through
                !is_square_attacked(0, 6, 'w'))   // Square the king ends up
            {
                moves.push_back("O-O"); // Kingside castling notation
            }
        }

        // Queenside castling for black (q)
        if (castling_availability.find('q') != std::string::npos)
        {
            // Ensure the squares between the king and rook are empty and king is not in/going through check
            if (board[0][1] == ' ' && board[0][2] == ' ' && board[0][3] == ' ' &&
                !is_square_attacked(0, 4, 'w') && // Current king square
                !is_square_attacked(0, 3, 'w') && // Square the king moves through
                !is_square_attacked(0, 2, 'w'))   // Square the king ends up
            {
                moves.push_back("O-O-O"); // Queenside castling notation
            }
        }
    }
}

void ChessEngine::get_pawn_moves(int r, int c, vector<string> &moves)
{
    // White Pawn
    if (active_color == 'w')
    {
        // Is on starting square
        if (r == 6)
        {
            if (board[r - 1][c] == ' ' && board[r - 2][c] == ' ')
            {
                if (!is_king_attacked_after_move(r, c, r - 2, c))
                {
                    moves.push_back(move_to_notation(r, c, r - 2, c));
                }
            }
        }

        // Forward 1 square
        if (board[r - 1][c] == ' ')
        {
            if (!is_king_attacked_after_move(r, c, r - 1, c))
            {
                moves.push_back(move_to_notation(r, c, r - 1, c));
            }
        }

        // Capture Diagonally
        if (c != 7 && islower(board[r - 1][c + 1]))
        {
            if (!is_king_attacked_after_move(r, c, r - 1, c + 1))
            {
                moves.push_back(move_to_notation(r, c, r - 1, c + 1));
            }
        }

        if (c != 0 && islower(board[r - 1][c - 1]))
        {
            if (!is_king_attacked_after_move(r, c, r - 1, c - 1))
            {
                moves.push_back(move_to_notation(r, c, r - 1, c - 1));
            }
        }
    }
    else
    { // Black Pawn
        // Is on starting square
        if (r == 1)
        {
            if (board[r + 1][c] == ' ' && board[r + 2][c] == ' ')
            {
                if (!is_king_attacked_after_move(r, c, r + 2, c))
                {
                    moves.push_back(move_to_notation(r, c, r + 2, c));
                }
            }
        }

        // Forward one square
        if (board[r + 1][c] == ' ')
        {
            if (!is_king_attacked_after_move(r, c, r + 1, c))
            {
                moves.push_back(move_to_notation(r, c, r + 1, c));
            }
        }

        // Capture diagonally
        if (c != 7 && isupper(board[r + 1][c + 1]))
        {
            if (!is_king_attacked_after_move(r, c, r + 1, c + 1))
            {
                moves.push_back(move_to_notation(r, c, r + 1, c + 1));
            }
        }

        if (c != 0 && isupper(board[r + 1][c - 1]))
        {
            if (!is_king_attacked_after_move(r, c, r + 1, c - 1))
            {
                moves.push_back(move_to_notation(r, c, r + 1, c - 1));
            }
        }
    }
}

void ChessEngine::get_rook_moves(int r, int c, vector<string> &moves)
{
    // Directions a rook can move: up, down, left, right
    const int directions[4][2] = {
        {-1, 0}, // Up
        {1, 0},  // Down
        {0, -1}, // Left
        {0, 1}   // Right
    };

    // Check each direction for possible moves
    for (int i = 0; i < 4; ++i)
    {
        int new_r = r;
        int new_c = c;

        // Keep moving in the current direction until we hit an obstacle (edge of board or piece)
        while (true)
        {
            new_r += directions[i][0];
            new_c += directions[i][1];

            // Ensure the new position is within board boundaries
            if (new_r < 0 || new_r >= 8 || new_c < 0 || new_c >= 8)
            {
                break;
            }

            // If the target square is empty, add the move
            if (board[new_r][new_c] == ' ')
            {
                if (!is_king_attacked_after_move(r, c, new_r, new_c))
                {
                    moves.push_back(move_to_notation(r, c, new_r, new_c));
                }
            }
            // If the target square has an opponent's piece, add the capture and stop
            else if ((active_color == 'w' && islower(board[new_r][new_c])) ||
                     (active_color == 'b' && isupper(board[new_r][new_c])))
            {
                if (!is_king_attacked_after_move(r, c, new_r, new_c))
                {
                    moves.push_back(move_to_notation(r, c, new_r, new_c));
                }
                break; // Rook can't move beyond a captured piece
            }
            // If the target square has one of our own pieces, stop
            else
            {
                break;
            }
        }
    }
}

void ChessEngine::get_knight_moves(int r, int c, vector<string> &moves)
{
    // Knight move offsets (8 possible moves)
    const int knight_offsets[8][2] = {
        {2, 1}, {2, -1}, {-2, 1}, {-2, -1}, {1, 2}, {1, -2}, {-1, 2}, {-1, -2}};

    // Check each potential knight move
    for (int i = 0; i < 8; ++i)
    {
        int new_r = r + knight_offsets[i][0];
        int new_c = c + knight_offsets[i][1];

        // Ensure the new position is within board boundaries
        if (new_r >= 0 && new_r < 8 && new_c >= 0 && new_c < 8)
        {
            // Check if the target square is empty or occupied by an opponent's piece
            if (board[new_r][new_c] == ' ' || (active_color == 'w' && islower(board[new_r][new_c])) ||
                (active_color == 'b' && isupper(board[new_r][new_c])))
            {
                // Check if moving to the new position puts the king in check
                if (!is_king_attacked_after_move(r, c, new_r, new_c))
                {
                    moves.push_back(move_to_notation(r, c, new_r, new_c));
                }
            }
        }
    }
}

void ChessEngine::get_bishop_moves(int r, int c, vector<string> &moves)
{
    // Directions a bishop can move: diagonals (4 directions)
    const int directions[4][2] = {
        {-1, -1}, // Up-left
        {-1, 1},  // Up-right
        {1, -1},  // Down-left
        {1, 1}    // Down-right
    };

    // Check each direction for possible moves
    for (int i = 0; i < 4; ++i)
    {
        int new_r = r;
        int new_c = c;

        // Keep moving in the current diagonal direction until we hit an obstacle (edge of board or piece)
        while (true)
        {
            new_r += directions[i][0];
            new_c += directions[i][1];

            // Ensure the new position is within board boundaries
            if (new_r < 0 || new_r >= 8 || new_c < 0 || new_c >= 8)
            {
                break;
            }

            // If the target square is empty, add the move
            if (board[new_r][new_c] == ' ')
            {
                if (!is_king_attacked_after_move(r, c, new_r, new_c))
                {
                    moves.push_back(move_to_notation(r, c, new_r, new_c));
                }
            }
            // If the target square has an opponent's piece, add the capture and stop
            else if ((active_color == 'w' && islower(board[new_r][new_c])) ||
                     (active_color == 'b' && isupper(board[new_r][new_c])))
            {
                if (!is_king_attacked_after_move(r, c, new_r, new_c))
                {
                    moves.push_back(move_to_notation(r, c, new_r, new_c));
                }
                break; // Bishop can't move beyond a captured piece
            }
            // If the target square has one of our own pieces, stop
            else
            {
                break;
            }
        }
    }
}

void ChessEngine::get_queen_moves(int r, int c, vector<string> &moves)
{
    // Queen is simply a rook and bishop
    get_rook_moves(r, c, moves);
    get_bishop_moves(r, c, moves);
}

void ChessEngine::get_king_moves(int r, int c, vector<string> &moves)
{
    // Directions the king can move: all 8 directions (1 square in each direction)
    const int directions[8][2] = {
        {-1, 0},  // Up
        {1, 0},   // Down
        {0, -1},  // Left
        {0, 1},   // Right
        {-1, -1}, // Up-left
        {-1, 1},  // Up-right
        {1, -1},  // Down-left
        {1, 1}    // Down-right
    };

    // Check each direction for possible moves
    for (int i = 0; i < 8; ++i)
    {
        int new_r = r + directions[i][0];
        int new_c = c + directions[i][1];

        // Ensure the new position is within board boundaries
        if (new_r >= 0 && new_r < 8 && new_c >= 0 && new_c < 8)
        {
            // Check if the target square is empty or occupied by an opponent's piece
            if (board[new_r][new_c] == ' ' ||
                (active_color == 'w' && islower(board[new_r][new_c])) ||
                (active_color == 'b' && isupper(board[new_r][new_c])))
            {
                // Ensure the king is not moving into check
                if (!is_king_attacked_after_move(r, c, new_r, new_c))
                {
                    moves.push_back(move_to_notation(r, c, new_r, new_c));
                }
            }
        }
    }
}

bool ChessEngine::is_king_attacked_after_move(int r, int c, int new_r, int new_c)
{
    // Store the piece at the destination square
    char temp_piece = board[new_r][new_c];

    // Perform the move temporarily
    board[new_r][new_c] = board[r][c];
    board[r][c] = ' ';

    // If the move involves the king, update its position temporarily
    std::pair<int, int> original_king_position = (active_color == 'w') ? white_king_position : black_king_position;
    if (board[new_r][new_c] == 'K')
    {
        white_king_position = {new_r, new_c};
    }
    else if (board[new_r][new_c] == 'k')
    {
        black_king_position = {new_r, new_c};
    }

    // Determine the current king's position to check if it is in danger
    std::pair<int, int> king_pos = (active_color == 'w') ? white_king_position : black_king_position;

    // Check if the king is in check after this move
    bool king_is_attacked = is_square_attacked(king_pos.first, king_pos.second, (active_color == 'w') ? 'b' : 'w');

    // Undo the move and restore the board to its original state
    board[r][c] = board[new_r][new_c];
    board[new_r][new_c] = temp_piece;

    // Restore king's original position if it was moved
    if (board[r][c] == 'K')
    {
        white_king_position = original_king_position;
    }
    else if (board[r][c] == 'k')
    {
        black_king_position = original_king_position;
    }

    // Return whether the king is in check or not
    return king_is_attacked;
}

bool ChessEngine::is_square_attacked(int r, int c, char attacking_color)
{
    // Check for pawn attacks
    if (attacking_color == 'w')
    {
        if ((r > 0 && c > 0 && board[r - 1][c - 1] == 'P') ||
            (r > 0 && c < 7 && board[r - 1][c + 1] == 'P'))
        {
            return true;
        }
    }
    else
    {
        if ((r < 7 && c > 0 && board[r + 1][c - 1] == 'p') ||
            (r < 7 && c < 7 && board[r + 1][c + 1] == 'p'))
        {
            return true;
        }
    }

    // Check for knight attacks
    const int knight_moves[8][2] = {
        {-2, -1}, {-2, 1}, {2, -1}, {2, 1}, {-1, -2}, {-1, 2}, {1, -2}, {1, 2}};
    for (int i = 0; i < 8; i++)
    {
        int new_r = r + knight_moves[i][0];
        int new_c = c + knight_moves[i][1];
        if (new_r >= 0 && new_r < 8 && new_c >= 0 && new_c < 8)
        {
            if ((attacking_color == 'w' && board[new_r][new_c] == 'N') ||
                (attacking_color == 'b' && board[new_r][new_c] == 'n'))
            {
                return true;
            }
        }
    }

    // Check for rook/queen (horizontal and vertical attacks)
    const int rook_directions[4][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
    for (int i = 0; i < 4; ++i)
    {
        int new_r = r;
        int new_c = c;
        while (true)
        {
            new_r += rook_directions[i][0];
            new_c += rook_directions[i][1];
            if (new_r < 0 || new_r >= 8 || new_c < 0 || new_c >= 8)
                break;
            if (board[new_r][new_c] != ' ')
            {
                if ((attacking_color == 'w' && (board[new_r][new_c] == 'R' || board[new_r][new_c] == 'Q')) ||
                    (attacking_color == 'b' && (board[new_r][new_c] == 'r' || board[new_r][new_c] == 'q')))
                {
                    return true;
                }
                break; // Blocked by a piece
            }
        }
    }

    // Check for bishop/queen (diagonal attacks)
    const int bishop_directions[4][2] = {{-1, -1}, {-1, 1}, {1, -1}, {1, 1}};
    for (int i = 0; i < 4; ++i)
    {
        int new_r = r;
        int new_c = c;
        while (true)
        {
            new_r += bishop_directions[i][0];
            new_c += bishop_directions[i][1];
            if (new_r < 0 || new_r >= 8 || new_c < 0 || new_c >= 8)
                break;
            if (board[new_r][new_c] != ' ')
            {
                if ((attacking_color == 'w' && (board[new_r][new_c] == 'B' || board[new_r][new_c] == 'Q')) ||
                    (attacking_color == 'b' && (board[new_r][new_c] == 'b' || board[new_r][new_c] == 'q')))
                {
                    return true;
                }
                break; // Blocked by a piece
            }
        }
    }

    // Check for king attacks (adjacent squares)
    const int king_moves[8][2] = {
        {-1, 0}, {1, 0}, {0, -1}, {0, 1}, {-1, -1}, {-1, 1}, {1, -1}, {1, 1}};
    for (int i = 0; i < 8; ++i)
    {
        int new_r = r + king_moves[i][0];
        int new_c = c + king_moves[i][1];
        if (new_r >= 0 && new_r < 8 && new_c >= 0 && new_c < 8)
        {
            if ((attacking_color == 'w' && board[new_r][new_c] == 'K') ||
                (attacking_color == 'b' && board[new_r][new_c] == 'k'))
            {
                return true;
            }
        }
    }

    // If no attacks are detected, return false
    return false;
}

string ChessEngine::move_to_notation(int r1, int c1, int r2, int c2)
{
    char start_rank = '8' - r1; // 0 -> 8, 1 -> 7, ..., 7 -> 1
    char end_rank = '8' - r2;   // 0 -> 8, 1 -> 7, ..., 7 -> 1

    char start_file = 'a' + c1; // 0 -> 'a', 1 -> 'b', ..., 7 -> 'h'
    char end_file = 'a' + c2;   // 0 -> 'a', 1 -> 'b', ..., 7 -> 'h'

    // Construct the move notation
    string notation = string(1, start_file) + start_rank + string(1, end_file) + end_rank;

    return notation; // e.g., "e2e4"
}