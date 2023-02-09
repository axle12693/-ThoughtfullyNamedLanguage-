from objects import Token
from string import ascii_letters
from error import TNLSyntax
import re

def ismatch(m) -> bool:
    if m == None:
        return False
    else:
        return True

def parse(tokens: list[Token]):
    ast = {}

    tslice: int = 0
    # Next 3 tokens
    n3t: list[Token] = None
    # Previous 2 tokens
    p2t: list[Token] = None

    skip2: bool = True

    for k in range(len(tokens)):
        tslice = k

        try:
            n3t = [tokens[tslice], tokens[tslice+1], tokens[tslice+2], tokens[tslice+3]]
        except IndexError:
            try:
                n3t = [tokens[tslice], tokens[tslice+1], tokens[tslice+2]]
            except IndexError:
                try:
                    n3t = [tokens[tslice], tokens[tslice+1]]
                except IndexError:
                    n3t = [tokens[tslice]]

        p2t = [tokens[tslice-2], tokens[tslice-1]]
        

        if skip2:
            skip2 = False
            continue
        if n3t[0].type == 'datatype' and n3t[1].type == 'string':
            print(f'declare var {n3t[1].val} of type {n3t[0].val}')
        if n3t[0].type == 'string' and n3t[1].type == 'assignment' and n3t[2].type == 'number':
            print(f'assign int {n3t[0].val} val {n3t[2].val}')
        if n3t[0].type == 'string' and n3t[1].type == 'assignment' and n3t[2].type == 'punctuator':
            skip2 = True
            continue
        if n3t[0].type == 'punctuator' and n3t[1].type == 'punctuator' and n3t[2].type == 'string':
            print(f'assign str {p2t[0].val} var {n3t[2].val}')
        



    return ast

'''if k in intdec:
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
pass'''

'''    intdec: list[int] = []
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
        if i.type == 'string' and i.val in ascii_letters:
            string.append(j)
            continue
        if i.type == 'punctuator' and (i.val == "'" or i.val == '"'):
            punct.append(j)

    all = [intdec,strdec,endstm,assign,number,string,punct]
'''

'''for l in all:
    for m in l:
        if m+1 in l:
            if n3t[0].type == 'datatype' and n3t[1].type == 'string':
                print(f'declare var {n3t[1].val} type {n3t[0].val}')
            if n3t[0].type == 'string' and n3t[1].type == 'assignment' and n3t[2].type == 'number':
                print(f'assign int {n3t[0].val} val {n3t[2].val}')
            if n3t[0].type == 'string' and n3t[1].type == 'assignment' and n3t[2].type == 'punctuator':
                print(f'assign str {n3t[0].val}')'''
            

'''declaration = re.search(r'datatype string', typestring)
if ismatch(declaration):
print(declaration.group(0))
print(declaration.start(0), declaration.end(0))'''
