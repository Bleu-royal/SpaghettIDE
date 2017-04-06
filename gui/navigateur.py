import sys
import os
from PySide.QtGui import *
from PySide.QtCore import *
from systeme import workplace
from themes import themes
from language.language import get_text

import kernel.variables as var

sys.path[:0] = ["../"]
sys.path[:0] = ["gui"]


class TreeView(QTreeView):
    function_declarations = Signal(tuple)

    def __init__(self, fenetre):
        """
        Hérite de QTreeView.
        Permet d'afficher le navigateur de fichiers, permettant d'ouvrir et de visualiser les documents
        d'un ou de plusieurs projets.

        :param fenetre: Fenêtre où est placée le navigateur de fichier (ici : Parent)
        :type fenetre: Fenetre
        :rtype: None
        """

        super().__init__()
        # self.img1 = QPixmap("Dragon.jpg")  # Image de lancement
        # self.ouvrir.setIcon(QIcon(self.img1))  # Image sur le bouton
        # self.ouvrir.setIconSize(QSize(self.code.width()*1.5, self.code.height()*1.5))  # Taille de l'image

        self.fenetre = fenetre

        # self.setStyleSheet("background-color: rgb(50, 50, 50); color: white")

        self.model = QFileSystemModel()
        self.file = QFile()
        self.model.setRootPath(self.fenetre.workplace_path)
        self.setModel(self.model)

        for i in range(1, 4):
             self.hideColumn(i)
        #irmodel = QDirModel()
        #dirmodel.setHeaderData(1,Qt.Horizontal,"Folders");

        self.setHeaderHidden(True)

        self.setAnimated(True)  # Animations

        self.filters = []
        extentions = var.extension_by_language[self.fenetre.project_type] + var.ext_neutres
        for ext in extentions:
            self.filters.append(ext)

        self.model.setNameFilters(self.filters)
        # self.model.setNameFilterDisables(False)
        # self.model.setFilter(QDir.Filter)
        self.model.setReadOnly(False)
        self.setRootIndex(self.model.index(self.fenetre.workplace_path))

        self.maj_style()  # Load theme using stylesheets

        self.cacher_pas_projet()

        self.function_declarations.connect(self.load_project)

    def change_worplace(self, workplace_path):
        self.model.setRootPath(workplace_path)
        self.setRootIndex(self.model.index(workplace_path))

    def maj_style(self):
        colors = themes.get_color_from_theme("treeview")
        self.setStyleSheet("QTreeView{background: " + themes.get_rgb(colors["BACKGROUND"]) +
                           ";}""QTreeView::item{color: " + themes.get_rgb(colors["ITEMS"]) +
                           ";}""QTreeView::item:hover{color: " + themes.get_rgb(colors["ITEMSHOVER"]) + ";}")

    def cacher_pas_projet(self):
        pass

    def mouseDoubleClickEvent(self, event):
        """ Lorsque l'on double-clique sur le navigateur, on ouvre soit un projet, soit un document dans un projet.
        :param event: Contient les positions x et y de l'endroit où on a cliqué. NON UTILISÉ ICI.
        :rtype: None
        """
        workplace.open_project(self)

    def keyPressEvent(self, event):
        """
        Bind de la touche entrée.
        Lorsque l'on sélectionne un document et que l'on appuie sur entrée, on ouvre le document
        ou le projet sélectionné.

        Contient les positions x et y de l'endroit où on a cliqué. NON UTILISÉ ICI.
        :rtype: None
        """
        if event.key() == 16777220:  # Référence de la touche "entrée"
            workplace.open_project(self)
        else:
            QTreeView.keyPressEvent(self, event)

    def load_project(self, declarators):
        """
        Calls open_project() in workplace module using a thread.

        :return:
        """
        if declarators != (None, None, None):
            self.fenetre.def_functions, self.fenetre.def_structs, self.fenetre.def_vars = declarators
            self.fenetre.status_message(get_text("project_opened"))
            self.fenetre.hide_progress_bar()

    def open(self):
        """
        Ouvre un document si son extension est valide.
        Appelle la fonction parent pour ouvrir un fichier.

        :rtype: None
        """
        path = self.model.filePath(self.currentIndex())
        name = self.model.fileName(self.currentIndex())
        ext = name.split(".")[-1]

        if ext in [i[1:] for i in var.extension_by_language[self.fenetre.project_type]] + [i[1:] for i in var.txt_extentions]:
            self.fenetre.open(path)
        elif ext in [i[1:] for i in var.imgs_extentions]:
            self.fenetre.open_img(path)
        elif ext in [i[1:] for i in var.gif_extentions]:
            self.fenetre.open_gif(path)
        else:
            QMessageBox.critical(self.fenetre, get_text("opening_fail"), get_text("opening_fail_text"))
