from pyDemineur.core.case import Case
from pyDemineur.core.etatCase import EtatCase

class CaseVide(Case):
    """Classe définissant les cases vides
    """

    def decouvrir(self):
        """Découvre la case
        """
        self._changer_etat(EtatCase.DECOUVERTE)
