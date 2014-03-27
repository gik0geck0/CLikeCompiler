# Yaccing
# assign : NAME EQUALS expr
# expr  : expr PLUS term
#       | expr MINUS term
#       | term
# term  : term TIMES factor
#       | term DIVIDE factor
#       factor
# factor : NUMBER

import ply.yacc as yacc
import debeaz_pycon_example_lexer as mylexer

tokens = mylexer.tokens

def p_assign(p):
    '''assign : NAME EQUALS expr'''
    p[0] = ('ASSIGN', p[1], p[3])

def p_expr_opr(p):
    '''expr : expr PLUS term
            | expr MINUS term'''
    p[0] = (p[2], p[1], p[3])

def p_expr_term(p):
    '''expr : term'''
    p[0] = p[1]

def p_term_opr(p):
    '''term  : term TIMES factor
             | term DIVIDE factor'''
    p[0] = (p[2], p[1], p[3])

def p_term_factor(p):
    '''term : factor'''
    p[0] = p[1]

def p_factor(p):
    'factor : NUMBER'
    p[0] = ('NUM', p[1])

def p_error(p):
    print("Syntax error at '%s'" % p.value)

yacc.yacc()
parseTree = yacc.parse(mylexer.data)

print(parseTree)
print(type(parseTree))
