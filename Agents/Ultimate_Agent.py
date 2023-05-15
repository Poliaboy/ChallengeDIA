from Agents.Agents import AlphaBetaAgent
from Agents.Heuristics import attack_heur, defensive_heur, heur1, heuristic_ultimate


class UltimateAgent():
    def __init__(self, player):
        self.agent = AlphaBetaAgent(4, heuristic_ultimate, player)
        self.name = "Ultimate Agent"
    def get_move(self, game):
        if game.turn < 3:
            self.agent.depth = 4
        elif game.turn < 15:
            self.agent.depth = 5
        else:
            self.agent.depth = 6
        eval, move = self.agent.get_move(game)
        print("Best Move evaluated: ", eval, move)

        return eval, move
