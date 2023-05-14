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

def play_game_human(game, agent, order):
    while not game.is_terminal():
        if order == 1:
            move = agent.get_move(game)
            game.make_move(move)
            game.display()

            if game.is_terminal():
                break
            print("Enter your move: ")
            move = tuple(map(int, input().split(" ")))
            game.make_move(move)
        else:
            print("Enter your move: ")
            move = tuple(map(int, input().split(" ")))
            game.make_move(move)

            if game.is_terminal():
                break

            move = agent.get_move(game)
            game.display()
            game.make_move(move)




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
