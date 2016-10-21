# Module relatif à l'interface graphique

import sys
from PySide.QtGui import *
from PySide.QtWebKit import *
sys.path[:0] = ["../"]
from systeme.couleurs import *
from systeme.document import *
sys.path[:0] = ["gui"]

class Editeur(QTextEdit):
    def __init__(self, police, couleur_fond, couleur_text, taille_text):
        QTextEdit.__init__(self)

        self.setStyleSheet("QTextEdit { background-color:" + couleur_fond + ";" +
                           "font-family:" + police + ";" +
                           "color:" + couleur_text + ";" +
                           "font-size:" + str(taille_text) + "pt; }")

        self.append("Coucou")


class Fenetre(QWidget):
    def __init__(self, titre):
        super().__init__()

        self.ecran = QDesktopWidget()
        self.setWindowTitle(titre)
        self.setGeometry(0, 50, self.ecran.screenGeometry().width()/2, self.ecran.screenGeometry().height()/2)  # Taille de la fenêtre

        self.layout = QGridLayout()

        self.code = Editeur("ABeeZee", "#2E2E2E", "white", 14)  # Zone d'écriture du code

        #self.code.setReadOnly(True)

        self.ouvrir = QPushButton("Ouvrir")  # Bouton de lancement

        # Bouton temporaire de sauvegarde
        self.bouton_sauvegarde = QPushButton("Sauvegarder")

        # Positionnement des Layouts
        self.layout.addWidget(self.code, 0, 1, 6, 10)
        self.layout.addWidget(self.ouvrir, 11, 0)
        self.layout.addWidget(self.bouton_sauvegarde, 10, 0)

        self.setLayout(self.layout)

        self.show()

    # Fonction de sauvegarde Temporaire
    def save(self):
        chemin = QFileDialog.getSaveFileName(self, 'Sauvegarder un fichier',"","Fichier C (*.c) ;; Fichier H (*.h)")[0]
        if chemin != "":
            self.doc = Document(self.code, chemin)

    def open(self):
        chemin = QFileDialog.getOpenFileName(self, 'Ouvrir un fichier',"","Fichier C (*.c) ;; Fichier H (*.h)")[0]
        if chemin != "":
            #self.ouvrir.hide()
            self.doc = Document(self.code, chemin, True)

