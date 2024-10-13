import ctypes
import glob

# find the shared library, the path depends on the platform and Python version
engine_lib = ctypes.CDLL('./engine.so')


engine_lib.get_best_move.argtypes = [ctypes.c_char_p]  # Takes a string (char*)
engine_lib.get_best_move.restype = ctypes.c_char_p  # Returns a string (char*)

board_state = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1"

# 3. call function mysum
text = engine_lib.get_best_move(board_state.encode())

print(text.decode())