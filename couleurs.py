# Module relatif au traitement des couleurs

from PySide.QtGui import *
from PySide.QtCore import *

class HTMLHighLighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)  # Appelle le __init__ de la classe parent

    def highlightBlock(self, text):
        rgx = QRegExp("<([\w|/|\s|=|\"|\.]+)>")  # Reconnaitre les balises
        pos = rgx.indexIn(text, 0)  # Position de la première balise rencontrée

        while pos != -1:
            self.setFormat(pos, rgx.matchedLength(), QColor.fromRgb(255, 0, 0))  # Modificateur du texte sélectionné
            pos += rgx.matchedLength()  # Déplacer à la fin de la balise
            pos = rgx.indexIn(text, pos)  # Balise suivante

        rgx = QRegExp("\"(\w|\.)+\"")  # Reconnaitre les guillemets
        pos = rgx.indexIn(text, 0)

        while pos != -1:
            self.setFormat(pos, rgx.matchedLength(), QColor.fromRgb(0, 255, 0))
            pos += rgx.matchedLength()
            pos = rgx.indexIn(text, pos)

        rgx = QRegExp(">(\w|\.|\s)+<")  # Reconnaitre ce qu'il y a entre les balises.
        pos = rgx.indexIn(text, 0)

        while pos != -1:
            self.setFormat(pos + 1, rgx.matchedLength() - 2, QColor.fromRgb(0, 0, 255))
            pos += rgx.matchedLength()
            pos = rgx.indexIn(text, pos)
