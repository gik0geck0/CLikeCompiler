import ply.lex as lex
tokens = [
    'NAME',
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'EQUALS'
    ]

t_ignore    = ' \t'
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_EQUALS    = r'='
t_NAME      = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print("Bad token: %s" % t)

lex.lex()

data = "x = 3 * 4 + 5 * 6"
lex.input(data)

while True:
    tok = lex.token()
    if not tok: break
    print(tok)


