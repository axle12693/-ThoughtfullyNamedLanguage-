#include "error.cpp"
#include "objects.cpp"
#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <map>
#include <string>
#include <vector>

std::vector<std::string> token_types = {
    "datatype",     "operator",   "punctuator", "number",   "string",
    "endstatement", "assignment", "operator",   "rawstring"};

std::vector<std::string> data_types = {"int", "str"};

std::string numbers = "0123456789";
std::string letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
std::vector<std::string> operators = {"*", "+", "-", "/"};

Token check_string(std::string str) {
    if (str.length() > 1) {
        if (std::binary_search(data_types.begin(), data_types.end(), str)) {
            return Token("datatype", str);
        }
    }

    if (str == "'" || str == "\"") {
        return Token("punctuator", str);
    }

    if (str.find_first_not_of(numbers) == std::string::npos) {
        return Token("number", str);
    }

    if (str == "=") {
        return Token("assignment", "null");
    }

    if (std::binary_search(operators.begin(), operators.end(), str)) {
        return Token("operator", str);
    }

    if (str == "\n") {
        return Token("endstatement", "null");
    }

    if (str.find_first_not_of(letters) == std::string::npos) {
        return Token("string", str);
    }

    try {
        throw TNLUnidentifiedToken("\n\nUnidentified token " + str + ".");
    } catch (TNLUnidentifiedToken &e) {
        std::cerr << e.what() << std::endl;
        std::exit(1);
    }
}

std::vector<Token> tokenize(std::string &code) {

    std::vector<Token> all_tokens;
    std::vector<std::string> strings;
    std::vector<char> current;
    if (code[code.length() - 1] != '\n') {
        code.push_back('\n');
    }

    for (int k = 0; k < code.length(); k++) {
        std::string i(1, code[k]);
        if (i == " " || i == "\n") {
            if (current.size() != 0) {
                all_tokens.push_back(
                    check_string(std::string(current.begin(), current.end())));
            }
            current.clear();
            if (i == "\n") {
                all_tokens.push_back(Token("endstatement", "null"));
            }
            continue;
        }

        if ((i == "'" || i == "\"")) {
            if (current.size() != 0) {
                all_tokens.push_back(
                    check_string(std::string(current.begin(), current.end())));
            }
            current.clear();
            all_tokens.push_back(check_string(std::string(i)));
            continue;
        }

        current.push_back(*i.data());
        continue;
    }

    return all_tokens;
}