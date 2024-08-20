#!/bin/python3
import requests
from bs4 import BeautifulSoup
import hashlib


if __name__ == '__main__':
    url = 'http://94.237.59.63:48408/' # change here

    try:
        session = requests.Session()
        response = session.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            
            clear_text = soup.find('h3').text

            print(f'[+] H3 tag clear text: {clear_text}')
            md5 = hashlib.md5(clear_text.encode()).hexdigest()
            print(f'[+] H3 tag MD5 hash: {md5}')
            
            response = session.post(url,
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                data={'hash':md5})

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                flag = soup.find('p').text
                print(f'[+] Flag: {flag}')
            else:
                response.raise_for_status()
        else:
            response.raise_for_status()
    except KeyboardInterrupt:
        print('[+] Detected Ctrl+C, quitting...')
    except Exception as ex:
        print(f'[-] {ex}')
