#!/bin/python3
from rsa import key_generation
from eval import decrypt

priv, pub = key_generation(300)
print("[+] Done with key generation")

m = int(input("[?] Enter your number message: "))
c = pub.encrypt_message(m)
print(f"[+] Your encrypted message: {c}")
m = priv.decrypt_message(c)
print(f"[+] Your decrypted message: {m}")
m = decrypt(pub, c)
print(f'[+] Eval decrypt the message: {m}')