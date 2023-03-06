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

    all_tokens: list[Token] = []
    current_string = []
    string_pos = [0]
    current_number = []
    number_pos = [0]

    punct = False

    for k, i in enumerate(code):
        if i.isspace() or i == '\n':
            if ''.join(current_string) in data_types:
                token_type = token_types[0]
                token_value = ''.join(current_string)
                token_pos = (string_pos[0], k)
                all_tokens.append(Token(token_type, token_value, token_pos))
                current_string = []
            if current_string:
                token_type = token_types[4]
                token_value = ''.join(current_string)
                token_pos = (string_pos[0], k)
                all_tokens.append(Token(token_type, token_value, token_pos))
                current_string = []
            if current_number:
                token_type = token_types[3]
                token_value = ''.join(current_number)
                token_pos = (number_pos[0], k)
                all_tokens.append(Token(token_type, token_value, token_pos))
                current_number = []
            if i == '\n':
                token_type = token_types[5]
                token_value = 'null'
                token_pos = (k, k)
                all_tokens.append(Token(token_type, token_value, token_pos))
                current_string = []
                current_number = []
            punct = False
            continue
        if i in '+-*/':
            all_tokens.append(Token(token_types[1], i, (k, k+1)))
            continue
        if i == '=':
            all_tokens.append(Token(token_types[6], 'null', (k, k+1)))
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
        if i in '\'"':
            if punct:
                all_tokens.append(Token(token_types[4], ''.join(current_string), (string_pos[0], k)))
                current_string = []
            punct = not punct
            all_tokens.append(Token(token_types[2], i, (k, k+1)))
            continue
        raise TNLUnidentifiedToken(f"{i}")

    if len(current_string) != 0:
        all_tokens.append(Token(token_types[4], ''.join(
            current_string), (string_pos[0], k)))
    if len(current_number) != 0:
        all_tokens.append(Token(token_types[3], ''.join(
            current_number), (number_pos[0], k)))
    if all_tokens[-1].type != 'endstatement':
        all_tokens.append(Token(token_types[5], 'null', (k+1, k+1)))

    return all_tokens
