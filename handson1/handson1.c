#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <errno.h>

#define MAX_SIZE 10
#define MAX_BUF  0x100LL

char *ptr_array[MAX_SIZE];

#define N 1024
#define PROCFS "/proc/%d/maps"
#define LIBCRT "/lib/x86_64-linux-gnu/libc-2.27.so" // Ubuntu 18.04 LTS(x64)
#define HEAP   "[heap]"

static unsigned long getlibc(void){
	unsigned long libc = 0U;
	char buf[N] = {'\0'};
	char tmp[0x20u] = {'\0'};
	FILE *fp = NULL;
	pid_t pid;
	pid = getpid();
	snprintf(tmp, 0x20u, PROCFS, pid);
	printf("[+] %s\n", tmp);
	if((fp = fopen(tmp, "r")) == NULL){
		fprintf(stderr, "[!] Can't Open %s\n", tmp);
		exit(EXIT_FAILURE);
	}
	while(fgets(buf, N, fp) != NULL){
		memset(tmp, '\0', 0x20u);
		if(strstr(buf, LIBCRT) != NULL){
			strncpy(tmp, buf, 12); // 48bit addr(userland)
			libc = strtoul(tmp, NULL, 0x10u);
			break;
		}

	}
	fclose(fp);
	return libc;
}

static unsigned long getheap(void){
    unsigned long heap_base = 0U;
	  char buf[N] = {'\0'};
	  char tmp[0x20u] = {'\0'};
	  FILE *fp = NULL;
	  pid_t pid;
	  pid = getpid();
	  snprintf(tmp, 0x20u, PROCFS, pid);
	  printf("[+] %s\n", tmp);
	  if((fp = fopen(tmp, "r")) == NULL){
		    fprintf(stderr, "[!] Can't Open %s\n", tmp);
		    exit(EXIT_FAILURE);
	  }
	  while(fgets(buf, N, fp) != NULL){
		    memset(tmp, '\0', 0x20u);
		    if(strstr(buf, HEAP) != NULL){
			      strncpy(tmp, buf, 12); // 48bit addr(userland)
			      heap_base = strtoul(tmp, NULL, 0x10u);
			      break;
		    }

	  }
	  fclose(fp);
	  return heap_base;
}

unsigned long read_ulong(void){
    unsigned long val = 0ul;
    char tmp[0x10] = {'\0'};
    fgets(tmp, 0x10 - 1, stdin);
    if(1 != sscanf_s(tmp, "%lx", &val)){
        exit(EXIT_FAILURE);
    }
    return val; 
}

ssize_t read_int(void){
    char buf[8] = {'\0'};
    ssize_t tmp = 0L;
    tmp = read(fileno(stdin), buf, 7);
    if(tmp < 0){
        fprintf(stderr,"[!] Error, %s\n",strerror(errno));
        exit(EXIT_FAILURE);
    }
    tmp = strtol(buf, NULL, 10);
    if(tmp < 0LL){
        fputs("[!] Invalid number\n", stderr);
        exit(EXIT_FAILURE);
    }
    return tmp;
} 


void create_note(void){
    int i;
    int length = 0;
    char *ptr = NULL;
    ssize_t read_num;
    
    for(i = 0; i < MAX_SIZE && ptr_array[i] != NULL; i++)
    if(i >= MAX_SIZE){
        fputs("[!] No Space Left!!\n", stderr);
        exit(EXIT_FAILURE);
    }   
    
    fputs("[*] Note data size:", stdout);
    length = (int)read_int();
    if(MAX_BUF < length || !length || length < 0L){
        fputs("[!] Invalid length\n", stderr);
        exit(EXIT_FAILURE);
    }

    ptr = (char *)malloc(length);
    if(ptr == NULL){
        fprintf(stderr, "[!] Error, %s\n", strerror(errno));
        exit(EXIT_FAILURE);
    }
    fputs("[*] Note data: ", stdout);
    read_num = read(fileno(stdin), ptr, length);
    if(read_num <= 0L){
        fprintf(stderr,"[!] Error, %s\n", strerror(errno));
        exit(EXIT_FAILURE); 
    }
    if(read_num > 0)
        ptr[read_num-1] = '\0';
    
    ptr_array[i] = ptr;
    printf("[+] Chunk stored Index: %d\n",i);
    ptr = NULL;
    return ;   
}



void delete_note(void){
    int idx;
    fputs("[+] Note index: ", stdout);
    idx = (int)read_int();
    if(0 > idx || MAX_SIZE <= idx){
        fputs("[!] Invalid index\n", stderr);
        exit(EXIT_FAILURE);
    }
    free(ptr_array[idx]);
    printf("[+] Chunk freed Index: %d\n", idx);
    return ;
}

int menu(){
    puts("1: create note");
    puts("2: delete note");
    puts("3: exit");
    fputs("Command >> ", stdout);
    return read_int();
}


int main(int argc, char **argv){
    int c;
    while(1){
        c = menu(); 
        switch(c){
            case 1:
                create_note();
                break;
            case 2:
                delete_note();
                break;
            case 3:
                puts("Bye!!");
                exit(EXIT_SUCCESS);     
                break;
            default:
                break;
        }
    }
}


__attribute__((constructor))
void setup(){
    setvbuf(stdin,  NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    // setvbuf(stderr, NULL, _IONBF, 0);
}
