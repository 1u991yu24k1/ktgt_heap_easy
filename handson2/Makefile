CC = /usr/bin/gcc
CFLAGS= -ggdb -O0 -fstack-protector-all
LFLAGS= -Wl,-z,relro,-z,now
SRC = handson2.c
TARGET = handson2

all: 
	$(CC) $(CFLAGS) -o $(TARGET) $(LFLAGS) $(SRC)


.PHONY: 
clean:
	rm -rf $(TARGET)
