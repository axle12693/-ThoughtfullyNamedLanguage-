from objects import Token
from lexer import token_types
import error


intvar: list[str] = []
strvar: list[str] = []
allvar: list[str] = []


def vardec(d: list, start: int, end: int, type: str, value: Token) -> None:
    d2 = {}
    d2['type'] = 'VariableDeclaration'
    d2['start'] = start
    d2['end'] = end
    d2['datatype'] = type
    d2['value'] = value.val
    d.append(d2)


def assign(d: list, start: int, end: int, name: Token, value: Token, line: int) -> None:

    if name.val not in allvar:
        raise error.TNLUndeclaredVariable(
            f"\n\nVariable {name.val} assigned value before declaration on line {line}.")

    d2 = {}
    d2['type'] = 'VariableAssignment'
    d2['start'] = start
    d2['end'] = end
    d2['name'] = name.val
    try:
        d2['value'] = int(value.val)
    except ValueError:
        d2['value'] = value.val
    d.append(d2)


def parse(tokenlist: list[Token]):
    tokens = tokenlist
    ast = []

    tslice: int = 0
    # Next 3 tokens
    n3t: list[Token] = None
    # Previous 2 tokens
    p2t: list[Token] = None

    skip2: bool = False
    line = 1

    for k in range(len(tokens)):
        tslice = k
        global allvar
        allvar = intvar+strvar

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
            if n3t[0].val == 'int':
                intvar.append(n3t[1].val)
                vardec(ast, n3t[0].pos[0], n3t[1].pos[1], 'int', n3t[1])
            elif n3t[0].val == 'str':
                strvar.append(n3t[1].val)
                vardec(ast, n3t[0].pos[0], n3t[1].pos[1], 'str', n3t[1])
            continue

        if n3t[0].type == 'string' and n3t[1].type == 'assignment' and n3t[2].type == 'number':
            assign(ast, n3t[0].pos[0], n3t[2].pos[1], n3t[0], n3t[2], line)
            continue

        if n3t[0].type == 'string' and n3t[1].type == 'assignment' and n3t[2].type == 'punctuator':
            skip2 = True
            continue

        if n3t[0].type == 'punctuator' and n3t[1].type == 'string' and n3t[2].type == 'punctuator' and n3t[0].val == n3t[2].val:
            rawstr = Token('rawstring', '"' +
                           n3t[1].val+'"', (n3t[0].pos[0], n3t[2].pos[1]))
            assign(ast, rawstr.pos[0], rawstr.pos[1], p2t[0], rawstr, line)
            continue

        # Syntax checking

        if n3t[0].type == 'string' and (n3t[0] in intvar or n3t[0] in strvar) and n3t[1].type != 'endstatement':
            raise error.TNLSyntax(
                f"\n\nNon-alphabetic character in variable name on line {line}")

        for i in token_types:
            if n3t[0].type == 'datatype' and n3t[1].type == i and i != 'string':
                raise error.TNLSyntax(
                    f"\n\nNon-alphabetic character in variable name on line {line}")

        if n3t[0].type == 'punctuator' and n3t[1].type == 'string' and not n3t[2].type == 'punctuator':
            raise error.TNLSyntax(f"\n\nUnclosed string on line {line}")

        if n3t[0].type == 'punctuator' and n3t[1].type == 'string' and n3t[2].type == 'punctuator' and n3t[0].val != n3t[2].val:
            raise error.TNLSyntax(f"\n\n Unmatched quotes on line {line}")

    return ast
