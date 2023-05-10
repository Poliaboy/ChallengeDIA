# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 08:36:21 2023

@author: qwent
"""


def Actions(table):
    liste = []
    for i in range(3):
        for j in range(3):
            if plateau[i][j] == " ":
                liste.append((i, j))
    return liste


def Result(table, a, player):
    i, j = a
    table[i][j] = player
    return table


def Terminal_Test(plateau):
    # Vérifie s'il reste des cases vides
    if all(plateau[i][j] != " " for i in range(3) for j in range(3)):
        return True

    else:
        for i in range(3):
            if plateau[i][0] == plateau[i][1] == plateau[i][2] != " ":
                return True

        # Vérifie si une colonne est complétée par un joueur
        for j in range(3):
            if plateau[0][j] == plateau[1][j] == plateau[2][j] != " ":
                return True

        # Vérifie si une diagonale est complétée par un joueur
        if plateau[0][0] == plateau[1][1] == plateau[2][2] != " ":
            return True
        if plateau[0][2] == plateau[1][1] == plateau[2][0] != " ":
            return True
    return False


def Utility(plateau):
    for symbole in ["O", "X"]:
        # Vérifie les lignes
        if any([all([case == symbole for case in ligne]) for ligne in plateau]):
            return -1 if symbole == "O" else 1
        # Vérifie les colonnes
        if any([all([plateau[i][j] == symbole for i in range(3)]) for j in range(3)]):
            return -1 if symbole == "O" else 1
        # Vérifie les diagonales
        if all([plateau[i][i] == symbole for i in range(3)]) or all([plateau[i][2 - i] == symbole for i in range(3)]):
            return -1 if symbole == "O" else 1
    return 0


def Minimax_Decision(plateau):
    # Détermine l'action optimale pour le joueur maximisant le gain
    v = float("-inf")
    meilleure_action = None
    for action in Actions(plateau):
        valeur = Min_Value(Result(plateau, action, "X"))
        if valeur > v:
            v = valeur
            meilleure_action = action
    return meilleure_action


# Retourne l'action optimale pour le joueur maximisant le gain
def Max_Value(plateau):
    if Terminal_Test(plateau):
        return Utility(plateau)
    v = float("-inf")
    for action in Actions(plateau):
        v = max(v, Min_Value(Result(plateau, action, "X")))
    return v


# Retourne l'action optimale pour le joueur minimisant le gain
def Min_Value(plateau):
    if Terminal_Test(plateau):
        return Utility(plateau)
    v = float("inf")
    for action in Actions(plateau):
        v = min(v, Max_Value(Result(plateau, action, "O")))

    return v


def affiche_plateau(plateau):
    for i in range(3):
        print("|", end="")
        for j in range(3):
            print(plateau[i][j] + "|", end="")
        print()

plateau = [[" "]*3 for _ in range(3)]
player='X'
# Boucle principale du jeu
while not Terminal_Test(plateau):
    affiche_plateau(plateau)
    print("C'est à votre tour de jouer (X) : ")
    action = input("Veuillez entrer les coordonnées de votre action sous forme i,j : ")
    i, j = action.split(",")
    i, j = int(i), int(j)

    # i, j=Minimax_Decision(plateau,player)
    if plateau[i][j] != " ":
        print("Case déjà remplie, choisissez une autre case.")

    Result(plateau, (i, j), player)

    player = 'O'
    if Terminal_Test(plateau):
        break
    print("L'ordinateur (O) joue : ")
    i, j = Minimax_Decision(plateau)
    plateau = Result(plateau, (i, j), player)
    player = 'X'