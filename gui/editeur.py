import sys
import os
import json
from PySide.QtGui import *
from PySide.QtCore import *

import lexer.lexer as lex
import themes.themes as themes
import gui.bouton as b
from systeme import workplace

sys.path[:0] = ["../"]
sys.path[:0] = ["gui"]

class LignesAndTab(QWidget):
    values = {True: "Anim.", False: "Inst."}

    def __init__(self, parent, lignes):
        """
        Contient le bouton d'annimation de l'affichage des lignes ainsi que la zone de numérotation des lignes.
        """
        QWidget.__init__(self)
        self.parent = parent

        self.anim = b.Bouton("Inst.", self.change_anim, 25)
        self.anim.setFixedWidth(60)

        lv = QVBoxLayout()
        lv.setContentsMargins(0, 0, 0, 0)

        lv.addWidget(self.anim)
        lv.addWidget(lignes)

        self.setLayout(lv)

    def change_anim(self):
        self.parent.anim_line = not self.parent.anim_line
        self.anim.setText(self.values[self.parent.anim_line])


class Lignes(QTextEdit):
    def __init__(self, master, police, taille_texte):
        """
        Liste de numérotation des lignes. On utilise un QTextEdit.
        Chaque élément de la liste correspond à une ligne.
        """
        QTextEdit.__init__(self)

        self.master = master

        self.police = police
        self.taille_texte = taille_texte
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setReadOnly(True)

        self.maj_style()

        self.setFixedWidth(50)

    def go_top(self):
        """
        Replace la numérotation des lignes tout en haut
        """
        if self.master.aller_en_haut_lignes:
            self.scrollToAnchor("1")
            self.master.aller_en_haut_lignes = False

    def maj_style(self):
        """
        Met à jour le style de la zone de numérotation des lignes
        """
        c = themes.get_color_from_theme("textedit")

        self.setStyleSheet("QTextEdit{ background-color:" + themes.get_rgb(c["text-back-color"]) + ";"
                           + "font-family:" + self.police + ";"
                           + "color:" + themes.get_rgb(c["text-color"]) + ";"
                           + "font-size:" + str(self.taille_texte) + "pt; }")

    def wheelEvent(self, e, syncr=False):
        """
        Évenement appelé lors du scroll via la souris

        :param e: evenemnt
        :type e: object
        """
        QTextEdit.wheelEvent(self, e)
        if not syncr:
            self.master.codes[self.master.get_idx()].wheelEvent(e, True)

    def enterEvent(self, event):
        """
        Evenement lors ce qu'on survole la numérotation des lignes
        Ici on change le curseur en normal.
        """
        self.viewport().setCursor(Qt.ArrowCursor)

class Editeur(QTextEdit):

    tabPress = Signal()

    def __init__(self, police, taille_texte, def_functions, keywords, parent):
        """
        Hérite de QTextEdit.
        C'est une zone de texte dans laquelle on peut écrire, que l'on utilise ici pour écrire du code.

        Ici, on modifie ses paramètres en fonction du thème souhaité.
        :param police: Police d'écriture
        :type police: str
        :param couleur_fond: Couleur d'arrière plan de l'éditeur (background)
        :type couleur_fond: str
        :param couleur_texte: Couleur du texte de base
        :type couleur_texte: str
        :param taille_texte: Taille de la police (en points)
        :type taille_texte: int
        :rtype: None
        """
        super().__init__()

        self.parent = parent
        self.police = police
        self.taille_texte = taille_texte
        self.def_functions = def_functions
        self.keywords = keywords
        self.snippets = self.get_snippets()

        self.setTabStopWidth(20)
        self.setLineWrapMode(QTextEdit.NoWrap)

        self.yacc_errors = []
        self.last_yacc_errors = []

        self.maj_style()
        self.setFocus()

        # self.append("int main ( int argc, char** argv ){\n\n\treturn 0;\n\n}")

    def get_snippets(self):
        """
        Récupère les snippets : prédéfinitions de fonctions.
        :rtype: list
        """
        try:
            fichier = open("snippets/%s.json"%self.parent.project_type, "r")
            res = json.loads(fichier.read())
            fichier.close()
        except BaseException as e:
            res = []


        return res

    def analyse(self):
        """ Cette fonction est liée au bouton Analyse si il y a au moins un éditeur d'ouvert. """
        idx = self.parent.get_idx()
        file_type = self.parent.docs[idx].extension
        file_path = self.parent.docs[idx].chemin_enregistrement

        self.parent.defaut_info_message()  # Actualisation des infos de base

        # process_yacc = Yaccer(self)  # Module parallele --> Sur un Thread
        # process_yacc.start()

        self.last_yacc_errors = self.yacc_errors
        self.yacc_errors, self.parent.def_functions = lex.yaccing(file_type, self.toPlainText())

        def_fonctions = workplace.GetDefFonctions([file_path])
        def_fonctions.resultat.connect(self.set_def_fonctions)
        def_fonctions.run()

        if self.last_yacc_errors != self.yacc_errors:
            self.parent.highlighters[idx].rehighlight()

    def set_def_fonctions(self, declarators):
        idx = self.parent.get_idx()
        file_path = self.parent.docs[idx].chemin_enregistrement

        if declarators != (None, None, None):
            if file_path in declarators[0]:
                self.parent.def_functions[file_path] = declarators[0][file_path]

            if file_path in declarators[1]:
                self.parent.def_structs[file_path] = declarators[1][file_path]

            if file_path in declarators[2]:
                self.parent.def_vars[file_path] = declarators[2][file_path]


    def auto_align(self):
        idx = self.parent.get_idx()
        lang = self.parent.docs[idx].extension

        textCursor = self.textCursor()
        textCursor.movePosition(QTextCursor.Up)
        textCursor.select(QTextCursor.LineUnderCursor)
        text = textCursor.selectedText()
        if text != "":
            nb_tab = self.get_current_tab()

            if lang == "py" and text[-1] == ":":
                nb_tab += 1
            elif lang == "c":
                if text.strip()[-1] == "{":
                    nb_tab += 1
            textCursor.movePosition(QTextCursor.Down)
            textCursor.insertText("\t"*nb_tab)
            self.setTextCursor(textCursor)



    def get_current_tab(self):
        textCursor = self.textCursor()
        textCursor.movePosition(QTextCursor.Up)
        textCursor.select(QTextCursor.LineUnderCursor)
        text = textCursor.selectedText()

        nb = 0
        while nb < len(text) and text[nb] == "\t":
            nb+=1
        return nb    


    def keyPressEvent(self, event):
        # self.parent.defaut_info_message()  # Actualisation des infos de base dès que l'on tape sur une touche
        """
        if event.key() == 16777220:  # enter key

            # process_yacc = Yaccer(self)  # Module parallele --> Sur un Thread
            # process_yacc.start()

            self.last_yacc_errors = self.yacc_errors
            self.yacc_errors = yaccing(self.toPlainText())

            if self.last_yacc_errors != self.yacc_errors:
                idx = self.parent.get_idx()
                self.parent.highlighters[idx].rehighlight()
        """

        if event.key() == 16777217:  # tab key

            if self.use_snippets(): return True

        if ("darwin" in sys.platform and event.nativeModifiers() == 4096) or \
                (not "darwin" in sys.platform and event.key() == 32 and event.nativeModifiers() == 514):
            self.tabPress.emit()
            return False

        super().keyPressEvent(event)

        if event.key() == 16777220: # enter key
            self.auto_align()



    def wheelEvent(self, e, syncr=False):
        """
        Évenement appelé lors du scroll via la souris

        On rappelle ici la même fonction sur l'objet pour afficher les lignes afin de les syncroniser.

        :param e: evenemnt
        :type e: object
        """
        QTextEdit.wheelEvent(self, e)
        if not syncr:
            self.parent.nb_lignes.wheelEvent(e, True)

    def use_snippets(self):
        """
        Lorsque l'on presse "TAB" et que l'on définit une fonction ou une structure ou encore une boucle, on
        complète automatiquement la suite avec une liste prédéfinie de le fichier snippets.json.
        """
        textCursor = self.textCursor()
        textCursor.select(QTextCursor.WordUnderCursor)
        word = textCursor.selectedText()
        if word in self.snippets:
            infos = self.snippets[word]
            textCursor.removeSelectedText()
            textCursor.insertText(infos[0])

            self.parent.indent()

            for i in range(infos[1]):
                self.moveCursor(QTextCursor.Up)

            for i in range(infos[2]):
                self.moveCursor(QTextCursor.Right)

            textCursor = self.textCursor()
            textCursor.select(QTextCursor.WordUnderCursor)
            self.setTextCursor(textCursor)

            return True

    def maj_style(self):
        """
        Met à jour le style de la zone de code.
        """
        c = themes.get_color_from_theme("textedit")

        self.setStyleSheet("QTextEdit { background-color:" + themes.get_rgb(c["text-back-color"]) + ";"
                           + "font-family:" + self.police + ";"
                           + "color:" + themes.get_rgb(c["text-color"]) + ";"
                           + "font-size:" + str(self.taille_texte) + "pt; }")

    def show_nb_prop(self, nb_prop):
        """
        Afficje le nombre de propositions de complétions dans l'infoBar
        """
        if nb_prop != 0:
            self.parent.info_message(str(nb_prop) + " proposition%s" % ("s" * (nb_prop != 1)))
        else:
            self.parent.defaut_info_message()

    def select_current_line(self):
        """
        Sélectionne la ligne sous le curseur
        """
        textCursor = self.textCursor()
        textCursor.select(QTextCursor.LineUnderCursor)

        self.setTextCursor(textCursor)

    def select_current_word(self):
        """
        Sélectionne le mot sous le curseur
        """
        textCursor = self.textCursor()
        textCursor.select(QTextCursor.WordUnderCursor)

        self.setTextCursor(textCursor)

    def duplicate(self):
        """
        Duplique la zone sélectionnée
        """
        textCursor = self.textCursor()
        return_ = ""

        if textCursor.selectedText() == "":
            textCursor.select(QTextCursor.LineUnderCursor)
            return_ = "\n"

        textCursor.insertText(textCursor.selectedText() + return_ + textCursor.selectedText())

    def comment_selection(self):
        """
        Commente la zone sélectionnée ou la ligne sous le curseur si rien n'est sélectionné.
        """
        textCursor = self.textCursor()

        if textCursor.selectedText() == "":
            textCursor.select(QTextCursor.LineUnderCursor)

        text = textCursor.selectedText()
        textCursor.removeSelectedText()

        lines = text.split("\u2029") # \u2029 -> \n

        is_commented = self.check_comment(lines)

        for i in range(len(lines)):
            if lines[i].strip() != "":
                if is_commented:
                    lines[i] = lines[i][2:]
                else:
                    lines[i] = "//" + lines[i]

        textCursor.insertText("\n".join(lines))

    def check_comment(self, lines):
        """
        Vérifie si une zone est commentée
        :rtype: bool
        """
        for line in lines:
            if line[:2] != "//" and line.strip() != "":
                return False
        return True

    def get_lines_functions(self):

        res = []

        idx = self.parent.get_idx()
        doc = self.parent.docs[idx]

        if doc.chemin_enregistrement in self.def_functions:
            def_functions = self.def_functions[doc.chemin_enregistrement]

            for def_function in def_functions:
                res += [def_function[-1]-1]

        return res

    def get_blocks(self):

        res = []

        lines_numbers = self.get_lines_functions()
        lines = self.toPlainText().split("\n")

        for i in lines_numbers:
            nb_acc = 0
            first_acc = False
            end = i
            while nb_acc != 0 or not first_acc:

                if "}" in lines[end]:
                    nb_acc -= 1
                if "{" in lines[end]:
                    nb_acc+=1
                    first_acc = True
                end += 1

            res += [(i, end-1)]

        return sorted(res)

    def highlight_by_block(self):

        self.setPlainText(self.toPlainText())

        # if len(self.toPlainText().split("\n")) > 50:
        #     blocks = self.get_blocks()

        #     if blocks != []:
        #         highlighter = self.parent.highlighters[self.parent.get_idx()]
        #         doc = self.document()
        #         number_of_block = doc.blockCount()

        #         for i in range(blocks[0][-1]+1):
        #             highlighter.rehighlightBlock(doc.findBlockByNumber(i))

        # else:
        #     self.setPlainText(self.toPlainText())

        # for i in range(min(80, number_of_block)):
        #     highlighter.rehighlightBlock(doc.findBlockByNumber(i)) 

