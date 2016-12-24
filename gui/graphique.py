# Module relatif à l'interface graphique

import sys
import os
from PySide.QtGui import *
from PySide.QtCore import *
from systeme.couleurs import *
from systeme.document import *
from systeme.workplace import *
from lexer import *
from themes.themes import *
from language.language import *

sys.path[:0] = ["../"]
sys.path[:0] = ["gui"]


class Editeur(QPlainTextEdit):

    def __init__(self, police, couleur_fond, couleur_texte, taille_texte):
        """
        Hérite de QTextEdit.
        C'est une zone de texte dans laquelle on peut écrire, que l'on utilise ici pour écrire du code.

        Ici, on modifie ses paramètres en fonction du thème souhaité.
        :param police: Police d'écriture
        :type police: str
        :param couleur_fond: Couleur d'arrière plan de l'éditeur (background)
        :type couleur_fond: str
        :param couleur_texte: Couleur du texte de base
        :type couleur_texte: str
        :param taille_texte: Taille de la police (en points)
        :type taille_texte: int
        :rtype: None
        """
        super().__init__()

        self.setStyleSheet("QPlainTextEdit { background-color:" + couleur_fond + ";"
                           + "font-family:" + police + ";"
                           + "color:" + couleur_texte + ";"
                           + "font-size:" + str(taille_texte) + "pt; }")

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

        self.set_style()

    def set_style(self):
        url = QDir().currentPath() + "/images/medium.jpg"
        c = get_color_from_theme("textedit")
        self.setStyleSheet("QTabWidget::pane{background-image: url(images/medium.gif);"
                           "background-repeat: no-repeat;background-position: center}"
                           "QTabWidget::tab-bar{left:0;}QTabBar::tab{color: "+get_rgb(c["tab-color"])+";"
                           "background-color:"+get_rgb(c["tab-back-color"])+";"
                           "border-bottom: 2px solid transparent;padding:7px 15px;"
                           "margin-top:0px;border-top-left-radius:10px;border-top-right-radius:10px;}"
                           "QTabBar::tab:selected,"
                           "QTabBar::tab:hover{background-color:"+get_rgb(c["tab-hover-back-color"])+";"
                           "color: "+get_rgb(c["tab-hover-color"])+";"
                           "border-bottom:"+get_rgb(c["tab-hover-bord-bot-color"])+";}"
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
    def __init__(self, parent, name, statut, fonction, shortcut_command=None):
        """
        Hérite de QAction.
        Crée ce qui est nécessaire pour faire un nouvel onglet dans la barre de menu, avec le nom,
        un raccourci, une fonction à exécuter.

        :param parent:  Classe qui appelle MyAction (ici Fenetre)
        :type parent: object
        :param name:  Nom à donner à l'action
        :type name: str
        :param statut:  Truc
        :type statut: str
        :param shortcut_command:  Commande de raccourci (facultative)
        :type shortcut_command: str
        :param fonction:  Fonction à exécuter
        :rtype: None
        """

        QAction.__init__(self, name, parent)  # Initialisation de l'action
        self.setMenuRole(QAction.NoRole)  # Pour que ca fonctionne sur toutes les plateformes
        self.setStatusTip(statut)
        self.setShortcut(shortcut_command)
        self.triggered.connect(fonction)


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

        #self.setStyleSheet("background-color: rgb(50, 50, 50); color: white")

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

        colors = get_color_from_theme("treeview")
        self.setStyleSheet("QTreeView{background: "+get_rgb(colors["BACKGROUND"])+";}"
                           "QTreeView::item{color: "+get_rgb(colors["ITEMS"])+";}"
                           "QTreeView::item:hover{color: "+get_rgb(colors["ITEMSHOVER"])+";}")

        self.cacher_pas_projet()

    def cacher_pas_projet(self):

        pass

    def mouseDoubleClickEvent(self, event):
        """
        Lorsque l'on double-clique sur le navigateur, on ouvre soit un projet, soit un document dans un projet.

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
            QMessageBox.critical(self.fenetre, "Erreur d'ouverture", "L'extention séléctionnée n'est pas lisible par notre IDE.\n\n"
                                                                     "Pour le moment...")


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
        self.master = parent

        # Nouveau Projet
        new_project_action = MyAction(parent, "&Nouveau Projet", "Nouveau projet", parent.new_project, "Ctrl+M")
        open_project_action = MyAction(parent, "&Ouvrir Projet", "Ouvrir un projet", parent.open_project, "Ctrl+L")
        exit_project_action = MyAction(parent, "&Fermer Projet", "Fermer le projet", parent.close_project, "Ctrl+K")

        # Nouveau Fichier
        new_fic_action = MyAction(parent, "&Nouveau", "Nouveau fichier", parent.new, "Ctrl+N")
        open_fic_action = MyAction(parent, "&Ouvrir", "Ouvrir un fichier", parent.open, "Ctrl+O")
        sauv_fic_action = MyAction(parent, "&Sauvegarder", "Sauvegarder le fichier courant", parent.save, "Ctrl+S")
        exit_ide_action = MyAction(parent, "&Fermer", "Fermer l'application", parent.quit_func, "Esc")

        # Menu divers
        apropos_ide_action = MyAction(parent, "&À Propos", "À propos de SpaghettIDE", parent.a_propos)
        help_ide_action = MyAction(parent, "&Aide", "Aide sur l'IDE", parent.help_func)

        ##### Menu Fichier et ses sous-menus ####
        fichier_menu = self.addMenu("&Fichier")
        self.set_actions(fichier_menu, new_fic_action, open_fic_action, sauv_fic_action, "sep", exit_ide_action)

        #### Menu Projet et ses sous-menus ####
        projet_menu = self.addMenu("&Projet")
        self.set_actions(projet_menu, new_project_action, open_project_action, exit_project_action)

        #### Menu Apparence ####
        apparence_menu = self.addMenu("&Apparence")

        # Thèmes
        groupe_theme = QActionGroup(parent)
        theme_basic = MyAction(parent, "&Thème Basique", "Thème basique", self.to_basic)
        theme_pimp = MyAction(parent, "&Thème Pimp", "Thème pimp", self.to_pimp)
        theme_forest = MyAction(parent, "&Thème Forêt", "Thème forêt", self.to_forest)
        theme_ocean = MyAction(parent, "&Thème Océan", "Thème océan", self.to_ocean)
        # autre_theme = MyAction(parent, "&nom theme", "nom theme", self.fonction_a_relier)

        self.set_group(theme_basic, groupe_theme, apparence_menu, "basic")
        self.set_group(theme_pimp, groupe_theme, apparence_menu, "pimp")
        self.set_group(theme_forest, groupe_theme, apparence_menu, "forest")
        self.set_group(theme_ocean, groupe_theme, apparence_menu, "ocean")
        # self.set_group(autre_theme, groupe_theme, apparence_menu, "nom theme")

        apparence_menu.addSeparator()

        #Langues
        groupe_langue = QActionGroup(parent)
        fr = MyAction(parent, "&Français", "Français", self.to_fr)
        en = MyAction(parent, "&English", "English", self.to_en)

        self.set_group(fr, groupe_langue, apparence_menu, "fr")
        self.set_group(en, groupe_langue, apparence_menu, "en")

        #### Menu SpaghettIDE ####
        spaghettide_menu = self.addMenu("&SpaghettIDE")
        self.set_actions(spaghettide_menu, apropos_ide_action, help_ide_action)

    def set_actions(self, menu, *args):
        """
        Sets all actions to a menu

        :param menu: Menu where actions will be added (QMenuBar)
        :type menu: object
        :param args: List of actions you wanna add
        :type args: list
        :rtype: None
        """
        for a in args:
            if a == "sep":
                menu.addSeparator()
            else:
                menu.addAction(a)

    def set_group(self, action, groupe, menu, name):
        """
        Create a groupe of action (especially for themes)

        :param action: Action to add in a group
        :param groupe: Group
        :param menu: Menu where is the groupe
        :param name: Name of the theme
        """
        action.setCheckable(True)
        if name in (get_current_theme(), get_current_language()):
            action.setChecked(True)
        groupe.addAction(action)
        menu.addAction(action)

    # Themes
    def __change_theme_to(self, theme):
        if get_current_theme() != theme:
            change_theme(theme)
            self.message_redemarrer()

    def to_basic(self):
        self.__change_theme_to("basic")

    def to_pimp(self):
        self.__change_theme_to("pimp")

    def to_forest(self):
        self.__change_theme_to("forest")

    def to_ocean(self):
        self.__change_theme_to("ocean")

    # Languages
    def to_fr(self):
        if get_current_language() != "fr":
            self.master.statusbar.showMessage("Changement en langue Française à venir.", 2000)

    def to_en(self):
        if get_current_language() != "en":
            self.master.statusbar.showMessage("English language comming soon !", 2000)

    def message_redemarrer(self):
        QMessageBox.critical(self.master, "Redémarrer", "Veuillez relancer l'application pour que le thème soit actualisé.")


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
        self.setStyleSheet("QObject::pane{background: "+get_rgb(get_color_from_theme("textedit")["text-back-color"])+";}")
        self.setGeometry(20, 50, self.ecran.screenGeometry().width() - 100, self.ecran.screenGeometry().height() - 100)
        # Taille de la fenêtre

        self.workplace_path = workplace_path

        self.project_path = ""

        self.gridLayout = QGridLayout()
        self.gridLayout.setContentsMargins(0, 0, 0, 0)  # No spacing around widgets

        # Ajout du logo pieuvre
        # self.label_img = QLabel()
        # self.pixmap_img = QPixmap("images/pieuvre.jpg")
        # self.label_img.setPixmap(self.pixmap_img)

        self.treeview = TreeView(self)

        self.codes = []
        self.highlighters = []
        self.docs = []

        self.tab_widget = TabWidget(self)

        self.splitter = QSplitter()
        self.splitter.addWidget(self.treeview)
        self.splitter.addWidget(self.tab_widget)
        self.splitter.setSizes([100, 400])
        self.splitter.setMinimumSize(self.width(), self.height()-50)

        self.statusbar = QStatusBar()
        status_color = get_color_from_theme("statusbar")
        self.statusbar.setStyleSheet("background: "+get_rgb(status_color["BACKGROUND"])+";"
                                     "color: "+get_rgb(status_color["TEXT"])+";")
        self.statusbar.showMessage("Hello !", 2000)
        self.statusbar.setFixedHeight(30)
        self.statusbar.setSizeGripEnabled(False)

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
        c = get_color_from_theme("textedit")
        self.codes += [Editeur("ABeeZee", get_rgb(c["text-back-color"]), get_rgb(c["text-color"]), 14)]
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

        apropos = open("content/apropos.txt", "r").readlines()

        QMessageBox.about(self, "À propos de SpaghettIDE ", "".join(apropos))

    def help_func(self):

        self.statusbar.showMessage("AIDEZ MOIIIIIIII", 1000)
        pass

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
            self.restart = False
            self.close()
        else:
            self.statusbar.showMessage("... ou pas !!", 1000)  # Message de status

