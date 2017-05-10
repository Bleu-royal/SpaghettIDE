# Module relatif à l'exécution de l'IDE

import sys 
import os 
import shutil
from gui.graphique import *  
from systeme.workplace import *
from PySide.QtGui import *
from gui.chargement import Loading
from xml import *

app = QApplication(sys.argv)

# Fonction permettant de cacher les dossiers __pycache__ et leur contenu en les supprimant à l'exécution du programme

def remove_folder(path):  # Inutile now
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
# remove_folder(".")

def remove_parsetab():
    if os.path.isfile("lexer/parsetab.py"):
        os.remove("lexer/parsetab.py")

try:
    verif = open("lexer/lexer.py", "r")
    verif.close()

    remove_parsetab()

    workplace_path = open_xml("conf.xml")["current_workplace"]

    if "racc_utilisateur.json" not in os.listdir("gui/raccourcis/"):
        os.system("cp gui/raccourcis/racc_defaut.json gui/raccourcis/racc_utilisateur.json")

    fenetre = Fenetre("SpaghettIDE (Bleu Royal)", workplace_path)  # Creation of the main window

    print(configuration)

    if configuration['numerote_lines'] == 'False':
        fenetre.show_line_column()
        write_xml("conf.xml", "numerote_lines", "False")

    create_workplace()

    if configuration['loading'] == 'True':
        load = Loading()
        load.exec()

    sys.exit(app.exec_())

except FileNotFoundError:
    mess = QMessageBox()
    mess.setText("FATAL ERROR")
    mess.setStandardButtons(QMessageBox.Close)
    mess.setDefaultButton(QMessageBox.Close)
    mess.exec_()
