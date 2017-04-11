import lexer.plyplus, lexer.plyplus.grammars

g = lexer.plyplus.Grammar(lexer.plyplus.grammars.open('python.g'))  

t = ""

def set_data_to_parse(data):
	global t
	try :
		t = g.parse(data + "\n")
	except:
		t = False
def is_function(word):
	if t:
		return word in t.select("funccall > name > *") or word in t.select("funcdef > name > *") or word in t.select("classdef > name > *")

def get_def_functions(data):
	t = g.parse(data)
	return list(t.select("funcdef > name > *"))

def get_def_class(data):
	t = g.parse(data)
	return list(t.select("classdef > name > *"))  

def get_def_vars(data):
	t = g.parse(data)
	return list(t.select("assign_stmt > name > *"))

