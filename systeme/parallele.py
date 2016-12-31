from threading import *
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
        nblignes = self.parent.docs[self.parent.tab_widget.currentIndex()].get_nb_lignes()
        self.parent.infobar.showMessage(str(nblignes) + " lignes")
