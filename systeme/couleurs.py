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

        self.maj_style()

    def maj_style(self):
        self.setStyleSheet("QListView{"
                           "color:white;"
                           "background-color: grey;"
                           "font-size:%spx;"
                           "}"
                           "QListView::item:hover{"
                           "color:grey;"
                           "background-color:white;"
                           "}"
                           %self.font_size)

    def addElement(self, elements):
        for element in elements:
            self.addItem(QListWidgetItem(element))

    def mouseDoubleClickEvent(self, event):
        idx = self.currentRow()
        self.complete(idx)

    def complete(self, idx=0):
        prop = self.props[idx]
        
        textCursor = self.parent.textCursor()

        if prop in self.props_files:
            textCursor.select(QTextCursor.WordUnderCursor)
            textCursor.removeSelectedText()

        textCursor.insertText(prop)


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

        self.prop.clear()
        self.prop.props = []
        self.prop.hide()

        textCursor = self.editeur.textCursor()
        textCursor.select(QTextCursor.WordUnderCursor)
        word = textCursor.selectedText()

        cursor_position = textCursor.columnNumber() - 1

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


        yacc_errors = self.editeur.yacc_errors

        if yacc_errors != []:
            textFormat = QTextCharFormat()
            textFormat.setFontUnderline(True)
            textFormat.setUnderlineColor(QColor.fromRgb(255, 0, 0))

            text_split = self.editeur.toPlainText().split("\n")
            line = yacc_errors[0][0]
            char = yacc_errors[0][1]
            end = yacc_errors[0][1]


            start = 0
            for i in range(line):
                start += len(text_split[i])
                start += 1

            start -= 1

            if line in range(len(text_split)) and text in text_split[line] and text != "":
                self.setFormat(char-start, end, textFormat)

        self.editeur.show_nb_prop(len(self.prop.props))  # Disp the number of propsitions

    def test(self):
        if self.prop.props != []:
            self.prop.complete()
