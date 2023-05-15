from Agents.Agents import AlphaBetaAgent
from Agents.Heuristics import attack_heur, defensive_heur, heur1


class UltimateAgent():
    def __init__(self, player):
        self.agentLate = AlphaBetaAgent(5, heur1, player)

    def get_move(self, game):
        evalLate, moveLate = self.agentLate.get_move(game)
        print("Late: ", evalLate, moveLate)

        return evalLate, moveLate
