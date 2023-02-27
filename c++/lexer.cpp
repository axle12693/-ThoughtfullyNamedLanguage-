#include "error.cpp"
#include "objects.cpp"
#include <map>
#include <string>
#include <vector>

std::vector<std::string> token_types = {
    "datatype", "operator",     "punctuator", "number",
    "string",   "endstatement", "assignment", "rawstring"};

std::vector<std::string> data_types = {"int", "str"};

bool isNumber(const std::string &s) {
    for (char const &ch : s) {
        if (std::isdigit(ch) == 0)
            return false;
    }
    return true;
}

std::vector<Token> tokenize(std::string &code) {

    std::vector<Token> all_tokens;
    std::vector<char> current_string;
    std::vector<char> current_number;

    bool punct = false;

    for (int k = 0; k < code.length(); k++) {
        std::string i(1, code[k]);
        if (i == " " or i == "\n") {

            for (auto j : data_types) {
                if (std::string(current_string.begin(), current_string.end()) ==
                    j) {
                    all_tokens.push_back(
                        Token("datatype", std::string(current_string.begin(),
                                                      current_string.end())));
                    current_string.clear();
                    continue;
                }
            }
            if (current_string.size() != 0) {
                all_tokens.push_back(
                    Token("string", std::string(current_string.begin(),
                                                current_string.end())));
                current_string.clear();
            }
            if (current_number.size() != 0) {
                all_tokens.push_back(
                    Token("number", std::string(current_number.begin(),
                                                current_number.end())));
                current_number.clear();
            }
            if (i == "\n") {
                all_tokens.push_back(Token("endstatement", "null"));
                current_string.clear();
                current_number.clear();
            }
            punct = false;
            continue;
        }

        if (i == "+" or i == "-" or i == "*" or i == "/") {
            all_tokens.push_back(Token("operator", i));
            continue;
        }

        if (i == "=") {
            all_tokens.push_back(Token("assignment", "null"));
            continue;
        }

        if (isNumber(i)) {
            current_number.push_back(*i.data());
            continue;
        }

        if (std::isalpha(*i.data())) {
            current_string.push_back(*i.data());
            continue;
        }

        if (i == "'" || i == "\"") {
            if (!punct) {
                punct = true;
                all_tokens.push_back(Token("punctuator", i));
                continue;
            }
            if (punct) {
                punct = false;
                all_tokens.push_back(
                    Token("string", std::string(current_string.begin(),
                                                current_string.end())));
                current_string.clear();
                all_tokens.push_back(Token("punctuator", i));
                continue;
            }
        }

        if (true) {
            throw TNLUnidentifiedToken("\n\nUnidentified token " + i + ".");
        }
    }

    if (current_string.size() != 0) {
        all_tokens.push_back(
            Token("string",
                  std::string(current_string.begin(), current_string.end())));
        current_string.clear();
    }
    if (current_number.size() != 0) {
        all_tokens.push_back(
            Token("number",
                  std::string(current_number.begin(), current_number.end())));
        current_number.clear();
    }
    if (all_tokens[all_tokens.size() - 1].gettype() != "endstatement") {
        all_tokens.push_back(Token("endstatement", "null"));
    }

    return all_tokens;
}