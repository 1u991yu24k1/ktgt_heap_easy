CC = /usr/bin/gcc
CFLAGS= -ggdb -O0 -fstack-protector-all
LFLAGS= -Wl,-z,relro,-z,now
SRC = handson5.c
TARGET = handson5

all: 
	$(CC) $(CFLAGS) -o $(TARGET) $(LFLAGS) $(SRC)


.PHONY: 
clean:
	rm -rf $(TARGET)
