from collections import namedtuple
import math
from collections import defaultdict
import random
import random

class Game:
    """A game is similar to a problem, but it has a terminal test instead of 
    a goal test, and a utility for each terminal state. To create a game, 
    subclass this class and implement `actions`, `result`, `is_terminal`, 
    and `utility`. You will also need to set the .initial attribute to the 
    initial state; this can be done in the constructor."""

    def actions(self, state):
        """Return a collection of the allowable moves from this state."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def is_terminal(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)
    
    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

    def terminal_test(self, state):
        return self.is_terminal(state)

    def to_move(self,state):
        return state.to_move


        

def play_game(game, strategies: dict, verbose=False):
    """Play a turn-taking game where each player makes two moves per turn."""
    state = game.initial
    while not game.is_terminal(state):
        player = state.to_move
        move1, move2 = strategies[player](game, state)
        state = game.result(state, move1, move2)
        if verbose:
            print('Player', player, 'moves:', move1, 'and', move2)
            print(state)
    return state



def minimax_search(game, state):
    """Search game tree to determine the best two consecutive moves; return (value, (move1, move2)) pair."""

    player = state.to_move

    def max_value(state):
        if game.is_terminal(state):
            return game.utility(state, player), (None, None)
        v, moves = -math.inf, (None, None)
        legal_moves = game.actions(state)
        for a1 in legal_moves:
            for a2 in legal_moves - {a1}:  # Ensure the second move is different
                v2, _ = min_value(game.result(state, a1, a2))
                if v2 > v:
                    v, moves = v2, (a1, a2)
        return v, moves

    def min_value(state):
        if game.is_terminal(state):
            return game.utility(state, player), (None, None)
        v, moves = +math.inf, (None, None)
        legal_moves = game.actions(state)
        for a1 in legal_moves:
            for a2 in legal_moves - {a1}:  # Ensure the second move is different
                v2, _ = max_value(game.result(state, a1, a2))
                if v2 < v:
                    v, moves = v2, (a1, a2)
        return v, moves

    return max_value(state)


class Board(defaultdict):
    """A board has the player to move, a cached utility value, 
    and a dict of {(x, y): player} entries, where player is 'X' or 'O'."""
    empty = '.'
    off = '#'
    
    def __init__(self, width=8, height=8, to_move=None, **kwds):
        self.__dict__.update(width=width, height=height, to_move=to_move, **kwds)
        
    def new(self, changes: dict, **kwds) -> 'Board':
        "Given a dict of {(x, y): contents} changes, return a new Board with the changes."
        board = Board(width=self.width, height=self.height, **kwds)
        board.update(self)
        board.update(changes)
        return board

    def __missing__(self, loc):
        x, y = loc
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.empty
        else:
            return self.off
            
    def __hash__(self): 
        return hash(tuple(sorted(self.items()))) + hash(self.to_move)
    
    def __repr__(self):
        def row(y): return ' '.join(self[x, y] for x in range(self.width))
        return '\n'.join(map(row, range(self.height))) +  '\n'
    


class TicTacToe(Game):
    """Play TicTacToe on an `height` by `width` board, needing `k` in a row to win.
    'X' plays first against 'O'."""

    def __init__(self, height=5, width=5, k=5):
        self.k = k # k in a row
        self.squares = {(x, y) for x in range(width) for y in range(height)}
        self.initial = Board(height=height, width=width, to_move='X', utility=0)

    def actions(self, board):
        """Legal moves are any square not yet taken."""
        return self.squares - set(board.keys())

    def result(self, board, square1, square2):
        """Place markers for the current player on two squares."""
        player = board.to_move
        board = board.new({square1: player, square2: player}, to_move=('O' if player == 'X' else 'X'))
        win1 = k_in_row(board, player, square1, self.k)
        win2 = k_in_row(board, player, square2, self.k)
        board.utility = (0 if not (win1 or win2) else +1 if player == 'X' else -1)
        return board

    def utility(self, board, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return board.utility if player == 'X' else -board.utility

    def is_terminal(self, board):
        """A board is a terminal state if it is won or there are no empty squares."""
        return board.utility != 0 or len(self.squares) == len(board)

    def display(self, board): print(board)     

    def add_random_barrier(self, board):
        """Add a random barrier to the board."""
        player = board.to_move
        square = random.choice(list(self.actions(board))) if self.actions(board) else None
        if square is None:
            return board
        print('adding random barrier at', square)
        board = board.new({square: '#'}, to_move=board.to_move)
        win = k_in_row(board, player, square, self.k)
        board.utility = (0 if not win else +1 if player == 'X' else -1)
        return board


def k_in_row(board, player, square, k):
    """True if player has k pieces in a line through square."""
    def in_row(x, y, dx, dy): 
        return 0 if board[x, y] != player else 1 + in_row(x + dx, y + dy, dx, dy)
    return any(in_row(*square, dx, dy) + in_row(*square, -dx, -dy) - 1 >= k
               for (dx, dy) in ((0, 1), (1, 0), (1, 1), (1, -1)))

def __repr__(self):
    return self.__class__.__name__ + ' ' + str(dict(self)) 





def random_player(game, state):
    """Select two random moves for the current player."""
    legal_moves = list(game.actions(state))
    if len(legal_moves) < 2:
        raise ValueError("Not enough legal moves for two consecutive moves.")
    move1 = random.choice(legal_moves)
    legal_moves.remove(move1)  # Ensure the second move is different
    move2 = random.choice(legal_moves)
    return move1, move2

def player(search_algorithm):
    """A game player who uses the specified search algorithm"""
    return lambda game, state: search_algorithm(game, state)[1]
    


#add main function to run the game
play_game(TicTacToe(height=3, width=3, k=3), dict(X=player(minimax_search), O=player(minimax_search)), verbose=True)


