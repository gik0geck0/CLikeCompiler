
# BNF for our C-Like language
# S -> Stmts
#
# Stmts -> lambda
#       | Stmt; Stmts
# Stmt -> ReturnStmt
#       | IfStmt
#       | VarAssn
#       | VarDecl
#
# ReturnStmt -> return Expr
# VarAssn -> LValue = Expr
#
# VarDecl -> Type Vars
# Type -> Qualifiers int
# Qualifiers -> lambda
#               | Qualifier Qualifiers
# Qualifier -> const
#
# Vars -> ID = Expr
#       | ID, Vars
#       | ID
#       | ID = Expr, Vars
# Expr -> Term
#       | Term plus Term
#       | Term minus Term
# Term -> Part
#       | Part times Part
#       | Part div Part
#       | Part rshift Part
#       | Part lshift Part
# Part -> id
#       | num
#       | lparen Expr rparen
# 

import ply.yacc as yacc
import lexer

tokens = lexer.tokens

def p_start(p):
    'start : statements'

def p_statements_empty(p):
    'statements : epsilon'
    p[0] = []

def p_statements_one(p):
    'statements : statement SEMICOL statements'
    p[0] = p[3].append(p[1])


def p_statement(p):
    '''statement : returnstmt
                 | ifstmt
                 | varassign
                 | vardecl'''
    p[0] = p[1]

def p_returnstmt(p):
    'returnstmt : RETURN expr'
    p[0] = ('RETURN', p[2])

def p_varassign(p):
    'varassign : ID EQUALS expr'
    p[0] = ('ASSIGN', p[1], p[3])

def p_vardecl(p):
    'vardecl : type vars'
    p[0] = ('DECLARE', p[1], p[2])

def p_ifstmt(p):
    '''ifstmt : IF LPAREN boolexpr RPAREN LCURLY statements RCURLY
              | IF LPAREN boolexpr RPAREN LCURLY statements RCURLY ELSE statement SEMICOL
              | IF LPAREN boolexpr RPAREN LCURLY statements RCURLY ELSE LCURLY statements RCURLY'''
    if len(p) > 8:
        # Has an else
        # The ternary-like part differentiates where the stmt/stmts come from
        p[0] = ('IF', p[3], 'THEN', p[6], 
                'ELSE', p[10] if len(p) > 11 else p[9])
    else:
        p[0] = ('IF', p[3], 'THEN', p[6])

def p_type(p):
    'type : qualifiers INT'
    p[0] = (p[1], p[2])

def p_qualifiers(p):
    '''qualifiers : qualifier
                  | qualifier qualifiers'''
    if len(p) > 2:
        # second rule: more qualifiers following
        p[0] = p[2].append(p[1])
    else:
        p[0] = [p[1]]

def p_qualifier(p):
    'qualifier : CONST'
    p[0] = p[1]

def p_qualifier_epsilon(p):
    'qualifier : epsilon'
    pass

def p_vars(p):
    '''vars : ID EQUALS expr
            | ID COMMA vars
            | ID
            | ID EQUALS expr COMMA vars'''
    if len(p) == 2:
        # Just an ID
        p[0] = [p[1]]
    elif p[2] == 'EQUALS':
        # we are definitely assigning the ID
        if len(p) > 4:
            p[0] = p[5].append(('INSTANTIATE', p[1], p[3]))
        else:
            p[0] = [('INSTANTIATE', p[1], p[3])]
    #elif p[2] == 'COMMA':
    else:
        p[0] = p[3].append(p[1])

def p_boolexpr(p):
    '''boolexpr : expr LTHAN expr
                | expr GTHAN expr
                | expr EQUALSEQUALS expr'''
    p[0] = (p[2], p[0], p[3])

def p_expr(p):
    '''expr : term
            | term PLUS term
            | term MINUS term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_term(p):
    '''term : part
            | part TIMES part
            | part DIVIDE part
            | part LSHIFT part
            | part RSHIFT part'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_part(p):
    '''part : ID
            | NUM
            | LPAREN expr RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

# Represents an epsilon / lambda / empty string / etc
def p_epsilon(p):
    'epsilon : '

def p_error(p):
    print("Syntax error at '%s'" % p.value)

yacc.yacc()
parseTree = yacc.parse(lexer.datainput)

print(parseTree)

