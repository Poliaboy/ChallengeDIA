import time

class Game:
    def __init__(self):
        self.board = [[None] * 9 for _ in range(9)]
        self.big_board = [[None] * 3 for _ in range(3)]
        self.player = "X"
        self.last_move = None

    def get_small_board(self, x, y):
        return [[self.board[x * 3 + i][y * 3 + j] for j in range(3)] for i in range(3)]

    def check_small_board(self, x, y):
        small_board = self.get_small_board(x, y)
        return self.check_winner(small_board)

    def check_big_board(self):
        return self.check_winner(self.big_board)

    def check_winner(self, board):
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] is not None:
                return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] is not None:
                return board[0][i]
        if board[0][0] == board[1][1] == board[2][2] is not None:
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] is not None:
            return board[0][2]
        return None

    def make_move(self, move):
        x, y = move
        if self.board[x][y] is not None:
            return False
        self.board[x][y] = self.player
        small_board_winner = self.check_small_board(x // 3, y // 3)
        if small_board_winner is not None:
            self.big_board[x // 3][y // 3] = small_board_winner
        big_board_winner = self.check_big_board()
        if big_board_winner is not None:
            return big_board_winner
        self.player = "O" if self.player == "X" else "X"
        self.last_move = move
        return None

    def undo_move(self, move):
        x, y = move
        self.board[x][y] = None
        self.big_board[x // 3][y // 3] = None
        self.player = "O" if self.player == "X" else "X"

    def get_legal_moves(self):
        if self.last_move is None:
            return [(i, j) for i in range(9) for j in range(9) if self.board[i][j] is None]
        else:
            x, y = self.last_move
            x, y = x % 3 * 3, y % 3 * 3
            moves = [(x+i, y+j) for i in range(3) for j in range(3) if self.board[x+i][y+j] is None]
            if not moves:
                return [(i, j) for i in range(9) for j in range(9) if self.board[i][j] is None]
            return moves

    def is_terminal(self):
        if self.check_big_board() is not None:
            return True
        if all(all(cell is not None for cell in row) for row in self.board):
            return True
        return False

    def print_board(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] is None:
                    print('.', end=' ')
                else:
                    print(self.board[i][j], end=' ')
                if (j + 1) % 3 == 0 and j != 8:  # separate small boards horizontally
                    print('|', end=' ')
            print()  # newline after each row
            if (i + 1) % 3 == 0 and i != 8:  # separate small boards vertically
                print('-' * 29)  # print horizontal line


def evaluate(game):
    winner = game.check_big_board()
    if winner is not None:
        return winner
    if all(all(cell is not None for cell in row) for row in game.board):
        return "draw"
    return None


def minimax(game, depth, maximizing_player):
    result = evaluate(game)
    if result == "X":
        return 1 if maximizing_player else -1
    elif result == "O":
        return -1 if maximizing_player else 1
    elif result == "draw":
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for x in range(9):
            for y in range(9):
                if game.board[x][y] is None:
                    game.board[x][y] = "X"
                    eval = minimax(game, depth - 1, False)
                    game.board[x][y] = None
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for x in range(9):
            for y in range(9):
                if game.board[x][y] is None:
                    game.board[x][y] = "O"
                    eval = minimax(game, depth - 1, True)
                    game.board[x][y] = None
                    min_eval = min(min_eval, eval)
        return min_eval


def alpha_beta_pruning(game, depth, alpha, beta, maximizing_player):
    result = evaluate(game)
    if result == "X":
        return 1 if maximizing_player else -1
    elif result == "O":
        return -1 if maximizing_player else 1
    elif result == "draw":
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for x in range(9):
            for y in range(9):
                if game.board[x][y] is None:
                    game.board[x][y] = "X"
                    eval = alpha_beta_pruning(game, depth - 1, alpha, beta, False)
                    game.board[x][y] = None
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float('inf')
        for x in range(9):
            for y in range(9):
                if game.board[x][y] is None:
                    game.board[x][y] = "O"
                    eval = alpha_beta_pruning(game, depth - 1, alpha, beta, True)
                    game.board[x][y] = None
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval


def heur1(game):
    x_wins = sum(cell == "X" for row in game.big_board for cell in row)
    o_wins = sum(cell == "O" for row in game.big_board for cell in row)
    return x_wins - o_wins


def heur2(game):
    score = 0
    # Check small board wins, center board wins, corner board wins,
    # center square in any small board and square in the center board
    for i in range(9):
        for j in range(9):
            if game.board[i][j] == "X":
                score += 5
                if i == 4 and j == 4:
                    score += 10
                if i in [0, 2, 6, 8] and j in [0, 2, 6, 8]:
                    score += 3
                if i % 3 == 1 and j % 3 == 1:
                    score += 3
                if i == 4 or j == 4:
                    score += 3
            elif game.board[i][j] == "O":
                score -= 5
                if i == 4 and j == 4:
                    score -= 10
                if i in [0, 2, 6, 8] and j in [0, 2, 6, 8]:
                    score -= 3
                if i % 3 == 1 and j % 3 == 1:
                    score -= 3
                if i == 4 or j == 4:
                    score -= 3

    # Check for two board wins in a row, column or diagonal
    # Also check for a similar sequence inside a small board
    for i in range(3):
        for j in range(3):
            if game.big_board[i][j] == "X":
                if ((game.big_board[i][(j + 1) % 3] == "X" and game.big_board[i][(j + 2) % 3] != "O") or
                        (game.big_board[(i + 1) % 3][j] == "X" and game.big_board[(i + 2) % 3][j] != "O") or
                        (i == j and game.big_board[(i + 1) % 3][(j + 1) % 3] == "X" and game.big_board[(i + 2) % 3][
                            (j + 2) % 3] != "O") or
                        (i + j == 2 and game.big_board[(i + 1) % 3][(2 - j + 1) % 3] == "X" and
                         game.big_board[(i + 2) % 3][(2 - j + 2) % 3] != "O")):
                    score += 4
            elif game.big_board[i][j] == "O":
                if ((game.big_board[i][(j + 1) % 3] == "O" and game.big_board[i][(j + 2) % 3] != "X") or
                        (game.big_board[(i + 1) % 3][j] == "O" and game.big_board[(i + 2) % 3][j] != "X") or
                        (i == j and game.big_board[(i + 1) % 3][(j + 1) % 3] == "O" and game.big_board[(i + 2) % 3][
                            (j + 2) % 3] != "X") or
                        (i + j == 2 and game.big_board[(i + 1) % 3][(2 - j + 1) % 3] == "O" and
                         game.big_board[(i + 2) % 3][(2 - j + 2) % 3] != "X")):
                    score -= 4

    return score


class MinimaxAgent:
    def __init__(self, depth, heuristic):
        self.depth = depth
        self.heuristic = heuristic

    def get_move(self, game):
        _, move = self.minimax(game, self.depth, True)
        return move

    def minimax(self, game, depth, maximizingPlayer):
        if depth == 0 or game.is_terminal():
            return self.heuristic(game), None

        if maximizingPlayer:
            maxEval = float('-inf')
            best_move = None
            for move in game.get_legal_moves():
                game.make_move(move)
                eval, _ = self.minimax(game, depth - 1, False)
                game.undo_move(move)
                if eval > maxEval:
                    maxEval = eval
                    best_move = move
            return maxEval, best_move
        else:
            minEval = float('inf')
            best_move = None
            for move in game.get_legal_moves():
                game.make_move(move)
                eval, _ = self.minimax(game, depth - 1, True)
                game.undo_move(move)
                if eval < minEval:
                    minEval = eval
                    best_move = move
            return minEval, best_move


class AlphaBetaAgent(MinimaxAgent):
    def get_move(self, game):
        _, move = self.alpha_beta(game, self.depth, float('-inf'), float('inf'), True)
        return move

    def alpha_beta(self, game, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or game.is_terminal():
            return self.heuristic(game), None

        if maximizingPlayer:
            maxEval = float('-inf')
            best_move = None
            for move in game.get_legal_moves():
                game.make_move(move)
                eval, _ = self.alpha_beta(game, depth - 1, alpha, beta, False)
                game.undo_move(move)
                if eval > maxEval:
                    maxEval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval, best_move
        else:
            minEval = float('inf')
            best_move = None
            for move in game.get_legal_moves():
                game.make_move(move)
                eval, _ = self.alpha_beta(game, depth - 1, alpha, beta, True)
                game.undo_move(move)
                if eval < minEval:
                    minEval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval, best_move


class ExpectimaxAgent(MinimaxAgent):
    def get_move(self, game):
        _, move = self.expectimax(game, self.depth, True)
        return move

    def expectimax(self, game, depth, maximizingPlayer):
        if depth == 0 or game.is_terminal():
            return self.heuristic(game), None

        if maximizingPlayer:
            maxEval = float('-inf')
            best_move = None
            for move in game.get_legal_moves():
                game.make_move(move)
                eval, _ = self.expectimax(game, depth - 1, False)
                game.undo_move(move)
                if eval > maxEval:
                    maxEval = eval
                    best_move = move
            return maxEval, best_move
        else:
            expectedValue = 0
            moves = game.get_legal_moves()
            for move in moves:
                game.make_move(move)
                eval, _ = self.expectimax(game, depth - 1, True)
                game.undo_move(move)
                expectedValue += eval / len(moves)
            return expectedValue, None



def play_game(game, agent1, agent2):
    while not game.is_terminal():
        start_time = time.time()
        move = agent1.get_move(game)
        end_time = time.time()
        game.print_board()
        print(f"Agent1's decision time: {end_time - start_time} seconds.")
        game.make_move(move)

        if game.is_terminal():
            break

        start_time = time.time()
        move = agent2.get_move(game)
        end_time = time.time()
        game.print_board()
        print(f"Agent2's decision time: {end_time - start_time} seconds.")
        game.make_move(move)

# Create the game and the agents
game = Game()
agent1 = AlphaBetaAgent(6, heur1)
agent2 = MinimaxAgent(2, heur2)

# Play the game
play_game(game, agent1, agent2)