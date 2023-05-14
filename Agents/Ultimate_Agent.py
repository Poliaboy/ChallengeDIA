from Agents.Agents import AlphaBetaAgent
from Agents.Heuristics import attack_heur, defensive_heur


class UltimateAgent(AlphaBetaAgent):
    def __init__(self, player):
        if player == "X":
            heuristic = attack_heur
        else:
            heuristic = defensive_heur

        super().__init__(6, heuristic, player)
