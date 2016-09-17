# Class relative à la gestion du navigateur permetant la prévisualisation du code HTML / CSS
from PySide.QtWebKit import *


class Navigateur(QWebView):
    def __init__(self, document = False):
        super().__init__()  # apelle de la fonction d'initialisation parent de la classe parent.

        self.document = document

        if self.document:
            self.ajouter_document(document)

    def ajouter_document(self, document):
        self.document = document
        self.afficher_document()

        self.document.textEdit.textChanged.connect(self.afficher_document)

    def afficher_document(self):
        self.setHtml(self.document.textEdit.toPlainText())