from lexer import c, python, ar, json, plyPlusPython

lexers = {"c" : c, "h" : c, "py" : python, "json": json}
plyPlusLexers = {"py" : plyPlusPython}

def lexing(language, word):
	return [] if language not in lexers else lexers[language].lexing(word)

def tokenize(language, data):
	return [] if language not in lexers else lexers[language].tokenize(data)

def colorate(language, data):
	return [] if language not in lexers else lexers[language].colorate(data)

def update_token_color():
	for lexer in lexers.values():
		lexer.update_token_color()

def update_text(language, data):
	if language in lexers:
		lexers[language].update_text(data)

def yaccing(language, data, get_errros=True):
	return [] if language not in lexers else lexers[language].yaccing(data, get_errros)

def get_keywords(language):
	return {} if language not in lexers else lexers[language].keywords

def get_know_functions(language):
	return [] if language not in lexers else lexers[language].know_functions

def get_def_functions(language, data):
	return [] if language not in plyPlusLexers else plyPlusLexers[language].get_def_functions(data)

def get_def_class(language, data):
	return [] if language not in plyPlusLexers else plyPlusLexers[language].get_def_class(data)

def get_def_vars(language, data):
	return [] if language not in plyPlusLexers else plyPlusLexers[language].get_def_vars(data)