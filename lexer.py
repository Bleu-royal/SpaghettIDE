import ply.lex as lex

# ----------- LEX -----------#

types = [
    "char",
    "bool",
    "double",
    "enum",
    "float",
    "int",
    "long",
    "short",
    "signed",
    "unsigned",
    "void"
]

operandes = [
    "equals",
    "times",
    "divide",
    "mod",
    "minus",
    "plus",
    "right_assign",
    "left_assign",
    "add_assign",
    "sub_assign",
    "mul_assign",
    "div_assign",
    "mod_assign",
    "and_assign",
    "xor_assign",
    "or_assign",
    "inc_op",
    "dec_op",
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

know_functions = [
    "srand",
    "rand",
    "time",
    "printf",
    "scanf"
]

know_const = [
    "NULL",
]

keywords = {
    "auto": "AUTO",
    "bool": "BOOL",
    "break": "BREAK",
    "case": "CASE",
    "char": "CHAR",
    "const": "CONST",
    "continue": "CONTINUE",
    "default": "DEFAULT",
    "do": "DO",
    "double": "DOUBLE",
    "else": "ELSE",
    "enum": "ENUM",
    "extern": "EXTERN",
    "float": "FLOAT",
    "for": "FOR",
    "goto": "GOTO",
    "if": "IF",
    "int": "INT",
    "long": "LONG",
    "register": "REGISTER",
    "return": "RETURN",
    "short": "SHORT",
    "signed": "SIGNED",
    "sizeof": "SIZEOF",
    "static": "STATIC",
    "struct": "STRUCT",
    "switch": "SWITCH",
    "typedef": "TYPEDEF",
    "union": "UNION",
    "unsigned": "UNSIGNED",
    "void": "VOID",
    "volatile": "VOLATILE",
    "while": "WHILE"
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

tokenColor = {

    "IDENTIFIER": [255, 255, 255],
    "KEYWORD": [246, 45, 115],
    "STRING_LITERAL" : [230, 218, 123],
    "COMMENT" : [117, 113, 95],
    "CONSTANT" : [174, 133, 252],

}

t_STRING_LITERAL = r"[A-Za-z_]?\"(\.|[^\"])*\""
t_ELLIPSIS = r"\.\.\."
t_RIGHT_ASSIGN = r">>="
t_LEFT_ASSIGN = r"<<="
t_ADD_ASSIGN = r"\+="
t_SUB_ASSIGN = r"-="
t_MUL_ASSIGN = r"\*="
t_DIV_ASSIGN = r"/="
t_MOD_ASSIGN = r"%="
t_AND_ASSIGN = r"&="
t_XOR_ASSIGN = r"\^="
t_OR_ASSIGN = r"\|="
t_RIGHT_OP = r">>"
t_LEFT_OP = r"<<"
t_INC_OP = r"\+\+"
t_DEC_OP = r"--"
t_PTR_OP = r"->"
t_AND_OP = r"&&"
t_OR_OP = r"\|\|"
t_LE_OP = r"<="
t_GE_OP = r">="
t_EQ_OP = r"=="
t_NE_OP = r"!="
t_SEMICOLON = r";"
# t_L_BRACE = r"{|<%"
# t_R_BRACE = r"}|%>"
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
t_AND = r"&"
t_NOT = r"!"
t_TILD = r"~"
t_MINUS = r"-"
t_PLUS = r"\+"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_MOD = r"\%"
t_INF = r"<"
t_SUP = r">"
t_EXOR = r"\^"
t_OR = r"\|"
t_INTER = r"\?"
t_CONSTANT =  r'[0-9]+'
t_COMMENT = r'(//.*)|(/\*(.)*\*/)'


def t_IDENTIFIER(t):
    r"[A-Za-z_][A-Za-z0-9_]*"
    t.type = keywords.get(t.value, "IDENTIFIER")
    return t


t_ignore = " \t\f\v"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    #print("Illegal character ’%s’" % t.value[0], "on line ", t.lineno)
    t.lexer.skip(1)


def colorate(data):
    lexer = lex.lex()
    lexer.input(data)
    res = []

    while True:
        token = lexer.token()
        if not token: break
        if token.type.lower() in types:
            res += [[token.value, [107, 217, 237]]]
        elif token.type.lower() in operandes:
            res += [[token.value, [246, 45, 115]]]
        elif token.type == "IDENTIFIER" and token.value in know_functions:
            res += [[token.value, [107, 217, 237]]]
        elif token.type == "IDENTIFIER" and token.value in know_const:
            res += [[token.value, tokenColor["CONSTANT"]]]
        elif token.type in list(keywords.values()):
            res += [[token.value, tokenColor["KEYWORD"]]]
        elif token.type in tokenColor:
            res += [[token.value, tokenColor[token.type]]]
        else:
            res += [[token.value, [255, 255, 255]]]
    return res
