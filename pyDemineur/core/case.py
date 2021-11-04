from pyDemineur.core.etatCase import EtatCase

class Case(object):
    """Classe abstraite définissant les cases

    Attributes
    ----------
    ligne : int
        ligne de la case
    colonne : int
        colonne de la case
    etat : EtatCase
        état de la case
    """

    def __init__(self, ligne, colonne):
        """Constructeur de la classe

        Parameters
        ----------
        ligne : int
            ligne de la case
        colonne : int
            colonne de la case
        """
        self._etat = EtatCase.MASQUEE
        self._ligne = ligne
        self._colonne = colonne

    @property
    def etat(self):
        """Retourne l'état de la case

        Returns
        -------
        EtatCase
            état de la case
        """
        return self._etat

    @property
    def ligne(self):
        """Retourne la ligne de la case

        Returns
        -------
        int
            ligne de la case
        """
        return self._ligne

    @property
    def colonne(self):
        """Retourne la colonne de la case

        Returns
        -------
        int
            colonne de la case
        """
        return self._colonne

    def marquer(self):
        """Marque ou démarque la case en changeant son état

        Returns
        -------
        int
            0 si on a marqué une non_mine
            -1 si on a démarqué une non_mine
        """
        if self._etat == EtatCase.MASQUEE:
            self._changer_etat(EtatCase.MARQUEE)
            return 0
        elif self._etat == EtatCase.MARQUEE:
            self._changer_etat(EtatCase.MASQUEE)
            return -1

    def decouvrir(self):
        """Découvre la case en changeant son état
        """
        raise NotImplementedError()

    def _changer_etat(self, etat):
        """Change l'etat de la case

        Parameters
        ----------
        etat : EtatCase
            Etat vers lequel la case doit transitionner
        """
        self._etat = etat
