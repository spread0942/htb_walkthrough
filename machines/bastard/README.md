# Bastard - Hack The Box Walkthrough

**Target IP**: `10.10.10.9`  
**Hostname**: `bastard.htb`  

---

## Initial Setup

### Preparing the Environment
1. Store the target IP in a file for reuse:
   ```bash
   echo 10.10.10.9 > target
   ```
2. Add the target to your `/etc/hosts` file for easier navigation:
   ```
   10.10.10.9   bastard.htb
   ```

---

## Enumeration

### Full Port Scan
I conducted a full TCP port scan to identify open ports:
```bash
nmap -p- -v -iL target -oN nmap/full_tcp_scan.txt
```

**Open Ports**:
- 80/tcp -
- 135/tcp - MSRPC
- 49154/tcp - MSRPC

```bash
nmap -p80,135,49154 -A -v -iL target -oN nmap/target_ports.txt
```

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
|_http-favicon: Unknown favicon MD5: CF2445DCB53A031C02F9B57E2199BC03
|_http-server-header: Microsoft-IIS/7.5
|_http-generator: Drupal 7 (http://drupal.org)
135/tcp   open  msrpc   Microsoft Windows RPC
49154/tcp open  msrpc   Microsoft Windows RPC
```

### Port 80

The port 80 show me a Drupal login.
You can read the version on nmap or also runngin the command:

```bash
curl http://bastard.htb | grep "<meta name=\"Generator\" content=\"Drupal"
```

Then I looking for known vulnerabilities:

```bash
searchsploit Drupal 7
```

![image](https://github.com/user-attachments/assets/07d958c6-e0f8-4994-9611-a9497633c627)

