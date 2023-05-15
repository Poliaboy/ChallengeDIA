from Agents.Agents import AlphaBetaAgent
from Agents.Heuristics import attack_heur, defensive_heur, heur1, heuristic_ultimate


class UltimateAgent():
    def __init__(self, player):
        self.agentLate = AlphaBetaAgent(5, heuristic_ultimate, player)

    def get_move(self, game):
        evalLate, moveLate = self.agentLate.get_move(game)
        print("Best Move evaluated: ", evalLate, moveLate)

        return evalLate, moveLate
