# Module relatif à l'interface graphique

import sys
from PySide.QtGui import *
from PySide.QtWebKit import *
from couleurs import *
from document import *

app = QApplication(sys.argv)

class Fenetre(QWidget):
    def __init__(self, titre, size=[600, 500]):
        super().__init__()
        self.setWindowTitle(titre)
        self.resize(size[0], size[1])

        self.layout = QGridLayout()

        self.code = QTextEdit()

        # Bouton temporaire de sauvegarde
        self.bouton_sauvegarde = QPushButton("Save")
        self.bouton_sauvegarde.clicked.connect(self.save)

        self.apercu = QWebView()
        self.apercu.load("")
        self.apercu.setMaximumWidth(450)
        self.apercu.setMaximumHeight(450)
        self.apercu.setZoomFactor(0.5)

        # Positionnement des Layouts
        self.layout.addWidget(self.apercu, 5, 0)
        self.layout.addWidget(self.code, 0, 1, 6, 10)
        self.layout.addWidget(self.bouton_sauvegarde, 10,0)

        self.setLayout(self.layout)

        self.show()

        self.highlighter = HTMLHighLighter(self.code.document())


    #Fonction de sauvgarde Temporaire
    def save(self):
        chemin = QFileDialog.getSaveFileName(self,'Open file','/home')[0]
        self.doc = Document(self.code, chemin)
        print(self.doc.nombre_lignes)
        print(self.doc.nom)
        print(self.doc.extension)


fenetre = Fenetre("IDE de la mort qui tue (Bleu Royal)", [400, 400])
sys.exit(app.exec_())
