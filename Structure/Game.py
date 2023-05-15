class Game:
    def __init__(self):
        self.previous_player = None
        self.board = [[None] * 9 for _ in range(9)]
        self.big_board = [[None] * 3 for _ in range(3)]
        self.small_boards = [[self.get_small_board(i, j) for j in range(3)] for i in range(3)]
        self.legal_moves = [(i, j) for i in range(9) for j in range(9) if self.board[i][j] is None]
        self.player = "X"
        self.last_move = None

    def get_small_board(self, x, y):
        return [self.board[x * 3 + i][y * 3 + j] for i in range(3) for j in range(3)]

    def winner(self):
        return self.check_big_board()

    def check_small_board(self, x, y):
        # check if there is a winner in the small board
        small_board = self.small_boards[x][y]
        winner = self.check_winner(small_board)
        if winner is not None:
            self.big_board[x][y] = winner
        return winner

    def check_big_board(self):
        # flatten the big_board to make it a list
        flat_board = [item for sublist in self.big_board for item in sublist]
        return self.check_winner(flat_board)

    def check_winner(self, board):
        # check rows
        for i in range(0, 9, 3):
            if board[i] == board[i + 1] == board[i + 2] is not None:
                return board[i]
        # check columns
        for i in range(3):
            if board[i] == board[i + 3] == board[i + 6] is not None:
                return board[i]
        # check diagonals
        if board[0] == board[4] == board[8] is not None:
            return board[0]
        if board[2] == board[4] == board[6] is not None:
            return board[2]
        # no winner
        return None

    def get_legal_moves_small_board(self, x, y):
        # get the list of legal moves in a given small board
        return [(x * 3 + i // 3, y * 3 + i % 3) for i in range(9) if self.small_boards[x][y][i] is None]

    def get_legal_moves(self):
        # get the list of legal moves
        if self.last_move is None:
            return [(i, j) for i in range(9) for j in range(9) if self.board[i][j] is None]

        last_x, last_y = self.last_move
        next_x, next_y = last_x % 3, last_y % 3

        if self.big_board[next_x][next_y] is None:
            return self.get_legal_moves_small_board(next_x, next_y)
        else:
            return self.legal_moves

    def make_move(self, move):
        x, y = move
        # make a move
        if self.board[x][y] is None:
            self.previous_player = self.player
            self.board[x][y] = self.player
            self.last_move = (x, y)
            # update small board
            self.small_boards[x // 3][y // 3] = self.get_small_board(x // 3, y // 3)
            # check if the small board is won
            small_board_winner = self.check_small_board(x // 3, y // 3)
            if small_board_winner is not None:
                self.big_board[x // 3][y // 3] = small_board_winner
            # update legal moves
            self.legal_moves = self.get_legal_moves()
            # switch player
            self.player = "O" if self.player == "X" else "X"

    def undo_move(self, move):
        x, y = move
        # undo a move
        if self.board[x][y] is not None:
            self.board[x][y] = None
            self.last_move = None
            # update small board
            self.small_boards[x // 3][y // 3] = self.get_small_board(x // 3, y // 3)
            # switch player back
            self.player = self.previous_player
            self.previous_player = "O" if self.previous_player == "X" else "X"
            # if the small board was won, undo the win
            if self.big_board[x // 3][y // 3] is not None:
                self.big_board[x // 3][y // 3] = None
            # update legal moves
            self.legal_moves = self.get_legal_moves()

    def is_terminal(self):
        # check if the game is over
        if self.check_big_board() is not None or not self.get_legal_moves():
            return True
        return False

    def display(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] is None:
                    print('.', end=' ')
                else:
                    print(self.board[i][j], end=' ')
                if (j + 1) % 3 == 0 and j != 8:  # separate small boards horizontally
                    print('|', end=' ')
            print()  # print new line
            if (i + 1) % 3 == 0 and i != 8:  # separate small boards vertically
                print('-' * 29)  # print horizontal line
