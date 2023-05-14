import time

from Agents.Agents import AlphaBetaAgent, MinimaxAgent
from Agents.Heuristics import heur1, heur2
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

def human_play(game):
    print("Enter your move: ")
    move = tuple(map(int, input().split(" ")))
    legal_moves = game.get_legal_moves()
    if move not in legal_moves:
        print("Illegal move!")
        while move not in legal_moves:
            print("Enter your move: ")
            move = tuple(map(int, input().split(" ")))
    return move

def play_game_human(game, agent, order):
    while not game.is_terminal():
        if order == 1:
            print("Ai's turn'")
            move = agent.get_move(game)
            game.make_move(move)
            game.display()

            if game.is_terminal():
                break

            move = human_play(game)
            game.make_move(move)
            game.display()


        else:
            move = human_play(game)
            game.make_move(move)
            game.display()

            if game.is_terminal():
                break

            print("Ai's turn'")
            move = agent.get_move(game)
            game.make_move(move)
            game.display()




if __name__ == '__main__':
    # Create the game and the agents
    game = Game()
    agent1 = MinimaxAgent(4, heur1, "X")
    agent2 = AlphaBetaAgent(4, heur2, "O")

    # Play the game
    print("Starting game...")
    print("Who starts? (1 - user, 2 - opponent)")
    order = int(input())
    play_game_human(game, agent1, order)
    game.display()
