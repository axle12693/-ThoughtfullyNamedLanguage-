#include "error.cpp"
#include "objects.cpp"
// #include "lexer.cpp"
#include <algorithm>
#include <iostream>
#include <map>
#include <string>
#include <vector>

std::vector<std::string> allvar;

void vardec(std::vector<std::map<std::string, std::string>> &d,
            std::string type, Token &value) {
    std::map<std::string, std::string> d2;
    d2["type"] = "VariableDeclaration";
    d2["datatype"] = type;
    d2["value"] = value.getval();
    d.push_back(d2);
}

void varassign(std::vector<std::map<std::string, std::string>> &d,
               std::string type, Token &name, Token &value, int line) {

    if (std::find(allvar.begin(), allvar.end(), name.getval()) ==
        allvar.end()) {
        try {
            throw TNLUndelcaredVariable(
                "\n\nVariable " + std::string(name.getval()) +
                " assigned value before declaration on line " +
                std::to_string(line) + ".");
        } catch (const std::exception &e) {
            std::cerr << e.what() << '\n';
        }
    }

    std::map<std::string, std::string> d2;
    d2["type"] = "VariableAssignment";
    d2["datatype"] = type;
    d2["name"] = name.getval();
    d2["value"] = value.getval();
    d.push_back(d2);
}

std::vector<std::map<std::string, std::string>>
parse(std::vector<Token> tokens) {
    static std::vector<std::map<std::string, std::string>> ast = {};

    std::vector<Token> n3t;
    std::vector<Token> p2t;

    bool skip2 = false;
    int line = 1;

    for (int k = 0; k < tokens.size(); k++) {

        try {
            n3t = {tokens[k], tokens[k + 1], tokens[k + 2], tokens[k + 3]};
        } catch (const std::exception &e) {
            try {
                n3t = {tokens[k], tokens[k + 1], tokens[k + 2]};
            } catch (const std::exception &e) {
                try {
                    n3t = {tokens[k], tokens[k + 1]};
                } catch (const std::exception &e) {
                    n3t = {tokens[k]};
                }
            }
        }

        p2t = {tokens[k - 2], tokens[k - 1]};

        if (tokens[k].gettype() == "endstatement") {
            line++;
            continue;
        }
        if (skip2) {
            skip2 = false;
            continue;
        }

        if (n3t[0].gettype() == "datatype" && n3t[1].gettype() == "string") {
            allvar.push_back(n3t[1].getval());
            if (n3t[0].getval() == "int") {
                vardec(ast, "int", n3t[1]);
            } else if (n3t[0].getval() == "str") {
                vardec(ast, "str", n3t[1]);
            }
            continue;
        }

        if (n3t[0].gettype() == "string" && n3t[1].gettype() == "assignment" &&
            n3t[2].gettype() == "number") {
            varassign(ast, "int", n3t[0], n3t[2], line);
            continue;
        }

        if (n3t[0].gettype() == "string" && n3t[1].gettype() == "assignment" &&
            n3t[2].gettype() == "punctuator") {
            skip2 = true;
            continue;
        }

        if (n3t[0].gettype() == "punctuator" && n3t[1].gettype() == "string" &&
            n3t[2].gettype() == "punctuator" &&
            n3t[0].getval() == n3t[2].getval()) {
            Token rawstr("rawstring",
                         "\"" + std::string(n3t[1].getval()) + "\"");
            varassign(ast, "str", p2t[0], rawstr, line);
            continue;
        }

        if (n3t[0].gettype() == "datatype" &&
            (std::find(allvar.begin(), allvar.end(), n3t[1].getval()) ==
             allvar.end()) &&
            n3t[1].gettype() != "endstatement") {
            try {
                throw TNLSyntax(
                    "\n\nNon-alphabetic character in variable name on line " +
                    std::to_string(line) + ".");
            } catch (TNLSyntax &e) {
                std::cerr << e.what() << '\n';
            }
        }

        if (n3t[0].gettype() == "datatype" &&
            (std::find(allvar.begin(), allvar.end(), n3t[2].getval()) ==
             allvar.end()) &&
            n3t[1].gettype() == "number") {
            try {
                throw TNLSyntax(
                    "\n\nNon-alphabetic character in variable name on line " +
                    std::to_string(line) + ".");
            } catch (TNLSyntax &e) {
                std::cerr << e.what() << '\n';
            }
        }

        if (n3t[0].gettype() == "datatype" && n3t[1].gettype() != "string") {
            try {
                throw TNLSyntax(
                    "\n\nNon-alphabetic character in variable name on line " +
                    std::to_string(line) + ".");
            } catch (TNLSyntax &e) {
                std::cerr << e.what() << '\n';
            }
        }

        if (n3t[0].gettype() == "punctuator" && n3t[1].gettype() == "string" &&
            n3t[2].gettype() != "punctuator") {
            try {
                throw TNLSyntax("\n\nUnclosed quotes on line " +
                                std::to_string(line) + ".");
            } catch (TNLSyntax &e) {
                std::cerr << e.what() << '\n';
            }
        }

        if (n3t[0].gettype() == "punctuator" && n3t[1].gettype() == "string" &&
            n3t[2].gettype() == "punctuator" &&
            n3t[0].getval() != n3t[2].getval()) {
            try {
                throw TNLSyntax("\n\nUnmatched quotes on line " +
                                std::to_string(line) + ".");
            } catch (TNLSyntax &e) {
                std::cerr << e.what() << '\n';
            }
        }
    }

    return ast;
}