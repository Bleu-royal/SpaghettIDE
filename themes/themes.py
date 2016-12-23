# Gestion des thèmes

import json

def get_current_theme():
    """
    Give the currrent theme of the application

    :rtype: str
    """
    file = open("themes/current_theme.txt", "r")
    current_theme_dir = file.read()  # We load the current theme
    file.close()

    return current_theme_dir


def get_color_from_theme(what):
    """
    Used to get colors of items depending of the selected theme

    token --> Coloration of tokens depending of their types.
    treeview --> Coloration of elements in the file searcher.

    :return: dict
    """
    dir = get_current_theme()

    dico = open("themes/"+dir+"/"+what+".json", "r")
    dict_colors = json.load(dico)
    dico.close()

    return dict_colors

def get_rgb(l):
    """
    Returns a RGB string from a list.

    :param l: Liste of color
    :type l: list
    :rtype: str
    """

    return "rgb(" + str(l[0]) + "," + str(l[1]) + "," + str(l[2]) + ")"

