# ============================================================
# JEU DU TAQUIN - Version BETA (mi-projet)
# Concepts utilisés : listes/tableaux, fonctions modulaires,
#                     dictionnaires, interface tkinter
# TODO : améliorer l'interface, ajouter chronomètre, scores...
# ============================================================

import tkinter as tk
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
        moves["haut"] = (li - 1, col)      # pièce du dessus vient dans le vide
    if li < TAILLE - 1:
        moves["bas"] = (li + 1, col)        # pièce du dessous
    if col > 0:
        moves["gauche"] = (li, col - 1)     # pièce de gauche
    if col < TAILLE - 1:
        moves["droite"] = (li, col + 1)     # pièce de droite

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
# MODULE : Interface graphique avec tkinter
# ============================================================

class TaquinApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu du Taquin - Version BETA")

        # Etat du jeu (dictionnaire)
        self.etat = {
            "grille": creer_grille(),
            "nb_coups": 0,
            "partie_en_cours": False
        }

        # Mélange initial
        melanger_grille(self.etat["grille"])
        self.etat["partie_en_cours"] = True

        # Construction de l'interface
        self._creer_interface()
        self._afficher_grille()

        # Gestion clavier (flèches)
        self.root.bind("<Up>", lambda e: self._jouer("haut"))
        self.root.bind("<Down>", lambda e: self._jouer("bas"))
        self.root.bind("<Left>", lambda e: self._jouer("gauche"))
        self.root.bind("<Right>", lambda e: self._jouer("droite"))

    def _creer_interface(self):
        """Crée tous les widgets tkinter"""

        # Titre
        tk.Label(
            self.root,
            text="=== JEU DU TAQUIN ===",
            font=("Courier", 14, "bold")
        ).pack(pady=5)

        tk.Label(
            self.root,
            text="VERSION BETA",
            font=("Courier", 9),
            fg="gray"
        ).pack()

        # Compteur de coups
        self.label_coups = tk.Label(
            self.root,
            text="Coups : 0",
            font=("Courier", 11)
        )
        self.label_coups.pack(pady=5)

        # Cadre pour la grille de boutons
        self.cadre_grille = tk.Frame(self.root, bd=2, relief="solid")
        self.cadre_grille.pack(padx=10, pady=5)

        # Création des boutons (tableau 2D de widgets)
        self.boutons = []
        for i in range(TAILLE):
            ligne_boutons = []
            for j in range(TAILLE):
                btn = tk.Button(
                    self.cadre_grille,
                    width=4,
                    height=2,
                    font=("Courier", 18, "bold"),
                    command=lambda li=i, col=j: self._clic_bouton(li, col)
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
                ligne_boutons.append(btn)
            self.boutons.append(ligne_boutons)

        # Instructions
        tk.Label(
            self.root,
            text="Cliquez sur une pièce ou utilisez les flèches",
            font=("Courier", 9),
            fg="blue"
        ).pack(pady=3)

        # Boutons actions
        cadre_btns = tk.Frame(self.root)
        cadre_btns.pack(pady=5)

        tk.Button(
            cadre_btns,
            text="Nouvelle Partie",
            font=("Courier", 10),
            command=self._nouvelle_partie
        ).pack(side="left", padx=5)

        tk.Button(
            cadre_btns,
            text="Quitter",
            font=("Courier", 10),
            command=self.root.quit
        ).pack(side="left", padx=5)

        # Message de victoire (caché au départ)
        self.label_victoire = tk.Label(
            self.root,
            text="",
            font=("Courier", 13, "bold"),
            fg="green"
        )
        self.label_victoire.pack(pady=5)

    def _afficher_grille(self):
        """Met à jour l'affichage de tous les boutons"""
        grille = self.etat["grille"]
        for i in range(TAILLE):
            for j in range(TAILLE):
                valeur = grille[i][j]
                if valeur == 0:
                    self.boutons[i][j].config(
                        text="",
                        bg="#cccccc",   # case vide grise
                        state="disabled"
                    )
                else:
                    self.boutons[i][j].config(
                        text=str(valeur),
                        bg="#4a90d9",   # pièce bleue
                        fg="white",
                        state="normal"
                    )

    def _clic_bouton(self, li, col):
        """Gère le clic sur une pièce"""
        if not self.etat["partie_en_cours"]:
            return

        li_vide, col_vide = trouver_vide(self.etat["grille"])

        # Détermine la direction du mouvement
        direction = None
        if li == li_vide - 1 and col == col_vide:
            direction = "haut"
        elif li == li_vide + 1 and col == col_vide:
            direction = "bas"
        elif li == li_vide and col == col_vide - 1:
            direction = "gauche"
        elif li == li_vide and col == col_vide + 1:
            direction = "droite"

        if direction:
            self._jouer(direction)

    def _jouer(self, direction):
        """Effectue un mouvement et vérifie la victoire"""
        if not self.etat["partie_en_cours"]:
            return

        if deplacer(self.etat["grille"], direction):
            self.etat["nb_coups"] += 1
            self.label_coups.config(text=f"Coups : {self.etat['nb_coups']}")
            self._afficher_grille()

            if est_gagne(self.etat["grille"]):
                self.etat["partie_en_cours"] = False
                self.label_victoire.config(
                    text=f"BRAVO ! Résolu en {self.etat['nb_coups']} coups !"
                )

    def _nouvelle_partie(self):
        """Réinitialise et relance une partie"""
        self.etat["grille"] = creer_grille()
        melanger_grille(self.etat["grille"])
        self.etat["nb_coups"] = 0
        self.etat["partie_en_cours"] = True
        self.label_coups.config(text="Coups : 0")
        self.label_victoire.config(text="")
        self._afficher_grille()


# ============================================================
# MODULE PRINCIPAL
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = TaquinApp(root)
    root.mainloop()
