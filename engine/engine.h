#ifndef CHESS_ENGINE_H
#define CHESS_ENGINE_H

#include <string>
#include <vector>

using namespace std;

// Example chess engine class
class ChessEngine
{
public:
    ChessEngine(string board_input); // Constructor
    string get_best_move();          // Function that computes best move
    vector<string> get_all_possible_moves();

private:
    // Board State
    vector<vector<char>> board;
    char active_color;            // 'w' for white, 'b' for black
    string castling_availability; // Castling rights
    string en_passant_target;     // En passant target square
    int evaluate_position();

    std::pair<int, int> white_king_position; // (row, col) for the white king
    std::pair<int, int> black_king_position; // (row, col) for the black king

    // Making Moves

    string move_to_notation(int r1, int c1, int r2, int c2);
    void get_castling_moves(vector<string> &moves);
    void get_pawn_moves(int r, int c, vector<string> &moves);
    void get_rook_moves(int r, int c, vector<string> &moves);
    void get_knight_moves(int r, int c, vector<string> &moves);
    void get_bishop_moves(int r, int c, vector<string> &moves);
    void get_queen_moves(int r, int c, vector<string> &moves);
    void get_king_moves(int r, int c, vector<string> &moves);

    bool is_king_attacked_after_move(int r1, int c1, int r2, int c2);
    bool is_square_attacked(int r, int c, char attacking_color);
    void make_move();
};

#endif