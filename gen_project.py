from PySide.QtCore import *
from PySide.QtGui import *

from datetime import datetime

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

create_empty()
create_files(100)
