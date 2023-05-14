#Minimax manually coded for tik tak toe² with modula
#Alex Ocean
import random
import math

def minimax_min_value(state):
    if state.is_terminal():
        return state.utility()
    v = float("inf")
    for a in state.actions():
        v = min(v, minimax_max_value(state.result(a)))
    return v

def minimax_max_value(state):
    if state.is_terminal():
        return state.utility()
    v = float("-inf")
    for a in state.actions():
        v = max(v, minimax_min_value(state.result(a)))
    return v

def minimax_decision(state):
    best_score = float("-inf")
    best_action = None
    for a in state.actions():
        v = minimax_min_value(state.result(a))
        if v > best_score:
            best_score = v
            best_action = a
    bestactions = [i for i in state.actions() if minimax_min_value(state.result(i)) == best_score]
    return random.choice(bestactions)

def alphabeta_search(state):
    v = alphabeta_max_value(state, float("-inf"), float("inf"))
    return random.choice([a for a in state.actions() if alphabeta_min_value(state.result(a), float("-inf"), float("inf")) == v])

def alphabeta_max_value(state, alpha, beta):
    if state.is_terminal():
        return state.utility()
    v = float("-inf")
    for a in state.actions():
        v = max(v, alphabeta_min_value(state.result(a), alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

def alphabeta_min_value(state, alpha, beta):
    if state.is_terminal():
        return state.utility()
    v = float("inf")
    for a in state.actions():
        v = min(v, alphabeta_max_value(state.result(a), alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

#Tic Tac Toe
class State:

    def __init__(self, board, player):
        self.board = board
        self.player = player

    def is_terminal(self):
        if self.utility() != 0:
            return True
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "-":
                    return False
        return True

    def utility(self):
        # Check rows
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2]:
                if self.board[i][0] == "X":
                    return 1
                elif self.board[i][0] == "O":
                    return -1

        # Check columns
        for j in range(3):
            if self.board[0][j] == self.board[1][j] == self.board[2][j]:
                if self.board[0][j] == "X":
                    return 1
                elif self.board[0][j] == "O":
                    return -1

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2]:
            if self.board[0][0] == "X":
                return 1
            elif self.board[0][0] == "O":
                return -1
        if self.board[0][2] == self.board[1][1] == self.board[2][0]:
            if self.board[0][2] == "X":
                return 1
            elif self.board[0][2] == "O":
                return -1

        # Game is not yet over
        return 0

    def actions(self):
        actions = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "-":
                    actions.append((i, j))
        return actions

    def result(self, action):
        i, j = action
        new_board = [row[:] for row in self.board]
        new_board[i][j] = self.player
        new_player = "O" if self.player == "X" else "X"
        return State(new_board, new_player)




def minimax():
    board = [["-", "-", "O"],
             ["-", "X", "-"],
             ["-", "-", "-"]]
    player = "X"
    state = State(board, player)

    # Play game

    while not state.is_terminal():
        if state.player == "X":
            # Player X's turn
            print("Player X's turn")
            print(state.board)
            action = minimax_decision(state)
            state = state.result(action)
        else:
            # Player O's turn
            print("Player O's turn")
            print(state.board)
            action = minimax_decision(state)
            state = state.result(action)

    # Print final result
    if state.utility() == 1:
        print("Player X wins!")
        print(state.board)
    elif state.utility() == -1:
        print("Player O wins!")
        print(state.board)
    else:
        print("Tie game.")
        print(state.board)

def alphabeta():
    board = [["-", "-", "O"],
             ["-", "X", "-"],
             ["-", "-", "-"]]
    player = "X"
    state = State(board, player)

    # Play game

    while not state.is_terminal():
        if state.player == "X":
            # Player X's turn
            print("Player X's turn")
            print(state.board)
            action = alphabeta_search(state)
            state = state.result(action)
        else:
            # Player O's turn
            print("Player O's turn")
            print(state.board)
            action = alphabeta_search(state)
            state = state.result(action)

    # Print final result
    if state.utility() == 1:
        print("Player X wins!")
        print(state.board)
    elif state.utility() == -1:
        print("Player O wins!")
        print(state.board)
    else:
        print("Tie game.")
        print(state.board)

if __name__ == '__main__':
    print("Taper 1 pour minimax et 2 pour alphabeta")
    choix = int(input())
    if choix == 1:
        minimax()
    else:
        alphabeta()


