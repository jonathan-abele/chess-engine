#include "engine.h"
#include <iostream>
#include <sstream>
#include <cctype>

using namespace std;

/**
 * @brief Constructs a ChessEngine instance from a given FEN string.
 *
 * The FEN (Forsyth-Edwards Notation) string provides a complete representation of the
 * current state of a chess game, including the arrangement of pieces on the board,
 * the active player, castling availability, and the en passant target square.
 *
 * The FEN string is expected to be formatted as follows:
 *
 * <piece placement> <active color> <castling availability> <en passant target>
 *
 * - **Piece Placement**: A series of characters representing the pieces on the board,
 *   where ranks are separated by slashes ('/'). Lowercase letters represent black pieces
 *   (e.g., 'p' for pawn, 'r' for rook, etc.), and uppercase letters represent white pieces.
 *   Digits (0-8) indicate the number of empty squares in that rank. For example:
 *   "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR" represents the starting position of a chess game.
 *
 * - **Active Color**: A single character ('w' or 'b') indicating which player's turn it is to move.
 *   'w' means it's White's turn, and 'b' means it's Black's turn.
 *
 * - **Castling Availability**: A string indicating the castling rights for both players.
 *   'K' means White can castle kingside, 'Q' means White can castle queenside,
 *   'k' means Black can castle kingside, and 'q' means Black can castle queenside.
 *   If neither player can castle, this field is represented by '-'.
 *
 * - **En Passant Target**: This indicates the square (in algebraic notation) that a pawn can
 *   potentially capture en passant. If there is no en passant target, this is represented by '-'.
 *
 *
 * @param board_state A string in FEN format representing the current state of the chess game.
 */
ChessEngine::ChessEngine(string board_string)
{
    // Split the FEN string into parts using space as a delimiter
    istringstream iss(board_string);
    string board_part;
    getline(iss, board_part, ' '); // Get the piece placement
    string active_color_str;
    getline(iss, active_color_str, ' ');      // Get active color
    getline(iss, castling_availability, ' '); // Get castling availability
    getline(iss, en_passant_target, ' ');     // Get en passant target square

    // Initialize the board with empty spaces
    board.resize(8, std::vector<char>(8, ' '));

    // Process the board part
    size_t row = 0;
    size_t col = 0;

    for (char c : board_part)
    {
        if (c == '/')
        {
            row++;   // Move to the next row
            col = 0; // Reset column to the first column
        }
        else if (isdigit(c))
        {
            // If the character is a digit, it indicates empty squares
            int empty_squares = c - '0'; // Convert char to int
            col += empty_squares;        // Skip those squares
        }
        else
        {
            // Place the piece on the board
            board[row][col] = c;
            col++;

            // Set kings position
            if (c == 'K')
                white_king_position = {row, col};
            if (c == 'k')
                black_king_position = {row, col};
        }
    }

    // Set the active color
    active_color = active_color_str[0];
}

// Function to return best move (example logic)
string ChessEngine::get_best_move()
{
    string str(1, active_color);
    // Here, you would have more complex logic for computing the best move
    return str; // Example move
}
