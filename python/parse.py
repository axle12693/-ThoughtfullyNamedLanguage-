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

    #types: list[str] = [i.type for i in tokens]
    #typestring: str = ' '.join(types)
    #values: list[str] = [i.val for i in tokens]
    #valuestring: str = ' '.join(values)

    intdec: list[int] = []
    strdec: list[int] = []
    endstm: list[int] = []
    assign: list[int] = []
    number: list[int] = []
    string: list[int] = []
    punct : list[int] = []

    for j, i in enumerate(tokens):
        if i.type == 'datatype' and i.val == 'int':
            intdec.append(j)
            continue
        if i.type == 'datatype' and i.val == 'str':
            strdec.append(j)
            continue
        if i.type == 'endstatement' and i.val == 'null':
            endstm.append(j)
            continue
        if i.type == 'assignment' and i.val == 'null':
            assign.append(j)
            continue
        if i.type == 'number' and i.val.isdigit():
            number.append(j)
            continue
        if i.type == 'string' and i.val == ascii_letters:
            string.append(j)
            continue
        if i.type == 'punctuator' and (i.val == "'" or i.val == '"'):
            punct.append(j)

    all = [intdec,strdec,endstm,assign,number,string,punct]

    tslice: int = 0
    tslicetype: str = None

    for k in range(len(tokens)):
        if k in intdec:
            tslice = k
        elif k in strdec:
            tslice = k
        elif k in endstm:
            tslice = k
        elif k in assign:
            tslice = k
        elif k in number:
            tslice = k
        elif k in string:
            tslice = k
        elif k in punct:
            tslice = k
        else:
            pass

        tslicetype = tokens[tslice].type

        if tslicetype == 'punctuator':
            pass
        
        for l in all:
            for m in l:
                if m+1 in l:
                    pass



    '''declaration = re.search(r'datatype string', typestring)
    if ismatch(declaration):
        print(declaration.group(0))
        print(declaration.start(0), declaration.end(0))'''


    return ast
