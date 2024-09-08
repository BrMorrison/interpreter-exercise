import ply.lex as lex
from enum import Enum
from dataclasses import dataclass
from typing import Any

class TokenType(Enum):
    # Constants
    INT = r'-?\d+'
    BOOL = r'true|false'
    ID = r'[a-zA-Z_][a-zA-Z_0-9]*'

    # Arithmetic
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    ASSIGN = r'='

    # Logic
    NEGATION = r'!'
    AND = r'&&'
    OR = r'\|\|'

    # Comparison
    EQ = r'=='
    NEQ = r'!='
    LEQ = r'<='
    GEQ = r'>='
    LT = r'<'
    GT = r'>'

    # Punctuation
    LPAREN = r'\('
    RPAREN = r'\)'
    LCURLY = r'\{'
    RCURLY = r'\}'
    SEMICOLON = r';'

    # Keywords
    IF = 'if'
    ELSE = 'else'
    WHILE = 'while'
    FOR = 'for'

    # Special End Of File token
    EOF = None


tokens = [name for name in TokenType.__members__.keys() if name != 'EOF']

# Keywords could be lexed as identifiers, so we call them out separately here
# so that we can manually mark them as the appropriate token.
keywords = {
    'if': TokenType.IF.name,
    'else': TokenType.ELSE.name,
    'while': TokenType.WHILE.name,
    'for': TokenType.FOR.name,
}

# Tokens that we don't want to auto generate lexing rules for
special_tokens = [TokenType.INT, TokenType.BOOL, TokenType.ID, TokenType.EOF] + list(keywords.values())

lex_rule_template = '''
t_{name} = r'{regex}'
'''

lex_rules = ""
for name, enum in TokenType.__members__.items():
    if enum not in special_tokens:
        lex_rules += lex_rule_template.format(name=name, regex=enum.value)

exec(lex_rules)

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # Keywords get lexed as IDs, so we have to undo that when we get one
    t.type = keywords.get(t.value, 'ID')
    return t

def t_INT(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

def t_BOOL(t):
    r'true|false'
    t.value = bool(t.value)
    return t

def t_eof(t):
    t.type = 'EOF'
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


@dataclass
class Token:
    type: TokenType
    value: Any


class Lexer:
    def __init__(self, program: str):
        self.lexer = lex.lex()
        self.lexer.input(program)
        self._next()
    
    def _next(self):
        raw_tok = next(self.lexer)
        self.next_tok = Token(TokenType.__members__[raw_tok.type], raw_tok.value)
    
    def next(self) -> Token:
        tok = self.next_tok
        self._next()
        return tok
    
    def get_line_number(self) -> int:
        return self.lexer.lineno
    
    def peek(self) -> Token:
        return self.next_tok
    

if __name__ == '__main__':
    test_data = '''
    i = 7;
    _foo87_ = 29;
    while (i <= 10) {
        i = i + 1;
    }
    if (i == _foo87_) {
        i = 0;
    } else {
    }
    '''

    lexer = Lexer(test_data)
    while (lexer.peek().type != TokenType.EOF):
        print(lexer.next())