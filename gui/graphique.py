# Module relatif à l'interface graphique

import sys, os
from PySide.QtGui import *
from PySide.QtCore import *
sys.path[:0] = ["../"]
from systeme.couleurs import *
from systeme.document import *
from systeme.workplace import *
from lexer import *
sys.path[:0] = ["gui"]

class Editeur(QPlainTextEdit):

    def __init__(self, police, couleur_fond, couleur_text, taille_text):
        """
        Hérite de QTextEdit.
        C'est une zone de texte dans laquelle on peut écrire, que l'on utilise ici pour écrire du code.

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
        super().__init__()

        self.setStyleSheet("QPlainTextEdit { background-color:" + couleur_fond + ";"
                           + "font-family:" + police + ";"
                           + "color:" + couleur_text + ";"
                           + "font-size:" + str(taille_text) + "pt; }")

        # self.append("int main ( int argc, char** argv ){\n\n\treturn 0;\n\n}")

    def keyPressEvent(self, event):

        super().keyPressEvent(event)

        if event.key() == 16777220:
            yaccing(self.toPlainText())


class TabWidget(QTabWidget):

    def __init__(self, parent):
        """
        Hérite de QTabWidget.
        Permet de faire plusieurs onglets de code ( utilisation de la classe Editeur ).
        On définit ici les raccourcis de navigation entre et pour les onglets
        pour fermer, ouvrir, aller au suivant...

        :param parent: Parent de la classe ( qui appelle )
        :type parent: object
        :rtype: None
        """
        super().__init__()

        self.parent = parent

        shortcut_close = QShortcut(QKeySequence.Close, self)
        shortcut_close.activated.connect(self.close_current_tab)

        shortcut_open = QShortcut(QKeySequence.Open, self)
        shortcut_open.activated.connect(self.parent.open)

        shortcut_new = QShortcut(QKeySequence.New, self)
        shortcut_new.activated.connect(self.parent.new)

        shortcut_save = QShortcut(QKeySequence.Save, self)
        shortcut_save.activated.connect(self.parent.save)

        shortcut_next_tab = QShortcut(QKeySequence('Alt+tab'), self)
        shortcut_next_tab.activated.connect(self.next_tab)

        shortcut_prev_tab = QShortcut(QKeySequence('Alt+Shift+tab'), self)
        shortcut_prev_tab.activated.connect(self.prev_tab)

        url = QDir().currentPath() + "/images/medium.jpg"
        self.setStyleSheet("QTabWidget::pane{background-image: url(images/medium.gif);"
                           "background-repeat: no-repeat;background-position: center}"
                           "QTabWidget::tab-bar{left:0;}QTabBar::tab{color:black;"
                           "background-color:gray;border-bottom: 2px solid transparent;padding:7px 15px;"
                           "margin-top:0px;border-top-left-radius:10px;border-top-right-radius:10px;}"
                           "QTabBar::tab:selected,"
                           "QTabBar::tab:hover{background-color:#2E2E2E; color: white;border-bottom:#2E2E2E;}"
                           "QTabBar::tab:!selected {margin-top: 5px;}")

    def close_current_tab(self):
        """
        Fonction pour fermer l'onglet courant.

        :rtype: None
        """
        if len(self.parent.codes) != 0:  # On vérifie que la liste d'onglet n'est pas vide.
            idx = self.currentIndex()

            self.removeTab(idx)

            doc = self.parent.docs[idx]
            code = self.parent.codes[idx]

            self.parent.docs.remove(doc)
            self.parent.codes.remove(code)

            self.parent.statusbar.showMessage("Fermeture de l'onglet courant.", 2000)

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
        On crée un nouvel onglet de code lorsqu'on double-clique sur la page vide (si on n'a pas d'onglet déjà ouvert).

        :param event: Contient les positions x et y de l'endroit où on a cliqué. NON UTILISÉ ICI.
        :rtype: None
        """
        if len(self.parent.docs) == 0:
            self.parent.new()


class MyAction(QAction):
    def __init__(self, parent, name, status, func, shortcut_command=None):
        """
        Hérite de QAction.
        Crée ce qui est nécessaire pour faire un nouvel onglet dans la barre de menu, avec le nom,
        un raccourci, une fonction à exécuter.

        :param parent:  Classe qui appelle MyAction (ici Fenetre)
        :type parent: object
        :param name:  Nom à donner à l'action
        :type name: str
        :param status:  Truc
        :type status: str
        :param shortcut_command:  Commande de raccourci (facultative)
        :type shortcut_command: str
        :param func:  Fonction à exécuter
        :rtype: None
        """

        QAction.__init__(self, name, parent)  # Initialisation de l'action
        self.setMenuRole(QAction.NoRole)  # Pour que ca fonctionne sur toutes les plateformes
        self.setStatusTip(status)
        self.setShortcut(shortcut_command)
        self.triggered.connect(func)


class TreeView(QTreeView):
    def __init__(self, fenetre):
        """
        Hérite de QTreeView.
        Permet d'afficher le navigateur de fichiers, permettant d'ouvrir et de visualiser les documents
        d'un ou de plusieurs projets.

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

    def mouseDoubleClickEvent(self, event):
        """
        Lorsque l'on double-clique sur le navigateur, on ouvre soit un projet, soit un document dans un projet.

        :param event: Contient les positions x et y de l'endroit où on a cliqué. NON UTILISÉ ICI.
        :rtype: None
        """
        name = self.model.fileName(self.currentIndex())
        check_file = QFileInfo(self.fenetre.workplace_path + name + "/.conf")
        if QDir(self.fenetre.workplace_path + name).exists() and check_file.exists() and check_file.isFile():
            self.fenetre.project_path = self.fenetre.workplace_path + name
            self.fenetre.statusbar.showMessage("Le projet " + name + " a bien été ouvert.", 2000)
        else:
            self.open()

    def keyPressEvent(self, event):
        """
        Bind de la touche entrée.
        Lorsque l'on sélectionne un document et que l'on appuie sur entrée, on ouvre le document
        ou le projet sélectionné.

        Contient les positions x et y de l'endroit où on a cliqué. NON UTILISÉ ICI.
        :rtype: None
        """
        if event.key() == 16777220:  # Référence de la touche "entrée"
            open_project()
        else:
            QTreeView.keyPressEvent(self, event)

    def open(self):
        """
        Ouvre un document si son extension est valide.
        Appelle la fonction parent pour ouvrir un fichier.

        :rtype: None
        """
        path = self.model.filePath(self.currentIndex())
        name = self.model.fileName(self.currentIndex())
        ext = name.split(".")[-1]
        if ext in ("c", "h") and self.fenetre.project_path in path and self.fenetre.project_path != "":
            self.fenetre.open(path)


class MenuBar(QMenuBar):

    def __init__(self, parent):
        """
        Hérite de QMenuBar.
        C'est ici que la barre de menu est créée.
        On appelle la classe MyAction pour chaque élément du menu que l'on souhaite créer, puis on ajoute
        ces éléments au menu principal.

        :param parent: Parent de la classe ( qui appelle )
        :type parent: object
        :rtype: None
        """
        super().__init__(parent)

        ## Menus

        # Nouveau Projet
        new_project_action = MyAction(parent, "&Nouveau Projet", "Nouveau projet", parent.new_project, "Ctrl+M")
        # Ouvrir un projet déjà existant
        open_project_action = MyAction(parent, "&Ouvrir Projet", "Ouvrir un projet", parent.open_project, "Ctrl+L")
        # Fermer le projet
        exit_project_action = MyAction(parent, "&Fermer Projet", "Fermer le projet", parent.close_project, "Ctrl+K")

        # Nouveau Fichier
        new_fic_action = MyAction(parent, "&Nouveau", "Nouveau fichier", parent.new, "Ctrl+N")
        # Ouvrir un fichier déjà existant
        open_fic_action = MyAction(parent, "&Ouvrir", "Ouvrir un fichier", parent.open, "Ctrl+O")
        # Sauvegarder le fichier courant
        sauv_fic_action = MyAction(parent, "&Sauvegarder", "Sauvegarder le fichier courant", parent.save, "Ctrl+S")

        #À Propos de Cthulhu
        apropos_ide_action = MyAction(parent, "&À Propos", "À propos de SpaghettIDE", parent.a_propos)
        # Fermer l'IDE
        exit_ide_action = MyAction(parent, "&Fermer", "Fermer l'application", parent.quit_func, "Esc")

        # Menu Fichier et ses sous-menus
        fichier_menu = self.addMenu("&Fichier")
        fichier_menu.addAction(new_fic_action)
        fichier_menu.addAction(open_fic_action)
        fichier_menu.addAction(sauv_fic_action)
        fichier_menu.addSeparator()
        fichier_menu.addAction(exit_ide_action)
        # Menu Projet et ses sous-menus
        projet_menu = self.addMenu("&Projet")
        projet_menu.addAction(new_project_action)
        projet_menu.addAction(open_project_action)
        projet_menu.addAction(exit_project_action)
        # Menu SpaghettIDE
        spaghettide_menu = self.addMenu("&SpaghettIDE")
        spaghettide_menu.addAction(apropos_ide_action)

class Fenetre(QWidget):
    def __init__(self, titre, workplace_path=QDir.homePath() + "/workplace/"):
        """
        Hérite de QWidget
        Class principale, dans laquelle tout est rassemblé. On appelle tout ce qui est nécessaire à la création
        de la fenêtre et au fonctionnement du programme.

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
        # self.label_img = QLabel()
        # self.pixmap_img = QPixmap("images/pieuvre.jpg")
        # self.label_img.setPixmap(self.pixmap_img)

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

        # self.statusbar.addWidget(MyReadWriteIndication)
        self.menuBar = MenuBar(self)

        # Positionnement des Layouts
        # self.gridLayout.addWidget(self.menuBar)
        self.gridLayout.addWidget(self.splitter)
        self.gridLayout.addWidget(self.statusbar)
        self.setLayout(self.gridLayout)

        # if sys.platform == "linux":
        #     self.show()

        self.show()

    def quit_func(self):
        """
        Fonction de fermeture de l'IDE.
        On affiche une petite boîte pour demander si l'on souhaite vraiment fermer l'IDE.
        Les touches "return" et "escape" sont respectivement reliées à "Fermer" et "Annuler".

        :rtype: None
        """
        self.statusbar.showMessage("Fermeture...")  # Message de status
        box = QMessageBox()
        box.setText("Voulez-vous vraiment fermer l'IDE ?")
        box.setStandardButtons(QMessageBox.Cancel | QMessageBox.Close)
        box.setDefaultButton(QMessageBox.Close)
        box.setEscapeButton(QMessageBox.Cancel)
        val = box.exec_()

        if val == QMessageBox.Close:
            self.close()
        else:
            self.statusbar.showMessage("... ou pas !!", 1000)  # Message de status

    def new(self):
        """
        Fonction de création de nouveau fichier reliée au sous-menu "Nouveau".
        On ajoute ici un nouvel onglet à nos codes déjà ouverts ( ou on créée un premier onglet )
        qui s'appelle par défaut "Sans nom" + le numéro courant dans la liste des onglets.
        On appelle la fonction self.addCode()

        :rtype: None
        """
        
        new_document(self)

    def save(self):
        """
        Fonction de sauvegarde reliée au sous-menu "Sauvergarder".
        On sauvegarde un fichier en l'enregistrant dans un projet (ou non).
        On ouvre une QFileDialog qui affiche le navigateur du système habituel pour enregistrer des documents.

        :return:
        """
        
        save_document(self)

    def deja_ouvert(self, chemin):

        return document_deja_ouvert(self, chemin)

    def open(self, chemin=False):
        """
        Fonction d'ouverture d'un fichier reliée au sous-menu "Ouvrir un fichier"
        On utilise une QFileDialog qui affiche le navigateur du système habituel pour ouvrir des documents.

        :param chemin: N'existe pas si on appelle via le menu ou le raccourcis clavier. Il est
        spécifié si il appartient au projet courant et que l'on souhaite l'ouvrir sans passer par
        la fenetre de dialogue.
        :type chemin: str
        :rtype: None
        """

        open_document(self, chemin)

    def add_code(self, title):
        """
        Fonction qui se charge d'ajouter à la liste des codes ouverts une nouvelle instance de la classe
        Editeur et de créer un nouvel onglet

        :param title: Nom du document
        :type title: str
        :rtype: None
        """
        self.codes += [Editeur("ABeeZee", "#2E2E2E", "white", 14)]
        self.highlighters += [CodeHighLighter(self.codes[-1], self.codes[-1].document())]
        self.tab_widget.addTab(self.codes[-1], title)
        self.tab_widget.setCurrentIndex(len(self.codes) - 1)

    def new_project(self):
        """
        Créée un nouveau projet
        Le projet créé doit avoir un nom différent d'un projet déjà existant,
        et ne doit pas comporter de "/" dans son nom.

        :rtype: None
        """

        newproject(self)

    def open_project(self):
        """
        Ouvre un projet
        :rtype: None
        """

        open_projects(self)

    def close_project(self):
        """
        Ferme un projet
        :rtype: None
        """

        closeproject(self)

    def delete_project(self):
        
        deleteproject(self)

    def close_document(self):
        
        closedocument(self)

    def delete_document(self):
        
        deletedocument(self) 

    def a_propos(self):
        """
        Donne des informations sur l'IDE
        :rtype: None
        """
        QMessageBox.about(self, "À propos de SpaghettIDE ", "Il s'agit d'un IDE avec un éditeur de texte pour du C gérant l'auto-complétion (en utilisant un arbre préfixe et la liste des classes), l'indentation automatique, la reconnaissance des balises et la coloration des ces dernières grâce à l'analyseur lexicale LEX et l'analyseur syntaxique YACC. L'IDE est en plusieurs langues. Il est possible de créer un ou plusieurs projet(s) ainsi donc qu'un ou plusieurs fichier(s) C ou H en tant que contenu, de sauvegarder le travail ainsi effectué et d'ouvrir un projet et un fichier C ou H. On peut ouvrir et/ou créer plusieurs fichiers C ou H avec une navigation par onglets avec le nom du ou des fichier(s). Au niveau de l'interface graphique, nous retrouvons un navigateur de fichier, un compilateur, des boutons, l'éditeur de texte, un menu de navigation ainsi qu'une barre d'état. Notre IDE a pour nom SpaghettIDE et a un logo composé d'une pieuvre avec une ancre !")
