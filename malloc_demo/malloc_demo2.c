#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>

#define CHUNKSZ 0x410

int main(int argc, char **argv){
    char *ptr = NULL;
    char *tmp = NULL;
    ptr = (char *)malloc(CHUNKSZ);
    malloc(1); // top併合防止用(ここでは気にしなくて良い).
    free(ptr);
    ptr = NULL;
    return 0;    
}
