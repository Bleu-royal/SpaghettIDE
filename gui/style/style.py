def __load(file, ext=".css", path="gui/style/"):
    f = open(path + file + ext, "r")
    txt = f.read()
    f.close()

    return txt

def get(*args):
    ch = ""
    for element in args:
        try:
            ch += __load(element)
        except:
            continue
    return ch
