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


class StatusBar(QStatusBar):
    def __init__(self, width=None):
        QStatusBar.__init__(self)
        if width is not None:
            self.setFixedWidth(width)

        self.setFixedHeight(30)
        self.setSizeGripEnabled(False)

        self.maj_style()

    def maj_style(self):
        status_color = get_color_from_theme("statusbar")
        self.setStyleSheet("QStatusBar {background: " + get_rgb(status_color["BACKGROUND"]) + ";""color: " +
                           get_rgb(status_color["TEXT"]) + ";}")
