# Module relatif à l'interface graphique

import sys,os
from PySide.QtGui import *
from PySide.QtCore import *

sys.path[:0] = ["../"]
from systeme.couleurs import *
from systeme.document import *
from lexer import *

sys.path[:0] = ["gui"]


class Editeur(QTextEdit):

    def __init__(self, police, couleur_fond, couleur_text, taille_text):
        QTextEdit.__init__(self)

        self.setStyleSheet("QTextEdit { background-color:" + couleur_fond + ";"
                           + "font-family:" + police + ";"
                           + "color:" + couleur_text + ";"
                           + "font-size:" + str(taille_text) + "pt; }")

        self.append("int main ( int argc, char** argv ){\n\n\treturn 0;\n\n}")


class TabWidget(QTabWidget):

    def __init__(self, parent):
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

        self.setStyleSheet("QTabWidget::pane{background-image: url(%s);"
                           "background-repeat: no-repeat;background-position: center}"
                           "QTabWidget::tab-bar{left:0;}QTabBar::tab{color:black;"
                           "background-color:gray;border-bottom: 2px solid transparent;padding:7px 15px;"
                           "margin-top:0px;border-top-left-radius:10px;border-top-right-radius:10px;}"
                           "QTabBar::tab:selected,"
                           "QTabBar::tab:hover{background-color:#2E2E2E; color: white;border-bottom:#2E2E2E;}"
                           "QTabBar::tab:!selected {margin-top: 5px;}"%url)

    def close_current_tab(self):

        if len(self.parent.codes) != 0:
            idx = self.currentIndex()

            self.removeTab(idx)

            doc = self.parent.docs[idx]
            code = self.parent.codes[idx]

            self.parent.docs.remove(doc)
            self.parent.codes.remove(code)

            self.parent.statusbar.showMessage("Fermeture de l'onglet courrant.", 2000)

    def next_tab(self):
        idx = self.currentIndex() + 1 if self.currentIndex() < self.count() - 1 else 0
        self.setCurrentIndex(idx)

    def prev_tab(self):
        idx = self.currentIndex() - 1 if self.currentIndex() >= 1 else self.count() - 1
        self.setCurrentIndex(idx)

    def mousePressEvent(self, event):
        if len(self.parent.docs) == 0:
            self.parent.new()


class MyAction(QAction):
    def __init__(self, papa, name, status, func, shortcut_command=None):
        """
        :param papa:  Class qui appelle MyAction (ici Fenetre)
        :type papa: object
        :param name:  Nom à donner à l'action
        :type name: str
        :param status:  Truc
        :type status: str
        :param shortcut_command:  Commande de raccourcis (facultative)
        :type shortcut_command: str
        :param func:  Fonction à exécuter
        """

        QAction.__init__(self, name, papa)  # Initialisation de l'action
        self.setMenuRole(QAction.NoRole)  # Pour que ca fonctionne sur toutes les plateformes
        self.setStatusTip(status)
        self.setShortcut(shortcut_command)
        self.triggered.connect(func)


class TreeView(QTreeView):
    def __init__(self, fenetre):

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

    def mouseDoubleClickEvent(self, event):
        name = self.model.fileName(self.currentIndex())
        if QDir(self.fenetre.workplace_path + name).exists():
            self.fenetre.project_path = self.fenetre.workplace_path + name
            self.fenetre.statusbar.showMessage("Le projet " + name + " a bien été ouvert.", 2000)
        else:
            self.open()

    def keyPressEvent(self, event):
        if event.key() == 16777220:
            name = self.model.fileName(self.currentIndex())
            if QDir(self.fenetre.workplace_path + name).exists():
                self.fenetre.project_path = self.fenetre.workplace_path + name
            else:
                self.open()
        else:
            QTreeView.keyPressEvent(self, event)

    def open(self):
        path = self.model.filePath(self.currentIndex())
        name = self.model.fileName(self.currentIndex())
        ext = name.split(".")[-1]
        if ext in ["c", "h"] and self.fenetre.project_path in path and self.fenetre.project_path != "":
            self.fenetre.open(path)


class MenuBar(QMenuBar):

    def __init__(self, parent):
        super().__init__(parent)

        ## Menus

        # Nouveau Projet (à relier avec de vraies fonctions qui font des trucs de fifous)
        # et ptet changer les raccourcis quand on aura de vraies fonctions.
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
        # Fermer l'IDE
        exit_ide_action = MyAction(parent, "&Fermer", "Quitter l'application", parent.quit_func, "Esc")

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


class Fenetre(QWidget):
    def __init__(self, titre, workplace_path=QDir.homePath() + "/workplace/"):
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

        self.show()
        MenuBar(self)
        self.show()

    def quit_func(self):  # Fonction de fermeture de l'IDE
        self.statusbar.showMessage("Fermeture...")
        box = QMessageBox()
        box.setText("Voulez-vous vraiment fermer l'IDE ?")
        box.setStandardButtons(QMessageBox.Cancel | QMessageBox.Close)
        box.setDefaultButton(QMessageBox.Close)
        box.setEscapeButton(QMessageBox.Cancel)
        val = box.exec_()

        if val == QMessageBox.Close:
            self.close()
        else:
            self.statusbar.showMessage("... ou pas !!", 1000)

    def new(self):  # Fonction de création de nouveau fichier reliée au sous-menu "Nouveau"
        new = "Unamed"+str(len(self.docs)+1)
        self.statusbar.showMessage(("Nouveau fichier " + new))
        self.addCode(new)
        self.docs += [Document(self.codes[-1], "")]
        self.tab_widget.setCurrentIndex(len(self.codes) - 1)

    def save(self):  # Fonction de sauvegarde reliée au sous-menu "Sauvergarder"
        if self.project_path != "":
            idx = self.tab_widget.currentIndex()
            if idx != -1:
                if self.docs[idx].chemin_enregistrement == "":
                    chemin = \
                        QFileDialog.getSaveFileName(self, 'Sauvegarder un fichier', self.project_path, "Fichier C (*.c) ;; Fichier H (*.h)")[0]
                    if chemin != "" and self.project_path in chemin:
                        self.docs[idx].set_chemin_enregistrement(chemin)
                        self.docs[idx].sauvegarde_document(chemin)
                        self.tab_widget.setTabText(idx, self.docs[idx].nom)

                        self.statusbar.showMessage(self.docs[idx].nom+" a bien été sauvegardé.", 2000)
                    else:
                        QMessageBox.critical(self, "Impossible de sauvegarder ce document", "Ce document ne fais pas partie du projet courant")
                else:
                    self.docs[idx].sauvegarde_document()
        else:
            QMessageBox.critical(self, "Aucun projet ouvert", "Veuillez ouvrir ou créer un projet")

    def open(self, chemin=False):  # Fonction d'ouverture d'un fichier reliée au sous-menu "Ouvrir un fichier"
        if self.project_path != "":
            if not chemin:
                chemin = QFileDialog.getOpenFileName(self, 'Ouvrir un fichier', self.project_path, "Fichier C (*.c) ;; Fichier H (*.h)")[0]
            print("--%s--" % self.project_path, "--%s--" % chemin, sep="\n")
            if self.project_path in chemin:
                print("ici")
            if chemin != "" and self.project_path in chemin:
                title = chemin.split("/")[-1]
                self.addCode(title)
                self.statusbar.showMessage("Ouverture de "+title, 2000)
                self.docs += [Document(self.codes[-1], chemin, True)]
                self.tab_widget.setCurrentIndex(len(self.codes) - 1)
            else:
                self.statusbar.showMessage("Impossible d'ouvrir ce document car il ne fait pas partit du projet courrant.", 2000)
        else:
            self.statusbar.showMessage("Aucun projet ouvert, veuillez ouvrir ou créer un projet.", 2000)

    def addCode(self, title):
        self.codes += [Editeur("ABeeZee", "#2E2E2E", "white", 14)]
        self.highlighters += [CodeHighLighter(self.codes[-1], self.codes[-1].document())]
        self.tab_widget.addTab(self.codes[-1], title)
        self.tab_widget.setCurrentIndex(len(self.codes) - 1)

    def new_project(self):
        project_name = QInputDialog.getText(self, 'Choix du nom du projet', 'Entrez un nom de projet :')
        while (project_name[0] == '' or "/" in project_name[0]) and project_name[1]:
            QMessageBox.critical(self, "Erreur de syntaxe", "Le nom de projet n'est pas valide (veuillez éviter /)")
            project_name = QInputDialog.getText(self, 'Choix du nom du projet', 'Entrez un nom de projet :')

        if not QDir(self.workplace_path + project_name[0]).exists():
            QDir(self.workplace_path).mkpath(project_name[0])
        elif self.project_path[1]:
            QMessageBox.critical(self, "Le projet existe déjà", "Veuillez entrer un autre nom de projet")
            self.new_project()

    def open_project(self):

        projet = os.listdir(self.workplace_path)
        for e in projet:
            if not os.path.isdir(self.workplace_path + e):
                projet.remove(e)
        print(projet)

    def close_project(self):

        self.project_path = ""
