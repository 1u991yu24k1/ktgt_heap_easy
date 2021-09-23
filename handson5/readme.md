# Handson5: main\_arena->topを使ったlibcアドレスリーク
`show_note`が実装されているので, unsorted binにつなげてリークさせる. 
glibc-2.31で実施想定.

# 事前準備. 
1. コンテナに入る. 
  - `docker exec -it handson bash`
2. コンテナ内部で使用するライブラリを切り替え. 
  - `patchelf --set-interpreter /tmp/ld-2.31.so --set-rpath /tmp ./handson5
3. `socat`を利用してコンテナ内のTCP-1337でバイナリを待ち受け. 
  - `socat TCP-L:1337,reuseaddr,fork SYSTEM:"./handson5"` 
