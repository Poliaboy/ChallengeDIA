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