# Module relatif à la gestion des projets

import sys
sys.path[:0] = ["../"]
from gui.graphique import *
sys.path[:0] = ["systeme"]

def new_project(self):
    """
    Créée un nouveau projet
    Le projet créé doit avoir un nom différent d'un projet déjà existant, et ne dois pas comporter de "/" dans son nom.

    :rtype: None
    """

    Fenetre.__init__()
    
    project_name = QInputDialog.getText(self, 'Choix du nom du projet', 'Entrez un nom de projet :')

    while (project_name[0] == '' or "/" in project_name[0]) and project_name[1]:
        QMessageBox.critical(self, "Erreur de syntaxe", "Le nom de projet n'est pas valide (veuillez éviter /)")
        project_name = QInputDialog.getText(self, 'Choix du nom du projet', 'Entrez un nom de projet :')

    if not QDir(self.workplace_path + project_name[0]).exists():
        QDir(self.workplace_path).mkpath(project_name[0])

        date = datetime.now()

        fichier = open("%s/.conf"%(QDir(self.workplace_path + project_name[0]).path()), "w")
        fichier.write("Created : %s/%s/%s"%(date.day,date.month,date.year))
        fichier.close()

    # elif self.project_path[1]:
    elif project_name[1]:
        QMessageBox.critical(self, "Le projet existe déjà", "Veuillez entrer un autre nom de projet")
        self.new_project()

def open_project(self):
    """
    Ouvre un projet
    :rtype: None
    """

    Fenetre.__init__()

    projet = os.listdir(self.workplace_path)
    for e in projet:
        check_file = QFileInfo(self.workplace_path + e + "/.conf")
        if not os.path.isdir(self.workplace_path + e) or not check_file.exists() and not check_file.isFile():
            projet.remove(e)

    print(projet)

def close_project(self):
    """
    Ferme un projet
    :rtype: None
    """

    Fenetre.__init__()

    self.tab_widget.clear()
    self.project_path = ""
    self.docs = []
    self.codes = []
    self.highlighters = []

def delete_project(self):

    Fenetre.__init__()
    
    pass