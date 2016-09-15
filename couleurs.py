# Module relatif au traitement des couleurs
from PySide.QtGui import *
from PySide.QtCore import *

class HTMLHighLighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

    def highlightBlock(self, text):
        rgx = QRegExp("<([\w|/|\s|=|\"|\.]+)>")
        pos = rgx.indexIn(text, 0)

        while pos != -1:
            self.setFormat(pos, rgx.matchedLength(), QColor.fromRgb(255, 0, 0))
            pos += rgx.matchedLength()
            pos = rgx.indexIn(text, pos)

        rgx = QRegExp("\"(\w|\.)+\"")
        pos = rgx.indexIn(text, 0)

        while pos != -1:
            self.setFormat(pos, rgx.matchedLength(), QColor.fromRgb(0, 255, 0))
            pos += rgx.matchedLength()
            pos = rgx.indexIn(text, pos)

        rgx = QRegExp(">(\w|\.|\s)+<")
        pos = rgx.indexIn(text, 0)

        while pos != -1:
            self.setFormat(pos + 1, rgx.matchedLength() - 2, QColor.fromRgb(0, 0, 255))
            pos += rgx.matchedLength()
            pos = rgx.indexIn(text, pos)