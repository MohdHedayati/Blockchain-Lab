# Blockchain Lab

Seven small experiments covering the building blocks of blockchains: finite fields, cryptography, hashing, Bitcoin keys, proof of work and Bitcoin Script.

**Requirements:** Python 3.8+ (no extra packages). Experiment 2 also needs OpenSSL (it comes with Git for Windows, so Git Bash works).

Run every script **from inside its own folder**, e.g. `cd exp1_finite_field` first. Each folder has a `sample_output.txt` showing a real run.

---

## Experiment 1 - Finite field element
**What it is:** A finite field F_p is the set of numbers 0 to p-1 where all arithmetic wraps around ("mod p"). Cryptography (including Bitcoin) is built on this. The `FieldElement` class stores a number and its prime, rejects numbers outside the range, and supports `==`, `+`, `-` and `*`.

```
cd exp1_finite_field
python field_element.py
```
Shows equality checks, arithmetic in F_31, and an invalid element raising `ValueError`.

## Experiment 2 - OpenSSL
**What it is:** Using the OpenSSL command-line tool for the basics of encryption. It generates 128/192/256-bit symmetric keys, encrypts a file with your name and address using AES, decrypts it back, and creates an RSA key pair.

```
cd exp2_openssl
bash commands.sh
```
To change the name or address, edit the `printf` line in `commands.sh`. Each run generates new keys.

## Experiment 3 - Merkle tree and hash chain
**What it is:**
- **Merkle tree:** every transaction is hashed, then hashes are paired and hashed again until one **root** remains. That root is a fingerprint of all the transactions; change any one and the root changes.
- **Hash chain:** each document's hash is combined with the previous hash, so every hash depends on everything before it.

```
cd exp3_merkle_hashchain
python merkle_tree.py     # 10 grade transactions -> Merkle root
python make_pdfs.py       # (optional) regenerates the 4 made-up grade-card PDFs
python hash_chain.py      # hashes the PDFs in pdfs/ -> final chain hash
```
To use your real grade cards, replace the files in `pdfs/` (keep the names `semesterN_gradecard.pdf`).

## Experiment 4 - Bitcoin keys and addresses
**What it is:** The path from a random number to a Bitcoin address: private key -> public key (elliptic curve math) -> hash -> Base58Check address. It also produces the WIF (a printable form of the private key), compressed and uncompressed versions, and a **vanity address**, which is one that starts with letters you choose, found by trying random keys until one matches.

```
cd exp4_bitcoin_keys
python keys.py            # vanity prefix defaults to 1Ka
python keys.py 1Abc       # your own prefix
```
Each extra character makes the search about 58 times slower, so keep prefixes short.

## Experiment 5 - Proof of Work
**What it is:** A mini blockchain where adding a block requires finding a **nonce** so the block's hash starts with several zeros. This takes effort to find but is instant to verify, which is what makes tampering expensive. It mines 4 blocks from the four records (including the registration ID), then shows that editing a block breaks the chain.

```
cd exp5_proof_of_work
python pow.py
```
Change `DIFFICULTY` at the top of `pow.py` to make mining faster (lower) or slower (higher).

## Experiment 6 - P2PKH script
**What it is:** Pay-to-Public-Key-Hash is the standard way Bitcoin locks coins to an address. The **locking script** says "whoever shows a public key matching this hash and a valid signature can spend". A small Script interpreter in `common/script.py` runs the unlocking and locking scripts step by step. A simulation, not a real network.

```
cd exp6_p2pkh
python p2pkh.py
```
Shows the scripts, an execution trace, a valid spend, and failed attacker attempts.

## Experiment 7 - 2-of-2 multisig
**What it is:** A multisig address needs several signatures to spend. Here both Alice **and** Bob must sign. The address is a P2SH address (starts with `3`) made from a hash of the redeem script. Also a simulation.

```
cd exp7_multisig
python multisig.py
```
Shows address creation, locking, a spend with both signatures, and failures (only one signature, fake signature, wrong order, wrong redeem script).

---

## Folder layout
```
common/    btc.py (keys, ECDSA, Base58, addresses), script.py (Script interpreter)
exp1_... to exp7_...   one folder per experiment, each with sample_output.txt
```
> Educational code only. Do not use these keys or scripts with real funds.
