# Querier

```bash
nmap -p- -iL target -v -oN nmap/fps.txt
```

```
PORT      STATE SERVICE
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
1433/tcp  open  ms-sql-s
5985/tcp  open  wsman
47001/tcp open  winrm
49664/tcp open  unknown
49665/tcp open  unknown
49666/tcp open  unknown
49667/tcp open  unknown
49668/tcp open  unknown
49669/tcp open  unknown
49670/tcp open  unknown
49671/tcp open  unknown
```

```bash
ports=awk -F '/' 'NR>=6 && NR<=18 {print $1}' nmap/fps.txt | paste -sd ','
nmap -p$ports -iL target -v -A -oN nmap/tcp_ports.txt -oX nmap/tcp_ports.xml
```

```
PORT      STATE SERVICE
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds?
1433/tcp  open  ms-sql-s      Microsoft SQL Server 2017 14.00.1000.00; RTM
| ms-sql-ntlm-info: 
|   10.10.10.125:1433: 
|     Target_Name: HTB
|     NetBIOS_Domain_Name: HTB
|     NetBIOS_Computer_Name: QUERIER
|     DNS_Domain_Name: HTB.LOCAL
|     DNS_Computer_Name: QUERIER.HTB.LOCAL
|     DNS_Tree_Name: HTB.LOCAL
|_    Product_Version: 10.0.17763
| ms-sql-info: 
|   10.10.10.125:1433: 
|     Version: 
|       name: Microsoft SQL Server 2017 RTM
|       number: 14.00.1000.00
|       Product: Microsoft SQL Server 2017
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
| Issuer: commonName=SSL_Self_Signed_Fallback
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2025-04-14T15:25:35
| Not valid after:  2055-04-14T15:25:35
| MD5:   e6d5:cf74:a311:d8fb:c529:491e:aa4a:e32d
|_SHA-1: 1001:000b:e6fe:6936:8f2b:d86c:22df:82a3:be7d:864b
|_ssl-date: 2025-04-14T15:31:59+00:00; 0s from scanner time.
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
49664/tcp open  msrpc         Microsoft Windows RPC
49665/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49668/tcp open  msrpc         Microsoft Windows RPC
49669/tcp open  msrpc         Microsoft Windows RPC
49670/tcp open  msrpc         Microsoft Windows RPC
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose|specialized
Running (JUST GUESSING): Microsoft Windows 2019|2012|2022|10|2016|2008|7|Vista|Longhorn (95%)
OS CPE: cpe:/o:microsoft:windows_server_2012:r2 cpe:/o:microsoft:windows_10 cpe:/o:microsoft:windows_server_2016 cpe:/o:microsoft:windows_server_2008:r2 cpe:/o:microsoft:windows_7::sp1 cpe:/o:microsoft:windows_10:1511 cpe:/o:microsoft:windows_vista::sp1:home_premium cpe:/o:microsoft:windows
Aggressive OS guesses: Microsoft Windows Server 2019 (95%), Microsoft Windows Server 2012 R2 (92%), Microsoft Windows Server 2022 (92%), Microsoft Windows 10 1909 (92%), Microsoft Windows 10 1709 - 1909 (87%), Microsoft Windows Server 2012 (87%), Microsoft Windows Server 2012 or Server 2012 R2 (87%), Microsoft Windows Server 2016 (87%), Microsoft Windows 10 1703 (86%), Microsoft Windows Server 2008 R2 (86%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
TCP Sequence Prediction: Difficulty=257 (Good luck!)
IP ID Sequence Generation: Incremental
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2025-04-14T15:31:54
|_  start_date: N/A
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
```

## SMB

```bash
smbclient -L //10.10.10.125
```

```
Password for [WORKGROUP\root]:

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
	Reports         Disk      
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to 10.10.10.125 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available
```

```└─# sudo apt install libimage-exiftool-perl

Upgrading:                      
  libimage-exiftool-perl

Summary:
  Upgrading: 1, Installing: 0, Removing: 0, Not Upgrading: 2274
  Download size: 5633 kB
  Space needed: 3640 kB / 286 GB available

Get:1 http://http.kali.org/kali kali-rolling/main amd64 libimage-exiftool-perl all 13.10+dfsg-1 [5633 kB]
Fetched 5633 kB in 1s (7480 kB/s)           
(Reading database ... 473470 files and directories currently installed.)
Preparing to unpack .../libimage-exiftool-perl_13.10+dfsg-1_all.deb ...
Unpacking libimage-exiftool-perl (13.10+dfsg-1) over (12.76+dfsg-1) ...
Setting up libimage-exiftool-perl (13.10+dfsg-1) ...
Processing triggers for doc-base (0.11.2) ...
Processing 1 changed doc-base file...
Processing triggers for man-db (2.12.1-1) ...
Processing triggers for kali-menu (2023.4.7) ...
Scanning processes...                                                                                             
Scanning linux images...                                                                                          

Running kernel seems to be up-to-date.

No services need to be restarted.

No containers need to be restarted.

No user sessions are running outdated binaries.

No VM guests are running outdated hypervisor (qemu) binaries on this host.
                                                                                                                  
┌──(root㉿vb-kali)-[~/htb/machines/querier]
└─# exiftool Currency\ Volume\ Report.xlsm 
ExifTool Version Number         : 13.10
File Name                       : Currency Volume Report.xlsm
Directory                       : .
File Size                       : 12 kB
File Modification Date/Time     : 2025:04:19 09:27:34-04:00
File Access Date/Time           : 2025:04:19 09:31:40-04:00
File Inode Change Date/Time     : 2025:04:19 09:27:34-04:00
File Permissions                : -rw-r--r--
File Type                       : XLSM
File Type Extension             : xlsm
MIME Type                       : application/vnd.ms-excel.sheet.macroEnabled.12
Zip Required Version            : 20
Zip Bit Flag                    : 0x0006
Zip Compression                 : Deflated
Zip Modify Date                 : 1980:01:01 00:00:00
Zip CRC                         : 0x513599ac
Zip Compressed Size             : 367
Zip Uncompressed Size           : 1087
Zip File Name                   : [Content_Types].xml
Creator                         : Luis
Last Modified By                : Luis
Create Date                     : 2019:01:21 20:38:56Z
Modify Date                     : 2019:01:27 22:21:34Z
Application                     : Microsoft Excel
Doc Security                    : None
Scale Crop                      : No
Heading Pairs                   : Worksheets, 1
Titles Of Parts                 : Currency Volume
Company                         : 
Links Up To Date                : No
Shared Doc                      : No
Hyperlinks Changed              : No
App Version                     : 16.0300
```

I have install olevba:

```bash
pipx install oletools
```

```bash
olevba Currency\ Volume\ Report.xlsm
```

This dump a SQL Connection string and I used to connect on SQL Server:

```bash
impacket-mssqlclient reporting@10.10.10.125 -windows-auth
xp_dirtree C:\\Users
```

---
