# Module relatif au traitement des couleurs

from PySide.QtGui import *
from PySide.QtCore import *
from lexer import *
from random import randint
from copy import deepcopy


class Proposition(QListWidget):
    def __init__(self, parent, font_size=16):
        super().__init__(parent)
        
        self.parent = parent
        self.font_size = font_size

        # self.setReadOnly(True)
        # self.setMaximumWidth(100)

        self.props = []
        self.props_files = []
        self.current_pos = []
        self.place = 0

        self.setStyleSheet("QListView{color:white;background-color: purple;font-size:%spx;}"%self.font_size)

    def addElement(self, elements):
        for element in elements:
            self.addItem(QListWidgetItem(element))

    def mouseDoubleClickEvent(self, event):
        idx = self.currentRow()
        self.complete(idx)

    def complete(self, idx=0):
        if idx in range(len(self.props)):
            prop = self.props[idx]

            h = deepcopy(self.current_pos[1])

            lines = self.parent.toPlainText().split("\n")

            line_splite = lines[h].replace("\t","").split(" ")

            l = self.current_pos[0] + len(prop) - len(line_splite[self.place])

            print(line_splite[:self.place])
            print(line_splite[self.place:])

            space = " " if len(line_splite) > 1 else ""

            if prop in self.props_files:
                nb_tab = self.get_nb_tab(lines[h])
                lines[h] ="\t" * nb_tab +  " ".join(line_splite[:self.place]) + space + prop + " " +" ".join(line_splite[self.place+1:])
            else:
                lines[h] = lines[h] + prop 
            self.parent.setPlainText("\n".join(lines))

            for i in range(h):
                self.parent.moveCursor(QTextCursor.Down)

            for i in range(l+1):
                self.parent.moveCursor(QTextCursor.Right)

    def get_nb_tab(self, text):
        res = 0
        for e in text:
            if e == "\t":
                res += 1
            else:
                return res
        return res


class CodeHighLighter(QSyntaxHighlighter):
    def __init__(self, editeur, parent=None):  # Parent --> QTextEdit
        super().__init__(parent)

        self.editeur = editeur

        self.prop = Proposition(self.editeur)

        self.props = ["int\nvoid\nbool\nchar", "(\n{", "+\n-\n*\n/"]

    def compare(self, word):

        res = []

        if word != "":
            for keyword in self.editeur.keywords:
                if word in keyword and not keyword in res and keyword != word: res += [keyword]
                
            for def_function in self.editeur.def_functions:
                if word in def_function[0] and not def_function[0] in res and def_function[0] != word: res += [def_function[0]]

        return res

    def highlightBlock(self, text):  # Appelée lorsqu'on change du texte dans le QTextEdit

        textCursor = self.editeur.textCursor()
        cursor_position = textCursor.columnNumber() - 1
        self.prop.current_pos = [cursor_position, textCursor.blockNumber()]

        self.prop.clear()
        self.prop.props = []
        self.prop.hide()
        
        idx = self.get_index(text, cursor_position)
        self.prop.place = idx


        word = text.split(" ")[idx].replace("\t","")
        possibilities = self.compare(word)

        if possibilities != [] and lexing(word) == "identifier":
            self.prop.props += possibilities
            self.prop.props_files += possibilities
            self.prop.addElement(possibilities)
            self.prop.show()

        if len(text) > 0 and cursor_position in range(len(text)) and text[cursor_position] == " ":
            # possibilities = self.props[randint(0, len(self.props) - 1)].split("\n")
            # self.prop.props += possibilities
            # self.prop.addElement(possibilities)
            # self.prop.show()
            pass # ajout des propositions de yacc

        x = self.editeur.cursorRect().x() + 10
        y = self.editeur.cursorRect().y()
        self.prop.move(x, y)
        self.editeur.setFocus()

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

    def test(self):
        if self.prop.props != []:
            self.prop.complete()

    def get_index(self, text, cursor_position):
        idx = 0
        for i in range(cursor_position):
            idx += text[i] == " "
        return idx
