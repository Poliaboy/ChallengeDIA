def heur1(game, player):
    otherPlayer = "O" if player == "X" else "X"
    p1_wins = sum(cell == player for row in game.big_board for cell in row)
    p2_wins = sum(cell == otherPlayer for row in game.big_board for cell in row)
    return (p1_wins - p2_wins) * 1000

def heur4(game, player):
    otherPlayer = "O" if player == "X" else "X"
    p2_wins = sum(cell == otherPlayer for row in game.big_board for cell in row)
    return p2_wins * 1000


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


def count_opportunities(board, player):
    otherPlayer = "O" if player == "X" else "X"
    lines = [board[i * 3:i * 3 + 3] for i in range(3)] + \
            [board[i::3] for i in range(3)] + \
            [board[::4], board[2:8:2]]
    return sum(line.count(player) == 2 and line.count(None) == 1 for line in lines), sum(
        line.count(otherPlayer) == 2 and line.count(None) == 1 for line in lines)


def heuristic_optimized(game, player):
    otherPlayer = "O" if player == "X" else "X"
    score = 0

    big_board_flat = [cell for row in game.big_board for cell in row]
    if game.check_winner(big_board_flat) == player:
        return 100000

    # Count opportunities in small boards
    for i in range(3):
        for j in range(3):
            small_board = game.small_boards[i][j]
            player_opportunities, player_penalty = count_opportunities(small_board, player)
            score += player_opportunities * 100
            score -= player_penalty * 100

    # Get legal moves only once
    legal_moves = game.legal_moves
    for move in legal_moves:
        game.make_move(move)
        if game.check_small_board(move[0] // 3, move[1] // 3) == otherPlayer:
            score -= 100
        game.undo_move(move)

    # Count opportunities in big board
    big_opportunities, big_penalty = count_opportunities(game.big_board, player)
    score += big_opportunities * 1000
    score -= big_penalty * 1000

    return score


def heuristic_ultimate(game, player):
    score = 0

    big_board_flat = [cell for row in game.big_board for cell in row]
    if game.check_winner(big_board_flat) == player:
        return 100000

    # Winning Small Boards
    score += heur1(game, player)

    # Potential to Win Small Boards
    for i in range(3):
        for j in range(3):
            small_board = game.small_boards[i][j]
            player_opportunities, opponent_opportunities = count_opportunities(small_board, player)
            score += player_opportunities * 100
            score -= opponent_opportunities * 100

    # Control of Big Board
    for i in range(3):
        for j in range(3):
            small_board = game.small_boards[i][j]
            score += sum(cell == player for cell in small_board) * 10

    # Center Control
    center_small_board = game.small_boards[1][1]
    score += sum(cell == player for cell in center_small_board) * 50

    # Forcing Moves
    if game.last_move is not None:
        last_x, last_y = game.last_move
        next_x, next_y = last_x % 3, last_y % 3
        if game.big_board[next_x][next_y] is None:
            score += 200

    return score


def heur3(game, player):
    otherPlayer = "O" if player == "X" else "X"
    score = 0

    big_board_flat = [cell for row in game.big_board for cell in row]
    if game.check_winner(big_board_flat) == player:
        return 100000

    for i in range(3):
        for j in range(3):
            small_board = game.small_boards[i][j]
            player_opportunities, player_penalty = count_opportunities(small_board, player)
            score += player_opportunities * 100
            score -= player_penalty * 100

    big_opportunities, big_penalty = count_opportunities(game.big_board, player)
    score += big_opportunities * 1000
    score -= big_penalty * 1000

    for move in game.legal_moves:
        game.make_move(move)
        if game.check_small_board(move[0] // 3, move[1] // 3) == otherPlayer:
            score -= 100
        game.undo_move(move)

    return score


def defensive_heur(game, player):
    score = 0

    big_board_flat = [cell for row in game.big_board for cell in row]
    if game.check_winner(big_board_flat) == player:
        return 1000

    # Winning Small Boards
    score -= heur4(game, player)

    # Potential to Win Small Boards
    for i in range(3):
        for j in range(3):
            small_board = game.small_boards[i][j]
            player_opportunities, opponent_opportunities = count_opportunities(small_board, player)
            score += player_opportunities * 100
            score -= opponent_opportunities * 100

    # Control of Big Board
    for i in range(3):
        for j in range(3):
            small_board = game.small_boards[i][j]
            score += sum(cell == player for cell in small_board) * 15

    # Center Control
    center_small_board = game.small_boards[1][1]
    score += sum(cell == player for cell in center_small_board) * 50

    # Forcing Moves
    if game.last_move is not None:
        last_x, last_y = game.last_move
        next_x, next_y = last_x % 3, last_y % 3
        if game.big_board[next_x][next_y] is None:
            score += 200

    return score



def attack_heur(game, player):
    return heur1(game, player) + heuristic_optimized(game, player)
