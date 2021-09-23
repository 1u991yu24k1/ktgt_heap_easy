# Handson1: tcacheのdouble-freeを利用して, 0xdeadbeefへのアクセスを起こす. 


# 事前準備 
1. コンテナに入る. 
  - `docker exec -it handson bash`
2. コンテナ内部で使用するライブラリを切り替え. 
  - `cp -p /glibc/2.27/64/lib/{ld-2.27.so,libc-2.27.so} /tmp/`
  - `patchelf --set-interpreter /tmp/ld-2.27.so --set-rpath /tmp ./handson1`
3. `socat`を利用してコンテナ内のTCP-1337でバイナリを待ち受け. 
  - `socat TCP-L:1337,reuseaddr,fork SYSTEM:"./handson1"`
