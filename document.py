# Module relatif au traitement des documents (noms, extention, sauvegarde, chargement...)

class Document():
    def __init__(self, textEdit, navigateur, chemin_enregistrement,ouverture=False):  # Sauvegarde des variables au sein de la class

        self.textEdit = textEdit
        self.navigateur = navigateur
        self.chemin_enregistrement = chemin_enregistrement
        self.nom = self.chemin_enregistrement.split("/")[-1]  # Recupération du nom du fichier
        self.extension = self.nom.split(".")[-1]  # Recupération de l'extension du fichier
        self.nombre_lignes = self.textEdit.document().lineCount()  # Obtention du nombre de lignes presentent dans le QTextEdit

        self.textEdit.textChanged.connect(self.maj_navigateur)

        if ouverture:
            self.ouverture_document()
        else:
            self.sauvegarde_document()

    def ouverture_document(self):
        fichier = open(self.chemin_enregistrement, "r")
        code = fichier.read()
        fichier.close()
        self.textEdit.setPlainText(code)

    def sauvegarde_document(self):
        fichier = open(self.chemin_enregistrement, "w")
        fichier.write(self.textEdit.toPlainText())  # Ecriture du fichier.
        fichier.close()

    def maj_navigateur(self):
        self.navigateur.setHtml(self.textEdit.toPlainText())
