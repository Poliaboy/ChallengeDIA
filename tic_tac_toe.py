class Tic_Tac_Toe:
    def __init__(self, board=None, player="X", state=False, winner=0):
        if board is None:
            self.board = [[" "]*3 for _ in range(3)]
        else:
            self.board = board
        self.player = player
        self.state = state
        self.winner = winner

    def is_terminal(self):
        self.winner = self.utility()
        if self.winner != 0:
            self.state = True
        self.state = all(cell != " " for row in self.board for cell in row)

    def utility(self):
        lines = [
            # Lignes horizontales
            [self.board[i][j] for j in range(3)] for i in range(3)
        ] + [
            # Lignes verticales
            [self.board[i][j] for i in range(3)] for j in range(3)
        ] + [
            # Diagonales
            [self.board[i][i] for i in range(3)],
            [self.board[i][2 - i] for i in range(3)]
        ]

        for line in lines:
            if all(cell == "X" for cell in line):
                return 1
            elif all(cell == "O" for cell in line):
                return -1

        # La partie n'est pas encore terminée
        return 0

    def possible_actions(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == " "]

    # should not be used
    def player_turn(self, action):
        i, j = action
        self.board[i][j] = self.player
        self.player = "O" if self.player == "X" else "X"
        self.is_terminal()

    # if the grid is won by a player display the grid as a big X or O like this:
    #  \ /
    #   X
    #  / \
    # Or
    #  ---
    # |   |
    #  ---
    # and display the grid with space between each cell if the grid is not won
    def display(self):
        if self.winner == 1:
            return " \ / \n  X  \n / \ \n"
        elif self.winner == -1:
            return " --- \n|   |\n --- \n"
        else:
            return "\n".join(" ".join(cell for cell in row) for row in self.board)

    def __str__(self):
        return "\n".join(" ".join(cell for cell in row) for row in self.board)

