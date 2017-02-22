import sys
from PySide.QtGui import *
from PySide.QtCore import *
import gui.style.style as style
sys.path[:0] = ["../"]
sys.path[:0] = ["gui"]


class Bouton(QPushButton):

    def __init__(self, nom, fonction, h=40):
        QPushButton.__init__(self, nom)

        self.setFixedHeight(h)
        self.clicked.connect(fonction)
        self.setStyleSheet(style.get("buttons"))

    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)
