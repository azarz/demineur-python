from pyDemineur.core.case import Case
from pyDemineur.core.etatCase import EtatCase

class CaseNumerotee(Case):
    """Classe définissant les cases vides

    Attributes
    ----------
    numero : int
        numéro de la case (nombre de case minées voisines)
    """

    def __init__(self, ligne, colonne, numero):
        """Constructeur de la classe

        Parameters
        ----------
        ligne : int
            ligne de la case
        colonne : int
            colonne de la case
        numero : int
            numéro de la case numérotée
        """
        super().__init__(ligne, colonne)
        self._numero = numero

    @property
    def numero(self):
        """Retourne le numéro de la case numérotée

        Returns
        -------
        int
            Numéro de la case
        """
        return self._numero

    def decouvrir(self):
        """Découvre la case
        """
        self._changer_etat(EtatCase.DECOUVERTE)
