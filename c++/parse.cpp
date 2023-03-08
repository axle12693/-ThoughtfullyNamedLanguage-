#include "error.cpp"
#include "objects.cpp"
//#include "newlexer.cpp"
#include <algorithm>
#include <iostream>
#include <map>
#include <string>
#include <vector>
#include <set>

std::map<std::string, std::string> allvar;

void vardec(std::vector<std::map<std::string, std::string>> &d,
            std::string type, Token &value) {

    allvar[value.val] = type;
    std::map<std::string, std::string> d2;
    d2["type"] = "VariableDeclaration";
    d2["datatype"] = type;
    d2["value"] = value.val;
    d.push_back(d2);
}

void varassign(std::vector<std::map<std::string, std::string>> &d,
               std::string type, Token &name, Token &value, int line) {


    if (allvar.find(name.val) == allvar.end()) {
        try {
            throw TNLUndelcaredVariable(
                "\n\nVariable " + std::string(name.val) +
                " assigned value before declaration on line " +
                std::to_string(line) + ".");
        } catch (const std::exception &e) {
            std::cerr << e.what() << '\n';
            std::exit(1);
        }
    }
    if (allvar[name.val] != type) {
        try {
            throw TNLMismatchedType("\n\nThe variable "+name.val+" has the type "+allvar[name.val]+", but was assigned type "+type+".");
        } catch (TNLMismatchedType &e) {
            std::cerr << e.what() << std::endl;
            std::exit(1);
        }
    }
    

    std::map<std::string, std::string> d2;
    d2["type"] = "VariableAssignment";
    d2["datatype"] = type;
    d2["name"] = name.val;
    d2["value"] = value.val;
    d.push_back(d2);
}

void operation(std::vector<std::map<std::string, std::string>> &d, Token &val);

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

        if (k > 3) {
            p2t = {tokens[k - 2], tokens[k - 1]};
        } else {
            p2t = {};
        }

        if (tokens[k].type == "endstatement") {
            line++;
            continue;
        }
        if (skip2) {
            skip2 = false;
            continue;
        }

        if (n3t[0].type == "datatype" && n3t[1].type == "string") {
            vardec(ast, n3t[0].val, n3t[1]);
            continue;
        }

        if (n3t[0].type == "string" && n3t[1].type == "assignment" &&
            n3t[2].type == "number") {
            varassign(ast, "int", n3t[0], n3t[2], line);
            continue;
        }

        if (n3t[0].type == "string" && n3t[1].type == "assignment" &&
            n3t[2].type == "punctuator") {
            skip2 = true;
            continue;
        }

        if (n3t[0].type == "punctuator" && n3t[1].type == "string" &&
            n3t[2].type == "punctuator" &&
            n3t[0].val == n3t[2].val) {
            Token rawstr("rawstring",
                         "\"" + std::string(n3t[1].val) + "\"");
            varassign(ast, "str", p2t[0], rawstr, line);
            continue;
        }

        if (n3t[0].type == "datatype" &&
            (allvar.find(n3t[1].val) == allvar.end()) &&
            n3t[1].type != "endstatement") {
            try {
                throw TNLSyntax(
                    "\n\nNon-alphabetic character in variable name on line " +
                    std::to_string(line) + ".");
            } catch (TNLSyntax &e) {
                std::cerr << e.what() << '\n';
                std::exit(1);
            }
        }

        if (n3t[0].type == "datatype" &&
            (allvar.find(n3t[2].val) == allvar.end()) &&
            n3t[1].type == "number") {
            try {
                throw TNLSyntax(
                    "\n\nNon-alphabetic character in variable name on line " +
                    std::to_string(line) + ".");
            } catch (TNLSyntax &e) {
                std::cerr << e.what() << '\n';
                std::exit(1);
            }
        }

        if (n3t[0].type == "datatype" && n3t[1].type != "string") {
            try {
                throw TNLSyntax(
                    "\n\nNon-alphabetic character in variable name on line " +
                    std::to_string(line) + ".");
            } catch (TNLSyntax &e) {
                std::cerr << e.what() << '\n';
                std::exit(1);
            }
        }

        if (n3t[0].type == "punctuator" && n3t[1].type == "string" &&
            n3t[2].type != "punctuator") {
            try {
                throw TNLSyntax("\n\nUnclosed quotes on line " +
                                std::to_string(line) + ".");
            } catch (TNLSyntax &e) {
                std::cerr << e.what() << '\n';
                std::exit(1);
            }
        }

        if (n3t[0].type == "punctuator" && n3t[1].type == "string" &&
            n3t[2].type == "punctuator" &&
            n3t[0].val != n3t[2].val) {
            try {
                throw TNLSyntax("\n\nUnmatched quotes on line " +
                                std::to_string(line) + ".");
            } catch (TNLSyntax &e) {
                std::cerr << e.what() << '\n';
                std::exit(1);
            }
        }
    }

    return ast;
}