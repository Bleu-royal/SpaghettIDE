import sys
from PySide.QtGui import *
from PySide.QtCore import *
import gui.style.style as style
sys.path[:0] = ["../"]
sys.path[:0] = ["gui"]


class Bouton(QPushButton):

    def __init__(self, nom, fonction):
        QPushButton.__init__(self, nom)

        self.setFixedHeight(40)
        self.clicked.connect(fonction)
        self.setStyleSheet(style.get("buttons"))

    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)
