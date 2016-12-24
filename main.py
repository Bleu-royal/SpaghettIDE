# Module relatif à l'exécution de l'IDE

import sys 
import os 
import shutil
from gui.graphique import *  
from kernel.bind import bind  
from systeme.workplace import *  
from PySide.QtGui import *

app = QApplication(sys.argv)
QResource.registerResource("./poulpe.rcc");

# Fonction permettant de cacher les dossiers __pycache__ et leur contenu en les supprimant à l'exécution du programme

def remove_folder(path):
    """
    Retire les __pycache__/ des répertoires de projets.

    :param path: Chemin du projet
    :rtype: None
    """
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

    fenetre = Fenetre("SpaghettIDE (Bleu Royal)")  # Creation of the main window
    bind(fenetre)  # Connection between buttons and functions
    create_workplace()

    sys.exit(app.exec_())
    
except FileNotFoundError:
    mess = QMessageBox()
    mess.setText("Veuillez lancer l'IDE via le répertoire du main.py")
    mess.setStandardButtons(QMessageBox.Close)
    mess.setDefaultButton(QMessageBox.Close)
    mess.exec_()
