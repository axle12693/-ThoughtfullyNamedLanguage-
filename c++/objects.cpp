#include <ossp/uuid.h>
#include <iostream>
#include <string>

#pragma once

char* new_uuid(void) {
    uuid_t *uuid;
    char *str;
    uuid_create(&uuid);
    uuid_make(uuid, UUID_MAKE_V1);
    str = NULL;
    uuid_export(uuid, UUID_FMT_STR, &str, NULL);
    uuid_destroy(uuid);
    return str;
}

class Token {
    private:
        char* guid = new_uuid();
        std::string type;
        std::string val;

    public:
        Token(std::string type, std::string value) : type(type), val(value) {}

        std::string getval() { return val; }
        std::string gettype() { return type; }
};