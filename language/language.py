import json
from xml import *

def get_current_language():
    """
    :return: La langue utilisée dans l'IDE, stockée dans le fichier conf.xml
    :rtype: str
    """
    configuration = open_xml("conf.xml")
    return configuration['language']

def get_text(key):
    """
    Permet de récupérer le texte dans la langue actuelle pour un élément. Si le texte n'est pas disponible dans la
    langue voulue, on affiche "--------" à la place.

    :param key: Élément dont on veut récupérer le texte. C'est une clef du dictionnaire contenant tous les textes.
    :type key: str
    :return: le texte voulu
    :rtype: str
    """

    fichier = open("language/textes.json", "r")
    dico = json.loads(fichier.read())
    fichier.close()

    if key in dico:
        if get_current_language() in dico[key]:
            return dico[key][get_current_language()]

    return "--------"

def get_tmenu(key):
    """
    On différencie cette fonction de 'get_text()' pour séparer le texte normal par celui des menus afin d'avoir un
    dictionnaire trop long. Mais le principe est exactement le même que pour 'get_text()'
    Permet de récupérer le texte dans la langue actuelle pour un élément de menu. Si le texte n'est pas disponible dans la
    langue voulue, on affiche "--------" à la place.

    :param key: Élément de menu dont on veut récupérer le texte. C'est une clef du dictionnaire contenant tous les textes
    pour les menus.
    :type key: str
    :return: le texte du menu voulu
    :rtype: str
    """

    fichier = open("language/menus.json", "r")
    dico = json.loads(fichier.read())
    fichier.close()

    if key in dico:
        if get_current_language() in dico[key]:
            return "&" + dico[key][get_current_language()]

    return "--------"
