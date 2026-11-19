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

## VS Code snippets
Every experiment is also saved as a VS Code snippet, so you can paste the full code anywhere by typing its prefix and pressing Tab/Enter. They live in your user snippets folder (`%APPDATA%\Code\User\snippets\`), not in this repo.

| Type this | In a | Pastes |
|---|---|---|
| `exp1_finite_field` | `.py` file | Experiment 1 |
| `exp2_openssl` | `.sh` file | Experiment 2 (in `shellscript.json`) |
| `exp3_merkle_tree` | `.py` file | Experiment 3, Merkle tree |
| `exp3_make_pdfs` | `.py` file | Experiment 3, creates the dummy PDFs |
| `exp3_hash_chain` | `.py` file | Experiment 3, hash chain (run `exp3_make_pdfs` first) |
| `exp4_bitcoin_keys` | `.py` file | Experiment 4 (self-contained) |
| `exp5_proof_of_work` | `.py` file | Experiment 5 |
| `exp6_p2pkh` | `.py` file | Experiment 6 (self-contained) |
| `exp7_multisig` | `.py` file | Experiment 7 (self-contained) |

Experiments 4, 6 and 7 include the code from `common/`, so they run without that folder. The snippets are copies: if you edit the code in the repo, the snippets do not update.

## Espanso triggers (work in any app)
The same experiments are also available system-wide through [espanso](https://espanso.org). Type a trigger anywhere (editor, browser, notepad) and the full code is pasted. They live in `%APPDATA%\espanso\match\blockchain_lab.yml`, not in this repo.

| Trigger | Short | Pastes |
|---|---|---|
| `:exp1_finite_field` | `:bc1` | Experiment 1 |
| `:exp2_openssl` | `:bc2` | Experiment 2 (shell commands) |
| `:exp3_merkle_tree` | `:bc3a` | Experiment 3, Merkle tree |
| `:exp3_make_pdfs` | `:bc3b` | Experiment 3, dummy PDF generator |
| `:exp3_hash_chain` | `:bc3c` | Experiment 3, hash chain |
| `:exp4_bitcoin_keys` | `:bc4` | Experiment 4 (self-contained) |
| `:exp5_proof_of_work` | `:bc5` | Experiment 5 |
| `:exp6_p2pkh` | `:bc6` | Experiment 6 (self-contained) |
| `:exp7_multisig` | `:bc7` | Experiment 7 (self-contained) |

Like the VS Code snippets, these are copies and do not update when the repo code changes.

## Folder layout
```
common/    btc.py (keys, ECDSA, Base58, addresses), script.py (Script interpreter)
exp1_... to exp7_...   one folder per experiment, each with sample_output.txt
```
> Educational code only. Do not use these keys or scripts with real funds.

---
---

# Detailed explanations (for explaining the code in the lab / viva)

## Experiment 1 - Finite field element (`exp1_finite_field/field_element.py`)

**Concept.** A finite field F_p, with p prime, is the set {0, 1, ..., p-1} with addition, subtraction and multiplication done "mod p" (clock arithmetic). Because p is prime, every non-zero element also has a multiplicative inverse (division), which is why prime fields are used in elliptic-curve cryptography. Bitcoin's curve works over a field with a 256-bit prime.

**Code walkthrough.**
- `__init__(num, prime)` stores both values as attributes. The check `if num < 0 or num >= prime` raises `ValueError`, so an object can only ever hold a valid field element. Rejecting invalid input at construction means no later operation has to re-check it.
- `__repr__` gives a readable form such as `FieldElement_31(2)` for printing.
- `__eq__` returns `True` only if `other` is a `FieldElement` **and** both `num` and `prime` match. So `2 in F_31` is not equal to `2 in F_17`. `__ne__` is the negation.
- `_check` is a helper: arithmetic between elements of different fields is meaningless, so it raises `TypeError`.
- `__add__`, `__sub__`, `__mul__` compute the plain integer operation and then `% prime`. Python's `%` always returns a non-negative result for a positive modulus, so `2 - 15 = -13` becomes `18` in F_31 with no special handling. The result is wrapped in a new `FieldElement`, so it is guaranteed to be in the same field.
- Defining `__add__` etc. is **operator overloading**: it lets us write `a + b` for our own class.

**Demo (`__main__`).** Uses p = 31, shows equality/inequality, the three operations, two invalid elements (31 and -1 in F_31) caught by `try/except`, and a cross-field operation that raises `TypeError`.

**Not implemented (not required):** division/inverse (done via Fermat's little theorem: `a^(p-2) mod p`) and exponentiation.

## Experiment 2 - OpenSSL (`exp2_openssl/commands.sh`)

**Concepts.**
- **Symmetric encryption:** the same secret key encrypts and decrypts (AES). Fast, but the key has to be shared secretly.
- **Asymmetric encryption:** a key *pair* - the public key encrypts (or verifies), the private key decrypts (or signs). RSA is the classic example.
- AES key sizes: 128, 192, 256 bits = 16, 24, 32 bytes.

**Commands, step by step.**
1. `openssl rand -hex 16 / 24 / 32` produces 16/24/32 cryptographically random bytes, printed as hex. These are the 128/192/256-bit keys, saved into `key128.txt`, `key192.txt`, `key256.txt`.
2. `printf ... > details.txt` creates the plaintext file with the name and address.
3. `openssl rand -hex 16` makes a 128-bit **IV** (initialisation vector). CBC mode needs one so that encrypting the same text twice gives different ciphertext.
4. `openssl enc -aes-256-cbc -in details.txt -out details.enc -K <key> -iv <iv>` encrypts. `-K` (capital) gives the raw hex key directly. (Using `-k`/`-pass` instead would derive the key from a password.) AES-CBC works on 16-byte blocks and **PKCS#7 padding** is added to the last block, which is why the ciphertext is a bit longer than the input.
5. `openssl enc -d ...` with the same key and IV decrypts. `diff` proves the decrypted file is identical to the original.
6. The 128-bit and 192-bit keys are used the same way with `-aes-128-cbc` and `-aes-192-cbc`.
7. `openssl genrsa -out rsa_private.pem 2048` generates a 2048-bit RSA private key (it contains the two primes p, q, the modulus n = p*q, and the exponents).
8. `openssl rsa -in rsa_private.pem -pubout -out rsa_public.pem` extracts the public key (n and e = 65537).
9. Bonus: `openssl pkeyutl -encrypt -pubin ...` / `-decrypt` encrypts a short message with the public key and decrypts with the private one. RSA can only encrypt data smaller than the key size, so in practice it encrypts a symmetric key and AES encrypts the bulk data (hybrid encryption).

**Security notes.** Never share `rsa_private.pem`. CBC without a MAC gives confidentiality but not integrity (AES-GCM is better in real systems).

## Experiment 3 - Merkle tree and hash chain (`exp3_merkle_hashchain/`)

**Concept - hash function.** SHA-256 turns any input into a fixed 256-bit digest. It is deterministic, one-way, and a tiny change in the input changes the output completely (avalanche effect).

### 3.1 Merkle tree (`merkle_tree.py`)
A Merkle tree is a binary tree of hashes. The leaves are hashes of the data items; every parent is the hash of its two children; the single top hash is the **Merkle root**. The root commits to the whole set: changing any one transaction changes its leaf, every hash above it, and finally the root. Bitcoin stores the Merkle root in each block header so a block's header commits to all its transactions.

- `make_transactions(10)` builds 10 text transactions of the form `TXn|student=...|sem=...|subject=...|grade=...`. Five subjects per semester, so 10 transactions = 2 semesters. A fixed random seed makes the grades reproducible.
- `sha256(data)` hashes a string and returns hex.
- `build_merkle_tree(leaves)`: level 0 = hash of each transaction. While more than one node remains: if the count is odd, **duplicate the last node** (this is Bitcoin's rule); then hash each pair as `sha256(left + right)`. The levels are stored in a list, so `levels[-1][0]` is the root. With 10 leaves the levels have 10 -> 5 -> 3 -> 2 -> 1 nodes (5 and 3 are odd and get a duplicate).
- The demo prints every level, the root as the "digital fingerprint", then edits TX4 and shows the root changes (tamper evidence).
- Simplification: the pair is joined by concatenating the *hex strings*; Bitcoin concatenates raw bytes and uses double SHA-256.
- Benefit: with a Merkle tree you can prove one transaction is in a block using only about log2(n) hashes (a **Merkle proof**, used by light/SPV wallets).

### 3.2 Hash chain (`hash_chain.py`, `make_pdfs.py`)
A hash chain links items so each hash depends on all previous ones: `chain_i = SHA256(chain_(i-1) || SHA256(document_i))`, starting from `chain_0 = 64 zeros` (genesis).
- `make_pdfs.py` writes four made-up grade-card PDFs by hand (a PDF is just a structured text file with objects, a cross-reference table and a trailer), so no library is needed. Replace them with real PDFs if you have them.
- `sha256_file` reads a file in 8 KB chunks (so large files don't fill memory) and returns its SHA-256.
- The main loop sorts the PDFs by name, hashes each, combines it with the running chain value, and prints the hash after every document plus the final hash.
- Altering any earlier PDF changes its hash and therefore every later chain hash, so one final hash proves the integrity *and order* of all documents. This is the same idea as blocks linked by `prev_hash` in a blockchain.

**Merkle tree vs hash chain:** the Merkle tree gives a fingerprint of an *unordered set* with efficient membership proofs; the hash chain gives a fingerprint of an *ordered sequence* where verifying requires walking the chain.

## Experiment 4 - Bitcoin keys and addresses (`exp4_bitcoin_keys/keys.py`, `common/btc.py`)

**The pipeline:**
`private key -> (elliptic curve multiplication) -> public key -> SHA-256 -> RIPEMD-160 -> add version byte + checksum -> Base58 -> address`
Every step is one-way, so you cannot go backwards.

**Elliptic curve (secp256k1).** The curve is y^2 = x^3 + 7 over the prime field F_p with p = 2^256 - 2^32 - 977. A fixed generator point `G` has prime order `n` (the number of valid private keys). The public key is `K = k * G`, which means adding G to itself k times. Computing K from k is easy; recovering k from K is the **elliptic curve discrete log problem**, which is infeasible.

**Code in `btc.py`.**
- `point_add` implements the chord/tangent addition formulas with slope `m` (for doubling, `m = 3x^2 / 2y`; otherwise `m = (y2-y1)/(x2-x1)`), using `pow(x, -1, P)` for modular inverse. `None` represents the point at infinity.
- `point_mul(k, pt)` is **double-and-add**: it walks the bits of k, adding the current power-of-two multiple of the point when the bit is 1. This takes about 256 doublings instead of 2^256 additions.
- `gen_private_key()` picks a random integer in [1, n-1] using Python's `secrets` module (a cryptographically secure source, unlike `random`).
- `pubkey_bytes(point, compressed)`: **uncompressed** = `04 || x || y` (65 bytes). **Compressed** = `02 || x` if y is even, `03 || x` if y is odd (33 bytes). Since y can be recovered from x using the curve equation, only x and the parity of y are needed. `pubkey_from_bytes` does the recovery using `y = (x^3+7)^((p+1)/4) mod p` (works because p = 3 mod 4).
- `hash160(x) = RIPEMD160(SHA256(x))` gives a 20-byte digest. Two different hashes are used for extra safety and a shorter address.
- **Base58Check** (`b58check_encode`): append the first 4 bytes of `SHA256(SHA256(payload))` as a checksum, then encode in Base58. Base58 is base-58 with the visually ambiguous characters `0 O I l` removed, and each leading zero byte is written as `1`. The checksum lets software catch typing mistakes (`b58check_decode` raises an error on a bad checksum).
- `address_from_hash160(h, version)`: payload = version byte + hash160. Version `0x00` (mainnet P2PKH) gives addresses starting with `1`; `0x05` (P2SH) gives `3`.
- `wif(priv, compressed)`: **Wallet Import Format** = Base58Check of `0x80 || 32-byte private key [|| 0x01 if compressed]`. Uncompressed WIFs start with `5`; compressed start with `K` or `L`. The trailing `01` tells a wallet to use the compressed public key (and hence a different address).
- ECDSA signing and verification are also in this file (explained under Experiment 6).

**`keys.py` flow.** 1) generate private key; 2) compute public key (x, y), print both uncompressed and compressed; 3) compute the address for both forms (two different addresses from the same private key), showing hash160, payload and checksum; 4) demonstrate Base58Check encode/decode round trip; 5) print both WIF forms and decode one to prove it round-trips; 6) vanity search.

**Vanity address.** The loop generates random keys until the address starts with the prefix (default `1Ka`). Each Base58 character has probability about 1/58 of matching, and the leading `1` is fixed, so `1Ka` has two free characters and needs about 58^2 = 3,364 tries on average (we got 1,281). Every extra character multiplies the work by 58 - a tiny version of proof-of-work, since it is pure brute force. Real tools use GPUs and never share the private key with third parties.

## Experiment 5 - Proof of Work (`exp5_proof_of_work/pow.py`)

**Concept.** In a decentralised network nobody trusts anyone, so who gets to add the next block? In **Proof of Work** miners must find a number (the **nonce**) such that the block's hash is below a target - practically, starts with a number of zeros. Hashes can't be predicted, so the only way is to try nonces one by one. Finding the answer is costly; checking it takes one hash. This makes rewriting history expensive: to change an old block an attacker must redo the work for that block and all blocks after it, and outpace the honest network (the longest valid chain wins).

**Code.**
- `RECORDS` holds the four records from the experiment, including the registration ID 241080023. `DIFFICULTY = 5` means the hash must start with 5 hex zeros (= 20 bits), so about 16^5 ~ 1 million attempts on average.
- `Block` stores `index`, `timestamp`, `data`, `prev_hash` and `nonce`. `compute_hash()` serialises these fields to JSON and returns SHA-256. Because `prev_hash` is part of the hashed data, each block is cryptographically linked to the one before it.
- `mine(difficulty)` increments `nonce` and recomputes the hash until it starts with `"0" * difficulty`, and returns the time taken.
- `Blockchain.__init__` mines a **genesis** block (index 0, `prev_hash` all zeros). `add_block(data)` creates a block pointing at the last block's hash, mines it, and appends it.
- `is_valid()` re-checks every block: the stored hash must equal the recomputed hash, must satisfy the difficulty, and `prev_hash` must equal the previous block's hash.
- The demo mines blocks 1-4 (one per record), prints nonce, hash and mining time, then **tampers** with Block 2's data. Its hash no longer matches, so `is_valid()` returns `False`. Re-mining that block would also change its hash and break Block 3's `prev_hash`, and so on - the cascade that protects the chain.

**Notes.** Difficulty is a tuning knob: Bitcoin adjusts it every 2016 blocks to keep roughly 10 minutes between blocks. This is a single-machine simulation: there's no network, no competing miners, no fork resolution and no reward. Mining time varies run to run because the nonce needed is random.

## Experiment 6 - P2PKH script (`exp6_p2pkh/p2pkh.py`, `common/script.py`)

**Concepts.** Bitcoin has no "accounts"; it has **UTXOs** (unspent transaction outputs). Each output carries a small program, the **locking script** (`scriptPubKey`), and to spend it the new transaction supplies an **unlocking script** (`scriptSig`). Both run on a stack-based, non-Turing-complete language called **Script**. The spend is valid if running `scriptSig` followed by `scriptPubKey` leaves `TRUE` on top of the stack without errors.

**P2PKH** (the classic `1...` address) locks funds to the hash of a public key:
- Locking: `OP_DUP OP_HASH160 <pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG` (hex `76 a9 14 <20 bytes> 88 ac`)
- Unlocking: `<signature> <publicKey>`

**Execution, step by step** (stack grows to the right):
1. Push `<sig>`, push `<pubKey>`. Stack: `sig pubKey`
2. `OP_DUP` copies the top: `sig pubKey pubKey`
3. `OP_HASH160` replaces the copy with its hash: `sig pubKey H(pubKey)`
4. Push `<pubKeyHash>` from the locking script: `sig pubKey H(pubKey) pubKeyHash`
5. `OP_EQUALVERIFY` pops both, fails if different: `sig pubKey` (proves the public key matches the address)
6. `OP_CHECKSIG` pops pubKey and sig and verifies the signature: leaves `TRUE`

So the spender proves two things: they know the public key behind the address, and they hold the private key (via the signature).

**`script.py` (interpreter).**
- `encode`/`decode` convert between a Python list (opcode names or byte strings) and raw script bytes. Data is encoded as a length byte followed by the data; opcodes are single bytes (e.g. `0x76` = `OP_DUP`).
- `run(script, stack, z)` executes each item: data items are pushed, opcodes manipulate the stack. With `trace=True` it prints the stack before every step (this is the trace in the sample output).
- `validate()` runs `scriptSig` then `scriptPubKey` on the same stack and checks for a truthy top value. Any error (such as popping an empty stack) is treated as an invalid spend.

**ECDSA signing (in `btc.py`).** `z` is the hash of the data being signed. To sign with private key `d`: pick a secret nonce `k`, compute `r = (k*G).x mod n`, then `s = k^-1 * (z + r*d) mod n`. The signature is `(r, s)`. To verify with public key `Q`: compute `w = s^-1`, then the point `(z*w)*G + (r*w)*Q`; its x-coordinate must equal `r`. Only the holder of `d` can produce a valid pair, but anyone with `Q` can check it.
- `k` is generated deterministically from the key and message (RFC 6979 style, using HMAC). A reused or predictable `k` leaks the private key, which is how real wallets have been broken.
- `s` is forced to the "low" half (`s > n/2 -> n - s`) to prevent signature malleability.
- `der_encode`/`der_decode` use the DER format Bitcoin puts on-chain.

**What `p2pkh.py` does.** Creates Bob's key and address; builds the locking script from his address's hash; signs a stand-in transaction message and builds `<sig> <pubKey>`; prints the trace and `True`; then shows two attacks failing: (1) Mallory uses her own key - her public key does not hash to Bob's hash, so `OP_EQUALVERIFY` fails; (2) Mallory presents Bob's public key with her own signature - the hash check passes but `OP_CHECKSIG` fails.

**Simplification to mention.** Real Bitcoin signs a specific serialisation of the whole transaction (the "sighash", e.g. `SIGHASH_ALL`) and the signature carries a hash-type byte. Here we sign `SHA256d` of a text message; the Script logic is otherwise the real thing.

## Experiment 7 - 2-of-2 multisig (`exp7_multisig/multisig.py`)

**Concept.** A multisignature (m-of-n) output needs m valid signatures from a list of n public keys. 2-of-2 means both parties must agree (e.g. a joint account); 2-of-3 is common for escrow and backups. Bitcoin implements this with `OP_CHECKMULTISIG`.

**Bare multisig** locking script: `OP_2 <pubA> <pubB> OP_2 OP_CHECKMULTISIG` (m, the keys, n, then the opcode). This is long, which makes addresses huge and moves cost to the sender, so **P2SH (Pay-to-Script-Hash)** is used instead.

**P2SH.**
- The **redeem script** is the multisig script above.
- The address is `Base58Check(0x05 || HASH160(redeem script))`, which starts with `3`. The sender only needs this short address.
- Locking script: `OP_HASH160 <scriptHash> OP_EQUAL`
- Unlocking script: `OP_0 <sigA> <sigB> <redeemScript>`
- Validation has two phases: (1) the redeem script is hashed and compared with `<scriptHash>`; (2) if it matches, the redeem script itself is executed with the remaining stack. The interpreter in `script.py` does this when it sees the `OP_HASH160 <h> OP_EQUAL` pattern.

**`OP_CHECKMULTISIG` in the code.** It pops `n`, then n public keys, then `m`, then m signatures, then one extra dummy element. The dummy is needed because of a historical off-by-one bug in the original implementation that can't be fixed without a hard fork; that is why every unlocking script begins with `OP_0`. Signatures must appear in the **same order** as their public keys, because the algorithm walks both lists once from front to back (the code moves a key pointer forward until a signature verifies; if it runs out of keys, the result is false).

**`multisig.py` flow.** Generate Alice's and Bob's keys; build the redeem script and print its hex; compute the `3...` address; build the locking script; both sign the same message; build the unlocking script and validate with a trace (True). Then four failures: only one signature (stack underflow -> invalid), Alice plus a forged signature, signatures in the wrong order, and a substituted redeem script (its hash does not match, so the P2SH check fails).

**Why P2SH is nicer:** the complexity is hidden until spend time, so senders pay to a normal-looking short address, and the spender (not the sender) pays the fee for the larger script.

**Simulation caveat.** No real UTXO, transaction or network is involved; the "transaction" is a text message that is signed. Run against Bitcoin Core regtest/testnet the same scripts and addresses would apply.

---

# Viva questions and answers

## General
1. **What is a blockchain?** An append-only, distributed ledger of blocks. Each block contains transactions and the hash of the previous block, so changing history breaks every later link. A consensus mechanism (e.g. proof of work) decides which block is added next.
2. **What properties of hash functions matter here?** Deterministic, fixed-size output, fast to compute, pre-image resistant (can't find input from output), second pre-image and collision resistant, and avalanche effect.
3. **Why is Python's `secrets` used instead of `random`?** `random` is predictable (Mersenne Twister); `secrets` uses the OS's cryptographically secure random source, which is required for private keys.

## Experiment 1
4. **What is a finite field and why must p be prime?** A finite set with +, -, *, / satisfying the field rules. With a prime p every non-zero element has a multiplicative inverse; with a composite modulus some elements (e.g. 2 mod 6) have none, so division fails.
5. **Why is `__eq__` checking `prime` as well?** Two elements are only the same if they are the same number in the *same* field; `2` in F_17 is a different object from `2` in F_31.
6. **How do you do subtraction/negative results?** `(a - b) % p`; Python's modulo of a positive modulus always returns a value in 0..p-1.
7. **How would you implement division?** `a / b = a * b^(p-2) mod p` by Fermat's little theorem, or the extended Euclidean algorithm.
8. **What is operator overloading?** Defining special methods (`__add__`, `__eq__`) so built-in operators work on user classes.

## Experiment 2
9. **Symmetric vs asymmetric encryption?** Symmetric: one shared key, fast, used for bulk data (AES). Asymmetric: public/private pair, slower, solves key distribution and enables signatures (RSA, ECC).
10. **What is an IV and why is it needed?** A random starting block for CBC mode so identical plaintexts encrypt differently. It is not secret but must not be reused with the same key predictably.
11. **What does CBC mode do?** Each plaintext block is XORed with the previous ciphertext block before being encrypted, chaining blocks together.
12. **What is padding?** Filling the last block to 16 bytes (PKCS#7) because AES is a block cipher.
13. **Why can't RSA encrypt a large file directly?** Data must be smaller than the modulus (minus padding), and RSA is slow. Use hybrid encryption: RSA protects a random AES key, AES protects the data.
14. **Which part of the RSA key is secret?** The private exponent `d` (and primes p, q). The public key is (n, e).
15. **Why is 128-bit AES considered secure?** Brute-forcing 2^128 keys is infeasible with current hardware; 192/256 give larger margins.

## Experiment 3
16. **What is a Merkle tree and what is the root?** A binary hash tree over data items; the root is one hash that commits to all leaves.
17. **What if the number of transactions is odd?** The last hash is duplicated to form a pair (Bitcoin's approach).
18. **What is a Merkle proof / why is it useful?** The sibling hashes along the path to the root, about log2(n) of them, proving a transaction is in a block without downloading all transactions (SPV wallets).
19. **Why store only the root in the block header?** Fixed header size, yet it commits to all transactions.
20. **What does changing one transaction do to the root?** It changes that leaf and all its ancestors up to the root (the tamper demo).
21. **Hash chain vs Merkle tree?** Chain: ordered sequence, each hash depends on the previous. Tree: set commitment with efficient proofs.
22. **How would you verify the hash chain later?** Recompute from genesis with the same documents in the same order and compare the final hash.
23. **How many levels for 10 leaves?** 10 -> 5 -> 3 -> 2 -> 1 (five levels including the root).

## Experiment 4
24. **Which curve does Bitcoin use?** secp256k1, y^2 = x^3 + 7 over a 256-bit prime field.
25. **How is the public key derived?** K = k * G, scalar multiplication on the curve.
26. **Why can't the private key be found from the public key?** It requires solving the elliptic curve discrete logarithm problem, which has no known efficient algorithm.
27. **What is double-and-add?** An algorithm to compute k*G in about log2(k) steps by using the binary expansion of k.
28. **Compressed vs uncompressed public key?** 33 bytes (`02/03 + x`) vs 65 bytes (`04 + x + y`). y is recoverable from x and parity. They give different addresses for the same private key.
29. **How is a P2PKH address made?** Version byte 0x00 + RIPEMD160(SHA256(pubkey)) + 4-byte double-SHA256 checksum, Base58 encoded.
30. **Why Base58 and not Base64?** It removes look-alike characters (`0 O I l`) and symbols such as `+` and `/`, making addresses easier to read and copy.
31. **Why a checksum?** To detect typos so funds aren't sent to a mistyped address.
32. **What is WIF and why does it start with 5 or K/L?** A printable private key format: Base58Check of `0x80 + key (+ 0x01)`. The version byte and length produce those leading characters; K/L means "compressed".
33. **Why hash the public key into an address?** Shorter address, and an extra layer of protection: the public key stays hidden until the coins are spent.
34. **How hard is a vanity address?** About 58^k tries for k free characters (here 58^2 ~ 3,364 for `1Ka`). It is brute force.
35. **Is a vanity-address generator safe to use online?** Only if run locally; a third party who knows the private key can steal the funds.

## Experiment 5
36. **What is proof of work?** A consensus method where miners must find a nonce that makes the block hash meet a difficulty target; hard to find, trivial to verify.
37. **What is a nonce?** A number miners change to get different hashes for the same block data.
38. **What is difficulty and how does Bitcoin adjust it?** The required number of leading zeros (target). Adjusted every 2016 blocks so blocks come about every 10 minutes.
39. **How many attempts for 5 hex zeros?** About 16^5 = 1,048,576 on average.
40. **Why does tampering with an old block invalidate the chain?** Its hash changes, so the next block's `prev_hash` no longer matches; the attacker would need to re-mine that block and all following blocks.
41. **What is the 51% attack?** An attacker controlling the majority of hash power could build a longer chain and rewrite recent history (double-spend).
42. **What is the genesis block?** The first block, with no real previous hash (zeros here).
43. **What are other consensus mechanisms?** Proof of Stake, Delegated PoS, PBFT, Proof of Authority.
44. **Drawbacks of PoW?** High energy use, limited throughput, mining centralisation.
45. **What if two miners find a block at the same time?** A temporary fork; nodes follow the longest (most work) chain and the other block is orphaned.

## Experiment 6
46. **What is a UTXO?** An unspent transaction output; Bitcoin tracks coins as a set of these instead of account balances.
47. **What are scriptPubKey and scriptSig?** The locking script on an output and the unlocking script in the input that spends it.
48. **Explain the P2PKH script.** `OP_DUP OP_HASH160 <hash> OP_EQUALVERIFY OP_CHECKSIG`: duplicate the public key, hash it, compare with the address hash, then verify the signature.
49. **What does OP_EQUALVERIFY do?** Compares the top two items and fails the script immediately if they differ.
50. **What does OP_CHECKSIG do?** Verifies the signature against the public key for the transaction data and pushes TRUE/FALSE.
51. **Is Bitcoin Script Turing complete?** No: no loops, so scripts always terminate and can't be abused to hang nodes.
52. **How does ECDSA signing work?** Choose nonce `k`; `r = (kG).x`; `s = k^-1 (z + r d) mod n`. Verify by checking that `(z/s)G + (r/s)Q` has x-coordinate `r`.
53. **What happens if the nonce `k` is reused?** The private key can be computed from two signatures; hence deterministic nonces (RFC 6979).
54. **Why can't someone who copies the public key steal the coins?** They can't produce a valid signature without the private key (attack 2 in the demo).
55. **What is signature malleability / low-s?** For any valid `(r, s)`, `(r, n - s)` is also valid; requiring the low `s` removes this ambiguity.
56. **What is `z` in the code?** The hash of the transaction data being signed (simplified here).
57. **Why is the address not the public key?** The address is a hash of it; see Experiment 4.

## Experiment 7
58. **What is multisig and where is it used?** m-of-n signature requirement: joint accounts, escrow, corporate treasuries, custody.
59. **Write a 2-of-2 script.** `OP_2 <pubA> <pubB> OP_2 OP_CHECKMULTISIG`.
60. **What is P2SH and why was it introduced?** The locking script only contains the hash of the real (redeem) script; the redeem script is revealed on spending. Senders use short addresses and the complexity moves to the spender.
61. **How does a P2SH address look and how is it built?** Starts with `3`; `Base58Check(0x05 || HASH160(redeem script))`.
62. **Why is there an `OP_0` at the start of the unlocking script?** `OP_CHECKMULTISIG` has an off-by-one bug that pops one extra stack item; the dummy element absorbs it.
63. **How is a P2SH spend validated?** Phase 1: hash of the supplied redeem script must equal the hash in the locking script. Phase 2: the redeem script runs with the signatures.
64. **Why does the signature order matter?** The algorithm matches signatures to public keys in order in a single pass.
65. **What happens with only one signature in a 2-of-2?** The script fails (underflow or FALSE) and the spend is rejected.
66. **What is the difference between 2-of-2 and 1-of-2?** 2-of-2 needs both parties (no one can spend alone, and losing a key loses the funds); 1-of-2 lets either party spend.
67. **What is the advantage of 2-of-3?** Redundancy: any two of three keys can spend, so one lost key doesn't lock the funds.
68. **What are the limits of this lab's multisig?** It's a simulation: simplified sighash, no real transaction or network; the opcodes and address format are real.
