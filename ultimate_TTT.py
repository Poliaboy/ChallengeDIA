from tic_tac_toe import Tic_Tac_Toe


class UltimateTTT:
    def __init__(self, board=None, player="X", state=False, winner=0, last_action=None):
        if board is None:
            self.boardU = [[Tic_Tac_Toe()] * 3 for _ in range(3)]
        else:
            self.boardU = board
        self.player = player
        self.state = state
        self.winner = winner
        self.next_grid = last_action

    def is_terminal(self):
        self.winner = self.utility()
        if self.winner != 0:
            self.state = True
        self.state = all(self.boardU[i][j].state for i in range(3) for j in range(3))

    def utility(self):
        for i in range(3):
            if self.boardU[i][0].winner == self.boardU[i][1].winner == self.boardU[i][2].winner != 0:
                return self.boardU[i][0].winner
            elif self.boardU[0][i].winner == self.boardU[1][i].winner == self.boardU[2][i].winner != 0:
                return self.boardU[0][i].winner
        if self.boardU[0][0].winner == self.boardU[1][1].winner == self.boardU[2][2].winner != 0:
            return self.boardU[0][0].winner
        elif self.boardU[0][2].winner == self.boardU[1][1].winner == self.boardU[2][0].winner != 0:
            return self.boardU[0][2].winner
        return 0

    def player_turn(self, boardNb, cell):
        # faire un if possible actions ?
        i, j = divmod(boardNb, 3)
        k, l = divmod(cell, 3)
        self.boardU[i][j].board[k][l] = self.player
        self.next_grid = cell
        self.player = "O" if self.player == "X" else "X"
        self.boardU[i][j].is_terminal()
        self.boardU.is_terminal()

    def is_next_grid_full(self):
        if self.next_grid is None:
            return True
        else:
            i, j = divmod(self.next_grid, 3)
            return self.boardU[i][j].state

    def possible_actions(self):
        # if the next grid is full, then all the grids that are not terminal are possible actions
        # and within those grids, all the cells that are not taken are possible actions
        if self.is_next_grid_full():
            return [(i, j, self.boardU[i][j].possible_actions()) for i in range(3) for j in range(3) if not self.boardU[i][j].state]
        else:
            i, j = divmod(self.next_grid, 3)
            return [(i, j, self.boardU[i][j].possible_actions())]

    # the game is displayed like this
    # X X X | O X X | X X X
    # X X X | O   O | X X X
    # X X X | X   X | X X X
    # ------+-------+------
    # X X X | X X X | X X X
    # X X X | X X X | X X X
    # X X X | X X X | X X X
    # ------+-------+------
    # X X X | X X X | X X X
    # X X X | X X X | X X X
    # X X X | X X X | X X X
    def __str__(self):
        return " ".join("------+-------+------\n".join(" | ".join(" ".join(self.boardU[i][j].__str__()) for j in range(3)) for i in range(3)))





