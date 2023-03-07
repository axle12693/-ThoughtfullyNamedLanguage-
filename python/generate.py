import os


def generate_c_code(ast):
    int_declarations = set()
    malloc_statements = set()
    code = "#include <stdlib.h>\n#include <string.h>\n\nint main() {"

    for node in ast:
        if node['type'] == 'VariableDeclaration':
            if node['datatype'] == 'int':
                if node['value'] not in int_declarations:
                    code += f"int {node['value']};"
                    int_declarations.add(node['value'])
            elif node['datatype'] == 'str':
                if node['value'] not in malloc_statements:
                    code += f"char *{node['value']} = malloc(256);"
                    malloc_statements.add(node['value'])
        elif node['type'] == 'VariableAssignment':
            if isinstance(node['value'], str):
                code += f"strcpy({node['name']}, {node['value']});"
            else:
                code += f"{node['name']} = {node['value']};"

    for variable in malloc_statements:
        code += f"free({variable});"

    code += "return 0;}"
    return code


def write_to_file(filename, code):
    with open(filename, 'w') as cfile:
        cfile.write(code)


def compile_c_file():
    if os.name != 'nt':
        os.system("cc output.c")


def gencode(ast):
    code = generate_c_code(ast)
    write_to_file('output.c', code)
    compile_c_file()