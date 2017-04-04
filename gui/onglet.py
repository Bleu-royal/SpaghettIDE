import sys
import os
from PySide.QtGui import *
from PySide.QtCore import *
from themes import themes

from language.language import get_text

sys.path[:0] = ["../"]
sys.path[:0] = ["gui"]


class TabWidget(QTabWidget):
    def __init__(self, parent):
        """
        Hérite de QTabWidget.
        Permet de faire plusieurs onglets de code ( utilisation de la classe Editeur ).
        On définit ici les raccourcis de navigation entre et pour les onglets
        pour fermer, ouvrir, aller au suivant...

        :param parent: Parent de la classe ( qui appelle )
        :type parent: Fenetre
        :rtype: None
        """
        super().__init__()

        self.parent = parent

        # shortcut_close = QShortcut(QKeySequence.Close, self)
        # shortcut_close.activated.connect(self.close_current_tab)

        # shortcut_open = QShortcut(QKeySequence.Open, self)
        # shortcut_open.activated.connect(self.parent.open)

        # shortcut_new = QShortcut(QKeySequence.New, self)
        # shortcut_new.activated.connect(self.parent.new)

        # shortcut_save = QShortcut(QKeySequence.Save, self)
        # shortcut_save.activated.connect(self.parent.save)

        shortcut_next_tab = QShortcut(QKeySequence('Alt+tab'), self)
        shortcut_next_tab.activated.connect(self.next_tab)

        shortcut_prev_tab = QShortcut(QKeySequence('Alt+Shift+tab'), self)
        shortcut_prev_tab.activated.connect(self.prev_tab)

        self.maj_style()
        # self.setMovable(True)
        # self.setTabsClosable(True)  # Signal : tabCloseRequested
        self.setUsesScrollButtons(True)  # Si il y a trop d'onglets

    def maj_style(self):
        """
        Met à jour le style du TabWidget
        """
        c = themes.get_color_from_theme("textedit")
        self.setStyleSheet("QTabWidget::pane{background-image: url(content/medium.gif);"
                           "background-repeat: no-repeat;background-position: center}"
                           "QTabWidget::tab-bar{left:0;}QTabBar::tab{color: " + themes.get_rgb(c["tab-color"]) +
                           ";""background-color:" + themes.get_rgb(c["tab-back-color"]) +
                           ";""border-bottom: 2px solid transparent;padding:7px 15px;"
                           "margin-top:0px;border-top-left-radius:10px;border-top-right-radius:10px;}"
                           "QTabBar::tab:selected,""QTabBar::tab:hover{background-color:" +
                           themes.get_rgb(c["tab-hover-back-color"]) + ";""color: " + themes.get_rgb(c["tab-hover-color"]) +
                           ";""border-bottom:" + themes.get_rgb(c["tab-hover-bord-bot-color"]) +
                           ";}""QTabBar::tab{margin-top: 2px;}")

    def close_current_tab(self):
        """
        Fonction pour fermer l'onglet courant.

        :rtype: None
        """
        if len(self.parent.codes) != 0:  # On vérifie que la liste d'onglet n'est pas vide.

            if self.parent.get_current_widget_used() in ("Inspecteur", "Inspector"):
                self.parent.change_affichage()  # On remplace l'Inspecteur par le navigateur si il était actif

            idx = self.currentIndex()

            self.removeTab(idx)

            doc = self.parent.docs[idx]
            code = self.parent.codes[idx]
            highlighter = self.parent.highlighters[idx]

            self.parent.docs.remove(doc)
            self.parent.codes.remove(code)
            self.parent.highlighters.remove(highlighter)

            self.parent.status_message(get_text("status_fic_closed"))
            self.parent.defaut_info_message()

    def next_tab(self):
        """
        Afficher l'onglet suivant, relativement à la position courante.
        Si on est au dernier, on retourne au premier.

        :rtype: None
        """
        idx = self.currentIndex() + 1 if self.currentIndex() < self.count() - 1 else 0
        self.setCurrentIndex(idx)

    def prev_tab(self):
        """
        Afficher l'onglet précédent, relativement à la position courante.
        Si on est au premier, on affiche le dernier.

        :rtype: None
        """
        idx = self.currentIndex() - 1 if self.currentIndex() >= 1 else self.count() - 1
        self.setCurrentIndex(idx)

    def mousePressEvent(self, event):
        """
        On crée un nouvel onglet de code lorsqu'on double-clique sur la page vide (si on n'a pas d'onglet déjà ouvert)
        et si on projet est ouvert.

        :param event: Contient les positions x et y de l'endroit où on a cliqué. NON UTILISÉ ICI.
        :rtype: None
        """
        if len(self.parent.docs) == 0:
            if self.parent.project_path != "":
                self.parent.new()
            else:
                self.parent.status_message(get_text("text_please_open_project"))

    def enterEvent(self, e):
        """
        Evenement lors ce qu'on survole les onglets ou le widget lorsqu'il est vide.
        Ici on change le curseur
        """
        self.setCursor(Qt.PointingHandCursor)
