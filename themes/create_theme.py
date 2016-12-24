import json
import os
import sys

def make_dico(keys):
    """
    Makes a dict using the keys from the args and sets all values to a list of 3 zeros.

    :param keys: List of keys.
    :type keys: tuple
    :rtype: dict
    """
    dico = {}
    for k in keys:
        dico[k] = [0, 0, 0]

    return dico

def make_json(name, dico):
    """
    Creates a json file using a dictionnary

    :param name: Name of the file
    :type name: str
    :param dico: Dictionnary to save in the json
    :type dico: dict
    :rtype: None
    """
    save = json.dumps(dico, indent=2)

    wfi = open(name + ".json", "w")  # json file
    wfi.write(save)
    wfi.close()

def make_files(name):
    """
    Makes differents json used to make a full theme. We use dicts to contain list of rgb colors.

    :param name: name of the theme
    :rtype: None
    """

    treeview_keys = ("BACKGROUND", "ITEMS", "ITEMSHOVER")
    token_keys = ("IDENTIFIER", "KEYWORD", "STRING_LITERAL", "COMMENT", "CONSTANT", "TYPE", "OP")
    textedit_keys = ("text-back-color", "text-color", "tab-color", "tab-back-color", "tab-hover-back-color",
                     "tab-hover-color", "tab-hover-bord-bot-color")
    statusbar_keys = ("BACKGROUND", "TEXT")

    treeview = make_dico(treeview_keys)
    make_json(name+"/treeview", treeview)

    token = make_dico(token_keys)
    make_json(name+"/token", token)

    textedit = make_dico(textedit_keys)
    make_json(name+"/textedit", textedit)

    statusbar = make_dico(statusbar_keys)
    make_json(name+"/statusbar", statusbar)


def new_theme(name):
    if name not in os.listdir("."):
        os.system("mkdir "+name)
        make_files(name)
    else:
        print(name+" is already a theme name. Please choose a new name.")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        name = sys.argv[1]
        if name != "":
            new_theme(name)
