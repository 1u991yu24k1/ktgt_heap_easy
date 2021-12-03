# Handson4
UAF版のtcache poisoning(glibc2.31版)
countのunderflow防止パッチがあたっているため, UAF時にリストのチャンクを揃えておく必要がある. 
なお、以降のHandsonはすべてglibc-2.31を使うとする. 

# 事前準備
1. コンテナに入る. 
  - `docker exec -it handson bash`
2. コンテナ内部で使用するライブラリを切り替え. 
  - `cp -p /glibc/2.27/64/lib/{ld-2.31.so,libc-2.31.so} /tmp/`; 
  - `rm /tmp/{ld-2.27.so,libc-2.27.so}`
  - `patchelf --set-interpreter /tmp/ld-2.31.so --set-rpath /tmp ./handson4`
3. `socat`を利用してコンテナ内のTCP-1337でバイナリを待ち受け. 
  - `socat TCP-L:1337,reuseaddr,fork SYSTEM:"./handson4"`

# 多分One Gadgetがうまく行かないので, `__free_hook`書き換えて, Heapにおいた`/bin/sh\0`を参照させてsystemに飛ばすがかんたん. 
