# Bastion

## Initial Setup

### Preparing the Scope

1. Store the target IP for reuse
```
echo 10.10.10.134 > target
```
2. Add the target to your `hosts`
```bash
10.10.10.134  bastion.htb
```

---

## Enumeration

Full port scan:

```bash
nmap -p- -iL target -v -oN nmap/tcp_ports_scan.txt
```

This is the output:

```
# Nmap 7.94SVN scan initiated Wed Apr  9 13:57:26 2025 as: nmap -p- -iL target -v -oN nmap/tcp_ports_scan.txt
Nmap scan report for bastion.htb (10.10.10.134)
Host is up (0.082s latency).
Not shown: 65522 closed tcp ports (reset)
PORT      STATE SERVICE
22/tcp    open  ssh
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
5985/tcp  open  wsman
47001/tcp open  winrm
49664/tcp open  unknown
49665/tcp open  unknown
49666/tcp open  unknown
49667/tcp open  unknown
49668/tcp open  unknown
49669/tcp open  unknown
49670/tcp open  unknown

Read data files from: /usr/bin/../share/nmap
# Nmap done at Wed Apr  9 13:59:19 2025 -- 1 IP address (1 host up) scanned in 113.27 seconds
```

Then I store the ports in a file:

```bash
awk -F '/' 'NR>=6 && NR<=18 {print $1}' nmap/tcp_ports_scan.txt | paste -sd ',' > nmap/ports.txxt
```

Then I performe an aggressive port scan:

```bash
nmap -p$(cat nmap/ports.txxt) -iL target -v -A -oN nmap/tcp_ports.txt -oX nmap/tcp_ports.xml
```

This is the output:

```
PORT      STATE SERVICE      VERSION
22/tcp    open  ssh          OpenSSH for_Windows_7.9 (protocol 2.0)
| ssh-hostkey: 
|   2048 3a:56:ae:75:3c:78:0e:c8:56:4d:cb:1c:22:bf:45:8a (RSA)
|   256 cc:2e:56:ab:19:97:d5:bb:03:fb:82:cd:63:da:68:01 (ECDSA)
|_  256 93:5f:5d:aa:ca:9f:53:e7:f2:82:e6:64:a8:a3:a0:18 (ED25519)
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds Windows Server 2016 Standard 14393 microsoft-ds
5985/tcp  open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
47001/tcp open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
49664/tcp open  msrpc        Microsoft Windows RPC
49665/tcp open  msrpc        Microsoft Windows RPC
49666/tcp open  msrpc        Microsoft Windows RPC
49667/tcp open  msrpc        Microsoft Windows RPC
49668/tcp open  msrpc        Microsoft Windows RPC
49669/tcp open  msrpc        Microsoft Windows RPC
49670/tcp open  msrpc        Microsoft Windows RPC
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose|specialized
Running (JUST GUESSING): Microsoft Windows 2016|2022|10|2012|7|2008|Vista|2019|8.1 (92%)
OS CPE: cpe:/o:microsoft:windows_server_2016 cpe:/o:microsoft:windows_10:1607 cpe:/o:microsoft:windows_10:1511 cpe:/o:microsoft:windows_server_2012:r2 cpe:/o:microsoft:windows_7::sp1 cpe:/o:microsoft:windows_server_2008::sp2 cpe:/o:microsoft:windows_vista::sp1:home_premium cpe:/o:microsoft:windows_8.1
Aggressive OS guesses: Microsoft Windows Server 2016 (92%), Microsoft Windows Server 2022 (92%), Microsoft Windows 10 1607 (92%), Microsoft Windows 10 1511 (92%), Microsoft Windows Server 2012 R2 (92%), Microsoft Windows Server 2016 build 10586 - 14393 (91%), Microsoft Windows 10 1507 (90%), Microsoft Windows 7 SP1 (89%), Microsoft Windows 7 SP1 or Windows Server 2008 SP2 (89%), Microsoft Windows 10 (89%)
No exact OS matches for host (test conditions non-ideal).
Uptime guess: 0.010 days (since Wed Apr  9 13:55:39 2025)
Network Distance: 2 hops
TCP Sequence Prediction: Difficulty=250 (Good luck!)
IP ID Sequence Generation: Incremental
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-time: 
|   date: 2025-04-09T18:09:49
|_  start_date: 2025-04-09T17:55:49
| smb-os-discovery: 
|   OS: Windows Server 2016 Standard 14393 (Windows Server 2016 Standard 6.3)
|   Computer name: Bastion
|   NetBIOS computer name: BASTION\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2025-04-09T20:09:47+02:00
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
|_clock-skew: mean: -39m58s, deviation: 1h09m15s, median: 0s
```

### SMB

```bash
└─# smbclient -L=$(cat target)                                                                  
Password for [WORKGROUP\root]:

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	Backups         Disk      
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to 10.10.10.134 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available
```

```bash
smbclient //10.10.10.134/Backups -N
```

```bash
apt-get install libguestfs-tools
```

```bash
apt-get install cifs-utils
```

```bash
mkdir /mnt/backups
mount -t cifs //10.10.10.134/Backups /mnt/backups -o rw
```

```bash
mkdir /mnt/vhd
guestmount --add /mnt/remote/path/to/vhdfile.vhd --inspector --ro /mnt/vhd -v
```

### RPC

```bash
└─# impacket-rpcdump @$(cat target)          
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Retrieving endpoint list from 10.10.10.134
Protocol: [MS-RSP]: Remote Shutdown Protocol 
Provider: wininit.exe 
UUID    : D95AFE70-A6D5-4259-822E-2C84DA1DDB0D v1.0 
Bindings: 
          ncacn_ip_tcp:10.10.10.134[49664]
          ncalrpc:[WindowsShutdown]
          ncacn_np:\\BASTION[\PIPE\InitShutdown]
          ncalrpc:[WMsgKRpc07D100]

Protocol: N/A 
Provider: winlogon.exe 
UUID    : 76F226C3-EC14-4325-8A99-6A46348418AF v1.0 
Bindings: 
          ncalrpc:[WindowsShutdown]
          ncacn_np:\\BASTION[\PIPE\InitShutdown]
          ncalrpc:[WMsgKRpc07D100]
          ncalrpc:[WMsgKRpc07D951]

Protocol: N/A 
Provider: N/A 
UUID    : 9B008953-F195-4BF9-BDE0-4471971E58ED v1.0 
Bindings: 
          ncalrpc:[LRPC-291936a30b636df8dd]
          ncalrpc:[dabrpc]
          ncalrpc:[csebpub]
          ncalrpc:[LRPC-481b82a306ab9b3597]
          ncalrpc:[LRPC-8bfe30c6ae23ab886d]
          ncalrpc:[LRPC-c0d6ac33af9d90e6d8]
          ncacn_np:\\BASTION[\pipe\LSM_API_service]
          ncalrpc:[LSMApi]
          ncalrpc:[LRPC-c5a80c33d1713c34d3]
          ncalrpc:[actkernel]
          ncalrpc:[umpo]

Protocol: N/A 
Provider: N/A 
UUID    : D09BDEB5-6171-4A34-BFE2-06FA82652568 v1.0 
Bindings: 
          ncalrpc:[csebpub]
          ncalrpc:[LRPC-481b82a306ab9b3597]
          ncalrpc:[LRPC-8bfe30c6ae23ab886d]
          ncalrpc:[LRPC-c0d6ac33af9d90e6d8]
          ncacn_np:\\BASTION[\pipe\LSM_API_service]
          ncalrpc:[LSMApi]
          ncalrpc:[LRPC-c5a80c33d1713c34d3]
          ncalrpc:[actkernel]
          ncalrpc:[umpo]
          ncalrpc:[LRPC-8bfe30c6ae23ab886d]
          ncalrpc:[LRPC-c0d6ac33af9d90e6d8]
          ncacn_np:\\BASTION[\pipe\LSM_API_service]
          ncalrpc:[LSMApi]
          ncalrpc:[LRPC-c5a80c33d1713c34d3]
          ncalrpc:[actkernel]
          ncalrpc:[umpo]
          ncalrpc:[LRPC-51739ad66e3e9b680c]
          ncalrpc:[LRPC-44a8b3ea1004b4da97]

Protocol: N/A 
Provider: N/A 
UUID    : 697DCDA9-3BA9-4EB2-9247-E11F1901B0D2 v1.0 
Bindings: 
          ncalrpc:[LRPC-481b82a306ab9b3597]
          ncalrpc:[LRPC-8bfe30c6ae23ab886d]
          ncalrpc:[LRPC-c0d6ac33af9d90e6d8]
          ncacn_np:\\BASTION[\pipe\LSM_API_service]
          ncalrpc:[LSMApi]
          ncalrpc:[LRPC-c5a80c33d1713c34d3]
          ncalrpc:[actkernel]
          ncalrpc:[umpo]

Protocol: N/A 
Provider: N/A 
UUID    : 857FB1BE-084F-4FB5-B59C-4B2C4BE5F0CF v1.0 
Bindings: 
          ncalrpc:[LRPC-c0d6ac33af9d90e6d8]
          ncacn_np:\\BASTION[\pipe\LSM_API_service]
          ncalrpc:[LSMApi]
          ncalrpc:[LRPC-c5a80c33d1713c34d3]
          ncalrpc:[actkernel]
          ncalrpc:[umpo]

Protocol: N/A 
Provider: N/A 
UUID    : B8CADBAF-E84B-46B9-84F2-6F71C03F9E55 v1.0 
Bindings: 
          ncalrpc:[LRPC-c0d6ac33af9d90e6d8]
          ncacn_np:\\BASTION[\pipe\LSM_API_service]
          ncalrpc:[LSMApi]
          ncalrpc:[LRPC-c5a80c33d1713c34d3]
          ncalrpc:[actkernel]
          ncalrpc:[umpo]

Protocol: N/A 
Provider: N/A 
UUID    : 20C40295-8DBA-48E6-AEBF-3E78EF3BB144 v1.0 
Bindings: 
          ncalrpc:[LRPC-c0d6ac33af9d90e6d8]
          ncacn_np:\\BASTION[\pipe\LSM_API_service]
          ncalrpc:[LSMApi]
          ncalrpc:[LRPC-c5a80c33d1713c34d3]
          ncalrpc:[actkernel]
          ncalrpc:[umpo]

Protocol: N/A 
Provider: N/A 
UUID    : 2513BCBE-6CD4-4348-855E-7EFB3C336DD3 v1.0 
Bindings: 
          ncalrpc:[LRPC-c0d6ac33af9d90e6d8]
          ncacn_np:\\BASTION[\pipe\LSM_API_service]
          ncalrpc:[LSMApi]
          ncalrpc:[LRPC-c5a80c33d1713c34d3]
          ncalrpc:[actkernel]
          ncalrpc:[umpo]

Protocol: N/A 
Provider: N/A 
UUID    : 88ABCBC3-34EA-76AE-8215-767520655A23 v0.0 
Bindings: 
          ncalrpc:[LRPC-c0d6ac33af9d90e6d8]
          ncacn_np:\\BASTION[\pipe\LSM_API_service]
          ncalrpc:[LSMApi]
          ncalrpc:[LRPC-c5a80c33d1713c34d3]
          ncalrpc:[actkernel]
          ncalrpc:[umpo]

Protocol: N/A 
Provider: N/A 
UUID    : 76C217BC-C8B4-4201-A745-373AD9032B1A v1.0 
Bindings: 
          ncalrpc:[LRPC-c0d6ac33af9d90e6d8]
          ncacn_np:\\BASTION[\pipe\LSM_API_service]
          ncalrpc:[LSMApi]
          ncalrpc:[LRPC-c5a80c33d1713c34d3]
          ncalrpc:[actkernel]
          ncalrpc:[umpo]

Protocol: N/A 
Provider: N/A 
UUID    : 55E6B932-1979-45D6-90C5-7F6270724112 v1.0 
Bindings: 
          ncalrpc:[LRPC-c0d6ac33af9d90e6d8]
          ncacn_np:\\BASTION[\pipe\LSM_API_service]
          ncalrpc:[LSMApi]
          ncalrpc:[LRPC-c5a80c33d1713c34d3]
          ncalrpc:[actkernel]
          ncalrpc:[umpo]

Protocol: N/A 
Provider: N/A 
UUID    : 4DACE966-A243-4450-AE3F-9B7BCB5315B8 v1.0 
Bindings: 
          ncacn_np:\\BASTION[\pipe\LSM_API_service]
          ncalrpc:[LSMApi]
          ncalrpc:[LRPC-c5a80c33d1713c34d3]
          ncalrpc:[actkernel]
          ncalrpc:[umpo]

Protocol: N/A 
Provider: N/A 
UUID    : 1832BCF6-CAB8-41D4-85D2-C9410764F75A v1.0 
Bindings: 
          ncacn_np:\\BASTION[\pipe\LSM_API_service]
          ncalrpc:[LSMApi]
          ncalrpc:[LRPC-c5a80c33d1713c34d3]
          ncalrpc:[actkernel]
          ncalrpc:[umpo]

Protocol: N/A 
Provider: N/A 
UUID    : C521FACF-09A9-42C5-B155-72388595CBF0 v0.0 
Bindings: 
          ncacn_np:\\BASTION[\pipe\LSM_API_service]
          ncalrpc:[LSMApi]
          ncalrpc:[LRPC-c5a80c33d1713c34d3]
          ncalrpc:[actkernel]
          ncalrpc:[umpo]

Protocol: N/A 
Provider: N/A 
UUID    : 2C7FD9CE-E706-4B40-B412-953107EF9BB0 v0.0 
Bindings: 
          ncacn_np:\\BASTION[\pipe\LSM_API_service]
          ncalrpc:[LSMApi]
          ncalrpc:[LRPC-c5a80c33d1713c34d3]
          ncalrpc:[actkernel]
          ncalrpc:[umpo]

Protocol: N/A 
Provider: N/A 
UUID    : 0D3E2735-CEA0-4ECC-A9E2-41A2D81AED4E v1.0 
Bindings: 
          ncacn_np:\\BASTION[\pipe\LSM_API_service]
          ncalrpc:[LSMApi]
          ncalrpc:[LRPC-c5a80c33d1713c34d3]
          ncalrpc:[actkernel]
          ncalrpc:[umpo]

Protocol: N/A 
Provider: N/A 
UUID    : C605F9FB-F0A3-4E2A-A073-73560F8D9E3E v1.0 
Bindings: 
          ncacn_np:\\BASTION[\pipe\LSM_API_service]
          ncalrpc:[LSMApi]
          ncalrpc:[LRPC-c5a80c33d1713c34d3]
          ncalrpc:[actkernel]
          ncalrpc:[umpo]

Protocol: N/A 
Provider: N/A 
UUID    : 1B37CA91-76B1-4F5E-A3C7-2ABFC61F2BB0 v1.0 
Bindings: 
          ncacn_np:\\BASTION[\pipe\LSM_API_service]
          ncalrpc:[LSMApi]
          ncalrpc:[LRPC-c5a80c33d1713c34d3]
          ncalrpc:[actkernel]
          ncalrpc:[umpo]

Protocol: N/A 
Provider: N/A 
UUID    : 8BFC3BE1-6DEF-4E2D-AF74-7C47CD0ADE4A v1.0 
Bindings: 
          ncacn_np:\\BASTION[\pipe\LSM_API_service]
          ncalrpc:[LSMApi]
          ncalrpc:[LRPC-c5a80c33d1713c34d3]
          ncalrpc:[actkernel]
          ncalrpc:[umpo]

Protocol: N/A 
Provider: N/A 
UUID    : 2D98A740-581D-41B9-AA0D-A88B9D5CE938 v1.0 
Bindings: 
          ncacn_np:\\BASTION[\pipe\LSM_API_service]
          ncalrpc:[LSMApi]
          ncalrpc:[LRPC-c5a80c33d1713c34d3]
          ncalrpc:[actkernel]
          ncalrpc:[umpo]

Protocol: N/A 
Provider: sysntfy.dll 
UUID    : C9AC6DB5-82B7-4E55-AE8A-E464ED7B4277 v1.0 Impl friendly name
Bindings: 
          ncalrpc:[LRPC-c5a80c33d1713c34d3]
          ncalrpc:[actkernel]
          ncalrpc:[umpo]
          ncalrpc:[senssvc]
          ncalrpc:[DeviceSetupManager]
          ncalrpc:[IUserProfile2]
          ncalrpc:[OLEE18EEB2BD45710A2FCA1FDFABCCF]
          ncalrpc:[IUserProfile2]
          ncalrpc:[OLEE18EEB2BD45710A2FCA1FDFABCCF]
          ncalrpc:[IUserProfile2]
          ncalrpc:[OLEE18EEB2BD45710A2FCA1FDFABCCF]

Protocol: N/A 
Provider: N/A 
UUID    : 5824833B-3C1A-4AD2-BDFD-C31D19E23ED2 v1.0 
Bindings: 
          ncalrpc:[actkernel]
          ncalrpc:[umpo]

Protocol: N/A 
Provider: N/A 
UUID    : BDAA0970-413B-4A3E-9E5D-F6DC9D7E0760 v1.0 
Bindings: 
          ncalrpc:[actkernel]
          ncalrpc:[umpo]

Protocol: N/A 
Provider: N/A 
UUID    : 3B338D89-6CFA-44B8-847E-531531BC9992 v1.0 
Bindings: 
          ncalrpc:[actkernel]
          ncalrpc:[umpo]

Protocol: N/A 
Provider: N/A 
UUID    : 8782D3B9-EBBD-4644-A3D8-E8725381919B v1.0 
Bindings: 
          ncalrpc:[actkernel]
          ncalrpc:[umpo]

Protocol: N/A 
Provider: N/A 
UUID    : 085B0334-E454-4D91-9B8C-4134F9E793F3 v1.0 
Bindings: 
          ncalrpc:[actkernel]
          ncalrpc:[umpo]

Protocol: N/A 
Provider: N/A 
UUID    : 4BEC6BB8-B5C2-4B6F-B2C1-5DA5CF92D0D9 v1.0 
Bindings: 
          ncalrpc:[actkernel]
          ncalrpc:[umpo]

Protocol: N/A 
Provider: dhcpcsvc6.dll 
UUID    : 3C4728C5-F0AB-448B-BDA1-6CE01EB0A6D6 v1.0 DHCPv6 Client LRPC Endpoint
Bindings: 
          ncalrpc:[dhcpcsvc6]
          ncalrpc:[dhcpcsvc]
          ncacn_ip_tcp:10.10.10.134[49665]
          ncacn_np:\\BASTION[\pipe\eventlog]
          ncalrpc:[eventlog]
          ncalrpc:[LRPC-6bfaefd1025ed269ea]
          ncalrpc:[LRPC-7045a19604fc5b108a]
          ncalrpc:[LRPC-51739ad66e3e9b680c]

Protocol: N/A 
Provider: dhcpcsvc.dll 
UUID    : 3C4728C5-F0AB-448B-BDA1-6CE01EB0A6D5 v1.0 DHCP Client LRPC Endpoint
Bindings: 
          ncalrpc:[dhcpcsvc]
          ncacn_ip_tcp:10.10.10.134[49665]
          ncacn_np:\\BASTION[\pipe\eventlog]
          ncalrpc:[eventlog]
          ncalrpc:[LRPC-6bfaefd1025ed269ea]
          ncalrpc:[LRPC-7045a19604fc5b108a]
          ncalrpc:[LRPC-51739ad66e3e9b680c]

Protocol: [MS-EVEN6]: EventLog Remoting Protocol 
Provider: wevtsvc.dll 
UUID    : F6BEAFF7-1E19-4FBB-9F8F-B89E2018337C v1.0 Event log TCPIP
Bindings: 
          ncacn_ip_tcp:10.10.10.134[49665]
          ncacn_np:\\BASTION[\pipe\eventlog]
          ncalrpc:[eventlog]
          ncalrpc:[LRPC-6bfaefd1025ed269ea]
          ncalrpc:[LRPC-7045a19604fc5b108a]
          ncalrpc:[LRPC-51739ad66e3e9b680c]

Protocol: N/A 
Provider: nrpsrv.dll 
UUID    : 30ADC50C-5CBC-46CE-9A0E-91914789E23C v1.0 NRP server endpoint
Bindings: 
          ncalrpc:[LRPC-6bfaefd1025ed269ea]
          ncalrpc:[LRPC-7045a19604fc5b108a]
          ncalrpc:[LRPC-51739ad66e3e9b680c]

Protocol: N/A 
Provider: N/A 
UUID    : A500D4C6-0DD1-4543-BC0C-D5F93486EAF8 v1.0 
Bindings: 
          ncalrpc:[LRPC-7045a19604fc5b108a]
          ncalrpc:[LRPC-51739ad66e3e9b680c]

Protocol: N/A 
Provider: N/A 
UUID    : BF4DC912-E52F-4904-8EBE-9317C1BDD497 v1.0 
Bindings: 
          ncalrpc:[LRPC-fa59c06926cd1ffab1]
          ncalrpc:[trkwks]
          ncacn_np:\\BASTION[\pipe\trkwks]
          ncalrpc:[LRPC-7b900925d3a9bd0f8c]
          ncalrpc:[OLE8E65CD98D8AC8B5DC83A860AA073]
          ncalrpc:[LRPC-13e4cbbeea21f89a42]
          ncalrpc:[LRPC-44a8b3ea1004b4da97]

Protocol: N/A 
Provider: pcasvc.dll 
UUID    : 0767A036-0D22-48AA-BA69-B619480F38CB v1.0 PcaSvc
Bindings: 
          ncalrpc:[LRPC-7b900925d3a9bd0f8c]
          ncalrpc:[OLE8E65CD98D8AC8B5DC83A860AA073]
          ncalrpc:[LRPC-13e4cbbeea21f89a42]
          ncalrpc:[LRPC-44a8b3ea1004b4da97]

Protocol: N/A 
Provider: N/A 
UUID    : E40F7B57-7A25-4CD3-A135-7F7D3DF9D16B v1.0 Network Connection Broker server endpoint
Bindings: 
          ncalrpc:[LRPC-7b900925d3a9bd0f8c]
          ncalrpc:[OLE8E65CD98D8AC8B5DC83A860AA073]
          ncalrpc:[LRPC-13e4cbbeea21f89a42]
          ncalrpc:[LRPC-44a8b3ea1004b4da97]

Protocol: N/A 
Provider: N/A 
UUID    : 880FD55E-43B9-11E0-B1A8-CF4EDFD72085 v1.0 KAPI Service endpoint
Bindings: 
          ncalrpc:[LRPC-7b900925d3a9bd0f8c]
          ncalrpc:[OLE8E65CD98D8AC8B5DC83A860AA073]
          ncalrpc:[LRPC-13e4cbbeea21f89a42]
          ncalrpc:[LRPC-44a8b3ea1004b4da97]

Protocol: N/A 
Provider: N/A 
UUID    : 5222821F-D5E2-4885-84F1-5F6185A0EC41 v1.0 Network Connection Broker server endpoint for NCB Reset module
Bindings: 
          ncalrpc:[LRPC-13e4cbbeea21f89a42]
          ncalrpc:[LRPC-44a8b3ea1004b4da97]

Protocol: N/A 
Provider: N/A 
UUID    : A4B8D482-80CE-40D6-934D-B22A01A44FE7 v1.0 LicenseManager
Bindings: 
          ncalrpc:[LicenseServiceEndpoint]

Protocol: N/A 
Provider: N/A 
UUID    : 3473DD4D-2E88-4006-9CBA-22570909DD10 v5.1 WinHttp Auto-Proxy Service
Bindings: 
          ncalrpc:[OLEB36FDFFCDC1B2EBB78D0CA27265D]
          ncalrpc:[LRPC-a242c193b94d3d0a3c]

Protocol: N/A 
Provider: nsisvc.dll 
UUID    : 7EA70BCF-48AF-4F6A-8968-6A440754D5FA v1.0 NSI server endpoint
Bindings: 
          ncalrpc:[LRPC-a242c193b94d3d0a3c]

Protocol: N/A 
Provider: MPSSVC.dll 
UUID    : 2FB92682-6599-42DC-AE13-BD2CA89BD11C v1.0 Fw APIs
Bindings: 
          ncalrpc:[LRPC-02324f9ed03bea5e15]
          ncalrpc:[LRPC-23e005491e36825c2d]
          ncalrpc:[LRPC-84caba443df621de01]

Protocol: N/A 
Provider: N/A 
UUID    : F47433C3-3E9D-4157-AAD4-83AA1F5C2D4C v1.0 Fw APIs
Bindings: 
          ncalrpc:[LRPC-02324f9ed03bea5e15]
          ncalrpc:[LRPC-23e005491e36825c2d]
          ncalrpc:[LRPC-84caba443df621de01]

Protocol: N/A 
Provider: MPSSVC.dll 
UUID    : 7F9D11BF-7FB9-436B-A812-B2D50C5D4C03 v1.0 Fw APIs
Bindings: 
          ncalrpc:[LRPC-02324f9ed03bea5e15]
          ncalrpc:[LRPC-23e005491e36825c2d]
          ncalrpc:[LRPC-84caba443df621de01]

Protocol: N/A 
Provider: BFE.DLL 
UUID    : DD490425-5325-4565-B774-7E27D6C09C24 v1.0 Base Firewall Engine API
Bindings: 
          ncalrpc:[LRPC-23e005491e36825c2d]
          ncalrpc:[LRPC-84caba443df621de01]

Protocol: N/A 
Provider: N/A 
UUID    : DF4DF73A-C52D-4E3A-8003-8437FDF8302A v0.0 WM_WindowManagerRPC\Server
Bindings: 
          ncalrpc:[LRPC-84caba443df621de01]

Protocol: N/A 
Provider: N/A 
UUID    : C49A5A70-8A7F-4E70-BA16-1E8F1F193EF1 v1.0 Adh APIs
Bindings: 
          ncalrpc:[LRPC-32c7ac8a5205151d4d]
          ncacn_ip_tcp:10.10.10.134[49666]
          ncalrpc:[LRPC-add60283a9acb82e6f]
          ncalrpc:[ubpmtaskhostchannel]
          ncacn_np:\\BASTION[\PIPE\atsvc]
          ncalrpc:[senssvc]
          ncalrpc:[DeviceSetupManager]
          ncalrpc:[IUserProfile2]
          ncalrpc:[OLEE18EEB2BD45710A2FCA1FDFABCCF]

Protocol: N/A 
Provider: N/A 
UUID    : C36BE077-E14B-4FE9-8ABC-E856EF4F048B v1.0 Proxy Manager client server endpoint
Bindings: 
          ncalrpc:[LRPC-32c7ac8a5205151d4d]
          ncacn_ip_tcp:10.10.10.134[49666]
          ncalrpc:[LRPC-add60283a9acb82e6f]
          ncalrpc:[ubpmtaskhostchannel]
          ncacn_np:\\BASTION[\PIPE\atsvc]
          ncalrpc:[senssvc]
          ncalrpc:[DeviceSetupManager]
          ncalrpc:[IUserProfile2]
          ncalrpc:[OLEE18EEB2BD45710A2FCA1FDFABCCF]

Protocol: N/A 
Provider: N/A 
UUID    : 2E6035B2-E8F1-41A7-A044-656B439C4C34 v1.0 Proxy Manager provider server endpoint
Bindings: 
          ncalrpc:[LRPC-32c7ac8a5205151d4d]
          ncacn_ip_tcp:10.10.10.134[49666]
          ncalrpc:[LRPC-add60283a9acb82e6f]
          ncalrpc:[ubpmtaskhostchannel]
          ncacn_np:\\BASTION[\PIPE\atsvc]
          ncalrpc:[senssvc]
          ncalrpc:[DeviceSetupManager]
          ncalrpc:[IUserProfile2]
          ncalrpc:[OLEE18EEB2BD45710A2FCA1FDFABCCF]

Protocol: N/A 
Provider: iphlpsvc.dll 
UUID    : 552D076A-CB29-4E44-8B6A-D15E59E2C0AF v1.0 IP Transition Configuration endpoint
Bindings: 
          ncalrpc:[LRPC-32c7ac8a5205151d4d]
          ncacn_ip_tcp:10.10.10.134[49666]
          ncalrpc:[LRPC-add60283a9acb82e6f]
          ncalrpc:[ubpmtaskhostchannel]
          ncacn_np:\\BASTION[\PIPE\atsvc]
          ncalrpc:[senssvc]
          ncalrpc:[DeviceSetupManager]
          ncalrpc:[IUserProfile2]
          ncalrpc:[OLEE18EEB2BD45710A2FCA1FDFABCCF]

Protocol: N/A 
Provider: N/A 
UUID    : 0D3C7F20-1C8D-4654-A1B3-51563B298BDA v1.0 UserMgrCli
Bindings: 
          ncalrpc:[LRPC-32c7ac8a5205151d4d]
          ncacn_ip_tcp:10.10.10.134[49666]
          ncalrpc:[LRPC-add60283a9acb82e6f]
          ncalrpc:[ubpmtaskhostchannel]
          ncacn_np:\\BASTION[\PIPE\atsvc]
          ncalrpc:[senssvc]
          ncalrpc:[DeviceSetupManager]
          ncalrpc:[IUserProfile2]
          ncalrpc:[OLEE18EEB2BD45710A2FCA1FDFABCCF]

Protocol: N/A 
Provider: N/A 
UUID    : B18FBAB6-56F8-4702-84E0-41053293A869 v1.0 UserMgrCli
Bindings: 
          ncalrpc:[LRPC-32c7ac8a5205151d4d]
          ncacn_ip_tcp:10.10.10.134[49666]
          ncalrpc:[LRPC-add60283a9acb82e6f]
          ncalrpc:[ubpmtaskhostchannel]
          ncacn_np:\\BASTION[\PIPE\atsvc]
          ncalrpc:[senssvc]
          ncalrpc:[DeviceSetupManager]
          ncalrpc:[IUserProfile2]
          ncalrpc:[OLEE18EEB2BD45710A2FCA1FDFABCCF]

Protocol: N/A 
Provider: IKEEXT.DLL 
UUID    : A398E520-D59A-4BDD-AA7A-3C1E0303A511 v1.0 IKE/Authip API
Bindings: 
          ncacn_ip_tcp:10.10.10.134[49666]
          ncalrpc:[LRPC-add60283a9acb82e6f]
          ncalrpc:[ubpmtaskhostchannel]
          ncacn_np:\\BASTION[\PIPE\atsvc]
          ncalrpc:[senssvc]
          ncalrpc:[DeviceSetupManager]
          ncalrpc:[IUserProfile2]
          ncalrpc:[OLEE18EEB2BD45710A2FCA1FDFABCCF]

Protocol: N/A 
Provider: N/A 
UUID    : 3A9EF155-691D-4449-8D05-09AD57031823 v1.0 
Bindings: 
          ncacn_ip_tcp:10.10.10.134[49666]
          ncalrpc:[LRPC-add60283a9acb82e6f]
          ncalrpc:[ubpmtaskhostchannel]
          ncacn_np:\\BASTION[\PIPE\atsvc]
          ncalrpc:[senssvc]
          ncalrpc:[DeviceSetupManager]
          ncalrpc:[IUserProfile2]
          ncalrpc:[OLEE18EEB2BD45710A2FCA1FDFABCCF]

Protocol: [MS-TSCH]: Task Scheduler Service Remoting Protocol 
Provider: schedsvc.dll 
UUID    : 86D35949-83C9-4044-B424-DB363231FD0C v1.0 
Bindings: 
          ncacn_ip_tcp:10.10.10.134[49666]
          ncalrpc:[LRPC-add60283a9acb82e6f]
          ncalrpc:[ubpmtaskhostchannel]
          ncacn_np:\\BASTION[\PIPE\atsvc]
          ncalrpc:[senssvc]
          ncalrpc:[DeviceSetupManager]
          ncalrpc:[IUserProfile2]
          ncalrpc:[OLEE18EEB2BD45710A2FCA1FDFABCCF]

Protocol: N/A 
Provider: N/A 
UUID    : 33D84484-3626-47EE-8C6F-E7E98B113BE1 v2.0 
Bindings: 
          ncalrpc:[LRPC-add60283a9acb82e6f]
          ncalrpc:[ubpmtaskhostchannel]
          ncacn_np:\\BASTION[\PIPE\atsvc]
          ncalrpc:[senssvc]
          ncalrpc:[DeviceSetupManager]
          ncalrpc:[IUserProfile2]
          ncalrpc:[OLEE18EEB2BD45710A2FCA1FDFABCCF]

Protocol: [MS-TSCH]: Task Scheduler Service Remoting Protocol 
Provider: taskcomp.dll 
UUID    : 378E52B0-C0A9-11CF-822D-00AA0051E40F v1.0 
Bindings: 
          ncacn_np:\\BASTION[\PIPE\atsvc]
          ncalrpc:[senssvc]
          ncalrpc:[DeviceSetupManager]
          ncalrpc:[IUserProfile2]
          ncalrpc:[OLEE18EEB2BD45710A2FCA1FDFABCCF]

Protocol: [MS-TSCH]: Task Scheduler Service Remoting Protocol 
Provider: taskcomp.dll 
UUID    : 1FF70682-0A51-30E8-076D-740BE8CEE98B v1.0 
Bindings: 
          ncacn_np:\\BASTION[\PIPE\atsvc]
          ncalrpc:[senssvc]
          ncalrpc:[DeviceSetupManager]
          ncalrpc:[IUserProfile2]
          ncalrpc:[OLEE18EEB2BD45710A2FCA1FDFABCCF]

Protocol: N/A 
Provider: schedsvc.dll 
UUID    : 0A74EF1C-41A4-4E06-83AE-DC74FB1CDD53 v1.0 
Bindings: 
          ncalrpc:[senssvc]
          ncalrpc:[DeviceSetupManager]
          ncalrpc:[IUserProfile2]
          ncalrpc:[OLEE18EEB2BD45710A2FCA1FDFABCCF]

Protocol: N/A 
Provider: gpsvc.dll 
UUID    : 2EB08E3E-639F-4FBA-97B1-14F878961076 v1.0 Group Policy RPC Interface
Bindings: 
          ncalrpc:[LRPC-b4b880fe63795c6051]

Protocol: N/A 
Provider: N/A 
UUID    : 7AEB6705-3AE6-471A-882D-F39C109EDC12 v1.0 
Bindings: 
          ncalrpc:[LRPC-8f7b67b1c308e40700]

Protocol: N/A 
Provider: N/A 
UUID    : E7F76134-9EF5-4949-A2D6-3368CC0988F3 v1.0 
Bindings: 
          ncalrpc:[LRPC-8f7b67b1c308e40700]

Protocol: N/A 
Provider: N/A 
UUID    : B3781086-6A54-489B-91C8-51D067172AB7 v1.0 
Bindings: 
          ncalrpc:[LRPC-8f7b67b1c308e40700]

Protocol: N/A 
Provider: N/A 
UUID    : B37F900A-EAE4-4304-A2AB-12BB668C0188 v1.0 
Bindings: 
          ncalrpc:[LRPC-8f7b67b1c308e40700]

Protocol: N/A 
Provider: N/A 
UUID    : ABFB6CA3-0C5E-4734-9285-0AEE72FE8D1C v1.0 
Bindings: 
          ncalrpc:[LRPC-8f7b67b1c308e40700]

Protocol: N/A 
Provider: N/A 
UUID    : 7F1343FE-50A9-4927-A778-0C5859517BAC v1.0 DfsDs service
Bindings: 
          ncacn_np:\\BASTION[\PIPE\wkssvc]
          ncalrpc:[DNSResolver]
          ncalrpc:[nlaapi]
          ncalrpc:[nlaplg]

Protocol: N/A 
Provider: N/A 
UUID    : EB081A0D-10EE-478A-A1DD-50995283E7A8 v3.0 Witness Client Test Interface
Bindings: 
          ncalrpc:[DNSResolver]
          ncalrpc:[nlaapi]
          ncalrpc:[nlaplg]

Protocol: N/A 
Provider: N/A 
UUID    : F2C9B409-C1C9-4100-8639-D8AB1486694A v1.0 Witness Client Upcall Server
Bindings: 
          ncalrpc:[DNSResolver]
          ncalrpc:[nlaapi]
          ncalrpc:[nlaplg]

Protocol: [MS-PAR]: Print System Asynchronous Remote Protocol 
Provider: spoolsv.exe 
UUID    : 76F03F96-CDFD-44FC-A22C-64950A001209 v1.0 
Bindings: 
          ncacn_ip_tcp:10.10.10.134[49667]
          ncalrpc:[LRPC-da67a25ed48958ab31]

Protocol: N/A 
Provider: spoolsv.exe 
UUID    : 4A452661-8290-4B36-8FBE-7F4093A94978 v1.0 
Bindings: 
          ncacn_ip_tcp:10.10.10.134[49667]
          ncalrpc:[LRPC-da67a25ed48958ab31]

Protocol: [MS-PAN]: Print System Asynchronous Notification Protocol 
Provider: spoolsv.exe 
UUID    : AE33069B-A2A8-46EE-A235-DDFD339BE281 v1.0 
Bindings: 
          ncacn_ip_tcp:10.10.10.134[49667]
          ncalrpc:[LRPC-da67a25ed48958ab31]

Protocol: [MS-PAN]: Print System Asynchronous Notification Protocol 
Provider: spoolsv.exe 
UUID    : 0B6EDBFA-4A24-4FC6-8A23-942B1ECA65D1 v1.0 
Bindings: 
          ncacn_ip_tcp:10.10.10.134[49667]
          ncalrpc:[LRPC-da67a25ed48958ab31]

Protocol: [MS-RPRN]: Print System Remote Protocol 
Provider: spoolsv.exe 
UUID    : 12345678-1234-ABCD-EF00-0123456789AB v1.0 
Bindings: 
          ncacn_ip_tcp:10.10.10.134[49667]
          ncalrpc:[LRPC-da67a25ed48958ab31]

Protocol: N/A 
Provider: N/A 
UUID    : 1A0D010F-1C33-432C-B0F5-8CF4E8053099 v1.0 IdSegSrv service
Bindings: 
          ncalrpc:[LRPC-cdef0c9b78777f69fe]

Protocol: N/A 
Provider: srvsvc.dll 
UUID    : 98716D03-89AC-44C7-BB8C-285824E51C4A v1.0 XactSrv service
Bindings: 
          ncalrpc:[LRPC-cdef0c9b78777f69fe]

Protocol: [MS-SCMR]: Service Control Manager Remote Protocol 
Provider: services.exe 
UUID    : 367ABB81-9844-35F1-AD32-98F038001003 v2.0 
Bindings: 
          ncacn_ip_tcp:10.10.10.134[49668]

Protocol: [MS-FASP]: Firewall and Advanced Security Protocol 
Provider: FwRemoteSvr.dll 
UUID    : 6B5BDD1E-528C-422C-AF8C-A4079BE4FE48 v1.0 Remote Fw APIs
Bindings: 
          ncacn_ip_tcp:10.10.10.134[49669]

Protocol: N/A 
Provider: N/A 
UUID    : E38F5360-8572-473E-B696-1B46873BEEAB v1.0 
Bindings: 
          ncalrpc:[LRPC-82ac649d8889f1d368]

Protocol: N/A 
Provider: N/A 
UUID    : 4C9DBF19-D39E-4BB9-90EE-8F7179B20283 v1.0 
Bindings: 
          ncalrpc:[LRPC-82ac649d8889f1d368]

Protocol: [MS-CMPO]: MSDTC Connection Manager: 
Provider: msdtcprx.dll 
UUID    : 906B0CE0-C70B-1067-B317-00DD010662DA v1.0 
Bindings: 
          ncalrpc:[LRPC-99a21f569845e1e715]
          ncalrpc:[OLED0A22333CED8F3E6663B732EF17B]
          ncalrpc:[LRPC-e27c7fcc0787c75a89]
          ncalrpc:[LRPC-e27c7fcc0787c75a89]
          ncalrpc:[LRPC-e27c7fcc0787c75a89]

Protocol: [MS-SAMR]: Security Account Manager (SAM) Remote Protocol 
Provider: samsrv.dll 
UUID    : 12345778-1234-ABCD-EF00-0123456789AC v1.0 
Bindings: 
          ncacn_ip_tcp:10.10.10.134[49670]
          ncalrpc:[samss lpc]
          ncalrpc:[SidKey Local End Point]
          ncalrpc:[protected_storage]
          ncalrpc:[lsasspirpc]
          ncalrpc:[lsapolicylookup]
          ncalrpc:[LSA_EAS_ENDPOINT]
          ncalrpc:[LSA_IDPEXT_ENDPOINT]
          ncalrpc:[lsacap]
          ncalrpc:[LSARPC_ENDPOINT]
          ncalrpc:[securityevent]
          ncalrpc:[audit]
          ncacn_np:\\BASTION[\pipe\lsass]

Protocol: N/A 
Provider: N/A 
UUID    : 51A227AE-825B-41F2-B4A9-1AC9557A1018 v1.0 Ngc Pop Key Service
Bindings: 
          ncalrpc:[samss lpc]
          ncalrpc:[SidKey Local End Point]
          ncalrpc:[protected_storage]
          ncalrpc:[lsasspirpc]
          ncalrpc:[lsapolicylookup]
          ncalrpc:[LSA_EAS_ENDPOINT]
          ncalrpc:[LSA_IDPEXT_ENDPOINT]
          ncalrpc:[lsacap]
          ncalrpc:[LSARPC_ENDPOINT]
          ncalrpc:[securityevent]
          ncalrpc:[audit]
          ncacn_np:\\BASTION[\pipe\lsass]

Protocol: N/A 
Provider: N/A 
UUID    : 8FB74744-B2FF-4C00-BE0D-9EF9A191FE1B v1.0 Ngc Pop Key Service
Bindings: 
          ncalrpc:[samss lpc]
          ncalrpc:[SidKey Local End Point]
          ncalrpc:[protected_storage]
          ncalrpc:[lsasspirpc]
          ncalrpc:[lsapolicylookup]
          ncalrpc:[LSA_EAS_ENDPOINT]
          ncalrpc:[LSA_IDPEXT_ENDPOINT]
          ncalrpc:[lsacap]
          ncalrpc:[LSARPC_ENDPOINT]
          ncalrpc:[securityevent]
          ncalrpc:[audit]
          ncacn_np:\\BASTION[\pipe\lsass]

Protocol: N/A 
Provider: N/A 
UUID    : B25A52BF-E5DD-4F4A-AEA6-8CA7272A0E86 v2.0 KeyIso
Bindings: 
          ncalrpc:[samss lpc]
          ncalrpc:[SidKey Local End Point]
          ncalrpc:[protected_storage]
          ncalrpc:[lsasspirpc]
          ncalrpc:[lsapolicylookup]
          ncalrpc:[LSA_EAS_ENDPOINT]
          ncalrpc:[LSA_IDPEXT_ENDPOINT]
          ncalrpc:[lsacap]
          ncalrpc:[LSARPC_ENDPOINT]
          ncalrpc:[securityevent]
          ncalrpc:[audit]
          ncacn_np:\\BASTION[\pipe\lsass]

Protocol: N/A 
Provider: N/A 
UUID    : F3F09FFD-FBCF-4291-944D-70AD6E0E73BB v1.0 
Bindings: 
          ncalrpc:[LRPC-b3049613527b00d498]

Protocol: N/A 
Provider: N/A 
UUID    : FF9FD3C4-742E-45E0-91DD-2F5BC632A1DF v1.0 appxsvc
Bindings: 
          ncalrpc:[LRPC-41156f309bc9862eb6]

Protocol: N/A 
Provider: N/A 
UUID    : AE2DC901-312D-41DF-8B79-E835E63DB874 v1.0 appxsvc
Bindings: 
          ncalrpc:[LRPC-41156f309bc9862eb6]

[*] Received 406 endpoints.

```

---
