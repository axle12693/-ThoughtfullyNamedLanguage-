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
    'assignment',
    'rawstring'
]

data_types = [
    'int',
    'str'
]


def tokenize(code: str) -> list[Token]:
    all_tokens = []
    current_string = ""
    string_pos = 0
    current_number = ""
    number_pos = 0

    for k, i in enumerate(code):
        if i.isspace() or i == '\n':
            if current_string and current_string in data_types:
                token_type = token_types[0]
                token_pos = (string_pos, k)
                all_tokens.append(Token(token_type, current_string, token_pos))
                current_string = ""
            elif current_string:
                token_type = token_types[4]
                token_pos = (string_pos, k)
                all_tokens.append(Token(token_type, current_string, token_pos))
                current_string = ""
            elif current_number:
                token_type = token_types[3]
                token_pos = (number_pos, k)
                all_tokens.append(Token(token_type, current_number, token_pos))
                current_number = ""
            if i == '\n':
                token_type = token_types[5]
                token_pos = (k, k)
                all_tokens.append(Token(token_type, 'null', token_pos))
        elif i in '+-*/':
            all_tokens.append(Token(token_types[1], i, (k, k+1)))
        elif i == '=':
            all_tokens.append(Token(token_types[6], 'null', (k, k+1)))
        elif i.isdigit():
            if not current_number:
                number_pos = k
            current_number += i
        elif i in string.ascii_letters:
            if not current_string:
                string_pos = k
            current_string += i
        elif i in '\'"':
            if current_string:
                all_tokens.append(Token(token_types[4], current_string, (string_pos, k)))
                current_string = ""
            all_tokens.append(Token(token_types[2], i, (k, k+1)))
        else:
            raise TNLUnidentifiedToken(f"{i}")

    if current_string:
        all_tokens.append(Token(token_types[4], current_string, (string_pos, k)))
    elif current_number:
        all_tokens.append(Token(token_types[3], current_number, (number_pos, k)))
    if all_tokens and all_tokens[-1].type != 'endstatement':
        all_tokens.append(Token(token_types[5], 'null', (k+1, k+1)))

    return all_tokens
