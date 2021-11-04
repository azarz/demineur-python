import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from PyQt5.QtWidgets import QApplication
from pyDemineur.ui.gui import DemineurFenetre

if __name__ == "__main__":
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    fen = DemineurFenetre()
    fen.show()

    app.exec_()
