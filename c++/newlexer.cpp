#include "error.cpp"
#include "objects.cpp"
#include <map>
#include <string>
#include <vector>

std::vector<std::string> token_types = {
    "datatype", "operator",     "punctuator", "number",
    "string",   "endstatement", "assignment", "rawstring"};

std::vector<std::string> data_types = {"int", "str"};

Token check_string(std::string str) {
    if (std::binary_search(data_types.begin(), data_types.end(), str)) {
        return Token("datatype", str);
    }

    if (str == "'" || str == "\"") {
        return Token("punctuator", str);
    }

    if (str.find_first_not_of("1234567890") == std::string::npos) {
        return Token("number", str);
    }

    if (str == "=") {
        return Token("assignment", "null");
    }

    if (str == "\n") {
        return Token("endstatement", "null");
    }

    return Token("string", str);
}

std::vector<Token> tokenize(std::string &code) {

    std::vector<Token> all_tokens;
    std::vector<std::string> strings;
    std::vector<char> current;

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