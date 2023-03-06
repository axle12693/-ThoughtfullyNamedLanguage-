import os


def gencode(ast: list[dict]) -> None:
    intdecs = set()
    mallocs = set()
    code = generate_c_code(ast, intdecs, mallocs)

    write_to_file('output.c', code)

    if os.name != 'nt':
        compile_c_file()

    return None


def generate_c_code(ast: list[dict], intdecs: set, mallocs: set) -> str:
    code = "#include <stdlib.h>\n#include <string.h>\n\nint main() {"

    for i in ast:
        if i['type'] == 'VariableDeclaration':
            code = generate_variable_declaration_code(i, intdecs, mallocs, code)

        elif i['type'] == 'VariableAssignment':
            code = generate_variable_assignment_code(i, code)

    code = free_memory_allocated_by_mallocs(mallocs, code)

    code += "return 0;}"
    return code


def generate_variable_declaration_code(i: dict, intdecs: set, mallocs: set, code: str) -> str:
    if i['datatype'] == 'int':
        code = generate_int_variable_declaration_code(i, intdecs, code)
    elif i['datatype'] == 'str':
        code = generate_str_variable_declaration_code(i, mallocs, code)

    return code


def generate_int_variable_declaration_code(i: dict, intdecs: set, code: str) -> str:
    if i['value'] not in intdecs:
        code += f"int {i['value']};"
        intdecs.add(i['value'])
    return code


def generate_str_variable_declaration_code(i: dict, mallocs: set, code: str) -> str:
    if i['value'] not in mallocs:
        code += f"char *{i['value']} = malloc(256);"
        mallocs.add(i['value'])
    return code


def generate_variable_assignment_code(i: dict, code: str) -> str:
    if isinstance(i['value'], str):
        code += f"strcpy({i['name']}, {i['value']});"
    else:
        code += f"{i['name']} = {i['value']};"
    return code


def free_memory_allocated_by_mallocs(mallocs: set, code: str) -> str:
    for var_name in mallocs:
        code += f"free({var_name});"
    return code


def write_to_file(filename: str, code: str) -> None:
    with open(filename, 'w') as cfile:
        cfile.write(code)


def compile_c_file() -> None:
    os.system("cc output.c")