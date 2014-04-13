
import sys
import ply.lex as lex

# List of token names.   This is always required
tokens = (
    'NUM',

    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',

    'LSHIFT',
    'RSHIFT',

    'EQUALSEQUALS',
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

    'RETURN',
    'IF',
    'ELSE',
    'INT',
    'CONST',
    'ID',
)

# Regular expression rules for simple tokens
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'

#t_COMMENT   = r'//.*$'
t_DIVIDE    = r'/'
t_LSHIFT     = r'<<'
t_RSHIFT     = r'>>'

t_EQUALSEQUALS  = r'=='
t_EQUALS    = r'='
t_LTHAN     = r'<'
t_GTHAN     = r'>'

t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LCURLY    = r'{'
t_RCURLY    = r'}'

t_COMMA     = r','
t_SEMICOL   = r';'

# MAJOR NOTE:
# Rules defined only by string are added with the longest REGEX first.
# Functions, however, are added in the order they appear
# t_IF        = r'if'
# t_ELSE      = r'else'
# t_RETURN    = r'return'
# t_INT       = r'int'
# t_CONST     = r'const'
# 
# t_ID    = r'[a-zA-Z_][a-zA-Z0-9_]*'

# A regular expression rule with some action code
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.lexer.line_lexpos = t.lexpos

def t_ignore_COMMENT(t):
    r'//.*'
    pass

def t_IF(t):
    r'if'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_RETURN(t):
    r'return'
    return t

def t_INT(t):
    r'int'
    return t

def t_CONST(t):
    r'const'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

def find_column(input,token):
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
        last_cr = -1
    column = (token.lexpos - last_cr)
    return column

# Error handling rule
def t_error(t):
    print("Illegal character '%s' at line %d, column %d" % (t.value[0], t.lineno, find_column(datainput, t)))
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
datainput = sys.stdin.read()

if __name__ == '__main__':
    # Give it some data
    lexer.input(datainput)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: break      # No more input
