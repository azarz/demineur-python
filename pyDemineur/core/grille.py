import numpy as np

from pyDemineur.core.caseMinee import CaseMinee
from pyDemineur.core.caseNumerotee import CaseNumerotee
from pyDemineur.core.caseVide import CaseVide
from pyDemineur.core.etatCase import EtatCase

class Grille(object):
    """Classe définissant la grille de démineur

    Attributes
    ----------
    nb_mines : int
        nombre de mines dans la grille
    taille_grille : int[2]
        taille de la grille sous le format [nombre de lignes, nombre de colonnes]
    cases : Case[lignes][colonnes]
        tableau à 2 dimensions contenant les Cases de la grille
    """

    def __init__(self, nb_mines, taille):
        """Constructeur de la classe Grille

        Parameters
        ----------
        nb_mines : int
            nombre de mines dans la grille
        taille_grille : int[2]
            taille de la grille sous le format [nombre de lignes, nombre de colonnes]
        """

        self._taille = taille
        self._cases = [[0 for col in range(taille[1])] for lin in range(taille[0])]
        positions = np.random.choice(taille[0] * taille[1], nb_mines, replace = False)
        for pos in positions:
            ligne = pos // taille[0]
            colonne = pos % taille[1]
            self._cases[ligne][colonne] = CaseMinee(ligne, colonne)

        # Pour l'initialisation de la partie sur une case vide
        cases_vides = []
        for ligne in range(self._taille[0]):
            for col in range(self._taille[1]):
                if self._cases[ligne][col] == 0:
                    count = self._countMines(self._voisinage(ligne, col))
                    if count == 0:
                        case_vide = CaseVide(ligne, col)
                        self._cases[ligne][col] = case_vide
                        cases_vides.append(case_vide)
                    else:
                        self._cases[ligne][col] = CaseNumerotee(ligne, col, count)

        self.decouvrir_case(np.random.choice(cases_vides))


    def __str__(self):
        """Définit l'affichage de la grille
        """
        result = ""
        for ligne in self._cases:
            for cell in ligne:
                if cell.etat == EtatCase.MASQUEE:
                    result += "? "
                elif cell.etat == EtatCase.MARQUEE:
                    result += "! "
                else:
                    if isinstance(cell, CaseMinee):
                        result += "M "
                    elif isinstance(cell, CaseNumerotee):
                        result += str(cell.numero)
                        result += " "
                    else:
                        result += "0 "
            result += "\n"

        return result

    def trouver_case(self, ligne, colonne):
        """Trouve une case à partir de ses coordonnées

        Parameters
        ----------
        ligne : int
            ligne de la case à trouver dans la grille
        colonne : int
            colonne de la case à trouver dans la grille
        """
        return self._cases[ligne][colonne]

    def marquer_case(self, case):
        """Marque ou démarque la case donnée en entrée

        Parameters
        ----------
        case : Case
            Case à marquer

        Returns
        -------
        int
            1 si on a marqué une mine
            2 si on a démarqué une mine
            0 si on a marqué une non_mine
            -1 si on a démarqué une non_mine
        """
        return case.marquer()

    def decouvrir_case(self, case):
        """Découvre la case donnée en entrée

        Parameters
        ----------
        case : Case
            Case à découvrir

        Returns
        -------
        bool
            True si la case découverte est une mine, False sinon
        """
        if case.etat == EtatCase.MARQUEE:
            return False
        case.decouvrir()
        if isinstance(case, CaseMinee):
            return True
        if isinstance(case, CaseVide):
            for voisin in self._voisinage(case.ligne, case.colonne):
                if voisin.etat == EtatCase.MASQUEE:
                    self.decouvrir_case(voisin)
        return False

    def _voisinage(self, ligne, colonne):
        """Retourne le voisinage (connectivité à 8) d'une cellule dans la grille

        Parameters
        ----------
        ligne : int
            ligne de la case dont on veut le voisinage
        colonne : int
            colonne de la case dont on veut le voisinage

        Returns
        -------
        Case[]
            Liste des cases du voisinage
        """
        result = []
        if ligne > 0 and colonne > 0:
            result.append(self._cases[ligne - 1][colonne - 1])
        if ligne > 0:
            result.append(self._cases[ligne - 1][colonne])
        if ligne > 0 and (colonne + 1) < self._taille[1]:
            result.append(self._cases[ligne - 1][colonne + 1])
        if colonne > 0:
            result.append(self._cases[ligne][colonne - 1])
        if (colonne + 1) < self._taille[1]:
            result.append(self._cases[ligne][colonne + 1])
        if (ligne + 1) < self._taille[0] and colonne > 0:
            result.append(self._cases[ligne + 1][colonne - 1])
        if (ligne + 1) < self._taille[0]:
            result.append(self._cases[ligne + 1][colonne])
        if (ligne + 1) < self._taille[0] and (colonne + 1) < self._taille[1]:
            result.append(self._cases[ligne + 1][colonne + 1])

        return result

    def _countMines(self, voisinage):
        """Compte le nombre de mines dans un voisinage

        Parameters
        ----------
        voisinnage : Case[]
            liste de Cases

        Returns
        -------
        int
            Nombre de case minées dans le voisinage
        """
        count = 0
        for case in voisinage:
            if isinstance(case, CaseMinee):
                count += 1

        return count
