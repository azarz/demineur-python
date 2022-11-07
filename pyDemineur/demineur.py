import argparse
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from PyQt5.QtWidgets import QApplication
from pyDemineur.ui.gui import DemineurFenetre
from pyDemineur.core.partie import Partie

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog = 'pyDemineur',
                    description = 'Démineur écrit en Python')
    parser.add_argument('-c', '--console', action='store_true')
    args = parser.parse_args()

    if args.console:
        print("Lancement du démineur en mode console")
        partie = Partie(10, [8, 8])
        partie.jouer()
    else:
        print("Lancement du démineur en mode fenêtre")
        app = QApplication.instance()
        if not app:
            app = QApplication(sys.argv)

        fen = DemineurFenetre()
        fen.show()

        app.exec_()
