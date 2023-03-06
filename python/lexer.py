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

    for i, char in enumerate(code):
        if char.isspace() or char == '\n':
            if current_string and current_string in data_types:
                token_type = token_types[0]
                token_pos = (string_pos, i)
                all_tokens.append(Token(token_type, current_string, token_pos))
                current_string = ""
            elif current_string:
                token_type = token_types[4]
                token_pos = (string_pos, i)
                all_tokens.append(Token(token_type, current_string, token_pos))
                current_string = ""
            elif current_number:
                token_type = token_types[3]
                token_pos = (number_pos, i)
                all_tokens.append(Token(token_type, current_number, token_pos))
                current_number = ""
            if char == '\n':
                token_type = token_types[5]
                token_pos = (i, i)
                all_tokens.append(Token(token_type, 'null', token_pos))
        elif char in '+-*/':
            all_tokens.append(Token(token_types[1], char, (i, i+1)))
        elif char == '=':
            all_tokens.append(Token(token_types[6], 'null', (i, i+1)))
        elif char.isdigit():
            if not current_number:
                number_pos = i
            current_number += char
        elif char in string.ascii_letters:
            if not current_string:
                string_pos = i
            current_string += char
        elif char in '\'"':
            if current_string:
                all_tokens.append(Token(token_types[4], current_string, (string_pos, i)))
                current_string = ""
            all_tokens.append(Token(token_types[2], char, (i, i+1)))
        else:
            raise TNLUnidentifiedToken(f"{char}")

    if current_string:
        all_tokens.append(Token(token_types[4], current_string, (string_pos, i)))
    elif current_number:
        all_tokens.append(Token(token_types[3], current_number, (number_pos, i)))
    if all_tokens and all_tokens[-1].type != 'endstatement':
        all_tokens.append(Token(token_types[5], 'null', (i+1, i+1)))

    return all_tokens
