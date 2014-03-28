import ply.yacc as yacc
import keith_lexer

tokens = keith_lexer.tokens

def p_sentence(p):
    '''sentence : SUBJECT VERB object'''
    p[0] = (p[1], p[2], p[3])

def p_object(p):
    '''object : NUMBER ADJECTIVE NOUN
              | NUMBER NOUN'''
    if len(p) == 4:
        p[0] = (p[1], p[2], p[3])
    else:
        p[0] = (p[1], '', p[2])

def p_error(p):
    print("Syntax error at '%s'" % p.value)

def parse(input):
    return yacc.yacc().parse(input)
