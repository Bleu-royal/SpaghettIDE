from PySide.QtCore import *

from datetime import datetime
import sys

project = ""

def create_empty():
    global project
    path = QDir.homePath() + "/workplace/"

    name = "projectTEST"
    i = 1
    while QDir(path+name+str(i)).exists():
        i += 1

    QDir(path).mkpath(name+str(i))
    project = path+name+str(i)

    date = datetime.now()
    fichier = open("%s/.conf" % project, "w")
    fichier.write("Created : %s/%s/%s" % (date.day, date.month, date.year))
    fichier.close()


def create_files(n):
    for i in range(n):
        f = open("%s/file%s.c" % (project, str(i)), "w")
        f.close()


if __name__ == "__main__":
    n = 100
    if len(sys.argv) == 2:
        try:
            n = int(sys.argv[1])
        except:
            print("L'argument doit être un entier. On prend 100 par défaut.")

    create_empty()
    create_files(n)
