CC := /usr/bin/gcc
CFLAGS := -ggdb -O0 -fstack-protector-all
LFLAGS := -Wl,-z,relro,-z,now

all: demo1 demo2 demo3


demo1:
	$(CC) $(CFLAGS) -o malloc_demo1 $(LFLAGS) malloc_demo1.c

 
demo2:
	$(CC) $(CFLAGS) -o malloc_demo2 $(LFLAGS) malloc_demo2.c


demo3:
	$(CC) $(CFLAGS) -o malloc_demo3 $(LFLAGS) malloc_demo3.c
