import os, xml, json
from PySide.QtGui import *

from subprocess import Popen, PIPE
from language.language import get_text

class LineEditPath(QLineEdit):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def mousePressEvent(self, event):
        self.open_selection_window()

    def keyPressEvent(self, event):
        return False

    def open_selection_window(self):
        nom_fichier, filtre = QFileDialog.getOpenFileName(self, get_text("open"), self.parent.project_path)
        self.setText(nom_fichier)

class LineEditPathDirectory(QLineEdit):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def mousePressEvent(self, event):
        self.open_selection_window()

    def keyPressEvent(self, event):
        return False

    def open_selection_window(self):
        nom_fichier = QFileDialog.getExistingDirectory(self, get_text("open"), self.parent.project_path)
        self.setText(nom_fichier)


class GroupBoxOptions(QGroupBox):

    def __init__(self):
        super().__init__(get_text("comp_opt"))

        self.options = []
        layout = QGridLayout()

        pipe_option = QCheckBox("-pipe")
        layout.addWidget(pipe_option, 0, 0)
        self.options += [pipe_option]

        pas_lien_option = QCheckBox("-c")
        layout.addWidget(pas_lien_option, 0, 1)
        self.options += [pas_lien_option]

        supp_avert_option = QCheckBox("-w")
        layout.addWidget(supp_avert_option, 0, 2)
        self.options += [supp_avert_option]

        W_option = QCheckBox("-W")
        layout.addWidget(W_option, 0, 3)
        self.options += [W_option]

        Wall_option = QCheckBox("-Wall")
        layout.addWidget(Wall_option, 1, 0)
        self.options += [Wall_option]

        Werror_option = QCheckBox("-Werror")
        layout.addWidget(Werror_option, 1, 1)
        self.options += [Werror_option]

        verbose_option = QCheckBox("-v")
        layout.addWidget(verbose_option, 1, 2)
        self.options += [verbose_option]

        self.setLayout(layout)

    def get_options(self):
        return self.options

class ConfigCompilC(QDialog):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.est_valide = False
        self.informations = []

        self.setWindowTitle(get_text("comp_config"))

        layout = QGridLayout()

        lbl_titre = QLabel(get_text("comp_config"))
        layout.addWidget(lbl_titre, 0, 0, 1, 2)

        # Gestion des fichiers à compiler
        lbl_fichiers_compiler = QLabel(get_text("comp_files"))
        layout.addWidget(lbl_fichiers_compiler, 1, 0)

        self.lineEdit_fichiers_compiler = LineEditPath(self.parent)
        layout.addWidget(self.lineEdit_fichiers_compiler, 1, 1)
        self.informations += [self.lineEdit_fichiers_compiler]

        # Gestion de l'emplacement des headers
        lbl_fichier_header = QLabel(get_text("comp_headers"))
        layout.addWidget(lbl_fichier_header, 2, 0)

        self.lineEdit_fichier_header = LineEditPathDirectory(self.parent)
        layout.addWidget(self.lineEdit_fichier_header, 2, 1)
        self.informations += [self.lineEdit_fichier_header]

        # Gestion de l'emplacement des librairies
        lbl_emplacement_librairie = QLabel(get_text("comp_lib"))
        layout.addWidget(lbl_emplacement_librairie, 3, 0)

        self.lineEdit_emplacement_librairie = LineEditPathDirectory(self.parent)
        layout.addWidget(self.lineEdit_emplacement_librairie, 3, 1)
        self.informations += [self.lineEdit_emplacement_librairie]

        # Gestion de l'emplacement des librairies
        lbl_nom_librairie = QLabel(get_text("comp_lib_name"))
        layout.addWidget(lbl_nom_librairie, 4, 0)

        self.lineEdit_nom_librairie = QLineEdit()
        layout.addWidget(self.lineEdit_nom_librairie, 4, 1)
        self.informations += [self.lineEdit_nom_librairie]

        # Gestion du nom du fichier de sortie
        lbl_fichier_sortie = QLabel(get_text("comp_out"))
        layout.addWidget(lbl_fichier_sortie, 5, 0)

        self.lineEdit_fichier_sortie = QLineEdit()
        layout.addWidget(self.lineEdit_fichier_sortie, 5, 1)
        self.informations += [self.lineEdit_fichier_sortie]

        # Gestion des options de compilation
        self.group_options = GroupBoxOptions()
        layout.addWidget(self.group_options, 6, 0, 1, 2)
        self.informations += self.group_options.get_options()

        # Gestion de l'execution au lancement
        self.checkBox_launch = QCheckBox(get_text("lanch_comp"))
        layout.addWidget(self.checkBox_launch, 7, 0, 1, 2)
        self.informations += [self.checkBox_launch]

        btn_valider = QPushButton(get_text("comp_run"))
        btn_valider.clicked.connect(self.valider)
        layout.addWidget(btn_valider, 8, 0, 1, 2)

        self.setLayout(layout)

    def valider(self):

        if self.est_configuration_valide():
            self.est_valide = True
            self.done(0)
        else:
            QMessageBox.critical(self, get_text("text_erreur"), get_text("comp_enter_good"))

    def est_configuration_valide(self):
        return self.lineEdit_fichiers_compiler.text().strip() != "" and len(self.lineEdit_fichier_sortie.text().split()) <= 1 and len(self.lineEdit_fichier_header.text().split()) <= 1 and len(self.lineEdit_emplacement_librairie.text().split()) <= 1 and len(self.lineEdit_nom_librairie.text().split()) <= 1

    def get_configuration_json(self):

        res = []

        for e in self.informations: 
            if isinstance(e, QLineEdit):
                res += [e.text()]
            else:
                res += [e.isChecked()]

        return json.dumps(res)

    def get_configuration_string(self):

        fichiers_compiler = self.lineEdit_fichiers_compiler.text()

        fichier_header = ""
        le_fichier_header = self.lineEdit_fichier_header.text()
        if le_fichier_header.strip() != "":
            fichier_header = "-I %s"%le_fichier_header

        fichier_sortie = ""
        le_fichier_sortie = self.lineEdit_fichier_sortie.text()
        if le_fichier_sortie.strip() != "":
            fichier_sortie = "-o %s"%le_fichier_sortie

        emplacement_librairie = ""
        le_emplacement_librarie = self.lineEdit_emplacement_librairie.text()
        if le_emplacement_librarie.strip() != "":
            emplacement_librairie = "-L %s"%le_emplacement_librarie

        nom_librairie = ""
        le_nom_librarie = self.lineEdit_nom_librairie.text()
        if le_nom_librarie.strip() != "":
            nom_librairie = "-l%s"%le_nom_librarie
 
        options = ""
        for e in self.group_options.get_options():
            if e.isChecked():
                options += "%s "%e.text()

        return "gcc %s %s %s %s %s %s"%(fichiers_compiler, fichier_header, emplacement_librairie, nom_librairie, options,fichier_sortie)

    def setConfig(self, config_json):
        config_json = json.loads(config_json)
        for i,e in enumerate(self.informations):
            if isinstance(e, QLineEdit):
                e.setText(config_json[i])
            else:
                e.setChecked(config_json[i])


class ConfigInterpPython(QDialog):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.est_valide = False
        self.informations = []

        self.setWindowTitle(get_text("comp_config_python"))

        layout = QGridLayout()

        lbl_titre = QLabel(get_text("comp_config_python"))
        layout.addWidget(lbl_titre, 0, 0, 1, 2)

        lbl_emplacement_interpreteur = QLabel(get_text("comp_py_loca"))
        layout.addWidget(lbl_emplacement_interpreteur, 1, 0)

        self.lineEdit_emplacement_interpreteur = LineEditPath(self.parent)
        layout.addWidget(self.lineEdit_emplacement_interpreteur, 1, 1)
        self.informations += [self.lineEdit_emplacement_interpreteur]

        lbl_emplacement_depart = QLabel(get_text("comp_file_py"))
        layout.addWidget(lbl_emplacement_depart, 2, 0)

        self.lineEdit_fichier_depart = LineEditPath(self.parent)
        layout.addWidget(self.lineEdit_fichier_depart, 2, 1)
        self.informations += [self.lineEdit_fichier_depart]

        btn_valider = QPushButton(get_text("comp_run"))
        btn_valider.clicked.connect(self.valider)
        layout.addWidget(btn_valider, 3, 0, 1, 2)

        self.setLayout(layout)

    def valider(self):
        if self.est_configuration_valide():
            self.est_valide = True
            self.done(0)
        else:
            QMessageBox.critical(self, get_text("text_erreur"), get_text("comp_enter_good"))

    def est_configuration_valide(self):
        return self.lineEdit_emplacement_interpreteur.text().strip() != "" and self.lineEdit_fichier_depart.text().strip() != "" and self.parent.project_path in self.lineEdit_fichier_depart.text()

    def get_configuration_json(self):
        res = []
        for e in self.informations:
            res += [e.text()]

        return json.dumps(res)

    def get_configuration_string(self):
        return "%s %s"%(self.lineEdit_emplacement_interpreteur.text(), self.lineEdit_fichier_depart.text())

    def setConfig(self, config_json):
        config_json = json.loads(config_json)
        for i,e in enumerate(self.informations):
            e.setText(config_json[i])

class DialogErreurs(QDialog):

    def __init__(self, erreurs):
        super().__init__()

        self.erreurs = erreurs

        self.layout = QVBoxLayout()

        self.comboBox = QComboBox()
        for i in range(len(self.erreurs)):
            self.comboBox.addItem("Erreur n° %s"%(i+1))
        self.comboBox.currentIndexChanged.connect(self.changeErreur)

        self.affiche_erreurs = QTextEdit()
        self.affiche_erreurs.setPlainText(self.erreurs[0])
        self.affiche_erreurs.readOnly = True

        self.layout.addWidget(self.comboBox)
        self.layout.addWidget(self.affiche_erreurs)

        self.setLayout(self.layout)

    def changeErreur(self):
        idx = self.comboBox.currentIndex()
        self.affiche_erreurs.setPlainText(self.erreurs[idx])

def get_erreurs(lines, project_path):

    erreurs = lines.split("%s/"%project_path)[1:]
    erreurs[-1] = "\n".join(erreurs[-1].split("\n")[:-2])
    erreurs = ["\n".join(e.split("\n")[:2]) for e in erreurs]
    return erreurs

def afficher_erreurs(parent, erreurs):
    lines = parent.nb_lignes

    for e in erreurs:
        splite = e.split(":")
        if len(splite) >= 5:
            lines.colorate_line(splite[0], int(splite[1]))

def compiler(parent):

    xml_path = "%s/%s.xml"%(parent.project_path, parent.project_path.split("/")[-1])

    configuration = xml.project_compil(xml_path)

    if configuration == "":
        configuration_compilation(parent)
        configuration = xml.project_compil(xml_path)
        if configuration == "":
            return False

    curt = os.getcwd()
    os.chdir(parent.project_path)
    out, res = Popen(configuration, shell=True, stdout=PIPE, stderr=PIPE).communicate()
    out, res = out.decode("utf-8"), res.decode("utf-8")
    os.chdir(curt)

    if parent.project_type == "c":
        if res != "":
            erreurs = get_erreurs(res, parent.project_path)
            afficher_erreurs(parent, erreurs)

            dialogErreur = DialogErreurs(erreurs)
            dialogErreur.exec()
        else:
            QMessageBox.about(parent, get_text("comp_res"), get_text("comp_ok"))
            config_json = json.loads(xml.project_compil_json(xml_path))
            if config_json[-1]: # lancer après la compilation ?
                name = "a.out" if config_json[4] == "" else config_json[4] # Nom du fichier
                os.system("%s/%s"%(parent.project_path, name))

    else:
        print("##### Debut du script python #####")
        print(out)
        print("##### Fin du script python #####")

def configuration_compilation(parent):

    xml_path = "%s/%s.xml"%(parent.project_path, parent.project_path.split("/")[-1])

    if parent.project_type == "c":
        config = ConfigCompilC(parent)
    else:
        config = ConfigInterpPython(parent)

    config_json = xml.project_compil_json(xml_path)
    if config_json != "":
        config.setConfig(config_json)

    config.exec()

    if config.est_valide:
        configuration = config.get_configuration_string()
        xml.compil_xml(xml_path, configuration)

        configuration_json = config.get_configuration_json()
        xml.compil_json_xml(xml_path, configuration_json)
