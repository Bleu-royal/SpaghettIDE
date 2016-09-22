# Module relatif au traitement des couleurs

from PySide.QtGui import *
from PySide.QtCore import *


class HTMLHighLighter(QSyntaxHighlighter):
    def __init__(self, parent=None):  # Parent --> QTextEdit
        super().__init__(parent)  # Appelle le __init__ de la classe parent
        self.balises = ('HTML', 'META', 'LINK', 'FORM', 'A', 'INPUT', 'STYLE', 'SCRIPT', 'BODY', 'HEAD', 'NAV', 'TITLE', 'BR', 'DIV', 'SPAN', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'IMG', 'P', 'UL', 'LI', 'BUTTON', "LABEL", "ASIDE", "SECTION", "NAV", "HEADER", "FOOTER", "ARTICLE", "EM")
        self.attributs = ('SRC', 'HREF', 'CLASS', 'ID', 'CHARSET', 'REL', 'TITLE', 'TYPE', 'NAME', 'VALUE', "LANG", "INTEGRITY", "CROSSORIGIN", "DATA-TOGGLE", "DATA-TARGET", "ARIA-EXPANDED", "ARIA-CONTROLS", "FOR","CONTENT")

    def select_n_color(self, exp_reguliere, color, text, word=False):
        text = text.upper()
        rgx = QRegExp(exp_reguliere)  # Reconnaitre les expressions à colorier
        pos = rgx.indexIn(text, 0)  # Position de la première expression régulière rencontrée

        while pos != -1:  # Tant qu'on est pas au bout de la ligne (text)
            if word:
                start = self.place_in_block(text, word, pos)
                self.setFormat(start, len(word), QColor.fromRgb(color[0], color[1], color[2]))  # Modificateur du texte sélectionné
            else:
                self.setFormat(pos, rgx.matchedLength(), QColor.fromRgb(color[0], color[1], color[2]))  # Modificateur du texte sélectionné
            pos += rgx.matchedLength()  # Déplacer à la fin de l'exp regulière
            pos = rgx.indexIn(text, pos)  # expr suivante

    def place_in_block(self, bloc, word, pos):

        for i in range(pos, len(bloc)):
            if bloc[i:i+len(word)] == word:
                return i
        return False

    def highlightBlock(self, text):  # Appelée lorsqu'on change du texte dans le QTextEdit
        for e in self.attributs:
            self.select_n_color("<(.)*(\s)+%s(\s|=)+(.)*>" % e, (166, 226, 46), text, e)  # Balises & attributs

        self.select_n_color("\"(\w|\.|\s|\+|/|-|,|#|\d|:|=)+\"", (230, 219, 116), text)  # Guillemets

        for e in self.balises:
            self.select_n_color("<(/)*%s(\s|>|/>)+(\w|\s|:|;|=|\"|\d|\.|/|\+|-|,|#)*(/)*(>)*"%e, (238, 38, 114), text, e)  # Balises

        self.select_n_color("<!--(\w|\s|:|;|=|\"|\d|\.|/|\+|-|,|#)*-->", (117, 113, 94), text)  # Commentaires HTML

        #self.select_n_color("/\*(\w|\s|:|;|=|\"|\d|\.|/|\+|-|,|#)*\*/",(117,113,94),text) # Commentaires CSS
