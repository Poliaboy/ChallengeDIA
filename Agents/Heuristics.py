def heur1(game, player):
    otherPlayer = "O" if player == "X" else "X"
    p1_wins = sum(cell == player for row in game.big_board for cell in row)
    p2_wins = sum(cell == otherPlayer for row in game.big_board for cell in row)
    return (p1_wins - p2_wins)*1000


def heur2(game, player):
    otherPlayer = "O" if player == "X" else "X"
    score = 0
    # Check small board wins, center board wins, corner board wins,
    # center square in any small board and square in the center board
    for i in range(9):
        for j in range(9):
            if game.board[i][j] == player:
                score += 5
                if i == 4 and j == 4:
                    score += 10
                if i in [0, 2, 6, 8] and j in [0, 2, 6, 8]:
                    score += 3
                if i % 3 == 1 and j % 3 == 1:
                    score += 3
                if i == 4 or j == 4:
                    score += 3
            elif game.board[i][j] == otherPlayer:
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
            if ((game.big_board[i][(j + 1) % 3] == player and game.big_board[i][(j + 2) % 3] != otherPlayer) or
                    (game.big_board[(i + 1) % 3][j] == player and game.big_board[(i + 2) % 3][j] != otherPlayer) or
                    (i == j and game.big_board[(i + 1) % 3][(j + 1) % 3] == player and game.big_board[(i + 2) % 3][
                        (j + 2) % 3] != otherPlayer) or
                    (i + j == 2 and game.big_board[(i + 1) % 3][(2 - j + 1) % 3] == player and
                     game.big_board[(i + 2) % 3][(2 - j + 2) % 3] != otherPlayer)):
                score = score + 4 if game.big_board[i][j] == player else score - 4

    return score


def heur3(game, player):
    otherPlayer = "O" if player == "X" else "X"

    score = 0
    for i in range(3):
        for j in range(3):
            small_board = game.get_small_board(i, j)
            score += count_opportunities(small_board, player)
            score -= count_opportunities(small_board, otherPlayer)

    # also consider the big board
    big_board_flat = [cell for row in game.big_board for cell in row]
    score += count_opportunities(big_board_flat, player)
    score -= count_opportunities(big_board_flat, otherPlayer)
    return score


def count_opportunities(board, player):
    lines = [board[i * 3:i * 3 + 3] for i in range(3)] + \
            [board[i::3] for i in range(3)] + \
            [board[::4], board[2:8:2]]
    return sum(line.count(player) == 2 and line.count(None) == 1 for line in lines)

def heur8(game, player):
    otherPlayer = "O" if player == "X" else "X"
    score = 0

    big_board_flat = [cell for row in game.big_board for cell in row]
    if game.check_winner(big_board_flat) == player:
        return 100000

    for i in range(3):
        for j in range(3):
            small_board = game.get_small_board(i, j)
            score += count_opportunities(small_board, player) * 100
            score -= count_opportunities(small_board, otherPlayer) * 100

    big_opportunities = count_opportunities(game.big_board, player)
    score += big_opportunities * 1000

    big_penalty = count_opportunities(game.big_board, otherPlayer)
    score -= big_penalty * 1000

    for move in game.get_legal_moves():
        game.make_move(move)
        if game.check_small_board(move[0] // 3, move[1] // 3) == otherPlayer:
            score -= 100
        game.undo_move(move)

    return score



def heur_tie_push(game, player):
    score = 0
    # consider the opposite player
    otherPlayer = 'O' if player == 'X' else 'X'

    for i in range(3):
        for j in range(3):
            small_board = game.get_small_board(i, j)
            player_opportunities = count_opportunities(small_board, player)
            opponent_opportunities = count_opportunities(small_board, otherPlayer)
            score += abs(player_opportunities - opponent_opportunities)

    # also consider the big board
    big_board_flat = [cell for row in game.big_board for cell in row]
    player_opportunities = count_opportunities(big_board_flat, player)
    opponent_opportunities = count_opportunities(big_board_flat, otherPlayer)
    score += abs(player_opportunities - opponent_opportunities)

    return score


def defensive_heur(game, player):
    # If the player wins the big board, return 10000
    big_board_flat = [cell for row in game.big_board for cell in row]
    if game.check_winner(big_board_flat) == player:
        return 10000

    score = 0
    # consider the opposite player
    opposite_player = 'O' if player == 'X' else 'X'

    for i in range(3):
        for j in range(3):
            small_board = game.get_small_board(i, j)
            player_opportunities = count_opportunities(small_board, player)
            opponent_opportunities = count_opportunities(small_board, opposite_player)
            # Defensive strategy: prioritize blocking opponent's opportunities over creating own opportunities
            score += player_opportunities * 5 - opponent_opportunities * 10

    # also consider the big board
    player_opportunities = count_opportunities(big_board_flat, player)
    opponent_opportunities = count_opportunities(big_board_flat, opposite_player)
    score += player_opportunities * 5 - opponent_opportunities * 10

    return score

def heur6(game, player):
    # If the player is one move away from winning, return a very high score
    big_board_flat = [cell for row in game.big_board for cell in row]
    if game.check_winner(big_board_flat) == player:
        return 10000

    score = 0
    # consider the opposite player
    otherPlayer = 'O' if player == 'X' else 'X'

    for i in range(3):
        for j in range(3):
            small_board = game.get_small_board(i, j)
            score += count_opportunities(small_board, player)
            score -= count_opportunities(small_board, otherPlayer)

    # also consider the big board
    score += count_opportunities(big_board_flat, player)
    score -= count_opportunities(big_board_flat, otherPlayer)

    return score


# Heuristic than combines heur1, heur2 and heur3, with weights 1, 2 and 3 respectively
def attack_heur(game, player):
    return heur1(game, player) + heur8(game, player)


def heuristic_combo(game, player):
    return heur6(game, player) + heur_tie_push(game, player)


def aggressive_heur(game, player):
    # If the player wins the big board, return 10000
    big_board_flat = [cell for row in game.big_board for cell in row]
    if game.check_winner(big_board_flat) == player:
        return 10000

    score = 0
    # consider the opposite player
    opposite_player = 'O' if player == 'X' else 'X'

    for i in range(3):
        for j in range(3):
            small_board = game.get_small_board(i, j)
            player_opportunities = count_opportunities(small_board, player)
            opponent_opportunities = count_opportunities(small_board, opposite_player)
            # Aggressive strategy: prioritize creating own opportunities and blocking opponent's opportunities
            score += player_opportunities * 10 - opponent_opportunities * 5

    # also consider the big board
    player_opportunities = count_opportunities(big_board_flat, player)
    opponent_opportunities = count_opportunities(big_board_flat, opposite_player)
    score += player_opportunities * 10 - opponent_opportunities * 5

    return score
