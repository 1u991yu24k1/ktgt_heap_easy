#!/bin/bash

SRC=$1
DST=$2
CFLAGS="-ggdb -O0 -fstack-protector-all"
LFLAGS="-Wl,-z,relro,-z,now"

gcc $CFLAGS -o ./$DST $LFLAGS $SRC && checksec ./$DST;
