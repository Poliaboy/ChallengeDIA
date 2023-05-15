class MinimaxAgent:
    def __init__(self, depth, heuristic, player):
        self.depth = depth
        self.heuristic = heuristic
        self.player = player

    def get_move(self, game):
        _, move = self.minimax(game, self.depth, True)
        return move

    def minimax(self, game, depth, maximizingPlayer):
        if depth == 0 or game.is_terminal():
            return self.heuristic(game, self.player), None

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
        return self.alpha_beta(game, self.depth, float('-inf'), float('inf'), True)


    def alpha_beta(self, game, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or game.is_terminal():
            return self.heuristic(game, self.player), None

        if maximizingPlayer:
            maxEval = float('-inf')
            best_move = None
            for move in game.legal_moves:
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
            for move in game.legal_moves:
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