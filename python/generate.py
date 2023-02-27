from os import system, name


def gencode(ast: list[dict]) -> None:
    intdecs = []
    mallocs = []

    code = "#include <stdlib.h>\n#include <string.h>\n\nint main() {"
    for i in ast:
        match i['type']:

            case 'VariableDeclaration':

                match i['datatype']:

                    case 'int':
                        if i['value'] not in intdecs:
                            code += f"int {i['value']};"
                            intdecs.append(i['value'])

                    case 'str':
                        if i['value'] not in mallocs:
                            code += f"char *{i['value']} = malloc(256);"
                            mallocs.append(i['value'])

            case 'VariableAssignment':

                if type(i['value']) == str:
                    code += f"strcpy({i['name']}, {i['value']});"
                else:
                    code += f"{i['name']} = {i['value']};"

    for i in mallocs:
        code += f"free({i});"

    code += "return 0;}"

    with open('output.c', 'w') as cfile:
        cfile.write(code)

    if name != 'nt':
        system(f"cc output.c")

    return None
