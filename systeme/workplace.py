# Module relatif à la création du dossier Workplace à la racine de l'ordinateur et à la gestion des projets

from PySide.QtCore import *
from PySide.QtGui import *
from datetime import datetime
import os
import sys

import shutil
import lexer.lexer as lex
from xml import *
from systeme.parallele import ProgressOpening, ProgressDisp
from language.language import get_text, get_tmenu
import kernel.variables as var

class NewProject(QDialog):
    def __init__(self):
        """
        Créé l'affichage pour la fenêtre de création de projet.
        """
        super().__init__()

        self.cancel = False
        self.valider = False

        self.setWindowTitle(get_text("proj_choice"))

        self.layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()

        self.lbl_line_edit = QLabel(get_text("proj_name"))

        self.line_edit = QLineEdit()
        
        self.project_name_lang = QComboBox()
        self.project_name_lang.addItem("Python")
        self.project_name_lang.addItem("C")
        self.project_name_lang.addItem("Arithmétique")

        self.cancel_button = QPushButton(get_text("cancel"))
        self.valider_button = QPushButton(get_text("create"))

        self.cancel_button.clearFocus()
        self.valider_button.setFocus()

        self.cancel_button.clicked.connect(self.cancel_action)
        self.valider_button.clicked.connect(self.valider_action)

        self.layout.addWidget(self.lbl_line_edit)
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.project_name_lang)

        self.buttons_layout.addWidget(self.cancel_button)
        self.buttons_layout.addWidget(self.valider_button)
        self.layout.addLayout(self.buttons_layout)

        self.setLayout(self.layout)

        self.activateWindow()
        self.valider_button.setFocus()

    def cancel_action(self):
        """
        Fonction associée au bouton Cancel.
        """     
        self.cancel = True
        self.done(0)

    def valider_action(self):
        """
        Fonction associée au bouton Valider.
        """
        self.valider = True
        self.done(0)

    def get_project_name(self):
        """
        Fonction retournant le nom du projet.
        """
        return self.line_edit.text()

    def get_project_lang(self):
        """
        Fonction retournant le langage du projet.
        """
        return self.project_name_lang.currentText()  # .replace("é","e").lower()

    def keyPressEvent(self, event):
        """
        Fonction associée au bouton échap.
        """
        if event.key() == 16777216:
            self.cancel = True

        super().keyPressEvent(event)

def update_infos(parent,path,project_name,date,project_lang,nb_files):
    """
    Fonction permettant de mettre à jour les informations de projet.
    """
    write_xml(path,"name",project_name)
    write_xml(path,"creation_date",date)
    write_xml(path,"language",project_lang)
    write_xml(path,"number_files",nb_files)
    write_xml(path,"location",QDir(parent.workplace_path + project_name).path())
    write_xml(path,"compil"," ")
    write_xml(path,"compil_json"," ")

def update_nb_files(parent, path, project_name):
    """
    Fonction permettant de mettre à jour le nombre de fichiers d'un projet.
    """
    write_xml(path,"number_files", get_nb_files(parent, project_name))

def get_nb_files(parent,project_name):
    """
    Fonction permettant de récupérer le nombre de fichiers.
    """
    nb_files = 0
    project_path = QDir(parent.workplace_path + project_name).path()

    for e in os.listdir(project_path):
        if os.path.isfile(project_path+"/"+e) and e!="%s.xml" %(project_name) and e[0]!=".":
            nb_files+=1
        elif os.path.isdir(project_path+"/"+e) and e[0] != ".":
            nb_files += int(get_nb_files(parent, "%s/%s"%(project_name, e)))

    return str(nb_files)

def create_workplace():
    """
    Créée un répertoire vide qui va contenir les projets

    :rtype: None
    """
    workplace_path = open_xml("conf.xml")["current_workplace"]

    if not QDir(workplace_path).exists():
        QDir("/").mkpath(workplace_path)


def newproject(parent):
    """
    Fonction associée au bouton pour créer un nouveau projet.
    """
    np = NewProject()
    np.exec()
    project_name = np.get_project_name()
    project_lang = np.get_project_lang()
    cancel = np.cancel
    valider = np.valider

    while (project_name == '' or "/" in project_name) and not cancel and valider:
        QMessageBox.critical(parent, get_text("text_erreur"), get_text("proj_name_fail"))
        np = NewProject()
        np.exec()
        project_name = np.get_project_name()
        project_lang = np.get_project_lang()
        cancel = np.cancel
        valider = np.valider

    if not QDir(parent.workplace_path + project_name).exists() and not cancel:
        QDir(parent.workplace_path).mkpath(project_name)

        create_xml("%s/%s.xml" % (QDir(parent.workplace_path + project_name).path(), project_name))

        date = str(datetime.now())
        path = "%s/%s.xml" % (QDir(parent.workplace_path + project_name).path(), project_name)
        project_nb_files = get_nb_files(parent,project_name)

        update_infos(parent,path,project_name,date,project_lang,project_nb_files)
        project_location = parent.workplace_path + project_name
        add_projects_xml(project_name,project_lang,project_location,date,project_nb_files) 

    # elif parent.project_path[1]:
    elif not cancel and valider:
        QMessageBox.critical(parent, get_text("text_erreur"), get_text("proj_choose_other"))
        parent.new_project()


# def open_projects(parent):
#     projet = os.listdir(parent.workplace_path)
#     for e in projet:
#         check_file = QFileInfo(parent.workplace_path + e + "/.conf")
#         if not os.path.isdir(parent.workplace_path + e) or not check_file.exists() and not check_file.isFile():
#             projet.remove(e)

#     print(projet)

def delete_project_cache(parent, project_path):
    if project_path != "":
        project_name = project_path.split("/")[-1]
        for file in os.listdir("cache/"):
            if project_name in file.split("_"):
                os.remove("cache/%s" % file)
        parent.status_message(get_text("cleared_local_cache"))
    else:
        parent.status_message(get_text("text_please_open_project"))

def delete_global_cache(parent):
    for file in os.listdir("cache/"):
        os.remove("cache/%s" % file)
    parent.status_message(get_text("cleared_global_cache"))

def importproject(parent, chemin=False):
    """
    Fonction associée au bouton pour importer un projet.
    """
    workplace_path = parent.workplace_path

    if not chemin:
        chemin = QFileDialog.getExistingDirectory(parent, get_text("proj_import"), workplace_path)

    if chemin != "":
        project_name = chemin.split("/")[-1]

        if not os.path.exists(workplace_path+project_name):
            QDir(parent.workplace_path).mkpath(project_name)

            os.system("cp -r %s/ %s/"%(chemin.replace(" ", "\ "), workplace_path + project_name.replace(" ","\ ")))
        
        if not os.path.exists("%s%s/%s.xml"%(workplace_path, project_name, project_name)):

            date = str(datetime.now())

            project_lang = "Python"

            for e in os.listdir(chemin):
                if os.path.isfile("%s/%s"%(chemin,e)) and e[0] != ".":
                    ext = "*" + e.split(".")[-1]
                    for e in var.extension_by_language:
                        print(ext, var.extension_by_language[e])
                        if ext in var.extension_by_language[e] and e != "":
                            project_lang = e[0].upper() + e[1:]
                            break
                    # project_lang = var.supported_extensions.get(ext, "Python")

            create_xml("%s/%s.xml" % (QDir(workplace_path + project_name).path(), project_name))
            path = "%s/%s.xml" % (QDir(workplace_path + project_name).path(), project_name)
            project_nb_files = get_nb_files(parent,project_name)
            update_infos(parent,path,project_name,date,project_lang,project_nb_files)
            project_location = workplace_path + project_name
            add_projects_xml(project_name,project_lang,project_location,date,project_nb_files) 

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

        if os.path.exists("%s/%s.xml"%(parent.fenetre.project_path, parent.fenetre.project_path.split("/")[-1])):
            parent.fenetre.project_type = project_language("%s/%s.xml"%(parent.fenetre.project_path, parent.fenetre.project_path.split("/")[-1]))
        else:
            QMessageBox.critical(parent, get_text("invalid_project"), get_text("please_import"))
            return

        memory = Mem()

        gdf = ProgressOpening(ProgressWin, project_files, memory, parent)
        gdf.start()  # Processing of the opening project function
        disp_gdf = ProgressDisp(memory, parent)
        disp_gdf.start()  # Displays of the files studied
        parent.fenetre.show_img()
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

    def __init__(self, files, parent=False):
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
            if self.parent:
                self.parent.update_progress(i*incr)
                self.parent.update_text(get_text("proj_opening") + file_)

            fichier = open(file_, "r")
            data = fichier.read()
            fichier.close()
            lignes = lex.yaccing(file_.split(".")[-1], data, False)

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
                if len(tmp) > 0:
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
                if len(tmp) > 0:
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


# def closeproject(parent):
#     parent.tab_widget.clear()
#     parent.project_path = ""
#     parent.docs = []
#     parent.codes = []
#     parent.highlighters = []

class DeleteProject(QDialog):
    def __init__(self, parent):
        """
        Fonction permettant d'afficher la fenêtre pour supprimer un projet.
        """
        super().__init__()

        self.parent = parent

        self.valider = False

        self.setWindowTitle(get_text("select_delete_project"))

        self.layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()

        self.project_name = QComboBox()
        for e in os.listdir(parent.workplace_path):
            if e != ".DS_Store" and e != ".conf":
                self.project_name.addItem(e)

        self.cancel_button = QPushButton(get_text("cancel"))
        self.valider_button = QPushButton(get_text("delete"))

        self.cancel_button.clicked.connect(self.cancel_action)
        self.valider_button.clicked.connect(self.valider_action)

        self.layout.addWidget(self.project_name)

        self.buttons_layout.addWidget(self.cancel_button)
        self.buttons_layout.addWidget(self.valider_button)
        self.layout.addLayout(self.buttons_layout)

        self.setLayout(self.layout)

        self.activateWindow()
        self.valider_button.setFocus()

    def cancel_action(self):
        """
        Fonction associée au bouton Cancel.
        """
        self.cancel = True
        self.done(0)

    def valider_action(self):
        """
        Fonction associée au bouton Valider.
        """
        self.valider = True
        self.done(0)

    def get_project(self):
        """
        Fonction permettant de récupérer le nom du projet.
        """
        return self.project_name.currentText()#.replace("é","e").lower()

    def keyPressEvent(self, event):
        """
        Fonction associée au bouton échap.
        """
        if event.key() == 16777216:
            self.cancel = True

        super().keyPressEvent(event)

def deleteproject(parent,chemin=False):
    """
    Fonction associée au bouton de suppresion de projet.
    """
    if not chemin:
        dp = DeleteProject(parent)
        dp.exec()
        project_name = dp.get_project()
        valider = dp.valider

        if QDir(parent.workplace_path + project_name).exists() and valider:
            shutil.rmtree(parent.workplace_path + project_name)
        
    else:
        shutil.rmtree(chemin)


class InfosProject(QDialog):
    def __init__(self, parent):
        """
        Fonction permettant l'affichage de la fenêtre des informations de projet.
        """
        super().__init__()

        self.parent = parent

        self.valider = False
        self.cancel = False
        self.modification = False
        self.appliquer = False

        self.setWindowTitle(get_text("select_infos_project"))

        self.layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()

        self.name = QLabel("")
        self.creation_date = QLabel("")
        self.language = QLabel("")
        self.location = QLabel("")
        self.number_files = QLabel("")

        self.project_name = QComboBox()
        for e in os.listdir(self.parent.workplace_path):
            if e != ".DS_Store" and e != ".conf":
                self.project_name.addItem(e)

        self.cancel_button = QPushButton(get_text("cancel"))
        self.valider_button = QPushButton(get_text("select"))
        self.modification_button = QPushButton(get_text("modify"))
        self.appliquer_button = QPushButton(get_text("apply"))

        self.cancel_button.clicked.connect(self.cancel_action)
        self.valider_button.clicked.connect(self.valider_action)
        self.modification_button.clicked.connect(self.modification_action)
        self.appliquer_button.clicked.connect(self.appliquer_action)

        self.layout.addWidget(self.project_name)

        self.buttons_layout.addWidget(self.cancel_button)
        self.buttons_layout.addWidget(self.valider_button)
        self.layout.addLayout(self.buttons_layout)

        self.setLayout(self.layout)

        self.activateWindow()
        self.valider_button.setFocus()

    def cancel_action(self):
        """
        Fonction associée au bouton Cancel.
        """
        self.cancel = True
        self.done(0)

    def valider_action(self):
        """
        Fonction associée au bouton Valider.
        """
        self.valider = True
        self.done(0)

    def modification_action(self):
        """
        Fonction associée au bouton Modifier.
        """
        self.modification = True
        self.done(0)

    def appliquer_action(self):
        """
        Fonction associée au bouton Appliquer.
        """
        self.appliquer = True
        self.done(0)

    def get_project(self):
        """
        Fonction permettant de récupérer le nom du projet.
        """
        return self.project_name.currentText()#.replace("é","e").lower()

    def get_project_name(self):
        """
        Fonction permettant de récupérer le nom du projet.
        """
        return self.name.text()

    def get_project_lang(self):
        """
        Fonction permettant de récupérer le langage du projet.
        """
        return self.language.currentText()#.replace("é","e").lower()

    def keyPressEvent(self, event):
        """
        Fonction associée au boutoné échap.
        """
        if event.key() == 16777216:
            self.cancel = True

        super().keyPressEvent(event)

class InfoProject(QDialog):
    def __init__(self, parent,chemin):
        """
        Fonction permettant l'affichage de la fenêtre des informations de projet dans le menu clic droit du navigateur de projets.
        """
        super().__init__()

        self.parent = parent
        self.setWindowTitle(get_text("info_project"))

        self.layout = QVBoxLayout()

        project_name = chemin.split("/")[-1]
        path = "%s/%s.xml"%(chemin, project_name)
        update_nb_files(parent, path, project_name)
        project = open_xml(path)
        self.name = QLabel(get_text("project_name") + project["name"])
        self.language = QLabel(get_text("project_language") + project["language"])
        self.location = QLabel(get_text("project_location") + chemin)
        self.creation_date = QLabel(get_text("project_creation_date") + project["creation_date"])
        self.number_files = QLabel(get_text("project_number_files") + project["number_files"])

        self.layout.addWidget(self.name)
        self.layout.addWidget(self.language)
        self.layout.addWidget(self.location)
        self.layout.addWidget(self.creation_date)  
        self.layout.addWidget(self.number_files)

        self.setLayout(self.layout)

        self.activateWindow()

        def get_project(self):
            """
            Fonction permettant de récupérer le nom du projet.
            """
            return self.project_name.currentText()#.replace("é","e").lower()

        def get_project_name(self):
            """
            Fonction permettant de récupérer le nom du projet.
            """
            return self.name.text()

        def get_project_lang(self):
            """
            Fonction permettant de récupérer le langage du projet.
            """
            return self.language.currentText()#.replace("é","e").lower()

        def keyPressEvent(self, event):
            """
            Fonction associée au bouton échap.
            """
            if event.key() == 16777216:
                self.done(0)
            super().keyPressEvent(event)

def infosproject(parent):
    """
    Fonction associée au bouton des informations de projet.
    """
    ip = InfosProject(parent)
    ip.exec()
    project = {}
    project_name = ip.get_project()
    valider = ip.valider
    cancel = ip.cancel
    modification = ip.modification
    appliquer = ip.appliquer

    while valider and not cancel and not modification and not appliquer and QDir(parent.workplace_path + project_name).exists():
        valider = ip.valider
        cancel = ip.cancel
        modification = ip.modification
        appliquer = ip.appliquer
        ip.setWindowTitle(get_text("info_project"))
        project_name = ip.get_project() 
        path = "%s/%s.xml" % (QDir(parent.workplace_path + project_name).path(), project_name)
        update_nb_files(parent, path, project_name)
        project = open_xml(path)
        ip.name.setParent(None)
        ip.name = QLabel(get_text("project_name") + project["name"])
        ip.layout.addWidget(ip.name)
        ip.language.setParent(None)
        ip.language = QLabel(get_text("project_language") + project["language"])
        ip.layout.addWidget(ip.language)
        ip.location.setParent(None)
        ip.location = QLabel(get_text("project_location") + QDir(parent.workplace_path + project_name).path())
        ip.layout.addWidget(ip.location)
        ip.creation_date.setParent(None)
        ip.creation_date = QLabel(get_text("project_creation_date") + project["creation_date"])
        ip.layout.addWidget(ip.creation_date)
        ip.number_files.setParent(None)
        ip.number_files = QLabel(get_text("project_number_files") + project["number_files"])
        ip.layout.addWidget(ip.number_files)
        ip.buttons_layout.addWidget(ip.modification_button)
        if not cancel and not modification and not appliquer:
            ip.exec()

    if modification and not cancel:
        ip.setWindowTitle(get_text("info_modify_project"))
        ip.name.setParent(None)
        ip.name = QLineEdit()
        ip.name.setPlaceholderText(project["name"])
        ip.layout.addWidget(ip.name)
        ip.language.setParent(None)
        ip.language = QComboBox()

        languages = ["Python", "Arithmétique", "C"]

        languages.remove(project["language"])
        ip.language.addItem(project["language"])
        for language in languages:
            ip.language.addItem(language)
            
        ip.layout.addWidget(ip.language)
        ip.location.setParent(None)
        ip.location = QLabel(get_text("project_location") + QDir(parent.workplace_path + project_name).path())
        ip.layout.addWidget(ip.location)
        ip.creation_date.setParent(None)
        ip.creation_date = QLabel(get_text("project_creation_date") + project["creation_date"])
        ip.layout.addWidget(ip.creation_date)
        ip.number_files.setParent(None)
        ip.number_files = QLabel(get_text("project_number_files") + project["number_files"])
        ip.layout.addWidget(ip.number_files)
        ip.modification_button.setParent(None)
        ip.buttons_layout.addWidget(ip.appliquer_button)
        ip.activateWindow()
        ip.appliquer_button.setFocus()
        ip.exec()

    if not appliquer and not cancel and project != {}:
        if ip.get_project_name() == "":
            project_name = project["name"]
        else:
            project_name = ip.get_project_name()
        os.rename(QDir(parent.workplace_path + project["name"]).path(), QDir(parent.workplace_path + project_name).path())
        os.rename("%s/%s.xml" % (QDir(parent.workplace_path + project_name).path(), project["name"]), "%s/%s.xml" % (QDir(parent.workplace_path + project_name).path(), project_name))
        path = "%s/%s.xml" % (QDir(parent.workplace_path + project_name).path(), project_name)
        project = open_xml(path)
        update_infos(parent,path,project_name,project["creation_date"],ip.get_project_lang(),project["number_files"])  

def infoproject(parent, chemin):
    """
    Fonction associée au bouton du menu clic droit des informations de projet du navigateur.
    """
    ip = InfoProject(parent, chemin)
    ip.exec()
    