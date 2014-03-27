
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
    p[0] = p[2].append(p[1])


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
    'varassign : SYMBOL EQUALS expr'
    p[0] = ('ASSIGN', p[1], p[3])

def p_vardecl(p):
    'vardecl : type vars'
    p[0] = ('DECLARE', p[1], p[2])

def p_ifstmt(p):
    '''ifstmt : IF LPAREN boolexpr RPAREN LCURLY stmts RCURLY
              | IF LPAREN boolexpr RPAREN LCURLY stmts RCURLY ELSE stmt SEMICOL
              | IF LPAREN boolexpr RPAREN LCURLY stmts RCURLY ELSE LCURLY stmts RCURLY'''
    if len(p) > 8:
        # Has an else
        # The ternary-like part differentiates where the stmt/stmts come from
        p[0] = ('IF', p[3], 'THEN', p[6], 
                'ELSE', p[10] if len(p) > 11 else p[9])
    else:
        p[0] = ('IF', p[3], 'THEN', p[6])

def p_type(p):
    'type : qualifiers INT'
    p[0]

def p_qualifiers(p):
    '''qualifiers : qualifier
                  | qualifier qualifiers'''

def p_qualifier(p):
    'qualifier : CONST'

def p_vars(p):
    '''vars : ID EQUALS expr
            | ID COMMA vars
            | ID
            | ID EQUALS expr COMMA vars'''

def p_boolexpr(p):
    '''boolexpr : expr LTHAN expr
                | expr GTHAN expr
                | expr EQUALS EQUALS expr'''

def p_expr(p):
    '''expr : term
            | term PLUS term
            | term MINUS term'''

def p_term(p):
    '''term : part
            | part TIMES part
            | part DIV part
            | part LSHIFT part
            | part RSHIFT part'''

def p_part(p):
    '''part : ID
            | NUM
            | LPAREN expr RPAREN'''

def p_error(p):
    print("Syntax error at '%s'" % p.value)

yacc.yacc()
parseTree = yacc.parse(mylexer.data)

print(parseTree)

