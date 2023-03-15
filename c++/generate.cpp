#include "objects.cpp"
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <vector>
#include <algorithm>

void gencode(std::vector<std::map<std::string, std::string>> &ast) {
    std::vector<std::string> intdecs;
    std::vector<std::string> mallocs;

    std::string code =
        "#include <stdlib.h>\n#include <string.h>\n\nint main() {";

    for (auto i : ast) {
        if (i["type"] == "VariableDeclaration") {

            if (i["datatype"] == "int" &&
                std::find(intdecs.begin(), intdecs.end(), i["value"]) ==
                    intdecs.end()) {
                code += ("int " + i["value"] + " = 0;");
                intdecs.push_back(i["value"]);
                continue;
            }

            if (i["datatype"] == "str" &&
                std::find(mallocs.begin(), mallocs.end(), i["value"]) ==
                    mallocs.end()) {
                code += ("char *" + i["value"] + " = (char*)malloc(256);");
                mallocs.push_back(i["value"]);
                continue;
            }

            continue;
        }

        if (i["type"] == "VariableAssignment") {
            if (i["datatype"] == "str") {
                code += ("strcpy(" + i["name"] + ", " + i["value"] + ");");
                continue;
            } else {
                code += (i["name"] + " = " + i["value"] + ";");
                continue;
            }
        }

        if (i["type"] == "Operation") {
            code += (i["v1"] + " = " + i["v2"] + " " + i["operator"] + " " + i["v3"] + ";");
        }
    }

    for (auto i : mallocs) {
        code += ("free(" + i + ");");
    }
    code += "return 0;}";

    std::ofstream cfile("output.c");
    if (cfile.is_open()) {
        cfile << code;
    }
    cfile.close();
}