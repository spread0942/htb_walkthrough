# Weak Rsa

Date: 2024-07-29

## Walkthrough

This challenge was quite easy, thanks to an RSA CTF tool: [GitHub - RsaCtfTool](https://github.com/RsaCtfTool/RsaCtfTool/tree/master).

To complete it, you just need to download it locally, install the required packages, and run it against your files:

```bash
git clone https://github.com/RsaCtfTool/RsaCtfTool.git /opt/RsaCtfTool
cd /opt/RsaCtfTool
pip3 install -r requirements.txt
./RsaCtfTool.py --publickey <PUBLIC KEY LOCATION> --decryptfile <ENCRYPTED FILE LOCATION>
....
utf-8 : HTB{...}
...
```

## RSA

I decided to understand the fundamentals a bit more. RSA is an asymmetric key encryption method used to encrypt data from one destination to another. In this protocol, there are some important components:

* `p` and `q` -> primes
* `n = p * q` -> modulus
* `e` -> exponent
* `d` -> modular multiplicative inverse of e

The Public Key is shared with everyone and is used to encrypt information. You can encrypt a message if you know the following information:

* `m` -> the message to encrypt
* `c = m^e mod n` -> with this formula, we get the encrypted message

The Private Key, as the name suggests, is kept private. It's used to decrypt the message if you have the following information:

* `c` -> the encrypted message
* `m = c^d mod n` -> you get back the original message with this formula

In the [rsa](https://github.com/spread0942/htb_walkthrough/tree/main/tracks/beginner_track/weak_rsa/rsa) folder, there is a naive example of RSA key exchange. After understanding the RSA protocol better, I decided to analyze the RsaCtfTool. I created a simplified script to get the flag.

## RsaCtfTool.py analysis

You can find the repo at [RsaCtfTool](https://github.com/RsaCtfTool/RsaCtfTool/tree/master).

I started from the RsaCtfTool.py script, at the end, there is a method that runs the attack (should be around line 585):

```python
args = run_attacks(args, logger)
```

This function handles the public key attack. In this scenario, it performs a single key attack:

```python
# Attack key
if args.publickey is not None:
    for publickey in args.publickey:
        attackobj.implemented_attacks = []
        attackobj.decrypted = []
        logger.info("\n[*] Testing key %s." % publickey)
        attackobj.attack_single_key(publickey, selected_attacks)
```

This loads several possible attacks:

```python
self.load_attacks(attacks_list)
```

Then it reads and loads the Public Key, which is handled by a class:

```python
# Read keyfile
try:
    with open(publickey, "rb") as pubkey_fd:
        self.publickey = PublicKey(pubkey_fd.read(), filename=publickey)
except Exception as e:
    self.logger.error(f"[!] {e}.")
    return
```

Then, it performs all the attacks. One that works is found in the [pastctfprimes.py](https://github.com/RsaCtfTool/RsaCtfTool/blob/master/attacks/single_key/pastctfprimes.py) file, which performs a factorization attack by trying weak prime numbers from previous CTF flags:

```python
# Loop through implemented attack methods and conduct attacks
for attack_module in self.implemented_attacks:
    t0 = time.time()
    if self.need_run:
        self.logger.info(
            f"[*] Performing {attack_module.get_name()} attack on {self.publickey.filename}."
        )
```

In more detail:

```python
class Attack(AbstractAttack):
    def __init__(self, timeout=60):
        super().__init__(timeout)
        self.speed = AbstractAttack.speed_enum["fast"]

    def attack(self, publickey, cipher=[], progress=True):
        """Search for previously used primes in CTFs"""
        for txtfile in glob.glob("data/*.txt"):
            self.logger.info(f"[+] loading prime list file {txtfile}...")
            primes are sorted([int(l.rstrip()) for l in open(txtfile, "r").readlines()])
            for prime in tqdm(primes, disable=(not progress)):
                if is_divisible(publickey.n, prime):
                    publickey.q = prime
                    publickey.p = publickey.n // publickey.q
                    priv_key = PrivateKey(
                        int(publickey.p),
                        int(publickey.q),
                        int(publickey.e),
                        int(publickey.n),
                    )
                    return priv_key, None
        return None, None
```

Then it generates the PrivateKey, which is handled by a class:

```python
self.priv_key = priv_key = PrivateKey(
    self.args.p, self.args.q, self.args.e, self.args.n
)
```

At the end, there is the print_result_details function where it decrypts the message with the found private key:

```python
for priv_key in priv_keys:
    decrypted = priv_key.decrypt(cipher)
    if not isinstance(decrypted, list):
        decrypted = [decrypted]
```

## How to run

To run the script:

```python
python main.py <PUB KEY> <ENCRYPT FLAG>
```

***




