#include <iostream>
#include <string>

#pragma once

typedef struct Token {
    std::string type, val;
    Token(std::string t, std::string v) : type(t), val(v) {}
} Token;
