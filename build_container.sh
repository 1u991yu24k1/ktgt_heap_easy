#!/bin/bash

TAGNAME="ktgt"
CNTNAME="handson"

docker build -t $TAGNAME $(pwd)

docker run -d --rm --name $CNTNAME --cap-add=SYS_PTRACE -v $(pwd):/ctf/work -p 1337:1337 -p 1234:1234 $TAGNAME;
