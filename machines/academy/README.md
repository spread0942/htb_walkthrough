# Lab Academy

Date: 2024/06/23

## Enumeration

### Port Scanning

I found three open ports by running the following Nmap command:

```bash
nmap -sV -sC -O -p22,80,33060 <IP> -v -oN services/v_ports.txt -oX services/v_ports.xml
```

The scan provided the following information:

```ruby
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 c0:90:a3:d8:35:25:6f:fa:33:06:cf:80:13:a0:a5:53 (RSA)
|   256 2a:d5:4b:d0:46:f0:ed:c9:3c:8d:f6:5d:ab:ae:77:96 (ECDSA)
|_  256 e1:64:14:c3:cc:51:b2:3b:a6:28:a7:b1:ae:5f:45:35 (ED25519)
80/tcp    open  http    Apache httpd 2.4.41 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Hack The Box Academy
|_http-server-header: Apache/2.4.41 (Ubuntu)
33060/tcp open  mysqlx?
| fingerprint-strings: 
|   DNSStatusRequestTCP, LDAPSearchReq, NotesRPC, SSLSessionReq, TLSSessionReq, X11Probe, afp: 
|     Invalid message"
|_    HY000
```

### Port 80 Analysis

To properly access the web service, I edited the hosts file located at */etc/hosts* and mapped the target IP to the name **academy.htb**. I then used BurpSuite to update the scope and track only the target hostname.

The website presented a simple web application allowing user registration and login. After logging in, the user is presented with a basic web page.
Using BurpSuite, I noticed that I could change the role ID from 0 to 1 during registration, allowing access to an admin page (admin.php). The modified request looked like this:

```
uid=super1&password=super1&confirm=super1&roleid=1
```

On the admin page, I found a virtual hostname **dev-staging-01.academy.htb**, which I also added to the hosts file. This new application provided additional information:

```
* SERVER_SOFTWARE   "Apache/2.4.41 (Ubuntu)"
* DOCUMENT_ROOT     "/var/www/html/htb-academy-dev-01/public"
* SERVER_ADMIN      "admin@htb"
* APP_DEBUG         "true"
* APP_NAME          "Laravel"
* DB_DATABASE       "homestead"
* DB_USERNAME       "homestead"
* DB_PASSWORD       "secret"
```

## Exploitation

Using Metasploit, I searched for potential exploits:

```bash
search laravel type:exploits
```

I found and used the exploit/unix/http/laravel_token_unserialize_exec module to get a shell as the www-data user.

## Post-Exploitation

In the academy web root folder, I found another **.env** file:

```bash
APP_NAME=Laravel
APP_ENV=local
APP_KEY=base64:dBLUaMuZz7Iq06XtL/Xnz/90Ejq+DEEynggqubHWFj0=
APP_DEBUG=false
APP_URL=http://localhost

LOG_CHANNEL=stack

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=academy
DB_USERNAME=dev
DB_PASSWORD=mySup3rP4s5w0rd!!

BROADCAST_DRIVER=log
CACHE_DRIVER=file
SESSION_DRIVER=file
SESSION_LIFETIME=120
QUEUE_DRIVER=sync

REDIS_HOST=127.0.0.1
REDIS_PASSWORD=null
REDIS_PORT=6379 

MAIL_DRIVER=smtp
MAIL_HOST=smtp.mailtrap.io
MAIL_PORT=2525
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null

PUSHER_APP_ID=
PUSHER_APP_KEY=
PUSHER_APP_SECRET=
PUSHER_APP_CLUSTER=mt1

MIX_PUSHER_APP_KEY="${PUSHER_APP_KEY}"
MIX_PUSHER_APP_CLUSTER="${PUSHER_APP_CLUSTER}"
```

Here I notice an interesting password: **mySup3rP4s5w0rd!!**.

## User Enumeration

From the */home* directory, I listed the users:

```bash
www-data@academy:/home$ ls -la
total 32
drwxr-xr-x  8 root     root     4096 Aug 10  2020 .
drwxr-xr-x 20 root     root     4096 Feb 10  2021 ..
drwxr-xr-x  2 21y4d    21y4d    4096 Aug 10  2020 21y4d
drwxr-xr-x  2 ch4p     ch4p     4096 Aug 10  2020 ch4p
drwxr-xr-x  4 cry0l1t3 cry0l1t3 4096 Aug 12  2020 cry0l1t3
drwxr-xr-x  3 egre55   egre55   4096 Aug 10  2020 egre55
drwxr-xr-x  2 g0blin   g0blin   4096 Aug 10  2020 g0blin
drwxr-xr-x  5 mrb3n    mrb3n    4096 Aug 12  2020 mrb3n
```

I also checked the */etc/passwd* file:

```bash
cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
...
egre55:x:1000:1000:egre55:/home/egre55:/bin/bash
lxd:x:998:100::/var/snap/lxd/common/lxd:/bin/false
mrb3n:x:1001:1001::/home/mrb3n:/bin/sh
cry0l1t3:x:1002:1002::/home/cry0l1t3:/bin/sh
mysql:x:112:120:MySQL Server,,,:/nonexistent:/bin/false
21y4d:x:1003:1003::/home/21y4d:/bin/sh
ch4p:x:1004:1004::/home/ch4p:/bin/sh
g0blin:x:1005:1005::/home/g0blin:/bin/sh
```

I used the password *mySup3rP4s5w0rd!!* from the .env file to access the user **cry0l1t3**.

## Local Enumeration

I check manually to enumerate local information, but I did't get any infomration.
I uploaded the [linPEAS.sh](https://github.com/peass-ng/PEASS-ng/blob/master/linPEAS/README.md) script to automate local enumerate and I found a new password for user **mrb3n** with **mrb3n_Ac@d3my!**.
Using this password, I gained access to the user and found that they had sudo permissions for the **composer** binary.
Referring to [GTFOBins](https://gtfobins.github.io/gtfobins/composer/#sudo), I executed commands to escalate privileges to root.

*** 
