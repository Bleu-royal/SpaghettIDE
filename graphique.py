# Module relatif à l'interface graphique

import sys
from PySide.QtGui import *
from PySide.QtWebKit import *
from couleurs import *
from document import *

app = QApplication(sys.argv)


class Fenetre(QWidget):
    def __init__(self, titre):
        super().__init__()
        self.ecran = QDesktopWidget()
        self.setWindowTitle(titre)
        self.setGeometry(0, 50, self.ecran.screenGeometry().width(), self.ecran.screenGeometry().height()-50)  # Taille de la fenêtre

        self.layout = QGridLayout()

        self.img1 = QPixmap("Dragon.jpg")
        self.code = QTextEdit()
        self.code.setReadOnly(True)
        self.ouvrir = QPushButton()
        self.ouvrir.setIcon(QIcon(self.img1))
        self.ouvrir.setIconSize(QSize(self.code.width()*1.5, self.code.height()*1.5))
        self.ouvrir.clicked.connect(self.open)

        # Bouton temporaire de sauvegarde
        self.bouton_sauvegarde = QPushButton("Save")
        self.bouton_sauvegarde.clicked.connect(self.save)

        self.apercu = QWebView()
        self.apercu.setMaximumWidth(450)
        self.apercu.setMaximumHeight(450)
        self.apercu.setZoomFactor(0.5)

        # Positionnement des Layouts
        self.layout.addWidget(self.apercu, 5, 0)
        self.layout.addWidget(self.code, 0, 1, 6, 10)
        self.layout.addWidget(self.ouvrir, 0, 1, 6, 10)
        self.layout.addWidget(self.bouton_sauvegarde, 10, 0)

        self.setLayout(self.layout)

        self.show()

        self.highlighter = HTMLHighLighter(self.code.document())

    # Fonction de sauvgarde Temporaire
    def save(self):
        chemin = QFileDialog.getSaveFileName(self, 'Save file')[0]
        if chemin != "":
            self.doc = Document(self.code, self.apercu, chemin)

    def open(self):
        chemin = QFileDialog.getOpenFileName(self, 'Open file')[0]
        if chemin != "":
            self.ouvrir.hide()
            self.code.setReadOnly(False)
            self.doc = Document(self.code, self.apercu, chemin, True)


fenetre = Fenetre("IDE de la mort qui tue (Bleu Royal)")
sys.exit(app.exec_())
