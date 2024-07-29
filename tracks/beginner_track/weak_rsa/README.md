# Weak Rsa

Date: 20240729

This challenge was quiet easy, thankfully to a Rsa Ctf tool: [GitHub - RsaCtfTool](https://github.com/RsaCtfTool/RsaCtfTool).

To complete it you just download it locally, install the reqired packages and run against your files:

```bash
git clone https://github.com/RsaCtfTool/RsaCtfTool.git /opt/RsaCtfTool
cd /opt/RsaCtfTool
pip3 install -r requirements.txt
./RsaCtfTool.py --publickey <PUBLIC KEY LOCATION> --decryptfile <ENCRYPTED FILE LOCATION>
....
utf-8 : HTB{...}
....
```

But I decide to understand a little bit more I decide to understand a little bit more the fundamental.
RSA is an assymetric keys exchange used to encrypt data from a destination to another.
In this protocol there are some important information:

* `p` and `q`       -> primes
* `n = p * q`       -> modulus
* `e`               -> exponent
* `d`               -> modular multiplicative inverse to e

The Public Key is share with all the people and it is use to encrypt information. You can encrypt a message if you know the following information:

* `m`               -> the message to encrypt
* `c = m^e mod n`   -> with this formula we can get the encrypted message

The Private Key, as the name said, is a private key, you can't share it to anyone. It's use to decrypt the message if you have the following information:

* `c`               -> the encrypted message
* `m = c^d mod n`   -> you get back the message with this formula

In the `./rsa/` folder there is a naive example of RSA key exchange.
After that I understand a little bit better the RSA protocol I try to analyze the [RsaCtfTool](https://github.com/RsaCtfTool/RsaCtfTool).
I have create a new simplify script to get the flag.
In the RsaCtfTool.py at the end there is a method that run the attack (should be at line 585):

```python
args = run_attacks(args, logger)
```

This function handled the public key attack, in this scenario it will do a single key attack:

```python
# Attack key
if args.publickey is not None:
    for publickey in args.publickey:
        attackobj.implemented_attacks = []
        attackobj.decrypted = []
        logger.info("\n[*] Testing key %s." % publickey)
        attackobj.attack_single_key(publickey, selected_attacks)
```

In this attacks load several possible attack:

```python
self.load_attacks(attacks_list)
```

Then it read and load the Public Key, the Public Key is handled by a class:

```python
# Read keyfile
try:
    with open(publickey, "rb") as pubkey_fd:
        self.publickey = PublicKey(pubkey_fd.read(), filename=publickey)
except Exception as e:
    self.logger.error(f"[!] {e}.")
    return
```

Then they are performing all the attacks, one that works is with [pastctfprimes.py](https://github.com/RsaCtfTool/RsaCtfTool/blob/master/attacks/single_key/pastctfprimes.py) file, which is doing a factorization attack trying weak prime number from all previous CTF flags:

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
            primes = sorted([int(l.rstrip()) for l in open(txtfile, "r").readlines()])
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

Then it generate the PrivateKey, handled by a class:

```python
self.priv_key = priv_key = PrivateKey(
    self.args.p, self.args.q, self.args.e, self.args.n
)
```

At the end there is the [print_result_details](https://github.com/RsaCtfTool/RsaCtfTool/blob/master/lib/rsa_attack.py#L58) where it decrypt the message with the private key founded:

```python
for priv_key in priv_keys:
    decrypted = priv_key.decrypt(cipher)
    if not isinstance(decrypted, list):
        decrypted = [decrypted]
```







