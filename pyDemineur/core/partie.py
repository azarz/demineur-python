from pyDemineur.core.grille import Grille

class Partie(object):
    """Classe définissant la partie de démineur

    Attributes
    ----------
    nb_mines_initial : int
        nombre initial de mines dans la grille
    taille_grille : int[2]
        taille de la grille sous le format [nombre de lignes, nombre de colonnes]
    nb_mines_restantes : int
        nombre de mines restant à marquer
    nb_mines_moins_cases_marquees : int
        nombre de mines moins nombre de cases marquées
    grille : Grille
        Grille de la partie
    cases_vides_marquees : int
        Nombre de cases qui ne sont pas des mines mais qui sont marquées
    """

    def __init__(self, nb_mines_initial, taille_grille):
        """Constructeur de la classe Partie

        Parameters
        ----------
        nb_mines_initial : int
            nombre initial de mines dans la grille
        taille_grille : int[2]
            taille de la grille sous le format [nombre de lignes, nombre de colonnes]
        """
        if nb_mines_initial >= taille_grille[0] * taille_grille[1]:
            raise ValueError("Il ne peut pas y avoir autant ou plus de mines que de cases dans la grille")

        self._nb_mines_initial = nb_mines_initial
        self._taille_grille = taille_grille
        self._nb_mines_restantes = nb_mines_initial
        self._nb_mines_moins_cases_marquees = nb_mines_initial

        self._grille = Grille(nb_mines_initial, taille_grille)

        self._cases_vides_marquees = 0

    @property
    def grille(self):
        """Retourne la grille de la partie

        Returns
        -------
        Grille
            Grille de la partie
        """
        return self._grille

    @property
    def nb_mines_moins_cases_marquees(self):
        """Retourne le nombre de mines moins nombre de cases marquées

        Returns
        -------
        int
            nombre de mines moins nombre de cases marquées
        """
        return self._nb_mines_moins_cases_marquees

    def jouer(self):
        """Fonction qui lance la partie
        """
        perdu = False
        while not perdu:
            print(self._grille)
            try:
                decouvrir = int(input("Action (Marquer: 0; Decouvrir: 1) : "))
                ligne = int(input("Ligne (entre 0 et {}) ? ".format(self._taille_grille[0] - 1)))
                colonne = int(input("Colonne (entre 0 et {}) ? ".format(self._taille_grille[0] - 1)))
                if decouvrir:
                    perdu = self.decouvrir_case(ligne, colonne)
                else:
                    # Mine marquée vaut 1 si on a marqué une mine et
                    # 2 si on a démarqué une mine : on change le compteur
                    # de mines restantes en conséquence
                    self.marquer_case(ligne, colonne)

                    if self.test_victoire():
                        print("Gagné !!")
                        break

            except IndexError:
                print("erreur de saisie : donner ligne et colonne valides")
                continue
            except ValueError:
                print("erreur de saisie")
                continue

        print("fini")
        print(self._grille)
        # Partie finie : réinitialisation de la grille
        self._grille = Grille(self._nb_mines_initial, self._taille_grille)
        self._nb_mines_restantes = self._nb_mines_initial

    def test_victoire(self):
        """Teste la victoire de la partie

        Returns
        -------
        bool
            True si la partie est gagnée, False sinon
        """
        if self._nb_mines_restantes == 0 and self._cases_vides_marquees == 0:
            return True
        return False

    def marquer_case(self, ligne, colonne):
        """Marque ou démarque une case à partir de ses coordonnées

        Parameters
        ----------
        ligne : int
            ligne de la case à marquer
        colonne : int
            colonne de la case à marquer

        Returns
        -------
        int

        """
        # Cette fonction retourne
        # 1 si on a marqué une mine,
        # 2 si on a démarqué une mine,
        # 0 si on a marqué une non mine et
        # -1 si on a démarqué une non_mine
        marquage = self._grille.marquer_case(self._grille.trouver_case(ligne, colonne))

        if marquage == 1:
            self._nb_mines_restantes -= 1
            self._nb_mines_moins_cases_marquees -= 1
        elif marquage == 2:
            self._nb_mines_restantes += 1
            self._nb_mines_moins_cases_marquees += 1
        # On compte le nombre de case non minées marquées pour avoir
        # un condition de victoire correcte.
        elif marquage == 0:
            self._cases_vides_marquees += 1
            self._nb_mines_moins_cases_marquees -= 1
        elif marquage == -1:
            self._cases_vides_marquees -= 1
            self._nb_mines_moins_cases_marquees += 1

    def decouvrir_case(self, ligne, colonne):
        """Découvre une case à partir de ses coordonnées

        Parameters
        ----------
        ligne : int
            ligne de la case à découvrir
        colonne : int
            colonne de la case à découvrir

        Returns
        -------
        bool
            True si la case découverte est une mine, False sinon
        """
        return self._grille.decouvrir_case(self._grille.trouver_case(ligne, colonne))


if __name__ == "__main__":
    partie = Partie(10, [8, 8])
    partie.jouer()
