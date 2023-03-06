import os


def gencode(ast: list[dict]) -> None:
    intdecs = set()
    mallocs = set()

    code = "#include <stdlib.h>\n#include <string.h>\n\nint main() {"
    for i in ast:
        if i['type'] == 'VariableDeclaration':
            if i['datatype'] == 'int':
                if i['value'] not in intdecs:
                    code += f"int {i['value']};"
                    intdecs.add(i['value'])
            elif i['datatype'] == 'str':
                if i['value'] not in mallocs:
                    code += f"char *{i['value']} = malloc(256);"
                    mallocs.add(i['value'])

        elif i['type'] == 'VariableAssignment':
            if isinstance(i['value'], str):
                code += f"strcpy({i['name']}, {i['value']});"
            else:
                code += f"{i['name']} = {i['value']};"

    for var_name in mallocs:
        code += f"free({var_name});"

    code += "return 0;}"

    with open('output.c', 'w') as cfile:
        cfile.write(code)

    if os.name != 'nt':
        os.system("cc output.c")

    return None