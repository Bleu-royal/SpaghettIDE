# Module relatif à l'inspecteur

import sys
import os
from PySide.QtGui import *
from PySide.QtCore import *

from themes.themes import *
from systeme.document import find

sys.path[:0] = ["../"]
sys.path[:0] = ["gui"]


class Inspecteur(QListWidget):

    def __init__(self, parent):

        super().__init__()

        self.parent = parent

        self.setStyleSheet("QListView{background: " + get_rgb(get_color_from_theme("treeview")["BACKGROUND"]) + ";"
                            "color: " + get_rgb(get_color_from_theme("treeview")["ITEMS"]) + "}")
        self.setMaximumHeight(1)

    def load(self):
        self.clear()

        idx = self.parent.get_idx()
        doc = self.parent.docs[idx]
        current_file = doc.chemin_enregistrement

        self.def_functions_infos = ""

        if current_file in self.parent.def_functions:
            self.def_functions_infos = self.parent.def_functions[current_file]

        for def_functions in self.def_functions_infos:
            self.add(def_functions[0])

    def add(self, item):

         self.addItem(QListWidgetItem(item))

    def mouseDoubleClickEvent(self, e):
        """
        Lorsqu'on double-clique sur un élément, on l'affiche dans le code
        """
        selected = self.currentItem().text()
        find(self.parent, selected, False, True)