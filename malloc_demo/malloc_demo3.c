#define _GNU_SOURCE

#include <stdio.h>
#include <malloc.h>

#define USA 0x90
#define USB 0x120
#define LISTNUM 8
#define LISTMAX 7

char *ptr_array_unsortedbin_A[LISTNUM];
char *ptr_array_unsortedbin_B[LISTNUM];

int main(int argc, char **argv){
    char *tmp1, *tmp2;
    int i;
    for(i = 0; i < LISTNUM; i++){
        ptr_array_unsortedbin_A[i] = (char *)malloc(USA); 
    }
    tmp1 = (char *)malloc(1); // Dummy用ここでは関係無い.(topの併合を防ぐために意図的に入れている)
    
    for(i = 0; i < LISTNUM; i++){
        ptr_array_unsortedbin_B[i] = (char *)malloc(USB); 
    }
    tmp2 = (char *)malloc(1); // Dummy用ここでは関係無い.(topの併合を防ぐために意図的に入れている)
    
    for(i = 0; i < LISTNUM; i++){
        free(ptr_array_unsortedbin_A[i]);
    }
    for(i = 0; i < LISTNUM; i++){
        free(ptr_array_unsortedbin_B[i]);
    }
    free(tmp1);    
    free(tmp2);
    return 0;
}
