# Module relatif au traitement des couleurs

from PySide.QtGui import *
from PySide.QtCore import *


class HTMLHighLighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)  # Appelle le __init__ de la classe parent
        self.balises = ('HTML', 'BODY', 'HEAD', 'TITLE', 'BR', 'DIV', 'SPAN', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'IMG', 'P')
        self.attributs = ('src', 'href', 'class', 'id', 'charset', 'rel')

    def select_n_color(self, exp_reguliere, color, text):
        rgx = QRegExp(exp_reguliere)  # Reconnaitre les expressions à colorier
        pos = rgx.indexIn(text, 0)  # Position de la première expression régulière rencontrée

        while pos != -1:
            if self.est_balise_valide(rgx.capturedTexts()[1].upper()):
                self.setFormat(pos, rgx.matchedLength(),QColor.fromRgb(color[0], color[1], color[2]))  # Modificateur du texte sélectionné
            pos += rgx.matchedLength()  # Déplacer à la fin de l'exp regulière
            pos = rgx.indexIn(text, pos)  # expr suivante

    def highlightBlock(self, text):

        self.select_n_color("<([\w|/|\s|=|\"|\.]+)>", (255, 0, 0), text)  # Balises
        self.select_n_color("\"(\w|\.)+\"", (40, 200, 40), text)  # Guillemets
        
    def est_balise_valide(self, balise):
        balise = balise.replace("/", "")
        balise = balise.split(" ")
        for e in balise:
            if e in self.balises:
                return True
        return False
