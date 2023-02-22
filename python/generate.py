from objects import Token
from os import system


def gencode(ast: list[dict]) -> None:
    code = "#include <stdlib.h>\n#include <string.h>\n\nint main() {"
    for i in ast:
        match i['type']:

            case 'VariableDeclaration':

                match i['datatype']:
                    
                    case 'int':
                        code += f"int {i['value']};"
                        var = i['value']

                    case 'str':
                        code += f"char *{i['value']} = malloc(256);"

            case 'VariableAssignment':

                if type(i['value']) == str:
                    code += f"strcpy({i['name']}, {i['value']});"
                else:
                    code += f"{i['name']} = {i['value']};"

    code += "return 0;}"

    with open('output.c', 'w') as cfile:
        cfile.write(code)

    system(f"cc output.c")

    return None


def runcode(ast: list[dict]):
    pass
