# Module relatif à l'analyseur lexical LEX

import lexer.ply.lex as lex
from lexer import plyPlusPython as lexPly
from themes.themes import *

# ----------- LEX -----------#

tokenColor = get_color_from_theme("token")

text = ""


def update_token_color():
    global tokenColor
    tokenColor = get_color_from_theme("token")

types = [
    "int",
    "list",
    "str",
    "tuple",
    "dict",
    "set",
    "float",
    "long",
    "bool",
]

operandes = [
    "equals",
    "times",
    "divide",
    "mod",
    "minus",
    "plus",
    "add_assign",
    "sub_assign",
    "mul_assign",
    "div_assign",
    "mod_assign",
    "and_assign",
    "or_assign",
    "and_op",
    "or_op",
    "le_op",
    "ge_op",
    "eq_op",
    "ne_op",
    "inf",
    "sup",
    "and",
    "not"
]

know_functions = ["ellipsis", "abs", "all", "any", "apply", "basestring", "buffer", "callable", "chr", "classmethod", "cmp", "coerce", "compile", "complex", "copyright", "credits", "delattr", "dir", "divmod", "enumerate", "eval", "execfile", "exit", "file", "filter", "float", "frozenset", "getattr", "globals", "hasattr", "hash", "help", "hex", "id", "input", "intern", "isinstance", "issubclass", "iter", "len", "license", "locals", "map", "max", "min", "object", "oct", "open", "ord", "pow", "property", "quit", "range", "raw_input", "reduce", "reload", "repr", "reversed", "round", "setattr", "slice", "sorted", "staticmethod", "sum", "super", "type", "unichr", "unicode", "vars", "xrange", "zip"]

know_const = [
    "NONE",
    "TRUE",
    "FALSE",
    "ARITHMETICERROR",
    "ASSERTIONERROR", 
    "ATTRIBUTEERROR", 
    "BASEEXCEPTION", 
    "DEPRECATIONWARNING", 
    "EOFERROR",  
    "ENVIRONMENTERROR", 
    "EXCEPTION",
    "FLOATINGPOINTERROR", 
    "FUTUREWARNING", 
    "GENERATOREXIT", 
    "IOERROR", 
    "IMPORTERROR", 
    "IMPORTWARNING", 
    "INDENTATIONERROR", 
    "INDEXERROR", 
    "KEYERROR", 
    "KEYBOARDINTERRUPT", 
    "LOOKUPERROR", 
    "MEMORYERROR", 
    "NAMEERROR", 
    "NOTIMPLEMENTED", 
    "NOTIMPLEMENTEDERROR", 
    "OSERROR", 
    "OVERFLOWERROR", 
    "PENDINGDEPRECATIONWARNING", 
    "REFERENCEERROR", 
    "RUNTIMEERROR", 
    "RUNTIMEWARNING", 
    "STANDARDERROR", 
    "STOPITERATION", 
    "SYNTAXERROR", 
    "SYNTAXWARNING", 
    "SYSTEMERROR", 
    "SYSTEMEXIT", 
    "TABERROR", 
    "TYPEERROR", 
    "UNBOUNDLOCALERROR", 
    "UNICODEDECODEERROR", 
    "UNICODEENCODEERROR", 
    "UNICODEERROR", 
    "UNICODETRANSLATEERROR", 
    "UNICODEWARNING", 
    "USERWARNING", 
    "VALUEERROR", 
    "WARNING", 
    "ZERODIVISIONERROR"
]

keywords = {
    "and" : "AND",
    "as" : "AS",
    "assert" : "ASSERT",
    "break" : "BREAK",
    "class" : "CLASS",
    "continue" : "CONTINUE",
    "def" : "DEF",
    "del" : "DEL",
    "elif" : "ELIF",
    "else" : "ELSE",
    "except" : "EXCEPT",
    "exec" : "EXEC",
    "finnaly" : "FINNALY",
    "for" : "FOR",
    "from" : "FROM",
    "global" : "GLOBAL",
    "if" : "IF",
    "import" : "IMPORT",
    "in" : "IN",
    "is" : "IS",
    "lambda" : "LAMBDA",
    "not" : "NOT",
    "or" : "OR",
    "pass" : "PASS",
    "print" : "PRINT",
    "raise" : "RAISE",
    "return" : "RETURN",
    "try" : "TRY",
    "while" : "WHILE",
    "with" : "WITH",
    "yield" : "YIELD",

}

tokens = [
    "IDENTIFIER",
    "CONSTANT",
    "STRING_LITERAL",
    "ELLIPSIS",
    "RIGHT_ASSIGN",
    "LEFT_ASSIGN",
    "ADD_ASSIGN",
    "SUB_ASSIGN",
    "MUL_ASSIGN",
    "DIV_ASSIGN",
    "MOD_ASSIGN",
    "AND_ASSIGN",
    "XOR_ASSIGN",
    "OR_ASSIGN",
    "AND_OP",
    "OR_OP",
    "LE_OP",
    "GE_OP",
    "EQ_OP",
    "NE_OP",
    "L_BRACE",
    "R_BRACE",
    "COMMA",
    "COLON",
    "EQUALS",
    "L_BRACKET",
    "R_BRACKET",
    "L_HOOK",
    "R_HOOK",
    "POINT",
    "TILD",
    "MINUS",
    "PLUS",
    "TIMES",
    "DIVIDE",
    "MOD",
    "INF",
    "SUP",
    "COMMENT",
    "DOTTED_NAME",
    "newline"
] + list(keywords.values())

t_STRING_LITERAL = r"([A-Za-z_]?\"(\.|[^\"])*\")|([A-Za-z_]?\'(\.|[^\'])*\')"
t_ELLIPSIS = r"\.\.\."
t_ADD_ASSIGN = r"\+="
t_SUB_ASSIGN = r"-="
t_MUL_ASSIGN = r"\*="
t_DIV_ASSIGN = r"/="
t_MOD_ASSIGN = r"%="
t_AND_ASSIGN = r"&="
t_OR_ASSIGN = r"\|="
t_AND_OP = r"&&"
t_OR_OP = r"\|\|"
t_LE_OP = r"<="
t_GE_OP = r">="
t_EQ_OP = r"=="
t_NE_OP = r"!="
t_L_BRACE = r"{"
t_R_BRACE = r"}"
t_COMMA = r","
t_COLON = r":"
t_EQUALS = r"="
t_L_BRACKET = r"\("
t_R_BRACKET = r"\)"
t_L_HOOK = r"\["
t_R_HOOK = r"\]"
t_POINT = r"\."
t_TILD = r"~"
t_MINUS = r"-"
t_PLUS = r"\+"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_MOD = r"\%"
t_INF = r"<"
t_SUP = r">"
t_CONSTANT = r'[0-9]+'
t_COMMENT = r'\#(.*)'


def t_DOTTED_NAME(t):
    r"[A-Za-z_][\.A-Za-z0-9_]*"
    t.type = keywords.get(t.value, "IDENTIFIER")
    return t

def t_IDENTIFIER(t):
    r"[A-Za-z_][A-Za-z0-9_]*"
    t.type = keywords.get(t.value, "IDENTIFIER")
    return t


t_ignore = " \t\f\v"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    # print("erreur : %s"%t)
    # print("Illegal character ’%s’" % t.value[0], "on line ", t.lineno)
    t.lexer.skip(1)

def lexing(word):
    lexer = lex.lex()
    lexer.input(word)
    token = lexer.token()
    return token.type.lower() if token else ""

def update_text(data):
    global text
    text = data

def tokenize(data):

    lexer = lex.lex()
    lexer.input(data)

    res = []

    if text != "":
        lexPly.set_data_to_parse(text)

    while True:
        token = lexer.token()
        if not token: break
        if lexPly.is_function(token.value):
            res += [("KNOWN_FUNC", token.value)]
        else:
            res += [(token.type, token.value)]

    return res

def colorate(data):
    res = []

    for e in data:
        type_, value = e
        if type_.lower() in types:
            res += [[value, tokenColor["TYPE"]]]
        elif type_.lower() in operandes:
            res += [[value, tokenColor["OP"]]]
        elif type_ == "IDENTIFIER" and value.lower() in know_functions or type_ == "KNOWN_FUNC":
            res += [[value, tokenColor["KNOWN_FUNC"]]]
        elif type_ == "IDENTIFIER" and value.upper() in know_const:
            res += [[value, tokenColor["CONSTANT"]]]
        elif type_ in list(keywords.values()):
            res += [[value, tokenColor["KEYWORD"]]]
        elif type_ in tokenColor:
            res += [[value, tokenColor[type_]]]
        else:
            res += [[value, tokenColor["PONCT"]]]
    
    return res


lignes = {}
erreurs = []


def p_error(p):
    # print("erreur : %s"%p)
    pass


def yaccing(data, get_errros=True):
    # global erreurs, lignes
    # erreurs = []
    # lignes = {}

    # lexer = lex.lex()
    # lexer.input(data)

    # import lexer.ply.yacc as yacc
    # parser = yacc.yacc()
    # parser.parse(data, tracking=True)
    # # parser.parse(data)

    # # for i in sorted([int(i) for i in list(lignes.keys())]):
    # #     print("ligne numero %s: %s" % (i + 1, lignes[str(i)]), "\n\n")

    return [erreurs, lignes] if get_errros else lignes
