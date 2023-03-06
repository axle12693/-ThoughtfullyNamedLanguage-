from objects import Token
from lexer import token_types
import error


intvar: list[str] = []
strvar: list[str] = []
allvar: list[str] = []


def vardec(d: list, start: int, end: int, datatype: str, value: Token) -> None:
    d.append({
        'type': 'VariableDeclaration',
        'start': start,
        'end': end,
        'datatype': datatype,
        'value': value.val
    })


def assign(d: list, start: int, end: int, name: Token, value: Token, line: int) -> None:
    if name.val not in allvar:
        raise error.TNLUndeclaredVariable(f"\n\nVariable {name.val} assigned value before declaration on line {line}.")
    d2 = {
        'type': 'VariableAssignment',
        'start': start,
        'end': end,
        'name': name.val
    }
    
    try:
        d2['value'] = int(value.val)
    except ValueError:
        d2['value'] = value.val
    d.append(d2)


def check_syntax(n3t, line):
    if n3t[0].type == 'string' and (n3t[0].val in intvar or n3t[0].val in strvar) and n3t[1].type != 'endstatement':
        raise error.TNLSyntax(f"\n\nNon-alphabetic character in variable name on line {line}")

    if n3t[0].type == 'number' and (n3t[1].val in intvar or n3t[1].val in strvar) and n3t[1].type == 'string':
        raise error.TNLSyntax(f"\n\nNon-alphabetic character in variable name on line {line}")

    for i in token_types:
        if n3t[0].type == 'datatype' and n3t[1].type == i and i != 'string':
            raise error.TNLSyntax(f"\n\nNon-alphabetic character in variable name on line {line}")

    if n3t[0].type == 'punctuator' and n3t[1].type == 'string' and not n3t[2].type == 'punctuator':
        raise error.TNLSyntax(f"\n\nUnclosed string on line {line}")

    if n3t[0].type == 'punctuator' and n3t[1].type == 'string' and n3t[2].type == 'punctuator' and n3t[0].val != n3t[2].val:
        raise error.TNLSyntax(f"\n\n Unmatched quotes on line {line}")


def parse(tokens: list[Token]):
    global allvar, intvar, strvar
    ast = []

    skip2: bool = False
    line = 1

    num_tokens = len(tokens)

    for i in range(num_tokens):
        allvar = intvar+strvar

        n3t = tokens[i:min(i + 4, num_tokens)]

        p2t = [tokens[i-2], tokens[i-1]]

        if tokens[i].type == 'endstatement':
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
            else:
                raise Exception("Unspecified Exception type - decide later")
            continue

        if n3t[0].type == 'string' and n3t[1].type == 'assignment':
            if n3t[2].type == 'number':
                assign(ast, n3t[0].pos[0], n3t[2].pos[1], n3t[0], n3t[2], line)
            elif n3t[2].type == 'punctuator':
                skip2 = True
            else:
                raise Exception("Unspecified Exception type - decide later")
            continue

        if n3t[0].type == 'punctuator' and n3t[1].type == 'string' and n3t[2].type == 'punctuator' and n3t[0].val == n3t[2].val:
            rawstr = Token('rawstring', '"' + n3t[1].val+'"', (n3t[0].pos[0], n3t[2].pos[1]))
            assign(ast, rawstr.pos[0], rawstr.pos[1], p2t[0], rawstr, line)
            continue

        # Syntax checking
        check_syntax(n3t, line)


    return ast
