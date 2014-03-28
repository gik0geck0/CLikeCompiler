import ply.lex as lex

tokens = [
    'SUBJECT',
    'VERB',
    'NUMBER',
    'ADJECTIVE',
    'NOUN',
]

t_ignore = '\t\n'
t_SUBJECT = r'I|we|she|he'
t_VERB = r'ate|made|sold|bought|threw\ away'
t_ADJECTIVE = r'candy|chocolate|Rice\ Krispie'
t_NOUN = r'bars|bar'

# Has to be handled specially because tokens can contain spaces
def t_SPACE(t):
    '[ ]'
    pass

def t_NUMBER(t):
    '[1-9]\d*'
    t.value = int(t.value)
    return t

def t_error(t):
    print("Bad token: %s" % t)

lex.lex(debug = 1)
