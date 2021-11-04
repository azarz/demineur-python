from pyDemineur.core.case import Case
from pyDemineur.core.etatCase import EtatCase

class CaseMinee(Case):
    """Classe définissant les cases minées
    """

    def decouvrir(self):
        """Découvre la case
        """
        self._changer_etat(EtatCase.DECOUVERTE)
        print("Perdu !!")

    def marquer(self):
        """Marque ou démarque la case

        Returns
        -------
        int
            1 si on a marqué la case
            2 si on a démarqué la case
        """
        if self._etat == EtatCase.MASQUEE:
            self._changer_etat(EtatCase.MARQUEE)
            return 1
        elif self._etat == EtatCase.MARQUEE:
            self._changer_etat(EtatCase.MASQUEE)
            return 2
