# Module relatif à l'analyseur lexical LEX

import lexer.ply.lex as lex
from themes.themes import *

# ----------- LEX -----------#

tokenColor = get_color_from_theme("token")


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
    "RIGHT_OP",
    "LEFT_OP",
    "INC_OP",
    "DEC_OP",
    "PTR_OP",
    "AND_OP",
    "OR_OP",
    "LE_OP",
    "GE_OP",
    "EQ_OP",
    "NE_OP",
    "SEMICOLON",
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
    "AND",
    "NOT",
    "TILD",
    "MINUS",
    "PLUS",
    "TIMES",
    "DIVIDE",
    "MOD",
    "INF",
    "SUP",
    "EXOR",
    "OR",
    "INTER",
    "COMMENT",
] + list(keywords.values())

def t_IDENTIFIER(t):
    r"[A-Za-z_][A-Za-z0-9_]*"
    t.type = keywords.get(t.value, "IDENTIFIER")
    return t




t_ignore = " \t\f\v"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("coucouc c'est moi")
    # print("Illegal character ’%s’" % t.value[0], "on line ", t.lineno)
    t.lexer.skip(1)

def lexing(word):
    lexer = lex.lex()
    lexer.input(word)
    token = lexer.token()
    return token.type.lower() if token else ""

def tokenize(data):
    lexer = lex.lex()
    lexer.input(data)

    res = []

    while True:
        token = lexer.token()
        if not token: break
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
        elif type_ == "IDENTIFIER" and value.upper() in know_functions:
            res += [[value, tokenColor["KNOWN_FUNC"]]]
        elif type_ == "IDENTIFIER" and value in know_const:
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

def yaccing(data, get_errros=True):
    global erreurs, lignes
    erreurs = []
    lignes = {}

    lexer = lex.lex()
    lexer.input(data)

    import lexer.ply.yacc as yacc
    parser = yacc.yacc()
    parser.parse(data, tracking=True)
    # parser.parse(data)

    # for i in sorted([int(i) for i in list(lignes.keys())]):
    #     print("ligne numero %s: %s" % (i + 1, lignes[str(i)]), "\n\n")

    return [erreurs, lignes] if get_errros else lignes