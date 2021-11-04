from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from pyDemineur.core.caseMinee import CaseMinee
from pyDemineur.core.caseNumerotee import CaseNumerotee
from pyDemineur.core.etatCase import EtatCase

numero_colors = ["blue", "green", "orange", "red", "darkviolet", "indigo", "cyan", "yellow"]

class UICase(QPushButton):
    """Classe définissant une case dans l'affichage

    Attributes
    ----------
    perdu_signal : pyqtSignal
        signal envoyé quand le jeu est perdu
    gagne_signal : pyqtSignal
        signal envoyé quand le jeu est gagné
    update_grid : pyqtSignal
        signal envoyé pour que la fenêtre principale mette à jour l'affichage de la grille
    x : int
        colonne de la case
    y : int
        ligne de la case
    _partie : Partie
        partie associée à la case
    """
    perdu_signal = pyqtSignal(int)
    gagne_signal = pyqtSignal(int)
    update_grid = pyqtSignal(int)

    def __init__(self, partie, x, y):
        """Constructeur de la classe

        Parameters
        ----------
        partie : Partie
            partie associée à la case
        x : int
            colonne de la case
        y : int
            ligne de la case
        """
        QPushButton.__init__(self)
        self.setFixedSize(QSize(20, 20))
        self.x = x
        self.y = y
        self._partie = partie

        self.setStyleSheet("""
            border: none;
            background-color: rgb(235, 235, 235);
        """)

    def mousePressEvent(self, event):
        """Evenement déclenché quand la souris a un bouton d'appuyé sur la case

        Lorqu'il s'agit d'un clic gauche, on découvre la case, et si c'est un clic droit, on la marque
        """
        if event.button() == Qt.RightButton:
            self._partie.marquer_case(self.y, self.x)
            self.updateDisplay()
            if self._partie.test_victoire():
                self.gagne_signal.emit(1)

        if event.button() == Qt.LeftButton:
            perdu = not self._partie.decouvrir_case(self.y, self.x)
            self.updateDisplay()
            if self._partie.test_victoire():
                self.gagne_signal.emit(1)
            if perdu:
                self.perdu_signal.emit(1)

        self.update_grid.emit(1)

    def updateDisplay(self):
        """Met à jour l'affichage de la case en fonction de son état et de son type
        """
        cell = self._partie.grille.trouver_case(self.y, self.x)
        if cell.etat == EtatCase.MASQUEE:
            self.setText("")
            self.setStyleSheet("""
                border: none;
                background-color: rgb(235, 235, 235);
            """)

        elif cell.etat == EtatCase.MARQUEE:
            self.setText("🚩")
            self.setStyleSheet("""
                border: none;
                background-color: rgb(235, 235, 235);
                color: red;
            """)

        else:
            self.setStyleSheet("""
                border: none;
                background-color: white;
            """)

            if isinstance(cell, CaseMinee):
                self.setText("💣")
            elif isinstance(cell, CaseNumerotee):
                self.setText(str(cell.numero))
                self.setStyleSheet("""
                    border: none;
                    background-color: white;
                    color: {};
                """.format(numero_colors[cell.numero - 1]))
            else:
                self.setText("")
