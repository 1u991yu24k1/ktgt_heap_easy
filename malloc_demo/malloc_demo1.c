#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SIZE 0x10

int main(int argc, char **argv)
{
    char *ptr1, *ptr2, *ptr3;
     
    ptr1 = (char *)malloc(SIZE);
    strncpy(ptr1, "AAAAAAAAAAAAAAA", SIZE);
    ptr2 = (char *)malloc(SIZE);
    strncpy(ptr2, "BBBBBBBBBBBBBBB", SIZE);
    ptr3 = (char *)malloc(SIZE);
    strncpy(ptr3, "CCCCCCCCCCCCCCC", SIZE);
    return 0;    
}


