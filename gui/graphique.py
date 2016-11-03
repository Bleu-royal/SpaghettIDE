# Module relatif à l'interface graphique

import sys
from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtWebKit import *

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

        # shortcut_next_tab = QShortcut(QKeySequence.NextChild, self)
        shortcut_next_tab = QShortcut(QKeySequence('alt+tab'), self)
        shortcut_next_tab.activated.connect(self.next_tab)

        shortcut_prev_tab = QShortcut(QKeySequence('alt+shift+tab'), self)
        shortcut_prev_tab.activated.connect(self.prev_tab)

    def close_current_tab(self):

        if len(self.parent.codes) != 0:
            idx = self.currentIndex()

            self.removeTab(idx)

            doc = self.parent.docs[idx]
            code = self.parent.codes[idx]

            self.parent.docs.remove(doc)
            self.parent.codes.remove(code)

    def next_tab(self):
        idx = self.currentIndex() + 1 if self.currentIndex() < self.count() - 1 else 0
        self.setCurrentIndex(idx)

    def prev_tab(self):
        idx = self.currentIndex() - 1 if self.currentIndex() >= 1 else self.count() - 1
        self.setCurrentIndex(idx)


class Fenetre(QWidget):
    def __init__(self, titre):
        super().__init__()

        self.ecran = QDesktopWidget()
        self.setWindowTitle(titre)
        self.setGeometry(50, 50, self.ecran.screenGeometry().width() - 100, self.ecran.screenGeometry().height() - 100)
        # Taille de la fenêtre

        self.layout = QGridLayout()

        #Ajout du logo pieuvre
        self.label_img  = QLabel()
        self.pixmap_img = QPixmap("images/pieuvre.jpg")
        self.label_img.setPixmap(self.pixmap_img)

        #Ajout du navigateur de fichier
        self.treeview = QTreeView()
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())
        self.treeview.setModel(self.model)
        self.treeview.hideColumn(1)
        self.treeview.hideColumn(2)
        self.treeview.hideColumn(3)
        self.treeview.setAnimated(True)
        #event=...
        #self.treeview.keyPressEvent(QKeyEvent*event)
        #QString.str(event.text("COUCOU"))
        self.treeview.setRootIndex(self.model.index(QDir.currentPath()))

        #self.img1 = QPixmap("Dragon.jpg")  # Image de lancement
        self.ouvrir = QPushButton("Ouvrir")  # Bouton de lancement  --> 1ère apparition
        #self.ouvrir.setIcon(QIcon(self.img1))  # Image sur le bouton
        #self.ouvrir.setIconSize(QSize(self.code.width()*1.5, self.code.height()*1.5))  # Taille de l'image

        self.codes = []
        # self.code = Editeur("ABeeZee", "#2E2E2E", "white", 14)  # Zone d'écriture du code
        self.highlighters = []
        self.docs = []
        self.tab_widget = TabWidget(self)
        # self.code.setReadOnly(True)

        # Bouton temporaire d'ouverture d'un fichier
        self.ouvrir = QPushButton("Ouvrir")  # --> 2ème apparition c'est normal ????????????
        # Bouton temporaire de sauvegarde
        self.bouton_sauvegarde = QPushButton("Sauvegarder")
        # Bouton temporaire d'ouverture de nouveau fichier
        self.bouton_nouveau = QPushButton("Nouveau")

        # Positionnement des Layouts
        self.layout.addWidget(self.treeview, 3, 0, 3, 2)
        self.layout.addWidget(self.label_img, 0, 0, 3, 1)
        self.layout.addWidget(self.tab_widget, 0, 2, 6, 10)
        # self.layout.addWidget(self.code, 0, 1, 6, 10)
        self.layout.addWidget(self.ouvrir, 1, 1)
        self.layout.addWidget(self.bouton_sauvegarde, 2, 1)
        self.layout.addWidget(self.bouton_nouveau, 0, 1)

        self.setLayout(self.layout)
        self.show()

        # Menus

        # Nouveau Fichier
        new_action = QAction("&Nouveau", self)
        new_action.setMenuRole(QAction.NoRole)
        new_action.setStatusTip("Nouveau fichier")
        new_action.triggered.connect(self.new)

        # Ouvrir un fichier déjà existant
        open_action = QAction("&Ouvrir", self)
        open_action.setMenuRole(QAction.NoRole)
        open_action.setStatusTip("Ouvrir un fichier")
        open_action.triggered.connect(self.open)

        # Sauvegarder le fichier courant
        sauv_action = QAction("&Sauvegarder", self)
        sauv_action.setMenuRole(QAction.NoRole)
        sauv_action.setStatusTip("Sauvegarder le fichier courant")
        sauv_action.triggered.connect(self.save)

        # Fermer l'IDE
        exit_action = QAction("&Exit", self)
        exit_action.setMenuRole(QAction.NoRole)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Quitter l'application")
        exit_action.triggered.connect(self.quit_func)

        menu = QMenuBar(self)

        # Menu Fichier et ses sous-menus
        fichier_menu = menu.addMenu("&Fichier")
        fichier_menu.addAction(new_action)
        fichier_menu.addAction(open_action)
        fichier_menu.addAction(sauv_action)
        fichier_menu.addAction(exit_action)
        self.show()

    def quit_func(self):  # Fonction de fermeture de l'IDE
        self.close()

    def new(self):  # Fonction de création de nouveau fichier reliée au sous-menu "Nouveau"
        self.addCode("Unamed")
        self.docs += [Document(self.codes[-1], "")]
        self.tab_widget.setCurrentIndex(len(self.codes) - 1)

    def save(self):  # Fonction de sauvegarde reliée au sous-menu "Sauvergarder"
        idx = self.tab_widget.currentIndex()
        if idx != -1:
            if self.docs[idx].chemin_enregistrement == "":
                chemin = \
                    QFileDialog.getSaveFileName(self, 'Sauvegarder un fichier', "", "Fichier C (*.c) ;; Fichier H (*.h)")[0]
                if chemin != "":
                    self.docs[idx].set_chemin_enregistrement(chemin)
                    self.docs[idx].sauvegarde_document(chemin)
                    self.tab_widget.setTabText(idx, self.docs[idx].nom)
            else:
                self.docs[idx].sauvegarde_document()

    def open(self):  # Fonction d'ouverture d'un fichier reliée au sous-menu "Ouvrir un fichier"
        chemin = QFileDialog.getOpenFileName(self, 'Ouvrir un fichier', "", "Fichier C (*.c) ;; Fichier H (*.h)")[0]
        if chemin != "":
            title = chemin.split("/")[-1]
            self.addCode(title)
            self.docs += [Document(self.codes[-1], chemin, True)]
            self.tab_widget.setCurrentIndex(len(self.codes) - 1)

    def addCode(self, title):
        self.codes += [Editeur("ABeeZee", "#2E2E2E", "white", 14)]
        self.highlighters += [CodeHighLighter(self.codes[-1].document())]
        self.tab_widget.addTab(self.codes[-1], title)
        self.tab_widget.setCurrentIndex(len(self.codes) - 1)
