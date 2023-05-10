from tic_tac_toe import Tic_Tac_Toe
from ultimate_TTT import UltimateTTT


def jouer():
    ultimate_ttt = UltimateTTT()
    while not ultimate_ttt.is_terminal():
        print(ultimate_ttt.__str__())
        print("C'est au joueur", ultimate_ttt.player, "de jouer.")
        if ultimate_ttt.is_next_grid_full():
            print("Choisissez une grille non complétée.")


        print("Veuillez entrer les coordonnées de votre action sous forme i,j : ")
        action = input()
        i, j = action.split(",")
        i, j = int(i), int(j)
        if ultimate_ttt.boardU[i][j].winner == 0:
            print("Case déjà remplie, choisissez une autre case.")
        else:
            ultimate_ttt.play_on_all_grid(i, j)
            ultimate_ttt.is_terminal()
            ultimate_ttt.player = "X" if ultimate_ttt.player == "O" else "O"
    print(ultimate_ttt)
    if ultimate_ttt.winner == 0:
        print("Match nul.")
    else:
        print("Le joueur", ultimate_ttt.winner, "a gagné.")


if __name__ == "__main__":
    jouer()