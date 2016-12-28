# Module relatif à la création du dossier Workplace à la racine de l'ordinateur et à la gestion des projets

from PySide.QtCore import *
from PySide.QtGui import *
from datetime import datetime
import os
from lexer import *


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

        fichier = open("%s/.conf" % (QDir(parent.workplace_path + project_name[0]).path()), "w")
        fichier.write("Created : %s/%s/%s" % (date.day, date.month, date.year))
        fichier.close()

    # elif parent.project_path[1]:
    elif project_name[1]:
        QMessageBox.critical(parent, "Le projet existe déjà", "Veuillez entrer un autre nom de projet")
        parent.new_project()


def open_projects(parent):
    projet = os.listdir(parent.workplace_path)
    for e in projet:
        check_file = QFileInfo(parent.workplace_path + e + "/.conf")
        if not os.path.isdir(parent.workplace_path + e) or not check_file.exists() and not check_file.isFile():
            projet.remove(e)

    print(projet)


def open_project(parent):
    name = parent.model.fileName(parent.currentIndex())
    if QDir(parent.fenetre.workplace_path + name).exists():
        parent.fenetre.project_path = parent.fenetre.workplace_path + name
        parent.fenetre.statusbar.showMessage("Le projet " + name + " a bien été ouvert.", 2000)

        project_files = get_project_files(parent.fenetre.project_path + "/")
        return get_def_functions(project_files)

    else:
        parent.open()


def get_project_files(path):
    res = []

    for e in os.listdir(path):

        if os.path.isfile(path + e):
            if e.split(".")[-1] == "c" or e.split(".")[-1] == "h":
                res += [path + e]
        else:
            res += get_project_files("%s%s/" % (path, e))

    return res


def get_def_functions(files):
    types = ["char", "bool", "double", "enum", "float", "int", "long", "short", "signed", "unsigned", "void"]

    res = []

    functions_by_files = yaccing_for_functions(files)

    for file_ in functions_by_files:
        fichier = open(file_, 'r')
        data = fichier.read()
        fichier.close()

        data_split = data.replace("\t", "").split("\n")
        for ligne in functions_by_files[file_]:
            tmp = data_split[int(ligne) - 1]

            for e in types:
                tmp = tmp.replace("%s " % e, "")

            tmp = tmp.replace(" ", "").replace(",", "|").replace("(", "|").replace(")", "").replace(";", "")
            tmp = tmp.split("{")[0]

            res += [tmp.split("|")]

            for i in range(len(res)):
                res[i] = res[i][:-1] if res[i][-1] == "" else res[i]

    return res


def yaccing_for_functions(files):
    res = {}

    for file_ in files:
        fichier = open(file_, "r")
        data = fichier.read()
        fichier.close()
        lignes = yaccing(data, False)

        for ligne in lignes:
            if "function_definition" in lignes[ligne]:
                if file_ in res:
                    res[file_] += [int(ligne) + 1]
                else:
                    res[file_] = [int(ligne) + 1]

    return res


def closeproject(parent):
    parent.tab_widget.clear()
    parent.project_path = ""
    parent.docs = []
    parent.codes = []
    parent.highlighters = []


def deleteproject(parent):
    pass
