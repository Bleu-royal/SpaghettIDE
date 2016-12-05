from PySide.QtCore import *
from PySide.QtGui import *
from datetime import datetime
import os


def create_workplace():
    """
    Créée un répertoire vide qui va contenir les projets

    :rtype: None
    """
    path = QDir.homePath()

    if not QDir(path + '/workplace/').exists():
        QDir(path).mkpath("workplace")


def newproject(parent):
    project_name = QInputDialog.getText(parent, 'Choix du nom du projet', 'Entrez un nom de projet :')

    while (project_name[0] == '' or "/" in project_name[0]) and project_name[1]:
        QMessageBox.critical(parent, "Erreur de syntaxe", "Le nom de projet n'est pas valide (veuillez éviter /)")
        project_name = QInputDialog.getText(parent, 'Choix du nom du projet', 'Entrez un nom de projet :')

    if not QDir(parent.workplace_path + project_name[0]).exists():
        QDir(parent.workplace_path).mkpath(project_name[0])

        date = datetime.now()

        fichier = open("%s/.conf"%(QDir(parent.workplace_path + project_name[0]).path()), "w")
        fichier.write("Created : %s/%s/%s"%(date.day,date.month,date.year))
        fichier.close()

    # elif parent.project_path[1]:
    elif project_name[1]:
        QMessageBox.critical(parent, "Le projet existe déjà", "Veuillez entrer un autre nom de projet")
        parent.new_project()


def openproject(parent):

    projet = os.listdir(parent.workplace_path)
    for e in projet:
        check_file = QFileInfo(parent.workplace_path + e + "/.conf")
        if not os.path.isdir(parent.workplace_path + e) or not check_file.exists() and not check_file.isFile():
            projet.remove(e)


def closeproject(parent):

    parent.tab_widget.clear()
    parent.project_path = ""
    parent.docs = []
    parent.codes = []
    parent.highlighters = []
