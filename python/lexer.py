import string
from objects import Token
from error import TNLUnidentifiedToken, TNLSyntax

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
    current_number = ""

    if len(code) == 0:
        raise TNLSyntax("Error: Empty code string.")

    for i, char in enumerate(code):
        if char.isspace() or char == '\n':
            if current_string:
                if current_string in data_types:
                    token_type = token_types[0]
                else:
                    token_type = token_types[4]
                token_pos = (i - len(current_string), i)
                all_tokens.append(Token(token_type, current_string, token_pos))
                current_string = ""
            elif current_number:
                token_type = token_types[3]
                token_pos = (i - len(current_number), i)
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
            current_number += char
        elif char in string.ascii_letters:
            current_string += char
        elif char in '\'"':
            if current_string:
                token_pos = (i - len(current_string), i)
                all_tokens.append(Token(token_types[4], current_string, token_pos))
                current_string = ""
            all_tokens.append(Token(token_types[2], char, (i, i+1)))
        else:
            raise TNLUnidentifiedToken(f"{char}")

    if current_string:
        token_pos = (i - len(current_string) + 1, i + 1)
        all_tokens.append(Token(token_types[4], current_string, token_pos))
    elif current_number:
        token_pos = (i - len(current_number) + 1, i + 1)
        all_tokens.append(Token(token_types[3], current_number, token_pos))
    if all_tokens and all_tokens[-1].type != 'endstatement':
        all_tokens.append(Token(token_types[5], 'null', (i+1, i+1)))

    return all_tokens