from objects import Token, Tree

def parse(tokens: list[Token]) -> Tree:
    ast = Tree()
    ast.append(Token('int', uuid=1))
    ast.append(Token('x'))
    ast.append(Token('5'))
    
    ast.connect('0', 'int', 'generic')
    ast.connect('int', 'x', 'type')
    ast.connect('x', '5', 'value')

    ast.append(Token('int', uuid=2))
    ast.append(Token('y'))
    ast.append(Token('6'))

    ast.connect('0', 'int', 'generic')
    ast.connect('int', 'y', 'type')
    ast.connect('y', '6', 'value')

    for a in ast.all:
        for b in a.c:
            print(f"There is a connection from {b.from_} ({a.uuid}) to {b.to} of type '{b.r}'")


    return ast

