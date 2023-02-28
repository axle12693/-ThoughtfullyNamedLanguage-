#include "error.cpp"
#include "objects.cpp"
#include <map>
#include <string>
#include <vector>

std::vector<std::string> token_types = {
    "datatype", "operator",     "punctuator", "number",
    "string",   "endstatement", "assignment", "rawstring"};

std::vector<std::string> data_types = {"int", "str"};

std::vector<Token> tokenize(std::string &code) {

    std::vector<Token> all_tokens;
    std::vector<std::string> strings;
    std::vector<char> current;

    bool punct = false;

    for (int k = 0; k < code.length(); k++) {
        std::string i(1, code[k]);
        if (i == " " || i == "\n") {
            if (current.size() != 0) {
                strings.push_back(std::string(current.begin(), current.end()));
                current.clear();
            }
            if (i == "\n") {
                strings.push_back("\n");
                current.clear();
            }
            punct = false;
            continue;
        }

        current.push_back(*i.data());
        continue;
    }

    if (current.size() != 0) {
        strings.push_back(std::string(current.begin(), current.end()));
        current.clear();
    }
    if (strings[strings.size() - 1] != "\n") {
        strings.push_back("\n");
    }

    for (auto i : strings) {
        
        if (std::binary_search(data_types.begin(), data_types.end(), i)) {
            all_tokens.push_back(Token("datatype", i));
            continue;
        }

        if ((i[0] == '\'' || i[0] == '"') && (i[i.size()-1] == '\'' || i[i.size()-1] == '"')) {
            auto i2 = i;
            all_tokens.push_back(Token("punctuator", std::string(1, i[0])));
            i2.erase(std::remove(i2.begin(), i2.end(), '"'), i2.end());
            i2.erase(std::remove(i2.begin(), i2.end(), '\''), i2.end());
            all_tokens.push_back(Token("string", i2));
            all_tokens.push_back(Token("punctuator", std::string(1, i[i.size()-1])));
            continue;
        }

        if (i.find_first_not_of("0123456789") == std::string::npos) {
            all_tokens.push_back(Token("number", i));
            continue;
        }

        if (i == "=") {
            all_tokens.push_back(Token("assignment", i));
            continue;
        }

        if (i == "\n") {
            all_tokens.push_back(Token("endstatement", "null"));
            continue;
        }

        all_tokens.push_back(Token("string", i));
    }

    return all_tokens;
}