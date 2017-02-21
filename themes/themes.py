# Gestion des thèmes

from xml import *
import json
import os


def change_theme(theme):

    write_xml('theme', theme)
    

def get_current_theme():
    """
    Give the currrent theme of the application

    :rtype: str
    """

    try:
        configuration = open_xml()
        current_theme_dir = str(configuration['theme'])  # We load the current theme
    except:  # Si le fichier n'existe pas
        change_theme("basic")
        return get_current_theme()

    if current_theme_dir not in os.listdir("themes"):  # If the theme doesn't exists, we use the basic theme.
        change_theme("basic")
        return get_current_theme()
    else:
        return current_theme_dir


def get_color_from_theme(what):
    """
    Used to get colors of items depending of the selected theme

    token --> Coloration of tokens depending of their types.
    treeview --> Coloration of elements in the TreeView (file searcher).
    statusbar --> Coloration of elements in the status bar.
    textedit --> Colors of the tabs and the background of the textedit area.

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
