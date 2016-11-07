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

        shortcut_next_tab = QShortcut(QKeySequence('Alt+tab'), self)
        shortcut_next_tab.activated.connect(self.next_tab)

        shortcut_prev_tab = QShortcut(QKeySequence('Alt+Shift+tab'), self)
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

class MyAction(QAction):
    def __init__(self, papa, name, status, func, shortcut_command=None):
        """
        :param papa:  Class qui appelle MyAction (ici Fenetre)
        :type papa: object
        :param name:  Nom à donner à l'action
        :type name: str
        :param status:  Truc
        :type status: str
        :param shortcut_command:  Commande de raccourcis (faculative)
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
        #self.img1 = QPixmap("Dragon.jpg")  # Image de lancement
        #self.ouvrir.setIcon(QIcon(self.img1))  # Image sur le bouton
        #self.ouvrir.setIconSize(QSize(self.code.width()*1.5, self.code.height()*1.5))  # Taille de l'image

        self.fenetre = fenetre

        self.model = QFileSystemModel()
        self.file = QFile()
        self.model.setRootPath(QDir.currentPath())
        self.setModel(self.model)
        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)
        self.setAnimated(True)
        self.filters = []
        self.filters.append("*c")
        self.filters.append("*h")
        self.model.setNameFilters(self.filters)
        self.model.setNameFilterDisables(False)
        self.model.setReadOnly(False)
        self.setRootIndex(self.model.index(QDir.currentPath()))

    def mouseDoubleClickEvent(self, event):
        self.open()

    def keyPressEvent(self, event):
        if event.key() == 16777220:
            self.open()
        else:
            QTreeView.keyPressEvent(self, event)

    def open(self):
        path = self.model.filePath(self.currentIndex())
        name = self.model.fileName(self.currentIndex())
        ext = name.split(".")[-1]
        if ext in ["c", "h"]:
            self.fenetre.open(path)


class MenuBar(QMenuBar):

    def __init__(self, parent):
        super().__init__(parent)

        ## Menus
        new_action = MyAction(parent, "&Nouveau", "Nouveau fichier", parent.new, "Ctrl+N")  # Nouveau Fichier
        open_action = MyAction(parent, "&Ouvrir", "Ouvrir un fichier", parent.open, "Ctrl+O")  # Ouvrir un fichier déjà existant
        sauv_action = MyAction(parent, "&Sauvegarder", "Sauvegarder le fichier courant", parent.save, "Ctrl+S")  # Sauvegarder le fichier courant
        exit_action = MyAction(parent, "&Fermer", "Quitter l'application", parent.quit_func, "Esc")  # Fermer l'IDE

        # Menu Fichier et ses sous-menus
        fichier_menu = self.addMenu("&Fichier")
        fichier_menu.addAction(new_action)
        fichier_menu.addAction(open_action)
        fichier_menu.addAction(sauv_action)
        fichier_menu.addSeparator()
        fichier_menu.addAction(exit_action)



class Fenetre(QWidget):
    def __init__(self, titre):
        super().__init__()

        self.ecran = QDesktopWidget()
        self.setWindowTitle(titre)
        self.setGeometry(50, 50, self.ecran.screenGeometry().width() - 100, self.ecran.screenGeometry().height() - 100)
        # Taille de la fenêtre

        self.layout = QGridLayout()

        #Ajout du logo pieuvre
        self.label_img = QLabel()
        self.pixmap_img = QPixmap("images/pieuvre.jpg")
        self.label_img.setPixmap(self.pixmap_img)

        self.treeview = TreeView(self)     
        
        self.codes = []
        self.highlighters = []
        self.docs = []

        self.tab_widget = TabWidget(self)

        self.splitter = QSplitter()
        self.splitter.addWidget(self.treeview)
        self.splitter.addWidget(self.tab_widget)
        self.splitter.setSizes([100, 400])

        # Positionnement des Layouts
        self.layout.addWidget(self.splitter)
        self.setLayout(self.layout)

        self.show()

        MenuBar(self)
        
        self.show()

    def quit_func(self):  # Fonction de fermeture de l'IDE
        box = QMessageBox()
        box.setText("Voulez-vous vraiment fermer notre IDE ?")
        box.setStandardButtons(QMessageBox.Cancel | QMessageBox.Close)
        box.setDefaultButton(QMessageBox.Close)
        box.setEscapeButton(QMessageBox.Cancel)
        val = box.exec_()

        if val == QMessageBox.Close:
            self.close()

    def new(self):  # Fonction de création de nouveau fichier reliée au sous-menu "Nouveau"
        self.addCode("Unamed"+str(len(self.docs)+1))
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

    def open(self, chemin=False):  # Fonction d'ouverture d'un fichier reliée au sous-menu "Ouvrir un fichier"
        if not chemin:
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
