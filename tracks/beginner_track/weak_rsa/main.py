from Crypto.PublicKey import RSA
import logging
import tempfile
import subprocess
import gmpy2
import sys


if __name__ == '__main__':
    if len(sys.argv) != 3:
        logging.error('[-] Require two parameters')
        logging.error(f'[-] Run: {sys.argv[0]} <PUBLIC KEY> <ENC FILE>')
        sys.exit(1)
    
    key_path = sys.argv[1]
    cipher = sys.argv[2]
    key = b''
    
    with open(key_path, 'rb') as f:
        key = f.read()
        logging.info('[+] Read Public Key')
    
    pub = RSA.importKey(key)
    logging.info('[+] Imported correctly')
    logging.info(f'[+] Modulus n: {pub.n}') # modulus n
    logging.info(f'[+] Public exponent: {pub.e}') # public exponent
    
    with open('./data/pastctfprimes.txt', 'r') as f:
        lines = f.readlines()
        logging.info('[+] Read lines from pastctfprimes.txt file')
        
        for l in lines:
            if pub.n % int(l) == 0:
                logging.info(f'[+] Found prime number: {l}')
                q = int(l)
                p = int(pub.n // q)
                e = int(pub.e)
                n = int(pub.n)
                phi = None
                d = None
                key = None

                if p is not None and q is not None and phi is None:
                    if p != q:
                        phi = (p - 1) * (q - 1)
                    else:
                        phi = (p**2) - p
                
                if phi is not None and e is not None:
                    try:
                        d = int(gmpy2.invert(e, phi))
                    except ValueError:
                        logging.error("[!] e^d==1 inversion error, check your math.")

                if p is not None and q is not None and d is not None:
                    try:
                        # There is no CRT coefficient to construct a key if p equals q
                        key = RSA.construct((n, e, d, p, q))
                        logging.info('[+] Got Private Key')
                    except ValueError:
                        logging.error("[!] Can't construct RSA PEM, internal error....")
                
                exp_key = ''

                if key is not None:
                    exp_key = key.exportKey().decode("utf-8")

                plain = ''
                
                try:
                    tmp_priv_key = tempfile.NamedTemporaryFile()
                    with open(tmp_priv_key.name, "wb") as tmpfd:
                        tmpfd.write(exp_key.encode("utf8"))
                    tmp_priv_key_name = tmp_priv_key.name
                    
                    c = b''
                    with open(cipher, 'rb') as f:
                        c = f.read()

                    tmp_cipher = tempfile.NamedTemporaryFile()
                    with open(tmp_cipher.name, "wb") as tmpfd:
                        tmpfd.write(c)
                    tmp_cipher_name = tmp_cipher.name

                    with open("/dev/null") as DN:
                        try:
                            openssl_result = subprocess.check_output(
                                [
                                    "openssl",
                                    "rsautl",
                                    "-raw",
                                    "-decrypt",
                                    "-in",
                                    "-oaep",
                                    tmp_cipher_name,
                                    "-inkey",
                                    tmp_priv_key_name,
                                ],
                                stderr=DN,
                                timeout=30,
                            )
                            plain = openssl_result
                        except:
                            pass

                        try:
                            openssl_result = subprocess.check_output(
                                [
                                    "openssl",
                                    "rsautl",
                                    "-raw",
                                    "-decrypt",
                                    "-in",
                                    tmp_cipher_name,
                                    "-inkey",
                                    tmp_priv_key_name,
                                ],
                                stderr=DN,
                                timeout=30,
                            )
                            plain = openssl_result
                        except:
                            pass
                except Exception as ex:
                    logging.error(f'[-] Exception: {ex}')
    print(plain)