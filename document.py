# Module relatif au traitement des documents (noms, extention, sauvegarde, chargement...)

class Document():
    def __init__(self, textEdit, chemin_enregistrement):
        # Sauvegarde des variables au sein de la class


        self.textEdit = textEdit
        self.nom = self.chemin_enregistrement.split("/")[-1] #Recupération du nom du fichier
        self.extension = self.nom.split(".")[-1] #Recupération de l'extension du fichier
        self.chemin_enregistrement = chemin_enregistrement
        self.nombre_lignes = self.textEdit.document().lineCount()  # Obtention du nombre de lignes presentent dans le QTextEdit
        self.sauvegarde_document()

    def sauvegarde_document(self):
        fichier = open(self.chemin_enregistrement, "w")
        fichier.write(self.textEdit.toPlainText())
        fichier.close()
