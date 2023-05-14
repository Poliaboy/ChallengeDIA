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





if __name__ == '__main__':
    # Create the game and the agents
    game = Game()
    agent1 = AlphaBetaAgent(6, heur1)
    agent2 = MinimaxAgent(2, heur2)

    # Play the game
    play_game(game, agent1, agent2)
    game.display()
