import sys
import os
import shutil
from gui.graphique import *
from kernel.bind import bind


app = QApplication(sys.argv)
"""
opts = Options("Cthulhu (Bleu Royal)")

def creer_fenetre():
    folder_path = QFileDialog.getExistingDirectory(opts, 'Ouverture du projet')
    if folder_path:
        fenetre = Fenetre("Cthulhu (Bleu Royal)", folder_path)  # Creation of the main window
        bind(fenetre)  # Connection between buttons and functions
        opts.close()

opts.button.clicked.connect(creer_fenetre)
"""

# Fonction permettant de cacher les dossiers __pycache__ et leur contenu en les supprimant à l'exécution du programme


def remove_folder(path):
    for e in os.listdir(path):
        if e == "__pycache__":
            shutil.rmtree(path + "/" + e)
        else:
            if os.path.isdir(e):
                remove_folder(e)
remove_folder(".")


try:
    verif = open("lexer.py", "r")
    verif.close()

    fenetre = Fenetre("Cthulhu (Bleu Royal)")  # Creation of the main window
    bind(fenetre)  # Connection between buttons and functions

    sys.exit(app.exec_())
    
except FileNotFoundError:
    mess = QMessageBox()
    mess.setText("Veuillez lancer l'IDE via le répertoire du main.py")
    mess.setStandardButtons(QMessageBox.Close)
    mess.setDefaultButton(QMessageBox.Close)
    mess.exec_()
