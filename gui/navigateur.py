import sys
import os
from PySide.QtGui import *
from PySide.QtCore import *
from systeme.workplace import *
from themes.themes import *

sys.path[:0] = ["../"]
sys.path[:0] = ["gui"]


class TreeView(QTreeView):
    function_declarations = Signal(list)

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

        self.setAnimated(True)  # Animations

        self.filters = []
        extentions = ("*c", "*h")
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

    def maj_style(self):
        colors = get_color_from_theme("treeview")
        self.setStyleSheet("QTreeView{background: " + get_rgb(colors["BACKGROUND"]) +
                           ";}""QTreeView::item{color: " + get_rgb(colors["ITEMS"]) +
                           ";}""QTreeView::item:hover{color: " + get_rgb(colors["ITEMSHOVER"]) + ";}")

    def cacher_pas_projet(self):

        pass

    def mouseDoubleClickEvent(self, event):
        """ Lorsque l'on double-clique sur le navigateur, on ouvre soit un projet, soit un document dans un projet.
        :param event: Contient les positions x et y de l'endroit où on a cliqué. NON UTILISÉ ICI.
        :rtype: None
        """
        open_project(self)

    def keyPressEvent(self, event):
        """
        Bind de la touche entrée.
        Lorsque l'on sélectionne un document et que l'on appuie sur entrée, on ouvre le document
        ou le projet sélectionné.

        Contient les positions x et y de l'endroit où on a cliqué. NON UTILISÉ ICI.
        :rtype: None
        """
        if event.key() == 16777220:  # Référence de la touche "entrée"
            open_project(self)
        else:
            QTreeView.keyPressEvent(self, event)

    def load_project(self, func_decla):
        """
        Calls open_project() in workplace module using a thread.

        :return:
        """
        if func_decla != None:
            self.fenetre.def_functions = func_decla
            self.fenetre.status_message("Le projet sélectionné a bien été ouvert")

    def open(self):
        """
        Ouvre un document si son extension est valide.
        Appelle la fonction parent pour ouvrir un fichier.

        :rtype: None
        """
        path = self.model.filePath(self.currentIndex())
        name = self.model.fileName(self.currentIndex())
        ext = name.split(".")[-1]
        if ext in ("c", "h"):
            self.fenetre.open(path)
        else:
            QMessageBox.critical(self.fenetre, "Erreur d'ouverture", "L'extention sélectionnée n'est pas lisible par "
                                                                     "notre IDE.\n\n"
                                                                     "Pour le moment...")
