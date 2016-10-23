# Module relatif au traitement des couleurs

from PySide.QtGui import *
from PySide.QtCore import *
from lexer import *


class CodeHighLighter(QSyntaxHighlighter):
    def __init__(self, parent=None):  # Parent --> QTextEdit
        super().__init__(parent)

    def highlightBlock(self, text):  # Appelée lorsqu'on change du texte dans le QTextEdit

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
