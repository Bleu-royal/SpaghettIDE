# Module relatif à la création du dossier Workplace à la racine de l'ordinateur

from PySide.QtCore import *

def create_workplace():
    """
    Créée un répertoire vide qui va contenir les projets

    :rtype: None
    """
    path = QDir.homePath()

    if not QDir(path + '/workplace/').exists():
        QDir(path).mkpath("workplace")
