# Module relatif à l'analyseur lexical LEX

import lexer.ply.lex as lex
from themes.themes import *

# ----------- LEX -----------#

tokenColor = get_color_from_theme("token")


def update_token_color():
    global tokenColor
    tokenColor = get_color_from_theme("token")

types = [
]

operandes = [
]

know_functions = [
]

know_const = [
]

keywords = {
}

tokens = [
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
        elif type_ == "IDENTIFIER" and value in know_functions:
            res += [[value, [107, 217, 237]]]
        elif type_ == "IDENTIFIER" and value in know_const:
            res += [[value, tokenColor["CONSTANT"]]]
        elif type_ in list(keywords.values()):
            res += [[value, tokenColor["KEYWORD"]]]
        elif type_ in tokenColor:
            res += [[value, tokenColor[type_]]]
        else:
            if "PONCT" not in tokenColor:
                ponct = [255, 255, 255]
            else:
                ponct = tokenColor["PONCT"]
            res += [[value, ponct]]
    
    return res


lignes = {}
erreurs = []

start = "translation_unit"

def p_include_expression(p):
    '''include_expression : INCLUDE INCLUDE_STRING'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["include_expression"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["include_expression"]
    #print("include_expression")


def p_primary_expression(p):
    '''primary_expression : IDENTIFIER
                          | CONSTANT
                          | STRING_LITERAL
                          | L_BRACKET expression R_BRACKET'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["primary_expression"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["primary_expression"]
    # Cette fonction est appelée lorsque Yacc trouve une primary expression, c'est-à-dire soit le token
    # IDENTIFIER, soit le token CONSTANT, ou encore STRING_LITERAL, ou bien une expression entre parenthèses.
    #print("primary_expression")


def p_postfix_expression(p):
    '''postfix_expression : primary_expression
                          | postfix_expression L_BRACE expression R_BRACE
                          | postfix_expression L_BRACKET R_BRACKET
                          | postfix_expression L_BRACKET argument_expression_list R_BRACKET
                          | postfix_expression POINT IDENTIFIER
                          | postfix_expression PTR_OP IDENTIFIER
                          | postfix_expression INC_OP
                          | postfix_expression DEC_OP'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["postfix_expression"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["postfix_expression"]
    #print("postfix_expression")


def p_argument_expression_list(p):
    '''argument_expression_list : assignment_expression
                                | argument_expression_list COMMA assignment_expression'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["argument_expression_list"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["argument_expression_list"]
    #print("argument_expression_list")


def p_unary_expression(p):
    '''unary_expression : postfix_expression
                         | INC_OP unary_expression
                         | DEC_OP unary_expression
                         | unary_operator cast_expression
                         | SIZEOF unary_expression
                         | SIZEOF L_BRACKET type_name R_BRACKET'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["unary_expression"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["unary_expression"]
    #print("unary_expression")


def p_unary_operator(p):
    '''unary_operator : AND
                       | TIMES
                       | PLUS
                       | MINUS
                       | TILD
                       | NOT'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["unary_operator"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["unary_operator"]
    #print("unary_operator")


def p_cast_expression(p):
    '''cast_expression : unary_expression
                       | L_BRACKET type_name R_BRACKET cast_expression'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["cast_expression"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["cast_expression"]
    #print("cast_expression")


def p_multiplicative_expression(p):
    '''multiplicative_expression : cast_expression
                                 | multiplicative_expression TIMES cast_expression
                                 | multiplicative_expression DIVIDE cast_expression
                                 | multiplicative_expression MOD cast_expression'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["multiplicative_expression"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["multiplicative_expression"]
    #print("multiplicative_expression")


def p_additive_expression(p):
    '''additive_expression : multiplicative_expression
                           | additive_expression PLUS multiplicative_expression
                           | additive_expression MINUS multiplicative_expression'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["additive_expression"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["additive_expression"]
    #print("additive_expression")


def p_shift_expression(p):
    '''shift_expression : additive_expression
                        | shift_expression LEFT_OP additive_expression
                        | shift_expression RIGHT_OP additive_expression'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["shift_expression"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["shift_expression"]
    #print("shift_expression")


def p_relational_expression(p):
    '''relational_expression : shift_expression
                             | relational_expression INF shift_expression
                             | relational_expression SUP shift_expression
                             | relational_expression LE_OP shift_expression
                             | relational_expression GE_OP shift_expression'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["relational_expression"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["relational_expression"]
    #print("relational_expression")


def p_equality_expression(p):
    '''equality_expression : relational_expression
                           | equality_expression EQ_OP relational_expression
                           | equality_expression NE_OP relational_expression'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["equality_expression"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["equality_expression"]
    #print("equality_expression")


def p_and_expression(p):
    '''and_expression : equality_expression
                      | and_expression AND equality_expression'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["and_expression"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["and_expression"]
    #print("and_expression")


def p_exclusive_or_expression(p):
    '''exclusive_or_expression : and_expression
                               | exclusive_or_expression EXOR and_expression'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["exclusive_or_expression"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["exclusive_or_expression"]
    #print("exclusive_or_expression")


def p_inclusive_or_expression(p):
    '''inclusive_or_expression : exclusive_or_expression
                               | inclusive_or_expression OR exclusive_or_expression'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["inclusive_or_expression"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["inclusive_or_expression"]
    #print("inclusive_or_expression")


def p_logical_and_expression(p):
    '''logical_and_expression : inclusive_or_expression
                              | logical_and_expression AND_OP inclusive_or_expression'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["logical_and_expression"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["logical_and_expression"]
    #print("logical_and_expression")


def p_logical_or_expression(p):
    '''logical_or_expression : logical_and_expression
                             | logical_or_expression OR_OP logical_and_expression'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["logical_or_expression"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["logical_or_expression"]
    #print("logical_or_expression")


def p_conditional_expression(p):
    '''conditional_expression : logical_or_expression
                              | logical_or_expression INTER expression COLON conditional_expression'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["conditional_expression"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["conditional_expression"]
    #print("conditional_expression")


def p_assignment_expression(p):
    '''assignment_expression : conditional_expression
                             | unary_expression assignment_operator assignment_expression'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["assignment_expression"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["assignment_expression"]
    #print("assignment_expression")


def p_assignment_operator(p):
    '''assignment_operator : EQUALS
                           | MUL_ASSIGN
                           | DIV_ASSIGN
                           | MOD_ASSIGN
                           | ADD_ASSIGN
                           | SUB_ASSIGN
                           | LEFT_ASSIGN
                           | RIGHT_ASSIGN
                           | AND_ASSIGN
                           | XOR_ASSIGN
                           | OR_ASSIGN'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["assignment_operator"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["assignment_operator"]
    #print("assignment_operator")


def p_expression(p):
    '''expression : assignment_expression
                  | expression COMMA assignment_expression'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["expression"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["expression"]
    #print("expression")


def p_constant_expression(p):
    '''constant_expression : conditional_expression'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["constant_expression"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["constant_expression"]
    #print("constant_expression")


def p_declaration(p):
    '''declaration : declaration_specifiers SEMICOLON
                   | declaration_specifiers init_declarator_list SEMICOLON'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["declaration"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["declaration"]
    #print("declaration")


def p_declaration_specifiers(p):
    '''declaration_specifiers : storage_class_specifier
                              | storage_class_specifier declaration_specifiers
                              | type_specifier
                              | type_specifier declaration_specifiers
                              | type_qualifier
                              | type_qualifier declaration_specifiers'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["declaration_specifiers"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["declaration_specifiers"]
    #print("declaration_specifiers")


def p_init_declarator_list(p):
    '''init_declarator_list : init_declarator
                            | init_declarator_list COMMA init_declarator'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["init_declarator_list"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["init_declarator_list"]
    #print("init_declarator_list")


def p_init_declarator(p):
    '''init_declarator : declarator
                       | declarator EQUALS initializer'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["init_declarator"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["init_declarator"]
    #print("init_declarator")


def p_storage_class_specifier(p):
    '''storage_class_specifier : TYPEDEF
                               | EXTERN
                               | STATIC
                               | AUTO
                               | REGISTER'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["storage_class_specifier"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["storage_class_specifier"]
    #print("storage_class_specifier")


def p_type_specifier(p):
    '''type_specifier : VOID
                      | CHAR
                      | SHORT
                      | INT
                      | LONG
                      | BOOL
                      | FLOAT
                      | DOUBLE
                      | SIGNED
                      | UNSIGNED
                      | struct_or_union_specifier
                      | enum_specifier'''  # TYPE_NAME
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["type_specifier"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["type_specifier"]
    #print("type_specifier")


def p_struct_or_union_specifier(p):
    '''struct_or_union_specifier : struct_or_union IDENTIFIER L_BRACE struct_declaration_list R_BRACE
                                 | struct_or_union L_BRACE struct_declaration_list R_BRACE
                                 | struct_or_union IDENTIFIER'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["struct_or_union_specifier"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["struct_or_union_specifier"]
    #print("struct_or_union_specifier")


def p_struct_or_union(p):
    '''struct_or_union : STRUCT
                       | UNION'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["struct_or_union"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["struct_or_union"]
    #print("struct_or_union")


def p_struct_declaration_list(p):
    '''struct_declaration_list : struct_declaration
                               | struct_declaration_list struct_declaration'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["struct_declaration_list"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["struct_declaration_list"]
    #print("struct_declaration_list")


def p_struct_declaration(p):
    '''struct_declaration : specifier_qualifier_list struct_declarator_list SEMICOLON'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["struct_declaration"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["struct_declaration"]
    #print("struct_declaration")


def p_specifier_qualifier_list(p):
    '''specifier_qualifier_list : type_specifier specifier_qualifier_list
                                | type_specifier
                                | type_qualifier specifier_qualifier_list
                                | type_qualifier'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["specifier_qualifier_list"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["specifier_qualifier_list"]
    #print("specifier_qualifier_list")


def p_struct_declarator_list(p):
    '''struct_declarator_list : struct_declarator
                              | struct_declarator_list COMMA struct_declarator'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["struct_declarator_list"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["struct_declarator_list"]
    #print("struct_declarator_list")


def p_struct_declarator(p):
    '''struct_declarator : declarator
                         | COLON constant_expression
                         | declarator COLON constant_expression'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["struct_declarator"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["struct_declarator"]
    #print("struct_declarator")


def p_enum_specifier(p):
    '''enum_specifier : ENUM L_BRACE enumerator_list R_BRACE
                      | ENUM IDENTIFIER L_BRACE enumerator_list R_BRACE
                      | ENUM IDENTIFIER'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["enum_specifier"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["enum_specifier"]
    #print("enum_specifier")


def p_enumerator_list(p):
    '''enumerator_list : enumerator
                       | enumerator_list COMMA enumerator'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["enumerator_list"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["enumerator_list"]
    #print("enumerator_list")


def p_enumerator(p):
    '''enumerator : IDENTIFIER
                  | IDENTIFIER EQUALS constant_expression'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["enumerator"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["enumerator"]
    #print("enumerator")


def p_type_qualifier(p):
    '''type_qualifier : CONST
                      | VOLATILE'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["type_qualifier"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["type_qualifier"]
    #print("type_qualifier")


def p_declarator(p):
    '''declarator : pointer direct_declarator
                  | direct_declarator'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["declarator"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["declarator"]
    #print("declarator")


def p_direct_declarator(p):
    '''direct_declarator : IDENTIFIER
                         | L_BRACKET declarator R_BRACKET
                         | direct_declarator L_HOOK constant_expression R_HOOK
                         | direct_declarator L_HOOK R_HOOK
                         | direct_declarator L_BRACKET parameter_type_list R_BRACKET
                         | direct_declarator L_BRACKET identifier_list R_BRACKET
                         | direct_declarator L_BRACKET R_BRACKET'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["declarator"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["declarator"]
    #print("direct_declarator")


def p_pointer(p):
    '''pointer : TIMES
               | TIMES type_qualifier_list
               | TIMES pointer
               | TIMES type_qualifier_list pointer'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["pointer"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["pointer"]
    #print("pointer")


def p_type_qualifier_list(p):
    '''type_qualifier_list : type_qualifier
                           | type_qualifier_list type_qualifier'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["type_qualifier_list"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["type_qualifier_list"]
    #print("type_qualifier_list")


def p_parameter_type_list(p):
    '''parameter_type_list : parameter_list
                           | parameter_list COMMA ELLIPSIS'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["parameter_type_list"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["parameter_type_list"]
    #print("parameter_type_list")


def p_parameter_list(p):
    '''parameter_list : parameter_declaration
                      | parameter_list COMMA parameter_declaration'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["parameter_list"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["parameter_list"]
    #print("parameter_list")


def p_parameter_declaration(p):
    '''parameter_declaration : declaration_specifiers declarator
                             | declaration_specifiers abstract_declarator
                             | declaration_specifiers'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["parameter_declaration"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["parameter_declaration"]
    #print("parameter_declaration")


def p_identifier_list(p):
    '''identifier_list : IDENTIFIER
                       | identifier_list COMMA IDENTIFIER'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["identifier_list"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["identifier_list"]
    #print("identifier_list")


def p_type_name(p):
    '''type_name : specifier_qualifier_list
                 | specifier_qualifier_list abstract_declarator'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["type_name"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["type_name"]
    #print("type_name")


def p_abstract_declarator(p):
    '''abstract_declarator : pointer
                           | direct_abstract_declarator
                           | pointer direct_abstract_declarator'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["abstract_declarator"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["abstract_declarator"]
    #print("abstract_declarator")


def p_direct_abstract_declarator(p):
    '''direct_abstract_declarator : L_BRACKET abstract_declarator R_BRACKET
                                  | L_HOOK R_HOOK
                                  | L_HOOK constant_expression R_HOOK
                                  | direct_abstract_declarator L_HOOK R_HOOK
                                  | direct_abstract_declarator L_HOOK constant_expression R_HOOK
                                  | L_BRACKET R_BRACKET
                                  | L_BRACKET parameter_type_list R_BRACKET
                                  | direct_abstract_declarator L_BRACKET R_BRACKET
                                  | direct_abstract_declarator L_BRACKET parameter_type_list R_BRACKET'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["direct_abstract_declarator"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["direct_abstract_declarator"]
    #print("direct_abstract_declarator")


def p_initializer(p):
    '''initializer : assignment_expression
                   | L_BRACE initializer_list R_BRACE
                   | L_BRACE initializer_list COMMA R_BRACE'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["initializer"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["initializer"]
    #print("initializer")


def p_initializer_list(p):
    '''initializer_list : initializer
                        | initializer_list COMMA initializer'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["initializer_list"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["initializer_list"]
    #print("initializer_list")


def p_statement(p):
    '''statement : labeled_statement
                 | compound_statement
                 | expression_statement
                 | selection_statement
                 | iteration_statement
                 | jump_statement'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["initializer_list"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["initializer_list"]
    #print("statement")


def p_labeled_statement(p):
    '''labeled_statement : IDENTIFIER COLON statement
                         | CASE constant_expression COLON statement
                         | DEFAULT COLON statement'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["labeled_statement"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["labeled_statement"]
    #print("labeled_statement")


def p_compound_statement(p):
    '''compound_statement : L_BRACE R_BRACE
                          | L_BRACE statement_list R_BRACE
                          | L_BRACE declaration_list R_BRACE
                          | L_BRACE declaration_list statement_list R_BRACE'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["compound_statement"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["compound_statement"]
    #print("compound_statement")


def p_declaration_list(p):
    '''declaration_list : declaration
                        | declaration_list declaration'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["declaration_list"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["declaration_list"]
    #print("declaration_list")


def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["statement_list"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["statement_list"]
    #print("statement_list")


def p_expression_statement(p):
    '''expression_statement : SEMICOLON
                            | expression SEMICOLON'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["expression_statement"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["expression_statement"]
    #print("expression_statement")


def p_selection_statement(p):
    '''selection_statement : IF L_BRACKET expression R_BRACKET statement
                           | IF L_BRACKET expression R_BRACKET statement ELSE statement
                           | SWITCH L_BRACKET expression R_BRACKET statement'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["selection_statement"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["selection_statement"]
    #print("selection_statement")


def p_iteration_statement(p):
    '''iteration_statement : WHILE L_BRACKET expression R_BRACKET statement
                           | DO statement WHILE L_BRACKET expression R_BRACKET SEMICOLON
                           | FOR L_BRACKET expression_statement expression_statement R_BRACKET statement
                           | FOR L_BRACKET expression_statement expression_statement expression R_BRACKET statement'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["iteration_statement"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["iteration_statement"]
    #print("iteration_statement")


def p_jump_statement(p):
    '''jump_statement : GOTO IDENTIFIER SEMICOLON
                      | CONTINUE SEMICOLON
                      | BREAK SEMICOLON
                      | RETURN SEMICOLON
                      | RETURN expression SEMICOLON'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["jump_statement"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["jump_statement"]
    #print("jump_statement")


def p_translation_unit(p):
    '''translation_unit : external_declaration
                        | translation_unit external_declaration
                        | include_expression'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["translation_unit"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["translation_unit"]
    #print("translation_unit")


def p_external_declaration(p):
    '''external_declaration : function_definition
                            | declaration'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["translation_unit"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["translation_unit"]
    #print("external_declaration")


def p_function_definition(p):
    '''function_definition : declaration_specifiers declarator declaration_list compound_statement
                           | declaration_specifiers declarator compound_statement
                           | declarator declaration_list compound_statement
                           | declarator compound_statement'''
    if not str(p.lineno(0) - 1) in lignes:
        lignes[str(p.lineno(0) - 1)] = ["function_definition"]
    else:
        lignes[str(p.lineno(0) - 1)] += ["function_definition"]
    nb = len(list(p)) - 1
    #print("function_definition, on line", p.lineno(0), "from char", p.lexspan(0)[0] + 1, "to char", p.lexspan(nb)[0] + 1)


def p_error(p):
    print("coucou c'est moi")
    if p and p.type != "COMMENT":
        global erreurs
        erreurs += [[p.lineno, p.lexpos, p.value]]
        #print("---------------Syntax error in input : ", p.lineno, p.type, p.value, p.lexpos)


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