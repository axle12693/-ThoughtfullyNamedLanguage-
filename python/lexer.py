import string
from objects import Token

token_types = [
    'datatype',
    'operator',
    'punctuator',
    'number',
    'string',
    'endstatement'
]

data_types = [
    'int',
    'str'
]

def tokenize(code: str) -> list[Token]:
    all_tokens: list[Token] = []
    current_string = []
    current_number = []
    for i in code:
        if i.isspace() or i == '\n':
            if len(current_string) != 0:
                all_tokens.append(Token(token_types[4], ''.join(current_string)))
                current_string = []
            if len(current_number) != 0:
                all_tokens.append(Token(token_types[3], ''.join(current_number)))
                current_number = []
            if i == '\n':
                all_tokens.append(Token(token_types[5], '0'))
                current_string = []
                current_number = []
                continue
        if i in '+-*/':
            all_tokens.append(Token(token_types[1], i))
            continue
        if i in '\'"':
            all_tokens.append(Token(token_types[2], i))
            continue
        if i.isdigit():
            current_number.append(i)
            continue
        if i in string.ascii_letters:
            current_string.append(i)
            continue

    if len(current_string) != 0:
        all_tokens.append(Token(token_types[4], ''.join(current_string)))
    if len(current_number) != 0:
        all_tokens.append(Token(token_types[3], ''.join(current_number)))

    return all_tokens
