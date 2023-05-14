from tic_tac_toe import Tic_Tac_Toe
from ultimate_TTT import UltimateTTT


def jouer():

    ultimate_ttt = UltimateTTT()
    for i in range(3):
        for j in range(3):
            ultimate_ttt.boardU[i][j].is_terminal()
    while not ultimate_ttt.is_terminal():
        print(ultimate_ttt.__str__())
        print("C'est au joueur", ultimate_ttt.player, "de jouer.")
        check = False
        if ultimate_ttt.is_next_board_full():
            while check is False:
                print("Choisissez une grille non complétée.")
                boardNb = int(input()) - 1
                if ultimate_ttt.boardU[boardNb // 3][boardNb % 3].state:
                    print("Cette grille est complétée.")
                    continue
                print("Choisissez une case non complétée (de 1 à 9).")
                cell = int(input()) - 1
                if divmod(cell,3) not in ultimate_ttt.boardU[boardNb // 3][boardNb % 3].possible_actions():
                    print("Cette case est complétée.")
                    continue
                check = True
        else:
            while check is False:
                print("Vous pouvez jouer dans la grille", ultimate_ttt.next_board + 1)
                boardNb = ultimate_ttt.next_board
                print("Choisissez une case non complétée (de 1 à 9).")
                cell = int(input()) - 1
                if divmod(cell,3) not in ultimate_ttt.boardU[boardNb // 3][boardNb % 3].possible_actions():
                    print("Cette case est complétée.")
                    continue
                check = True
        ultimate_ttt.player_turn(boardNb, cell)
        # winner
        if ultimate_ttt.winner != 0:
            print(ultimate_ttt.__str__())
            print("Le joueur", ultimate_ttt.winner, "a gagné.")
            break



if __name__ == "__main__":
    jouer()

