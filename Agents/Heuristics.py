def heur1(game, player):
    otherPlayer = "O" if player == "X" else "X"
    p1_wins = sum(cell == player for row in game.big_board for cell in row)
    p2_wins = sum(cell == otherPlayer for row in game.big_board for cell in row)
    return p1_wins - p2_wins


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
            if game.big_board[i][j] == player:
                if ((game.big_board[i][(j + 1) % 3] == player and game.big_board[i][(j + 2) % 3] != otherPlayer) or
                        (game.big_board[(i + 1) % 3][j] == player and game.big_board[(i + 2) % 3][j] != otherPlayer) or
                        (i == j and game.big_board[(i + 1) % 3][(j + 1) % 3] == player and game.big_board[(i + 2) % 3][
                            (j + 2) % 3] != otherPlayer) or
                        (i + j == 2 and game.big_board[(i + 1) % 3][(2 - j + 1) % 3] == player and
                         game.big_board[(i + 2) % 3][(2 - j + 2) % 3] != otherPlayer)):
                    score += 4
            elif game.big_board[i][j] == otherPlayer:
                if ((game.big_board[i][(j + 1) % 3] == otherPlayer and game.big_board[i][(j + 2) % 3] != player) or
                        (game.big_board[(i + 1) % 3][j] == otherPlayer and game.big_board[(i + 2) % 3][j] != player) or
                        (i == j and game.big_board[(i + 1) % 3][(j + 1) % 3] == otherPlayer and
                         game.big_board[(i + 2) % 3][
                             (j + 2) % 3] != player) or
                        (i + j == 2 and game.big_board[(i + 1) % 3][(2 - j + 1) % 3] == otherPlayer and
                         game.big_board[(i + 2) % 3][(2 - j + 2) % 3] != player)):
                    score -= 4

    return score