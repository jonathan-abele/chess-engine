#include "engine.h"
#include <string>
#include <cstring>
#include <iostream>

// Compile: g++ -shared -o engine.so -fPIC -std=c++11 engine/engine.cpp engine/engine_interface.cpp

extern "C"
{
    // Expose C-style function to get the best move
    const char *get_best_move(const char *board_state)
    {
        std::string board(board_state);

        ChessEngine engine(board);

        std::string move = engine.get_best_move();

        // Return the move as a C-style string (char*)
        // Use strdup to ensure the memory is allocated properly for ctypes in Python
        return strdup(move.c_str());
    }
}
