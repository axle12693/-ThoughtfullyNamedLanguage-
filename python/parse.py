from objects import Token
from lexer import token_types
from error import TNLSyntax

def register(d: dict, subcat: str, start: int, end: int, **kwargs):
    value = kwargs.get('value')
    d[subcat] = {}
    d[subcat]['start'] = start
    d[subcat]['end'] = end


def parse(tokenlist: list[Token]):
    tokens = tokenlist
    ast = {}

    tslice: int = 0
    # Next 3 tokens
    n3t: list[Token] = None
    # Previous 2 tokens
    p2t: list[Token] = None

    intvar = []
    strvar = []

    skip2: bool = False
    line = 1

    for k in range(len(tokens)):
        tslice = k

        try:
            n3t = [tokens[tslice], tokens[tslice+1],
                   tokens[tslice+2], tokens[tslice+3]]
        except IndexError:
            try:
                n3t = [tokens[tslice], tokens[tslice+1], tokens[tslice+2]]
            except IndexError:
                try:
                    n3t = [tokens[tslice], tokens[tslice+1]]
                except IndexError:
                    n3t = [tokens[tslice]]

        p2t = [tokens[tslice-2], tokens[tslice-1]]

        if tokens[tslice].type == 'endstatement':
            line += 1
        if skip2:
            skip2 = False
            continue

        if n3t[0].type == 'datatype' and n3t[1].type == 'string':
            print(f'declare var {n3t[1].val} of type {n3t[0].val}')
            if n3t[0].val == 'int':
                intvar.append(n3t[1])
                register(ast, 'VariableDeclaration', n3t[0].pos[0], n3t[1].pos[1])
            elif n3t[0].val == 'str':
                strvar.append(n3t[1])
            continue

        if n3t[0].type == 'string' and n3t[1].type == 'assignment' and n3t[2].type == 'number':
            print(f'assign int {n3t[0].val} val {n3t[2].val}')
            continue

        if n3t[0].type == 'string' and n3t[1].type == 'assignment' and n3t[2].type == 'punctuator':
            skip2 = True
            continue

        if n3t[0].type == 'punctuator' and n3t[1].type == 'string' and n3t[2].type == 'punctuator' and n3t[0].val == n3t[2].val:
            print(
                f'assign str {p2t[0].val} var {n3t[0].val+n3t[1].val+n3t[2].val}')
            continue
                

        # Syntax checking

        if n3t[0].type == 'string' and (n3t[0] in intvar or n3t[0] in strvar) and n3t[1].type != 'endstatement':
            raise TNLSyntax(
                    f"\n\nNon-alphabetic character in variable name on line {line}")

        for i in token_types:
            if n3t[0].type == 'datatype' and n3t[1].type == i and i != 'string':
                raise TNLSyntax(
                    f"\n\nNon-alphabetic character in variable name on line {line}")

        if n3t[0].type == 'punctuator' and n3t[1].type == 'string' and not n3t[2].type == 'punctuator':
            raise TNLSyntax(f"\n\nUnclosed string on line {line}")

        if n3t[0].type == 'punctuator' and n3t[1].type == 'string' and n3t[2].type == 'punctuator' and n3t[0].val != n3t[2].val:
            raise TNLSyntax(f"\n\n Unmatched quotes on line {line}")


    return ast