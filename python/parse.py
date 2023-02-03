from objects import Token
from string import ascii_letters
import re

def ismatch(m) -> bool:
    if m == None:
        return False
    else:
        return True

def parse(tokens: list[Token]):
    ast = {}

    types = [i.type for i in tokens]
    typestring = ' '.join(types)
    values = [i.val for i in tokens]
    valuestring = ' '.join(values)

    intdec = []
    strdec = []
    endstm = []
    assign = []
    string = []

    for i, j in enumerate(tokens):
        if j.type == 'datatype' and j.val == 'int':
            intdec.append(i)
            continue
        if j.type == 'datatype' and j.val == 'str':
            strdec.append(i)
            continue
        if j.type == 'endstatement' and j.val == 'null':
            endstm.append(i)
            continue
        if j.type == ''
        if j.type == 'string' and j.val == ascii_letters:
            string.append(i)
            continue

    '''declaration = re.search(r'datatype string', typestring)
    if ismatch(declaration):
        print(declaration.group(0))
        print(declaration.start(0), declaration.end(0))'''


    return ast
