# Module relatif à la création du dossier Workplace à la racine de l'ordinateur et à la gestion des projets

from PySide.QtCore import *
from PySide.QtGui import *
from datetime import datetime
import os
import sys
from lexer import *
from xml import *
from systeme.parallele import ProgressOpening, ProgressDisp

class NewProject(QDialog):
    def __init__(self):
        super().__init__()

        self.cancel = False

        self.setWindowTitle("Choix du nom du projet")

        self.layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()

        self.lbl_line_edit = QLabel("Entrez un nom de projet :")

        self.line_edit = QLineEdit()
        
        self.project_name_lang = QComboBox()
        self.project_name_lang.addItem("Python")
        self.project_name_lang.addItem("C")
        self.project_name_lang.addItem("Arithmétique")

        self.cancel_button = QPushButton("Cancel")
        self.valider_button = QPushButton("Valider")

        self.cancel_button.clicked.connect(self.cancel_action)
        self.valider_button.clicked.connect(self.valider_action)

        self.layout.addWidget(self.lbl_line_edit)
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.project_name_lang)

        self.buttons_layout.addWidget(self.cancel_button)
        self.buttons_layout.addWidget(self.valider_button)
        self.layout.addLayout(self.buttons_layout)

        self.setLayout(self.layout)

        tree = etree.parse("projets.xml")
        root = tree.getroot()
        projets = etree.Element("projets")
        projet = etree.SubElement(projets, "projet")
        name = etree.SubElement(projet, "name")
        name.text = get_project_name(self)
        language = etree.SubElement(projet, "language")
        language.text = get_project_lang(self)
        location = etree.SubElement(projet, "location")
        location.text = ""
        

    def cancel_action(self):
        self.cancel = True
        self.done(0)

    def valider_action(self):
        self.done(0)

    def get_project_name(self):
        return self.line_edit.text()

    def get_project_lang(self):
        return self.project_name_lang.currentText().replace("é","e").lower()

    def keyPressEvent(self, event):

        if event.key() == 16777216:
            self.cancel = True

        super().keyPressEvent(event)


def create_workplace():
    """
    Créée un répertoire vide qui va contenir les projets

    :rtype: None
    """
    path = QDir.homePath()

    if not QDir(path + '/workplace/').exists():
        QDir(path).mkpath("workplace")


def newproject(parent):

    np = NewProject()
    np.exec()
    project_name = np.get_project_name()
    project_lang = np.get_project_lang()
    cancel = np.cancel

    while (project_name == '' or "/" in project_name) and not cancel:
        QMessageBox.critical(parent, "Erreur de syntaxe", "Le nom de projet n'est pas valide (veuillez éviter /)")
        np = NewProject()
        np.exec()
        project_name = np.get_project_name()
        project_lang = np.get_project_lang()
        cancel = np.cancel

    if not QDir(parent.workplace_path + project_name).exists() and not cancel:
        QDir(parent.workplace_path).mkpath(project_name)

        # date = datetime.now()

        # fichier = open("%s/.conf" % (QDir(parent.workplace_path + project_name[0]).path()), "w")
        # fichier.write("Created : %s/%s/%s" % (date.day, date.month, date.year))
        # fichier.close()

    # elif parent.project_path[1]:
    elif not cancel:
        QMessageBox.critical(parent, "Le projet existe déjà", "Veuillez entrer un autre nom de projet")
        parent.new_project()


# def open_projects(parent):
#     projet = os.listdir(parent.workplace_path)
#     for e in projet:
#         check_file = QFileInfo(parent.workplace_path + e + "/.conf")
#         if not os.path.isdir(parent.workplace_path + e) or not check_file.exists() and not check_file.isFile():
#             projet.remove(e)

#     print(projet)


class Mem:
    def __init__(self):
        self.res = None
        self.message = ""
        self.progress = 0


def open_project(parent, name=False):

    if not name:
        name = parent.model.fileName(parent.currentIndex())

    if QDir(parent.fenetre.workplace_path + name).exists():
        if name:
            parent.fenetre.docs = []
            parent.fenetre.highlighters = []
            parent.fenetre.codes = []
            parent.fenetre.tab_widget.clear()

        parent.fenetre.show_progress_bar()

        parent.fenetre.project_path = parent.fenetre.workplace_path + name
        project_files = get_project_files(parent.fenetre.project_path + "/")

        memory = Mem()

        gdf = ProgressOpening(ProgressWin, project_files, memory, parent)
        gdf.start()  # Processing of the opening project function
        disp_gdf = ProgressDisp(memory, parent)
        disp_gdf.start()  # Displays of the files studied
        """
        # Problèmes de plantage du serveur graphique sur Linux lors de la modification du GUI via un Thread
        ProgressWin(project_files, memory)
        parent.function_declarations.emit(memory.res)
        """

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


class GetDefFonctions(QObject):
    resultat = Signal(tuple)

    def __init__(self, files, parent):
        QObject.__init__(self)
        self.files = files
        self.parent = parent

    def run(self):
        # # Yaccing for functions and structs
        functions = {}
        structs = {}
        vars_ = {}

        l = len(self.files)
        if l>0: incr = 100/l
        else: incr = 100

        i = 0
        for file_ in self.files:
            i += 1
            self.parent.update_progress(i*incr)
            self.parent.update_text("Ouverture du projet...  --- PROCESS : Traitement du fichier %s" %file_)

            fichier = open(file_, "r")
            data = fichier.read()
            fichier.close()
            lignes = yaccing(data, False)

            for ligne in lignes:
                if "function_definition" in lignes[ligne]:
                    if file_ in functions:
                        functions[file_] += [int(ligne) + 1]
                    else:
                        functions[file_] = [int(ligne) + 1]
                elif "struct_or_union" in lignes[ligne]:
                    if file_ in structs:
                        structs[file_] += [int(ligne) + 1]
                    else:
                        structs[file_] = [int(ligne) + 1]
                elif "declaration" in lignes[ligne]:
                    if file_ in vars_:
                        vars_[file_] += [int(ligne) + 1]
                    else:
                        vars_[file_] = [int(ligne) + 1]

        funct_by_files = functions
        struct_by_files = structs
        vars_by_files = vars_

        # # Get Definitions of Functions
        types = ["char", "bool", "double", "enum", "float", "int", "long", "short", "signed", "unsigned", "void"]
        functions = {}
        structs = {}
        vars_ = {}

        for file_ in funct_by_files:
            fichier = open(file_, 'r')
            data = fichier.read()
            fichier.close()

            data_split = data.replace("\t", "").split("\n")
            for ligne in funct_by_files[file_]:
                tmp = data_split[int(ligne) - 1]

                for e in types:
                    tmp = tmp.replace("%s " % e, "")

                tmp = tmp.replace(" ", "").replace(",", "|").replace("(", "|").replace(")", "").replace(";", "")
                tmp = tmp.split("{")[0]

                if file_ in functions:
                    functions[file_] += [tmp.replace("}", "").split("|")]
                else:
                    functions[file_] = [tmp.replace("}", "").split("|")]

                functions[file_][-1] += [int(ligne)]

                for fi in functions:
                    functions[fi] = functions[fi][:-1] if functions[fi][-1] == "" else functions[fi]

        for file_ in struct_by_files:
            fichier = open(file_, 'r')
            data = fichier.read()
            fichier.close()

            data_split = data.replace("\t", "").split("\n")
            for ligne in struct_by_files[file_]:
                tmp = data_split[int(ligne) - 1].split()
                if tmp[0] == "struct":
                    name = tmp[1].replace("{","").replace("}", "")
                    if file_ in structs:
                        structs[file_] += [name]
                    else:
                        structs[file_] = [name]

        for file_ in vars_by_files:
            fichier = open(file_, 'r')
            data = fichier.read()
            fichier.close()

            data_split = data.replace("\t", "").split("\n")
            for ligne in vars_by_files[file_]:
                tmp = data_split[int(ligne) - 1].split()
                if tmp[0] in types:
                    name = tmp[1].replace("{","")
                    if file_ in vars_:
                        vars_[file_] += [name]
                    else:
                        vars_[file_] = [name]

        self.resultat.emit((functions, structs, vars_))


class ProgressWin(QObject):
    def __init__(self, liste, memory):
        QObject.__init__(self)

        self.memory = memory
        self.prev_text = ""

        # Lancement des opérations
        self.process = GetDefFonctions(liste, self)
        self.process.resultat.connect(self.resultat)
        self.process.run()

    def update_text(self, m):
        if m != self.prev_text:
            self.memory.message = m
            self.prev_text = m

    def update_progress(self, n):
        self.memory.progress = n

    def resultat(self, res):
        self.memory.res = res


def closeproject(parent):
    parent.tab_widget.clear()
    parent.project_path = ""
    parent.docs = []
    parent.codes = []
    parent.highlighters = []


def deleteproject(parent):
    pass
