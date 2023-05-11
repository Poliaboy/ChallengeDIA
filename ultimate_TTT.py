from tic_tac_toe import Tic_Tac_Toe


class UltimateTTT:
    def __init__(self, board=None, player="X", state=False, winner=0, last_action=None):
        if board is None:
            self.boardU = [[Tic_Tac_Toe() for i in range(3)] for j in range(3)]
        else:
            self.boardU = board
        self.player = player
        self.state = state
        self.winner = winner
        self.next_board = last_action

    def is_terminal(self):
        self.winner = self.utility()
        if self.winner != 0:
            self.state = True
        else:
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
        i, j = divmod(boardNb, 3)
        k, l = divmod(cell, 3)
        self.boardU[i][j].board[k][l] = self.player
        self.next_board = cell
        self.player = "O" if self.player == "X" else "X"
        self.boardU[i][j].is_terminal()
        self.is_terminal()

    def is_next_board_full(self):
        if self.next_board is None:
            return True
        else:
            i, j = divmod(self.next_board, 3)
            return self.boardU[i][j].state

    def possible_actions(self):
        # if the next grid is full, then all the grids that are not terminal are possible actions
        # and within those grids, all the cells that are not taken are possible actions
        if self.is_next_board_full():
            return [(i, j, self.boardU[i][j].possible_actions()) for i in range(3) for j in range(3) if not self.boardU[i][j].state]
        else:
            i, j = divmod(self.next_board, 3)
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
        s = ""
        for i in range(3):
            for k in range(3):
                for j in range(3):
                    for l in range(3):
                        s += self.boardU[i][j].board[k][l] + " "
                    if j < 2:
                        s += "| "
                s += "\n"
            s = s[:-2] + "\n"
            if i < 2:
                s += "------+-------+------\n"
        return s





