# Module relatif à l'analyseur lexical LEX

import ply.lex as lex

tokens = (
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
)

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NUMBER  = r'\d+'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal charascter '%s'" % t.value[0])
    t.lexer.skip(1)

t_ignore  = ' \t'

prop = []

def p_expression(p):
    '''expression :   expression PLUS terme
                    | expression MINUS terme
                    | terme
    '''
    # global prop
    if not "+" in prop:
        prop.extend(["+", "-"])

def p_terme(p):
    '''terme :    terme TIMES facteur
                | terme DIVIDE facteur
                | facteur
    '''
    if not "/" in prop:
        prop.extend(["/", "*"])

def p_facteur(p):
    '''facteur :  LPAREN expression RPAREN
                | MINUS facteur
                | NUMBER
    '''
    if not "0" in prop:
        prop.extend([str(x) for x in range(10)])


def p_error(p):
    global prop
    prop = []
    prop.extend([str(x) for x in range(10)])

def parse(data):
    global prop
    prop = []

    lexer = lex.lex()
    lexer.input(data)

    import ply.yacc as yacc
    parser = yacc.yacc()
    parser.parse(data, tracking=True)
    return prop

