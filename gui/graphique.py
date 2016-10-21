# Module relatif à l'interface graphique

import sys
from PySide.QtGui import *
from PySide.QtWebKit import *
sys.path[:0] = ["../"]
from systeme.couleurs import *
from systeme.document import *
sys.path[:0] = ["gui"]


class Fenetre(QWidget):
    def __init__(self, titre):
        super().__init__()

        self.police_code = "ABeeZee"
        self.couleur_fond_code = QPalette()
        self.couleur_fond_code.setColor(QPalette.Base, "#2E2E2E")
        self.couleur_ecriture_basique = "white"
        self.taille_police = 14

        self.ecran = QDesktopWidget()
        self.setWindowTitle(titre)
        self.setGeometry(0, 50, self.ecran.screenGeometry().width()/2, self.ecran.screenGeometry().height()/2)
        # Taille de la fenêtre

        self.layout = QGridLayout()

        self.code = QTextEdit()  # Zone d'écriture du code
        self.code.setFontFamily(self.police_code)  # Police d'écriture
        self.code.setPalette(self.couleur_fond_code)  # Couleur de fond
        self.code.setTextColor(self.couleur_ecriture_basique)  # Couleur d'écriture
        self.code.setFontPointSize(self.taille_police)  # Taille de police
        # self.code.setReadOnly(True)

        # self.img1 = QPixmap("Dragon.jpg")  # Image de lancement
        self.ouvrir = QPushButton("Ouvrir")  # Bouton de lancement
        # self.ouvrir.setIcon(QIcon(self.img1))  # Image sur le bouton
        # self.ouvrir.setIconSize(QSize(self.code.width()*1.5, self.code.height()*1.5))  # Taille de l'image

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
            self.ouvrir.hide()
            self.doc = Document(self.code, chemin, True)
