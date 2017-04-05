from lexer import c, python, ar

lexers = {"c" : c, "h" : c, "py" : python}

def lexing(language, word):
    return [] if language not in lexers else lexers[language].lexing(word)

def tokenize(language, data):
    return [] if language not in lexers else lexers[language].tokenize(data)

def colorate(language, data):
    return [] if language not in lexers else lexers[language].colorate(data)

def update_token_color(language):
    if language in lexers : lexers[language].update_token_color()

def yaccing(language, data, get_errros=True):
    return [] if language not in lexers else lexers[language].yaccing(data, get_errros)

def get_keywords(language):
    return {} if language not in lexers else lexers[language].keywords

def get_know_functions(language):
    return [] if language not in lexers else lexers[language].know_functions