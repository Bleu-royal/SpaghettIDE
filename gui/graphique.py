# Module relatif à l'interface graphique

import sys,os
from datetime import datetime

from PySide.QtGui import *
from PySide.QtCore import *

sys.path[:0] = ["../"]
from systeme.couleurs import *
from systeme.document import *
from systeme.fichiers import * 
from systeme.projets import *
from lexer import *

sys.path[:0] = ["gui"]

class Editeur(QTextEdit):

    def __init__(self, police, couleur_fond, couleur_text, taille_text):
        """
        Hérite de QTextEdit.
        C'est une zone de texte dans laquelle on peut écrire. C'est ce qu'on utilise ici pour la zone où le code est écrit.

        Ici, on modifie ses paramètres en fonction du thème souhaité.
        :param police: Police d'écriture
        :type police: str
        :param couleur_fond: Couleur d'arrière plan de l'éditeur (background)
        :type couleur_fond: str
        :param couleur_text: Couleur du texte de base
        :type couleur_text: str
        :param taille_text: Taille de la police (en points)
        :type taille_text: int
        :rtype: None
        """
        QTextEdit.__init__(self)

        self.setStyleSheet("QTextEdit { background-color:" + couleur_fond + ";"
                           + "font-family:" + police + ";"
                           + "color:" + couleur_text + ";"
                           + "font-size:" + str(taille_text) + "pt; }")

        self.append("int main ( int argc, char** argv ){\n\n\treturn 0;\n\n}")


class TabWidget(QTabWidget):

    def __init__(self, parent):
        """
        Hérite de QTabWidget.
        Permet de faire plusieurs onglets de code ( On utilise notre class Editeur ).
        On définit ici les raccourcis de navigation entre et pour les onglets de code pour fermer, ouvrir, aller au suivant...

        :param parent: Parent de la class ( qui appelle )
        :type parent: object
        :rtype: None
        """
        super().__init__()

        self.parent = parent

        shortcut_close = QShortcut(QKeySequence.Close, self)
        shortcut_close.activated.connect(close_current_tab)

        shortcut_open = QShortcut(QKeySequence.Open, self)
        shortcut_open.activated.connect(open_file)

        shortcut_new = QShortcut(QKeySequence.New, self)
        shortcut_new.activated.connect(new)

        shortcut_save = QShortcut(QKeySequence.Save, self)
        shortcut_save.activated.connect(save)

        shortcut_next_tab = QShortcut(QKeySequence('Alt+tab'), self)
        shortcut_next_tab.activated.connect(self.next_tab)

        shortcut_prev_tab = QShortcut(QKeySequence('Alt+Shift+tab'), self)
        shortcut_prev_tab.activated.connect(self.prev_tab)

        url = QDir().currentPath() + "/images/medium.jpg"
        self.setStyleSheet("QTabWidget::pane{background-image: url(:/images/medium.jpg);"
                           "background-repeat: no-repeat;background-position: center}"
                           "QTabWidget::tab-bar{left:0;}QTabBar::tab{color:black;"
                           "background-color:gray;border-bottom: 2px solid transparent;padding:7px 15px;"
                           "margin-top:0px;border-top-left-radius:10px;border-top-right-radius:10px;}"
                           "QTabBar::tab:selected,"
                           "QTabBar::tab:hover{background-color:#2E2E2E; color: white;border-bottom:#2E2E2E;}"
                           "QTabBar::tab:!selected {margin-top: 5px;}")

    
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


class MyAction(QAction):
    def __init__(self, papa, name, status, func, shortcut_command=None):
        """
        Hérite de QAction.
        Créée ce qui est nécessaire pour faire un nouvel onglet dans la barre de menu, avec le nom, un raccourcis, une fonction à exécuter.

        :param papa:  Class qui appelle MyAction (ici Fenetre)
        :type papa: object
        :param name:  Nom à donner à l'action
        :type name: str
        :param status:  Truc
        :type status: str
        :param shortcut_command:  Commande de raccourcis (facultative)
        :type shortcut_command: str
        :param func:  Fonction à exécuter
        :rtype: None
        """

        QAction.__init__(self, name, papa)  # Initialisation de l'action
        self.setMenuRole(QAction.NoRole)  # Pour que ca fonctionne sur toutes les plateformes
        self.setStatusTip(status)
        self.setShortcut(shortcut_command)
        self.triggered.connect(func)


class TreeView(QTreeView):
    def __init__(self, fenetre):
        """
        Hérite de QTreeView.
        Permet d'afficher le navigateur de fichiers, permettant d'ouvrir et de visualiser les documents d'un ou de plusieurs projets.

        :param fenetre: Fenêtre où est placée le navigateur de fichier (ici : Parent)
        :type fenetre: object
        :rtype: None
        """

        super().__init__()
        # self.img1 = QPixmap("Dragon.jpg")  # Image de lancement
        # self.ouvrir.setIcon(QIcon(self.img1))  # Image sur le bouton
        # self.ouvrir.setIconSize(QSize(self.code.width()*1.5, self.code.height()*1.5))  # Taille de l'image

        self.fenetre = fenetre

        self.model = QFileSystemModel()
        self.file = QFile()
        self.model.setRootPath(self.fenetre.workplace_path)
        self.setModel(self.model)
        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)
        self.setAnimated(True)
        self.filters = []
        self.filters.append("*c")
        self.filters.append("*h")
        self.model.setNameFilters(self.filters)
        # self.model.setNameFilterDisables(False)
        # self.model.setFilter(QDir.Filter)
        self.model.setReadOnly(False)
        self.setRootIndex(self.model.index(self.fenetre.workplace_path))

        self.cacher_pas_projet()

    def cacher_pas_projet(self):

        pass


class MenuBar(QMenuBar):

    def __init__(self, parent):
        """
        Hérite de QMenuBar.
        C'est ici que la barre de menu est créée.
        On appelle la class MyAction pour chaque élément du menu que l'on souhaite créer, puis on ajoute ces éléments au menu principal.

        :param parent: Parent de la class ( qui appelle )
        :type parent: object
        :rtype: None
        """
        super().__init__(parent)

        ## Menus

        # Nouveau Projet
        new_project_action = MyAction(parent, "&Nouveau Projet", "Nouveau projet", new_project, "Ctrl+M")
        # Ouvrir un projet déjà existant
        open_project_action = MyAction(parent, "&Ouvrir Projet", "Ouvrir un projet", open_project, "Ctrl+L")
        # Fermer le projet
        exit_project_action = MyAction(parent, "&Fermer Projet", "Fermer le projet", close_project, "Ctrl+K")

        # Nouveau Fichier
        new_fic_action = MyAction(parent, "&Nouveau", "Nouveau fichier", new, "Ctrl+N")
        # Ouvrir un fichier déjà existant
        open_fic_action = MyAction(parent, "&Ouvrir", "Ouvrir un fichier", open_file, "Ctrl+O")
        # Sauvegarder le fichier courant
        sauv_fic_action = MyAction(parent, "&Sauvegarder", "Sauvegarder le fichier courant", save, "Ctrl+S")

        #À Propos de Cthulhu
        apropos_ide_action = MyAction(parent, "&À Propos", "À propos de Cthulhu", parent.a_propos)
        # Fermer l'IDE
        exit_ide_action = MyAction(parent, "&Quitter", "Quitter l'application", parent.quit_func, "Esc")

        # Menu Fichier et ses sous-menus
        fichier_menu = self.addMenu("&Fichier")
        fichier_menu.addAction(new_fic_action)
        fichier_menu.addAction(open_fic_action)
        fichier_menu.addAction(sauv_fic_action)
        # Menu Projet et ses sous-menus
        projet_menu = self.addMenu("&Projet")
        projet_menu.addAction(new_project_action)
        projet_menu.addAction(open_project_action)
        projet_menu.addAction(exit_project_action)
        # Menu Cthulhu
        cthulhu_menu = self.addMenu("&Cthulhu")
        cthulhu_menu.addAction(apropos_ide_action)
        cthulhu_menu.addAction(exit_ide_action)
        


class Fenetre(QWidget):
    def __init__(self, titre, workplace_path=QDir.homePath() + "/workplace/"):
        """
        Hérite de QWidget
        Class principale, dans laquelle tout est rassemblé. On appelle tout ce qui est nécessaire à la création de la fenêtre et au fonctionnement du programme.

        :param titre: Nom de la fenêtre
        :type titre: str
        :param workplace_path: Chemin absolu vers l'emplacement où sont placés les projets créés.
        :rtype: None
        """
        super().__init__()

        self.ecran = QDesktopWidget()
        self.setWindowTitle(titre)
        self.setGeometry(50, 50, self.ecran.screenGeometry().width() - 100, self.ecran.screenGeometry().height() - 100)
        # Taille de la fenêtre

        self.workplace_path = workplace_path

        self.project_path = ""

        self.gridLayout = QGridLayout()

        # Ajout du logo pieuvre
        self.label_img = QLabel()
        self.pixmap_img = QPixmap("images/pieuvre.jpg")
        self.label_img.setPixmap(self.pixmap_img)

        self.treeview = TreeView(self)

        self.codes = []
        self.highlighters = []
        self.docs = []

        self.tab_widget = TabWidget(self)

        self.statusbar = QStatusBar()
        self.statusbar.showMessage("Hello !", 2000)
        self.statusbar.setFixedSize(self.ecran.screenGeometry().width() * 4/5, 20)
        self.statusbar.setSizeGripEnabled(False)

        self.splitter = QSplitter()
        self.splitter.addWidget(self.treeview)
        self.splitter.addWidget(self.tab_widget)
        self.splitter.setSizes([100, 400])

        #self.statusbar.addWidget(MyReadWriteIndication)

        # Positionnement des Layouts
        self.gridLayout.addWidget(self.splitter)
        self.gridLayout.addWidget(self.statusbar)
        self.setLayout(self.gridLayout)

        if sys.platform == "linux":
            self.show()
        MenuBar(self)
        self.show()

    def quit_func(self):
        """
        Fonction de fermeture de l'IDE.
        On affiche une petite boîte pour demander si l'on souhaite vraiment fermer l'IDE.
        Les touches "return" et "escape" sont reliée resectivement à "Fermer" et "Annuler".

        :rtype: None
        """
        self.statusbar.showMessage("Fermeture...")  # Message de status
        box = QMessageBox()
        box.setText("Voulez-vous vraiment quitter l'IDE ?")
        box.setStandardButtons(QMessageBox.Cancel | QMessageBox.Close)
        box.setDefaultButton(QMessageBox.Close)
        box.setEscapeButton(QMessageBox.Cancel)
        val = box.exec_()

        if val == QMessageBox.Close:
            self.close()
        else:
            self.statusbar.showMessage("... ou pas !!", 1000)  # Message de status


    def addCode(self, title):
        """
        Fonction qui se charge d'ajouter à la liste des codes ouverts une nouvelle instance de la class Editeur et de créer un nouvel onglet

        :param title: Nom du document
        :type title: str
        :rtype: None
        """
        self.codes += [Editeur("ABeeZee", "#2E2E2E", "white", 14)]
        self.highlighters += [CodeHighLighter(self.codes[-1], self.codes[-1].document())]
        self.tab_widget.addTab(self.codes[-1], title)
        self.tab_widget.setCurrentIndex(len(self.codes) - 1)

    def a_propos(self):
        """
        Donne des informations sur l'IDE
        :rtype: None
        """
        QMessageBox.about(self, "À propos de Cthulhu", "Il s'agit d'un IDE avec un éditeur de texte pour du C gérant l'auto-complétion (en utilisant un arbre préfixe et la liste des classes), l'indentation automatique, la reconnaissance des balises et la coloration des ces dernières grâce à l'analyseur lexicale LEX et l'analyseur syntaxique YACC. L'IDE est en plusieurs langues. Il est possible de créer un ou plusieurs projet(s) ainsi donc qu'un ou plusieurs fichier(s) C ou H en tant que contenu, de sauvegarder le travail ainsi effectué et d'ouvrir un projet et un fichier C ou H. On peut ouvrir et/ou créer plusieurs fichiers C ou H avec une navigation par onglets avec le nom du ou des fichier(s). Au niveau de l'interface graphique, nous retrouvons un navigateur de fichier, un compilateur, des boutons, l'éditeur de texte, un menu de navigation ainsi qu'une barre d'état. Notre IDE a pour nom Cthulhu et a un logo composé d'une pieuvre avec une ancre !")