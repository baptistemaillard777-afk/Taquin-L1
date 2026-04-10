# ============================================================
# JEU DU TAQUIN - Version BETA (mi-projet)
# Concepts utilisés : listes/tableaux, fonctions modulaires,
#                     dictionnaires
# TODO : ajouter une interface graphique tkinter
# ============================================================

import random

# ============================================================
# MODULE : Logique du jeu (tableaux / listes)
# ============================================================

TAILLE = 3  # grille 3x3

def creer_grille():
    """Crée une grille résolue sous forme de liste 2D"""
    grille = []
    compteur = 1
    for i in range(TAILLE):
        ligne = []
        for j in range(TAILLE):
            if i == TAILLE - 1 and j == TAILLE - 1:
                ligne.append(0)  # 0 = case vide
            else:
                ligne.append(compteur)
            compteur += 1
        grille.append(ligne)
    return grille

def melanger_grille(grille):
    """Mélange la grille avec des mouvements aléatoires valides"""
    for _ in range(200):
        moves = mouvements_possibles(grille)
        direction = random.choice(list(moves.keys()))
        deplacer(grille, direction)
    return grille

def trouver_vide(grille):
    """Retourne la position (ligne, col) de la case vide (0)"""
    for i in range(TAILLE):
        for j in range(TAILLE):
            if grille[i][j] == 0:
                return (i, j)
    return None

def mouvements_possibles(grille):
    """
    Retourne un dictionnaire des mouvements possibles
    Clé = direction, Valeur = position de la pièce à déplacer
    Utilisation du cours : DICTIONNAIRES
    """
    li, col = trouver_vide(grille)
    moves = {}

    if li > 0:
        moves["haut"] = (li - 1, col)
    if li < TAILLE - 1:
        moves["bas"] = (li + 1, col)
    if col > 0:
        moves["gauche"] = (li, col - 1)
    if col < TAILLE - 1:
        moves["droite"] = (li, col + 1)

    return moves

def deplacer(grille, direction):
    """Déplace une pièce dans la direction donnée si possible"""
    moves = mouvements_possibles(grille)
    if direction not in moves:
        return False

    li_vide, col_vide = trouver_vide(grille)
    li_piece, col_piece = moves[direction]

    # Échange la pièce avec la case vide
    grille[li_vide][col_vide] = grille[li_piece][col_piece]
    grille[li_piece][col_piece] = 0
    return True

def est_gagne(grille):
    """Vérifie si la grille est dans l'état résolu"""
    grille_gagnante = creer_grille()
    return grille == grille_gagnante

# ============================================================
# MODULE : Affichage terminal
# ============================================================

def afficher_grille(grille):
    """Affiche la grille dans le terminal"""
    print("\n+---+---+---+")
    for ligne in grille:
        print("|", end="")
        for val in ligne:
            if val == 0:
                print("   |", end="")
            else:
                print(f" {val} |", end="")
        print("\n+---+---+---+")

# ============================================================
# MODULE PRINCIPAL
# ============================================================

def main():
    grille = creer_grille()
    melanger_grille(grille)
    nb_coups = 0

    print("=== JEU DU TAQUIN - Version BETA ===")
    print("Commandes : haut / bas / gauche / droite / quitter")

    while True:
        afficher_grille(grille)
        print(f"Coups : {nb_coups}")

        if est_gagne(grille):
            print(f"BRAVO ! Puzzle résolu en {nb_coups} coups !")
            break

        moves = mouvements_possibles(grille)
        print(f"Mouvements possibles : {list(moves.keys())}")

        saisie = input("Votre coup : ").strip().lower()

        if saisie == "quitter":
            print("Au revoir !")
            break
        elif saisie in moves:
            deplacer(grille, saisie)
            nb_coups += 1
        else:
            print("Mouvement invalide, réessayez.")

if __name__ == "__main__":
    main()
