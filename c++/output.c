#include <stdlib.h>
#include <string.h>

int main() {int x;x = 5;char *y = malloc(256);char *a = malloc(256);strcpy(y, "lol");strcpy(a, "lamoloserwannabe");free(y);free(a);return 0;}