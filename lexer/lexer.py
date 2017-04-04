from lexer import c, ar


def lexing(language, word):
    if language in ("c", "h"):
        return c.lexing(word)
    else:
        return []

def tokenize(language, data):
    if language in ("c", "h"):
        return c.tokenize(data)
    else:
        []

def colorate(language, data):
    
    if language in ("c", "h"):
        return c.colorate(data)
    else:
        return []

def update_token_color(language):
    if language in ("c", "h"):
        c.update_token_color()


def yaccing(language, data, get_errros=True):

    if language in ("c", "h"):
        return c.yaccing(data, get_errros)
    else:
        if get_errros: return ([],[])
        else: return []

def get_keywords(language):
    print(language)
    if language in ("c", "h"):
        return c.keywords
    else:
        return {}


def get_know_functions(language):
    print(language)
    if language in ("c", "h"):
        return c.know_functions
    else:
        return []
