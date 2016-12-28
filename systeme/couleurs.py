# Module relatif au traitement des couleurs

from PySide.QtGui import *
from PySide.QtCore import *
from lexer import *
from random import randint


class Proposition(QTextEdit):
    def __init__(self, parent=None):
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

    def compare(self, word):

        res = []
        
        if word != "":
            for def_function in self.editeur.def_functions:
                if ((def_function[0] in word and word.isalnum()) or word in def_function[0]) and not def_function[0] in res: res += [def_function[0]]
        return res

    def highlightBlock(self, text):  # Appelée lorsqu'on change du texte dans le QTextEdit

        word = text.split(" ")[-1]
        possibilities = self.compare(word)

        if possibilities != [] and lexing(word) == "identifier":

            self.prop.setPlainText("")
            self.prop.append("\n".join(possibilities))

            if len(text) > 0 and text[-1] == " ":
                self.prop.append(self.props[randint(0, len(self.props) - 1)])

            x = self.editeur.cursorRect().x() + 10
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

        yacc_erreurs = self.editeur.yacc_erreurs

        if yacc_erreurs != []:
            textFormat = QTextCharFormat()
            textFormat.setFontUnderline(True)
            textFormat.setUnderlineColor(QColor.fromRgb(255, 0, 0))

            if text[yacc_erreurs[0][1]: yacc_erreurs[0][1] + yacc_erreurs[0][2] + 1].strip() == "":
                self.setFormat(0, len(text), textFormat)
            else:
                self.setFormat(yacc_erreurs[0][1], yacc_erreurs[0][2], textFormat)
