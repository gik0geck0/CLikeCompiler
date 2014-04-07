# Parser for a C-Like language, written by Matt Buland, Jesse Weaver, Garrison Davis and Aakash Shah


import ply.yacc as yacc
import lexer
import ast
from ast import makeNode
from ast import makeFamily

tokens = lexer.tokens

# Returns a Program Node, which has Statements as its children
def p_program(p):
    'program : statements'
    p[0] = makeFamily('PROGRAM', p[1])

# Returns a single statement node, which is the left-most sibling in its set
def p_statements(p):
    '''statements : statement
                | statement statements'''
    if len(p) == 2:
        # Luckily, p[1] is already a statement node
        p[0] = p[1]
    else:
        # p[2] will be the head of its sibling list.
        # So all we need to do is add it and its siblings to the right
        # of p[1]
        p[0] = p[1].makeSiblings(p[2])

def p_statement(p):
    '''statement : returnstmt SEMICOL
                 | ifstmt
                 | varassign SEMICOL
                 | vardecl SEMICOL'''
    # Alternation of semicolon-statements, so no node-association logic
    p[0] = p[1]

def p_returnstmt(p):
    'returnstmt : RETURN expr'
    p[0] = makeFamily('RETURN', p[2])

def p_varassign(p):
    'varassign : ID EQUALS expr'
    p[0] = makeFamily('ASSIGN', makeNode(p[1]), p[3])

def p_vardecl(p):
    'vardecl : typeconstructor vars'
    p[0] = makeFamily('DECLARE', p[1], p[2])

def p_ifstmt(p):
    '''ifstmt : IF LPAREN boolexpr RPAREN LCURLY statements RCURLY
              | IF LPAREN boolexpr RPAREN LCURLY statements RCURLY ELSE statement SEMICOL
              | IF LPAREN boolexpr RPAREN LCURLY statements RCURLY ELSE LCURLY statements RCURLY'''
    # print("Entering if with: ", p[1], p[2], p[3], p[4], p[5], p[6], p[7])
    if len(p) > 8:
        # Has an else
        # The ternary-like part differentiates where the stmt/stmts come from
        # p[0] = ('IF', p[3], 'THEN', p[6], 'ELSE', p[10] if len(p) > 11 else p[9])
        p[0] = makeFamily('IF', p[3], p[6], p[10] if len(p) > 11 else p[9])
    else:
        # p[0] = ('IF', p[3], 'THEN', p[6])
        p[0] = makeFamily('IF', p[3], p[6], makeNode())
    # print("IFSTMT", p[0])

# -> ( [Qualifer], Type )
def p_typeconstructor(p):
    '''typeconstructor : qualifier typeconstructor
            | type'''
    if len(p) > 2:
        # print("Type with qualifier: %s on type %s" % (p[1], p[2]))
        # p[0] = (p[2][0] + [p[1]], p[2][1])
        p[0] = p[2].makeSiblings(p[1])
    else:
        p[0] = p[1]

def p_type(p):
    ''' type : INT'''
    p[0] = makeNode(p[1])

def p_qualifier(p):
    'qualifier : CONST'
    p[0] = makeNode(p[1])

def p_vars(p):
    '''vars : ID
            | ID COMMA vars
            | ID EQUALS expr
            | ID EQUALS expr COMMA vars'''
    if len(p) == 2:
        # Just an ID
        p[0] = makeFamily('DECLARE', makeNode(p[1]))
    elif p[2] == '=':
        # we are definitely assigning the ID
        if len(p) > 4:
            # Creates a new family alongside other families:
            #   The new family is a DECLARE node strung with [ID -> VALUE]
            p[0] = p[5].makeSiblings(makeFamily('DECLARE', makeNode(p[1]), p[3]))
        else:
            p[0] = makeFamily('DECLARE', makeNode(p[1]), p[3])
    else:
        p[0] = makeFamily('DECLARE', makeNode(p[1])).makeSiblings(p[3])

def p_boolexpr(p):
    '''boolexpr : expr LTHAN expr
                | expr GTHAN expr
                | expr EQUALSEQUALS expr
                | expr LTHAN EQUALS expr
                | expr GTHAN EQUALS expr
                | expr'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = makeFamily(p[2], p[1], p[3])
    else:
        p[0] = makeFamily(p[2]+p[3], p[1], p[4])

def p_expr(p):
    '''expr : term
            | term PLUS term
            | term MINUS term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        # Creates an oprator node that's strung with the terms to opreate on as its children
        p[0] = makeFamily(p[2], p[1], p[3])

def p_term(p):
    '''term : part
            | part TIMES part
            | part DIVIDE part
            | part LSHIFT part
            | part RSHIFT part'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        # Creates an operator node that's strung with the parts to operate on as its children
        p[0] = makeFamily(p[2], p[1], p[3])

def p_part(p):
    '''part : ID
            | NUM
            | LPAREN expr RPAREN'''
    if len(p) == 2:
        p[0] = makeNode(p[1])
    else:
        p[0] = p[2]

def p_error(p):
    if p is not None:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at Null. WTF")

yacc.yacc()
parseTree = yacc.parse(lexer.datainput)

print("")
print("Parse Tree:")
parseTree.prettyPrintStructure()

# import pprint
# pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(parseTree)

