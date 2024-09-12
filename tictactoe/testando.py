from tictactoe import *

X = "X"
O = "O"
EMPTY = None

board = [[X, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY]]


print(minimax(board)[1])