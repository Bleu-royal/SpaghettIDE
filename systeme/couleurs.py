# Module relatif au traitement des couleurs

from PySide.QtGui import *
from PySide.QtCore import *
from lexer import *
from random import randint
from copy import deepcopy
import json

import os

import lexerAR as AR


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

        self.first_launch = True

        self.cache_name = ""

    def compare(self, word):

        self.def_functions = []

        for e in self.editeur.def_functions:
            for e2 in self.editeur.def_functions[e]:
                self.def_functions += [e2]

        res = []

        if word != "":
            for keyword in self.editeur.keywords:
                if word in keyword and not keyword in res and keyword != word: res += [keyword]
            
            for def_function in self.def_functions:
                if word in def_function[0] and not def_function[0] in res and def_function[0] != word: res += [def_function[0]]

        return res

    def highlightBlock(self, text):  # Appelée lorsqu'on change du texte dans le QTextEdit

        self.prop.clear()
        self.prop.props = []
        self.prop.hide()

        if not self.first_launch and text != "":

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

            if len(text) == 0:
                last_char = " "
            else:
                last_char = text[-1]

            if last_char in [str(i) for i in range(10)] or last_char in "/+*-":
                poss = AR.parse(text)
                self.prop.props += poss
                self.prop.addElement(poss)
                self.prop.show()

            x = self.editeur.cursorRect().x() + 10
            y = self.editeur.cursorRect().y()
            self.prop.move(x, y)
            self.editeur.setFocus()

            space_remember = []

            for i in range(len(text)):
                if text[i] == "\t" or text[i] == " ":
                    space_remember += [i]

            # get_from_cache = False

            colored_cache = {}

            if self.cache_name != "":
                if os.path.isfile("cache/%s.json"%self.cache_name): 
                    cache = open("cache/%s.json"%self.cache_name, "r")
                    colored_cache = json.loads(cache.read())
                    cache.close()
                else:
                    cache = open("cache/%s.json"%self.cache_name, "w")
                    cache.write("{}")
                    cache.close()
                    colored_cache = {}

            if text in colored_cache:
                colored = colored_cache[text]
            else:
                print("coloration par Lex")
                colored = colorate(text)
                if self.cache_name != "":
                    cache = open("cache/%s.json"%self.cache_name, "r")
                    tmp = json.loads(cache.read())
                    cache.close()

                    cache = open("cache/%s.json"%self.cache_name, "w")
                    tmp.update({text:colored})
                    cache.write(json.dumps(tmp))
                    cache.close()

            current_pos = 0

            for info in colored:

                while current_pos in space_remember:
                    current_pos += 1

                word, color = info

                self.setFormat(current_pos, len(word), QColor.fromRgb(color[0], color[1], color[2]))
                current_pos += len(word)

            yacc_errors = self.editeur.yacc_errors

            lines = self.editeur.toPlainText().split("\n")

            current_line = 0
            for i,line in enumerate(lines):
                if line == text:
                    current_line = i

            if yacc_errors != []:
                line = yacc_errors[0][0]
                char = yacc_errors[0][1]
                value = yacc_errors[0][2]
                if value in text and current_line == line - 1:
                    textFormat = QTextCharFormat()
                    textFormat.setFontUnderline(True)
                    textFormat.setUnderlineColor(QColor.fromRgb(255, 0, 0))

                    text_split = self.editeur.toPlainText().split("\n")

                    self.setFormat(0, len(text_split[line-1]), textFormat)

            self.editeur.show_nb_prop(len(self.prop.props))  # Disp the number of propsitions

        else:
            self.editeur.parent.defaut_info_message()

    def test(self):
        if self.prop.props != []:
            self.prop.complete()

def create_cache_folder():
    if not os.path.exists("cache"):
        os.makedirs("cache")

create_cache_folder()
