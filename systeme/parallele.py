from threading import *
import os
import sys

from lexer import yaccing
from time import sleep


class SayMessage(Thread):
    def __init__(self, message):
        """
        Assistance vocale

        :param message:
        :return:
        """
        Thread.__init__(self, name="Message")
        self.message = message

    def run(self):
        os.system("say " + self.message)


class Yaccer(Thread):
    def __init__(self, parent):
        """
        Yacc processing

        :param parent:
        :return:
        """
        Thread.__init__(self, name="Yacc")
        self.parent = parent

    def run(self):
        self.last_yacc_errors = self.parent.yacc_errors
        self.parent.yacc_errors = yaccing(self.parent.toPlainText())

        if self.last_yacc_errors != self.parent.yacc_errors:
            idx = self.parent.parent.get_idx()
            self.parent.parent.highlighters[idx].rehighlight()


class ProgressOpening(Thread):
    def __init__(self, obj, liste_files, memory, parent):
        Thread.__init__(self, name="Project")
        self.obj = obj
        self.parent = parent
        self.memo = memory
        self.liste_files = liste_files

    def run(self):
        self.obj(self.liste_files, self.memo)
        self.parent.function_declarations.emit(self.memo.res)


class ProgressDisp(Thread):
    def __init__(self, memo, parent):
        Thread.__init__(self, name="Disp")
        self.memo = memo
        self.parent = parent

    def run(self):
        """
        Actualisation de la progression lors de l'ouverture d'un projet
        """
        prev = ""
        prev_val = 0
        while self.memo.res is None:
            if self.memo.message != prev: #and self.parent.empty_status_message():
                #self.parent.fenetre.status_message(self.memo.message, -1, False)
                self.parent.fenetre.sig_message.emit(self.memo.message)
                prev = self.memo.message

            if self.memo.progress != prev_val:
                #self.parent.fenetre.progress_bar.setValue(self.memo.progress)
                self.parent.fenetre.sig_progress.emit(self.memo.progress)
                prev_val = self.memo.progress

            sleep(0.01)
        self.parent.fenetre.sig_progress_termine.emit(True)

class LinesActualise(Thread):
    def __init__(self, parent, nb_lignes, animate):
        Thread.__init__(self, name="Lines")

        self.n = nb_lignes
        self.parent = parent
        self.animate = animate

    def run(self):
        """
        Actualisation du nombre de lignes dans la zone de numérotation des lignes
        :return:
        """
        for i in range(1, self.n+1):
            self.parent.sig_update_lines.emit(i)
            if self.animate:
                sleep(0.01)
        self.parent.sig_update_lines_termine.emit(True)
