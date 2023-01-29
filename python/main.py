import sys

import parse
import syntax


# Simple function to read a file
def readfile(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def main():
    code = readfile(sys.argv[1])
    ast = parse.parse(code)
    res = syntax.validate(ast)
    if type(res) == str:
        raise res
    elif res == True:
        pass

if __name__ == '__main__':
    main()