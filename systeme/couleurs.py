# Module relatif au traitement des couleurs

from PySide.QtGui import *
from PySide.QtCore import *
from lexer import *
from random import randint

class Proposition(QTextEdit):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setMaximumWidth(100)

        self.setStyleSheet("QTextEdit{color:white;background-color: purple;}")

class CodeHighLighter(QSyntaxHighlighter):
    def __init__(self, editeur, parent=None):  # Parent --> QTextEdit
        super().__init__(parent)

        self.editeur = editeur

        self.prop = Proposition(self.editeur)

        self.props = ["int\nvoid\nbool\nchar", "(\n{\n", "+\n-\n*\n/"]

    def highlightBlock(self, text):  # Appelée lorsqu'on change du texte dans le QTextEdit

        if len(text) > 0 and text[-1] == " ":

            self.prop.setPlainText("")
            self.prop.append(self.props[randint(0, len(self.props) - 1)])

            x = self.editeur.cursorRect().x()
            y = self.editeur.cursorRect().y()
            self.prop.move(x, y)

            self.prop.show()
            self.editeur.setFocus()

        else:
            self.prop.hide()



        space_remember = []

        for i in range(len(text)):
            if text[i] == "\t" or text[i] == " ":
                space_remember += [i]

        colored = colorate(text)

        current_pos = 0

        for info in colored:

            while current_pos in space_remember:
                current_pos += 1

            word, color = info

            self.setFormat(current_pos, len(word), QColor.fromRgb(color[0], color[1], color[2]))
            current_pos += len(word)
