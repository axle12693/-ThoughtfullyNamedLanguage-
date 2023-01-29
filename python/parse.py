
class Tree:

    def __init__(self) -> None:
        self.all: list[Connection] = []

class Connection:

    def __init__(self, to, from_) -> None:
        self.to = to
        self.from_ = from_

class Thing:

    def __init__(self, tree: Tree, nexts: list, identifier: str) -> None:
        self.c: list[Connection] = []
        self.id = identifier
        if nexts != None:
            for i in nexts:
                self.c.append(Connection(i, self))
                tree.all.append(Connection(i, self))





def parse(code: str) -> Tree:
    ast = Tree()
    t2 = Thing(ast, None, '4')
    t1 = Thing(ast, [t2], 'x')
    print(ast.all)
    print(ast.all[0].from_.id)
    print(ast.all[0].to.id)
    return ast