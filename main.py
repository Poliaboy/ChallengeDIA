import time

from Agents.Agents import AlphaBetaAgent, MinimaxAgent
from Agents.Heuristics import heur1, heur2, Heuristic, heuristic_combo, heur_tie_push
from Structure.UltimateTTT import Game


def play_game(game, agent1, agent2):
    while not game.is_terminal():
        start_time = time.time()
        move = agent1.get_move(game)
        end_time = time.time()
        game.display()
        print(f"Agent1's decision time: {end_time - start_time} seconds.")
        game.make_move(move)

        if game.is_terminal():
            break

        start_time = time.time()
        move = agent2.get_move(game)
        end_time = time.time()
        game.display()
        print(f"Agent2's decision time: {end_time - start_time} seconds.")
        game.make_move(move)


def get_move():
    big_board_number, small_board_number = tuple(map(int, input().split(" ")))
    # Convert into X and Y coordinates, X being lines and Y being columns
    move = ((big_board_number - 1) // 3) * 3 + ((small_board_number - 1) // 3), ((big_board_number - 1) % 3) * 3 + (
            (small_board_number - 1) % 3)

    return move


def human_play(game):
    print("Enter your move: (Select a small board first from 1 to 9, then a cell from 1 to 9), eg 1 1")
    move = get_move()
    legal_moves = game.get_legal_moves()
    print(legal_moves)
    while move not in legal_moves:
        print("Illegal move, try again")
        move = get_move()
    return move


def play_game_human(game, agent, order):
    while not game.is_terminal():
        if order == 1:
            print("Ai's turn'")
            start_time = time.time()
            move = agent.get_move(game)
            end_time = time.time()
            game.make_move(move)
            game.display()

            if game.is_terminal():
                break

            move = human_play(game)
            game.make_move(move)
            game.display()
            print(f"Agent's decision time: {end_time - start_time} seconds.")


        else:
            game.display()
            move = human_play(game)
            game.make_move(move)

            if game.is_terminal():
                break

            print("Ai's turn'")
            start_time = time.time()
            move = agent.get_move(game)
            end_time = time.time()
            game.make_move(move)
            game.display()
            print(f"Agent's decision time: {end_time - start_time} seconds.")
    print("Game over")


def human_vs_ai():
    # Create the game and the agents
    game = Game()
    agent1 = MinimaxAgent(4, Heuristic, "X")
    agent2 = AlphaBetaAgent(6, Heuristic, "O")

    # Play the game
    print("Starting game...")
    print("Who starts? (1 - opponent, 2 - user)")
    order = int(input())
    play_game_human(game, agent2, order)
    game.display()

    # display winner
    if game.winner() == "X":
        print("Player X wins!")
    elif game.winner() == "O":
        print("Player O wins!")
    else:
        print("Tie game.")


def ai_vs_ai():
    # Create the game and the agents
    game = Game()
    agent1 = MinimaxAgent(3, heuristic_combo, "X")
    agent2 = AlphaBetaAgent(6, heuristic_combo, "O")

    play_game(game, agent1, agent2)
    game.display()

    # display winner
    if game.winner() == "X":
        print("Player X wins!")
    elif game.winner() == "O":
        print("Player O wins!")
    else:
        print("Tie game.")


if __name__ == '__main__':
    print("Choose mode: 1 - AI vs AI, 2 - Human vs AI")
    choix = int(input())
    if choix == 1:
        ai_vs_ai()
    else:
        human_vs_ai()
