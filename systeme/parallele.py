from threading import *
from lexer import yaccing
import os

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


class DefautInfo(Thread):
    def __init__(self, parent):
        """
        Default information of the infobar

        :param parent:
        :return:
        """
        Thread.__init__(self, name="Defaut info")
        self.parent = parent

    def run(self):
        idx = self.parent.tab_widget.currentIndex()
        if idx in range(len(self.parent.docs)):
            nblignes = self.parent.docs[idx].get_nb_lignes()
            self.parent.infobar.showMessage(str(nblignes) + " lignes")


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
