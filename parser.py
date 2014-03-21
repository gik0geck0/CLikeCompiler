
import sys
import ply.lex as lex

# List of token names.   This is always required
tokens = (
    'NUMBER',

    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',

    'EQUALS',
    'LTHAN',
    'GTHAN',

    'LPAREN',
    'RPAREN',
    'LCURLY',
    'RCURLY',

    'COMMA',
    'COMMENT',
    'SEMICOL',
    'SYMBOL',
)

# Regular expression rules for simple tokens
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'

t_COMMENT   = r'//.*$'
t_DIVIDE    = r'/'

t_EQUALS    = r'='
t_LTHAN     = r'<'
t_GTHAN     = r'>'

t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LCURLY    = r'{'
t_RCURLY    = r'}'

t_COMMA     = r','
t_SEMICOL   = r';'
t_SYMBOL    = r'[a-zA-Z][a-zA-Z]*'

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Give it some data
lexer.input(sys.stdin.read())

# Tokenize
while True:
    tok = lexer.token()
    if not tok: break      # No more input
    print(tok)
