#include <stdlib.h>
#include <string.h>

int main() {int x;x = 5;x = 2 + 3;char *y = (char*)malloc(256);char *a = (char*)malloc(256);strcpy(y, "lol");strcpy(a, "lamoloserwannabe");free(y);free(a);return 0;}