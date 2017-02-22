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

        self.setMaximumHeight(1)

    def load(self):
        self.clear()

        idx = self.parent.get_idx()
        doc = self.parent.docs[idx]
        current_file = doc.chemin_enregistrement

        self.def_functions_infos = ""
        self.def_structs_infos = ""

        if current_file in self.parent.def_functions:
            self.def_functions_infos = self.parent.def_functions[current_file]

        if current_file in self.parent.def_structs:
            self.def_structs_infos = self.parent.def_structs[current_file]

        for def_functions in self.def_functions_infos:
            self.add("+ " + def_functions[0])

        for def_struct in self.def_structs_infos:
            self.add("- " + def_struct)

    def add(self, item):

         self.addItem(QListWidgetItem(item))

    def mouseDoubleClickEvent(self, e):
        """
        Lorsqu'on double-clique sur un élément, on l'affiche dans le code
        """
        selected = self.currentItem().text()[2:]
        find(self.parent, selected, False, True)

    def maj_style(self):
        colors = get_color_from_theme("treeview")
        self.setStyleSheet("QListWidget{background: " + get_rgb(colors["BACKGROUND"]) + ";}"
                           "QListWidget::item{color: " + get_rgb(colors["ITEMS"]) + ";}"
                           "QListWidget::item:hover{color: " + get_rgb(colors["ITEMSHOVER"]) + ";}")