from pkg_resources import resource_filename
import sys

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFontDatabase, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLayout, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QLabel
from pyDemineur.core.partie import Partie
from pyDemineur.ui.uiCase import UICase


class DemineurFenetre(QWidget):
    """Classe QT définissant l'affichage de la fenêtre principale
   """
    def __init__(self):
        QWidget.__init__(self)
        # Ajout de la police personnalisée dans l'application
        QFontDatabase.addApplicationFont(resource_filename("pyDemineur.res", "Open-24-Display-St.ttf"))
        # Définition de l'icône dans la barre des tâches
        self.setWindowIcon(QIcon(resource_filename("pyDemineur.res", "icon.png")))

        self.partie = None

        self.setWindowTitle("Démineur")

        self.start_bouton_easy = QPushButton("Easy")
        self.start_bouton_medium = QPushButton("Medium")
        self.start_bouton_hard = QPushButton("Hard")
        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        self.grid.setSizeConstraint(QLayout.SetFixedSize)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_bouton_easy)
        button_layout.addWidget(self.start_bouton_medium)
        button_layout.addWidget(self.start_bouton_hard)

        self.remaining_count_label = QLabel()
        self.remaining_count_label.setAlignment(Qt.AlignCenter)
        self.remaining_count_label.setStyleSheet("""
            background-color: black;
            color: red;
            font-weight: bold;
            font-family: Open 24 Display St;
            font-size: 40px;
            padding: 0px;
        """)
        self.remaining_count_label.setFixedSize(QSize(120, 40))

        self.layout = QVBoxLayout()
        self.layout.setSizeConstraint(QLayout.SetFixedSize)

        self.layout.addLayout(button_layout)
        self.layout.addWidget(self.remaining_count_label)
        self.layout.setAlignment(self.remaining_count_label, Qt.AlignHCenter);
        self.layout.addLayout(self.grid)
        self.setLayout(self.layout)

        self.ui_cases = []

        self.start_bouton_easy.clicked.connect(lambda: self._initPartie(10, [8, 8]))
        self.start_bouton_medium.clicked.connect(lambda: self._initPartie(40, [16, 16]))
        self.start_bouton_hard.clicked.connect(lambda: self._initPartie(99, [24, 24]))

        self.setStyleSheet("""
            background-color: white;
        """)

    def _initPartie(self, nb_mines_initial, taille_grille):
        """Initialise une partie de démineur

        Parameters
        ----------
        nb_mines_initial : int
            nombre de mines inital dans la partie
        taille_grille : int[2]
            taille de la grille sous le format [nombre de lignes, nombre de colonnes]
        """
        self.partie = Partie(nb_mines_initial, taille_grille)
        self.remaining_count_label.setText(str(nb_mines_initial))

        # Suppression des éléments de la partie précédente
        for i in reversed(range(self.grid .count())):
            self.grid.itemAt(i).widget().setParent(None)

        self.ui_cases = []

        for x in range(taille_grille[1]):
            for y in range(taille_grille[0]):
                uiCase = UICase(self.partie, x, y)
                uiCase.perdu_signal.connect(self._perdre)
                uiCase.gagne_signal.connect(self._gagner)
                uiCase.update_grid.connect(self._updateDisplay)

                self.grid.addWidget(uiCase, y, x)
                self.ui_cases.append(uiCase)

        self._updateDisplay()

    def _perdre(self):
        """Fonction déclenchée lors de la défaite
        """
        msg = QMessageBox()
        msg.setWindowTitle("Perdu")
        msg.setText("Perdu !")
        msg.exec_()
        self._initPartie(10, [8, 8])

    def _gagner(self):
        """Fonction déclenchée lors de la victoire
        """
        msg = QMessageBox()
        msg.setWindowTitle("Gagné")
        msg.setText("Gagné !")
        msg.exec_()

    def _updateDisplay(self):
        """Met à jour l'affichage de la grille
        """
        self.remaining_count_label.setText(str(self.partie.nb_mines_moins_cases_marquees))
        for uiCase in self.ui_cases:
            uiCase.updateDisplay()


if __name__ == "__main__":
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    fen = DemineurFenetre()
    fen.show()

    app.exec_()
