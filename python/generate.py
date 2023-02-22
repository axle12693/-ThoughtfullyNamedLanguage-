from objects import Token


def gencode(ast: list[dict]) -> None:
    code = "int main() {"
    for i in ast:
        match i['type']:

            case 'VariableDeclaration':

                match i['datatype']:

                    case 'int':
                        code += f"int {i['value']};"

                    case 'str':
                        code += f"char[] {i['value']};"

            case 'VariableAssignment':

                code += f"{i['name']} = {i['value']};"
    
    code += "return 0;}"

    with open('output.c', 'w') as cfile:
        cfile.write(code)
    
    return None


def runcode(ast: list[dict]):
    pass
