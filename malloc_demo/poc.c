/* tcacheが埋まってunsorted binに繋がったあとmallocするときの動きを確認する. */
/*
    tcache/unsorted binのどちらからチャンクが確保されるのか？
*/
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>


int main(int argc, char **argv){
    char *p[8];
    char *target; 
    char *t; // top併合防止用
    
    for(int i = 0; i < 7; i++){
        p[i] = (char *)malloc(0x100); // tcacheかつ. 非fastbinレンジなサイズ
    }
    p[7] = (char *)malloc(0x100); 
    t = (char *)malloc(1); 

    for(int i = 0; i < 7; i++){
        free(p[i]);
    }
    free(p[7]);// unsorted binに0x110-sizedなチャンクが繋がっている. 
    
    // 0x100でチャンクサイズが確保される.=>unsorted binから切り出すと,残りの領域のサイズがチャンクの最小サイズを下回る 
    target = (char *)malloc(0xf0); 
    printf("[*] malloc returns %p\n", target); 
FIN:
    getchar();
    free(t);
    return 0;
}
