# Module relatif à l'inspecteur

import sys
import os
from PySide.QtGui import *
from PySide.QtCore import *

from themes.themes import *

sys.path[:0] = ["../"]
sys.path[:0] = ["gui"]


class Inspecteur(QTextEdit):

    def __init__(self, parent):

        super().__init__()

        self.parent = parent

        self.setStyleSheet("QObject::pane{background: " +
                           get_rgb(get_color_from_theme("treeview")["BACKGROUND"]) + "}")
        self.setTextColor(QColor(255, 255, 255))
        self.setReadOnly(True)
        self.setMaximumHeight(1)

    def load(self):

        idx = self.parent.get_idx()

        doc = self.parent.docs[idx]

        current_file = doc.chemin_enregistrement

        print(current_file)

        if current_file in self.parent.def_functions:
            self.def_functions_infos = self.parent.def_functions[current_file]

        self.def_functions = []
        for def_functions in self.def_functions_infos:
            self.def_functions += ["   - " +  def_functions[0]]

        self.setPlainText("Fonction du fichier %s : \n"%doc.nom)
        text = self.toPlainText()

        self.setPlainText(text + "\n".join(self.def_functions))

        print('loading')
