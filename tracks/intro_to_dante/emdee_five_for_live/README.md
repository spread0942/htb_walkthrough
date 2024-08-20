# Emdee five for life

Date: 2024/08/20

## Overview

In this lab, you are presented with a web endpoint. When accessed, the web page asks you to encrypt a given text using the MD5 hash algorithm. However, manually providing the MD5 hash results in a "Too slow!" message.

To solve this challenge, I created a Python script that automates the process of fetching the text, generating the MD5 hash, and submitting it back to the server to retrieve the flag.

## Requirements

The script requires the following Python modules:

* `requests`
* `BeautifulSoup`
* `hashlib`

Install the necessary dependencies by running:

```bash
pip3 install -r requirements.txt
```
## Usage

Update the endpoint in the main.py script to match the one provided in the lab.
Run the script to automatically retrieve the flag:

```bash
└─# python3 main.py  
[+] H3 tag clear text: rwnp7W5Jl5JuFRP62oRM
[+] H3 tag MD5 hash: 80a7d5729f1bf570d0b3578870b4a6c8
[+] Flag: HTB{...}
```

The script extracts the text within the `<h3>` tag, computes its MD5 hash, and submits the result to the server, returning the flag.

***

