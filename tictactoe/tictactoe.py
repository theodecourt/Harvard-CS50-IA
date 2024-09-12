import math

class InvalidMoveError(Exception):
    """Exception raised for invalid moves in Tic-Tac-Toe."""
    def __init__(self, message="Invalid move. This position is already taken or out of bounds."):
        self.message = message
        super().__init__(self.message)

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    nulls = null_count(board)

    return X if nulls % 2 == 1 else O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_moves.add((i, j))

    return possible_moves

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if board[i][j] != EMPTY:
        raise InvalidMoveError(f"Move ({i}, {j}) is not valid.")
    
    new_board = [row[:] for row in board]
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
        
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j]:
            return board[0][j]

    if board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    elif null_count(board) == 0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return utility(board), None
    else:
        best_movement = None
        if player(board) == X:
            value = float('-inf')
            possible_moves = actions(board)
            
            for move in possible_moves:
                child = result(board, move)

                tmp = minimax(child)[0]
                if tmp > value:
                    value = tmp
                    best_movement = move
        else:
            value = float('inf')
            possible_moves = actions(board)
            
            for move in possible_moves:
                child = result(board, move)

                tmp = minimax(child)[0]
                if tmp < value:
                    value = tmp
                    best_movement = move            

        return value, best_movement
    

def null_count(board):
    nulls = 0

    for linha in board:
        for coluna in linha:
            if coluna == EMPTY:
                nulls += 1
    
    return nulls