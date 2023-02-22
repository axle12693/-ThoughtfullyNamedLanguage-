from objects import Token
from os import system


def gencode(ast: list[dict]) -> None:
    code = "int main() {"
    for i in ast:
        match i['type']:

            case 'VariableDeclaration':

                match i['datatype']:

                    case 'int':
                        code += f"int {i['value']};"

                    case 'str':
                        code += f"char {i['value']}[] = "

            case 'VariableAssignment':

                if type(i['value']) == str:
                    code += f"{i['value']};"
                else:
                    code += f"{i['name']} = {i['value']};"

    code += "return 0;}"

    with open('output.c', 'w') as cfile:
        cfile.write(code)

    system(f"cc output.c")

    return None


def runcode(ast: list[dict]):
    pass
