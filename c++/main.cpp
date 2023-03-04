#include "generate.cpp"
#include "newlexer.cpp"
#include "objects.cpp"
#include "parse.cpp"
#include <fstream>
#include <iostream>
#include <sstream>

std::string readfile(std::string filename) {
    std::ifstream f(filename);

    std::stringstream buffer;
    buffer << f.rdbuf();
    f.close();
    return buffer.str();
}

void printtokens(std::vector<Token> &tokens) {
    for (auto i : tokens) {
        std::cout << i.type << ": " << i.val << std::endl;
    }
}

void printast(std::vector<std::map<std::string, std::string>> &ast) {
    for (std::map<std::string, std::string> i : ast) {
        for (std::pair<std::string, std::string> j : i) {
            std::cout << j.first;
            std::cout << ": ";
            std::cout << j.second;
            std::cout << " ";
        }
        std::cout << std::endl << std::endl;
    }
}

int main(int argc, char *argv[]) {
    // Get the code
    if (argc <= 1) {
        std::cout << "Please provide file to compile";
        return 1;
    } else {
        std::string code = readfile(std::string(argv[1]));
        // Convert into tokens
        std::vector<Token> tokens = tokenize(code);
        // printtokens(tokens);
        // Do magic to get an ast and check syntax
        //std::vector<std::map<std::string, std::string>> ast = parse(tokens);
        // printast(ast);
        // Generate C code because why not
        //gencode(ast);
        return 0;
    }
    return 0;
}
