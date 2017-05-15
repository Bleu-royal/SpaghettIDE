file_by_language = {"c": "Fichier C (*.c);;Fichier H (*.h)", "python": "Fichier PY (*.py)"}
extension_by_language = {"c": ["*c", "*h"], "python": ["*py"], "": ["*c", "*h", "*py"]}
supported_extensions = {"c": "C", "h": "C", "py": "Python", "jpg": "jpg", "png": "png", "gif": "gif", "txt": "txt"}

inter_lang = ["python"]
compil_lang = ["c"]

imgs_extentions = ["*jpg", "*png"]
txt_ext_open = "Fichier texte (*.txt)"  # Pour quand on ouvre avec Ctrl+O il faut l'ajouter aux fichiers ouvrable.
txt_extentions_filedialog = "Fichier Text (*.txt);;Fichier Json (*.json);;Fichier XML (*.xml)"
txt_extentions = ["*txt", "*json", "*xml"]
gif_extentions = ["*gif"]
ext_neutres = txt_extentions + imgs_extentions + gif_extentions