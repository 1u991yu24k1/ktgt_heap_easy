dir /glibc/src/malloc
dir /glibc/src/stdlib
dir /glibc/src/io
dir /glibc/src/libio
dir /glibc/src/stdio-common
dir /glibc/src/nptl
dir /glibc/src/setjmp
dir /glibc/src/sysdeps
dir /glibc/src/sysdeps/generic
dir /glibc/src/sysdeps/gnu
dir /glibc/src/sysdeps/posix
dir /glibc/src/sysdeps/pthread
dir /glibc/src/sysdeps/x86_64

define dis
    x/32i $rip
end

define dd
  x/64xw $arg0
end

define ddx
  x/256xw $arg0
end

define ddh
  x/32xg $arg0
end

define ddhx
  x/256xg $arg0
end

define dq
    x/32gx $arg0
end

define dqx
    x/64gx $arg0
end

file ./handson6
