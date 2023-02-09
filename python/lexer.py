import string
from objects import Token
from error import TNLUnidentifiedToken

token_types = [
    'datatype',
    'operator',
    'punctuator',
    'number',
    'string',
    'endstatement',
    'assignment'
]

data_types = [
    'int',
    'str'
]

def tokenize(code: str) -> list[Token]:
    all_tokens: list[Token] = []
    current_string = []
    string_pos = [0]
    current_number = []
    number_pos = [0]
    for k, i in enumerate(code):
        if i.isspace() or i == '\n':
            for j in data_types:
                if ''.join(current_string) == j:
                    all_tokens.append(Token(token_types[0], ''.join(current_string), (string_pos[0], k)))
                    current_string = []
                    continue
            if len(current_string) != 0:
                all_tokens.append(Token(token_types[4], ''.join(current_string), (string_pos[0], k)))
                current_string = []
            if len(current_number) != 0:
                all_tokens.append(Token(token_types[3], ''.join(current_number), (number_pos[0], k)))
                current_number = []
            if i == '\n':
                all_tokens.append(Token(token_types[5], 'null', (k, k)))
                current_string = []
                current_number = []
            continue
        if i in '+-*/':
            all_tokens.append(Token(token_types[1], i, (k, k+1)))
            continue
        if i == '=':
            all_tokens.append(Token(token_types[6], 'null', (k, k+1)))
            continue
        if i in '\'"':
            all_tokens.append(Token(token_types[2], i, (k, k+1)))
            continue
        if i.isdigit():
            if len(current_number) == 0:
                number_pos[0] = k
            current_number.append(i)
            continue
        if i in string.ascii_letters:
            if len(current_string) == 0:
                string_pos[0] = k
            current_string.append(i)
            continue
        if True:
            raise TNLUnidentifiedToken(f"{i}")

    if len(current_string) != 0:
        all_tokens.append(Token(token_types[4], ''.join(current_string), (string_pos[0], k)))
    if len(current_number) != 0:
        all_tokens.append(Token(token_types[3], ''.join(current_number), (number_pos[0], k)))
    if all_tokens[-1].type != 'endstatement':
        all_tokens.append(Token(token_types[5], 'null', (k+1, k+1)))

    return all_tokens
