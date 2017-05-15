# Module relatif à l'inspecteur

import sys
import os
from PySide.QtGui import *
from PySide.QtCore import *

from themes import themes
from systeme.document import find
import kernel.variables as var

sys.path[:0] = ["../"]
sys.path[:0] = ["gui"]


class Inspecteur(QListWidget):

    def __init__(self, parent):

        super().__init__()

        self.parent = parent

        self.setMaximumHeight(1)

    def load(self):
        self.clear()

        if self.parent.project_type in [x[1:] for x in var.extension_by_language[""]]:

            class_name = {"py" : "Classes", "c": "Structs", "h" : "Structs"}

            idx = self.parent.get_idx()
            doc = self.parent.docs[idx]
            ext = doc.extension
            current_file = doc.chemin_enregistrement

            self.def_functions_infos = ""
            self.def_structs_infos = ""
            self.def_vars_infos = ""

            if current_file in self.parent.def_functions:
                self.def_functions_infos = self.parent.def_functions[current_file]

            if current_file in self.parent.def_structs:
                self.def_structs_infos = self.parent.def_structs[current_file]

            if current_file in self.parent.def_vars:
                self.def_vars_infos = self.parent.def_vars[current_file]

            if self.def_functions_infos != []:
                self.add("Fonctions : ")

            for def_functions in self.def_functions_infos:
                if isinstance(def_functions, list):
                    self.add("    - %s" % def_functions[0])
                else:
                    self.add("    - %s" % def_functions)

            if self.def_structs_infos != []:
                self.add("%s : " % class_name[ext])

            for def_struct in self.def_structs_infos:
                self.add("    - %s" % def_struct)

            if self.def_vars_infos != []:
                self.add("Variables : ")

            for def_var in self.def_vars_infos:
                self.add("    - %s" % def_var)

    def add(self, item):

        self.addItem(QListWidgetItem(item))

    def mouseDoubleClickEvent(self, e):
        """
        Lorsqu'on double-clique sur un élément, on l'affiche dans le code
        """
        selected = self.currentItem().text()[6:]
        find(self.parent, selected, False, True)

    def maj_style(self):
        colors = themes.get_color_from_theme("treeview")
        self.setStyleSheet("QListWidget{background: " + themes.get_rgb(colors["BACKGROUND"]) + ";}"
                           "QListWidget::item{color: " + themes.get_rgb(colors["ITEMS"]) + ";}"
                           "QListWidget::item:hover{color: " + themes.get_rgb(colors["ITEMSHOVER"]) + ";}")
