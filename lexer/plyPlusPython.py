import lexer.plyplus, lexer.plyplus.grammars

g = lexer.plyplus.Grammar(lexer.plyplus.grammars.open('python.g'))  

def get_def_functions(data):
	t = g.parse(data)
	return list(t.select("funcdef > name > *"))

def get_def_class(data):
	t = g.parse(data)
	return list(t.select("classdef > name > *"))  

def get_def_vars(data):
	t = g.parse(data)
	return list(t.select("assign_stmt > name > *"))

