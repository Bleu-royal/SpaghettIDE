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

        self.setStyleSheet("QTextEdit { background-color:" + couleur_fond + ";" +
                           "font-family:" + police + ";" +
                           "color:" + couleur_text + ";" +
                           "font-size:" + str(taille_text) + "pt; }")

        self.append("Coucou")

class TabWidget(QTabWidget):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_W), self)
        shortcut.activated.connect(self.close_current_tab)

    def close_current_tab(self):
        idx = self.currentIndex()
        self.removeTab(idx)

        doc = self.parent.docs[idx]
        code = self.parent.codes[idx]

        self.parent.docs.remove(doc)
        self.parent.codes.remove(code)

class Fenetre(QWidget):
    def __init__(self, titre):
        super().__init__()

        self.ecran = QDesktopWidget()
        self.setWindowTitle(titre)

        self.setGeometry(50, 50, self.ecran.screenGeometry().width()-100, self.ecran.screenGeometry().height()-100)  # Taille de la fenêtre

        self.layout = QGridLayout()

        # self.img1 = QPixmap("Dragon.jpg")  # Image de lancement
        self.ouvrir = QPushButton("Ouvrir")  # Bouton de lancement
        # self.ouvrir.setIcon(QIcon(self.img1))  # Image sur le bouton
        # self.ouvrir.setIconSize(QSize(self.code.width()*1.5, self.code.height()*1.5))  # Taille de l'image


        self.codes = []
        #self.code = Editeur("ABeeZee", "#2E2E2E", "white", 14)  # Zone d'écriture du code
        self.highlighters = []

        self.docs = []


        self.tab_widget = TabWidget(self)

        #self.code.setReadOnly(True)

        self.ouvrir = QPushButton("Ouvrir")  # Bouton de lancement

        # Bouton temporaire de sauvegarde
        self.bouton_sauvegarde = QPushButton("Sauvegarder")

        self.bouton_nouveau = QPushButton("Nouveau")

        # Positionnement des Layouts
        self.layout.addWidget(self.tab_widget, 0, 1, 6, 10)
        #self.layout.addWidget(self.code, 0, 1, 6, 10)
        self.layout.addWidget(self.ouvrir, 11, 0)
        self.layout.addWidget(self.bouton_sauvegarde, 10, 0)
        self.layout.addWidget(self.bouton_nouveau, 12, 0)

        self.setLayout(self.layout)

        self.show()

    def addCode(self, title):
        self.codes += [Editeur("ABeeZee", "#2E2E2E", "white", 14)]
        self.highlighters += [CodeHighLighter(self.codes[-1].document())]
        self.tab_widget.addTab(self.codes[-1], title)
        self.tab_widget.setCurrentIndex(len(self.codes) - 1)

    def new(self):
        self.addCode("Unamed")
        self.docs += [Document(self.codes[-1], "")]
        self.tab_widget.setCurrentIndex(len(self.codes) - 1)

    # Fonction de sauvegarde Temporaire

    def save(self):
        idx = self.tab_widget.currentIndex()
        if self.docs[idx].chemin_enregistrement == "":
            chemin = QFileDialog.getSaveFileName(self, 'Sauvegarder un fichier', "", "Fichier C (*.c) ;; Fichier H (*.h)")[0]
            if chemin != "":
                self.docs[idx].set_chemin_enregistrement(chemin)
                self.docs[idx].sauvegarde_document(chemin)
                self.tab_widget.setTabText(idx, self.docs[idx].nom)
        else:
            self.docs[idx].sauvegarde_document()

    def open(self):
        chemin = QFileDialog.getOpenFileName(self, 'Ouvrir un fichier', "", "Fichier C (*.c) ;; Fichier H (*.h)")[0]
        if chemin != "":
            title = chemin.split("/")[-1]
            self.addCode(title)
            self.docs += [Document(self.codes[-1], chemin, True)]
            self.tab_widget.setCurrentIndex(len(self.codes) - 1)