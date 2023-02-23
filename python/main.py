import sys

from objects import Token
import lexer
import parse
import generate

# Simple function to read a file


def readfile(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()

# Function to print the details of a list of tokens


def printtokens(tokens: list[Token]):
    for i in tokens:
        print(i.type, i.val, i.pos[0], i.pos[1])


def main():
    # Get the code
    code = readfile(sys.argv[1])
    # Convert into tokens
    tokens = lexer.tokenize(code)
    # printtokens(tokens)
    # Do magic to get an ast and check syntax
    ast = parse.parse(tokens)
    # print(ast)
    # Generate the C code because why not
    generate.gencode(ast)


if __name__ == '__main__':
    main()
