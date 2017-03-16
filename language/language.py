import json

def get_current_language():
    """
    :return: La langue utilisée dans l'IDE, stoquée dans le fichier conf.xml
    :rtype: str
    """
    return "en"

def get_text(key):
    """
    Permet de récupérer le texte dans la langue actuelle pour un élément. Si le texte n'est pas disponnible dans la
    langue voulue, on renvoie "indisponible"

    :param key: Élément dont on veut récupérer le texte. C'est une clef du dictionnaire contenant tout les textes.
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

    return "Indisponible"
