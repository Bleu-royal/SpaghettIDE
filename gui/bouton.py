import sys
import os
from PySide.QtGui import *
from PySide.QtCore import *

from lexer import *
from themes.themes import *
import gui.style.style as style
from language.language import *

from systeme.workplace import *
# Importation du module relatif à la coloration lexicale et de la gestion des documents
from systeme.couleurs import *
from systeme.document import *
from systeme.parallele import *

# Importation des modules du menu, des onglets, du navigateur de fichiers et de l'éditeur
from gui.menu import *
from gui.navigateur import *
from gui.onglet import *
from gui.editeur import *

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
