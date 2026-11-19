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

---
---

# Theoretical background (concepts behind each experiment)

## Theory for Experiment 1 - Finite fields and why blockchains use them

- **Group, ring, field.** A *group* is a set with one operation that is closed, associative, has an identity and inverses. A *ring* has two operations (+ and *) where + forms a commutative group and * is closed and distributes over +. A *field* is a ring where every non-zero element also has a multiplicative inverse, so you can add, subtract, multiply and divide (except by 0). Rational numbers and real numbers are fields; integers are not (no inverse for 2).
- **Finite field F_p (also written GF(p) or Z_p).** The integers modulo a prime p form a field with exactly p elements. A finite field of size q exists only when q is a prime power (p^k); the size is called the **order**. This lab uses prime fields.
- **Modular arithmetic.** `a ≡ b (mod p)` means p divides a - b. Addition, subtraction and multiplication can be reduced mod p at any step.
- **Why prime?** In Z_n with composite n (say n = 6), `2 * 3 = 0`, so zero divisors exist and 2 has no inverse. With prime p, `gcd(a, p) = 1` for every non-zero a, so an inverse always exists (extended Euclid).
- **Fermat's little theorem.** If p is prime and a is not divisible by p, then `a^(p-1) ≡ 1 (mod p)`. Hence the inverse is `a^(p-2) mod p`, and division is `a / b = a * b^(p-2)`. The multiplicative group of non-zero elements is cyclic, so a generator exists.
- **Why cryptography wants finite fields.** Arithmetic on a finite set is exact (no rounding), numbers never grow beyond log2(p) bits, and operations are easily reversible *only* with extra knowledge (discrete logarithm problem). Elliptic curves defined over F_p turn into a finite group where hard problems exist.
- **Where used:** elliptic-curve cryptography (Bitcoin, Ethereum), Diffie-Hellman, zero-knowledge proofs (zk-SNARKs work over large prime fields), Reed-Solomon codes and AES (which uses GF(2^8)).

## Theory for Experiment 2 - Cryptography basics

- **Goals of cryptography:** confidentiality (only intended people read), integrity (not altered), authentication (who sent it) and non-repudiation (sender can't deny). Encryption gives confidentiality; hashes and MACs give integrity; signatures give authentication and non-repudiation.
- **Kerckhoffs's principle.** A system must stay secure even if everything except the key is public. This is why we use public algorithms (AES, RSA) and protect only keys.
- **Block ciphers and AES.** AES (Rijndael, standard since 2001) encrypts 128-bit blocks with 128/192/256-bit keys using 10/12/14 rounds. Each round does SubBytes (non-linear S-box substitution), ShiftRows, MixColumns (diffusion) and AddRoundKey (XOR with a round key from the key schedule). Confusion + diffusion make output look random.
- **Modes of operation.** A block cipher only handles one block; a mode handles long data. **ECB** encrypts blocks independently (identical blocks give identical ciphertext, so patterns leak - never use). **CBC** chains blocks with an IV. **CTR** turns the cipher into a stream cipher. **GCM** is CTR plus authentication (an *AEAD* mode) and is the modern default.
- **Key size and brute force.** 2^128 operations is beyond any known computing; the best known attacks on full AES barely reduce this. Larger key = more work and slightly slower. Quantum computers (Grover) roughly halve the effective bits, so 256-bit AES stays comfortable.
- **Why random keys matter.** Security reduces to key secrecy and unpredictability; keys must come from a CSPRNG (like `openssl rand`).
- **Public-key cryptography.** Based on **trapdoor one-way functions**: easy forwards, hard backwards unless you know a secret.
- **RSA mathematics.** Choose two large primes p, q; n = p*q; φ(n) = (p-1)(q-1); pick e coprime to φ(n) (commonly 65537); compute d = e^-1 mod φ(n). Public key = (n, e), private key = d. Encrypt `c = m^e mod n`; decrypt `m = c^d mod n` (correct by Euler's theorem). Security rests on the difficulty of **factoring n**. 2048-bit RSA is today's minimum; padding (OAEP for encryption, PSS for signatures) is essential since "textbook RSA" is insecure.
- **Key exchange and hybrid encryption.** Public-key methods (RSA, Diffie-Hellman) are slow, so protocols such as TLS use them only to agree on a session key and then switch to AES.
- **Key management problem.** Symmetric cryptography needs a safe channel to share keys (n people need n(n-1)/2 keys); public-key cryptography solves distribution but needs a way to trust public keys (certificates / PKI). Blockchains avoid PKI because a public key (or its hash) *is* the identity.
- **PEM format.** Base64-encoded DER data between `-----BEGIN ...-----` and `-----END ...-----` lines.
- **OpenSSL.** An open-source toolkit and library (used by TLS/HTTPS) that implements these algorithms from the command line.

## Theory for Experiment 3 - Hashing, Merkle trees, tamper evidence

- **Cryptographic hash function** `H: {0,1}* -> {0,1}^n`. Required properties:
  - *Pre-image resistance* (one-way): given h, can't find m with H(m) = h (about 2^n work).
  - *Second pre-image resistance*: given m1, can't find m2 ≠ m1 with the same hash.
  - *Collision resistance*: can't find any two inputs with the same hash (about 2^(n/2) work because of the **birthday paradox**; for SHA-256 that is 2^128).
  - *Determinism, speed, avalanche effect* (flipping one input bit flips about half the output bits).
- **SHA-256** belongs to the SHA-2 family (NSA design, NIST standard), uses the Merkle-Damgard construction with a 512-bit block size and 64 rounds, and outputs 256 bits. MD5 and SHA-1 are broken for collisions. Bitcoin uses SHA-256 (often applied twice, "double SHA-256", to avoid length-extension attacks).
- **Hash vs encryption.** A hash is keyless and irreversible; encryption is reversible with a key. A hash is *not* encryption and can't be "decrypted".
- **Data integrity & digital fingerprints.** Comparing hashes verifies that a file is unchanged (e.g. download checksums). A hash alone doesn't prove *who* produced it; for that you sign it, or use a keyed MAC.
- **Merkle tree (hash tree), Ralph Merkle 1979.** Leaves = hashes of data blocks; internal nodes = hash of children's concatenation. Properties: root commits to all data; inclusion proof size O(log n); verifying needs no other leaves; detects exactly which part changed by comparing subtrees. Used in Bitcoin (transaction root), Ethereum (state trees, Merkle-Patricia), Git, IPFS, Certificate Transparency and databases such as Cassandra and DynamoDB (anti-entropy).
- **SPV (Simplified Payment Verification).** Light wallets download only block headers (80 bytes each) and ask a full node for the Merkle path of their transaction, then check it matches the root in the header.
- **Hash chain.** A sequence where each element hashes the previous. Applications: blockchain linking (`prev_hash`), password/OTP schemes (S/KEY, Lamport), audit logs, timestamping. It makes records append-only and tamper-evident because any change forces recomputation of all later hashes - and in a distributed network others hold the original hashes.
- **Immutability is tamper-*evidence*.** A blockchain doesn't physically stop edits; it makes them detectable and (with consensus) practically rejected.
- **Why academic records on a blockchain?** Certificates/grades are verified by anyone against a published root without contacting the university, and cannot be forged retrospectively. Only the hash is stored on-chain, so private data stays private.

## Theory for Experiment 4 - Public-key cryptography in Bitcoin

- **Digital signatures.** Sign with the private key, verify with the public key. Provide authentication, integrity and non-repudiation. In Bitcoin a signature *is* the authorisation to spend; there are no passwords or accounts.
- **Elliptic curves.** An elliptic curve over a prime field is the set of points (x, y) satisfying y^2 = x^3 + ax + b (mod p), plus a point at infinity O (the identity). Bitcoin's secp256k1 has a = 0, b = 7. Points form an abelian group under the **chord-and-tangent** rule: draw a line through P and Q, find the third intersection and reflect it over the x-axis to get P + Q; for P = Q use the tangent.
- **Scalar multiplication and the ECDLP.** `kP = P + P + ... + P`. Given P and Q = kP, finding k is the **Elliptic Curve Discrete Logarithm Problem**; the best generic attacks need about sqrt(n) steps, so a 256-bit curve gives about 128 bits of security. A 256-bit ECC key is comparable to a 3072-bit RSA key but much smaller and faster.
- **secp256k1 domain parameters.** Prime p = 2^256 - 2^32 - 977, curve y^2 = x^3 + 7, base point G, group order n (about 2^256), cofactor 1. "sec" = Standards for Efficient Cryptography, "p" = prime field, "256" = bits, "k" = Koblitz curve, "1" = first variant.
- **Why key space is safe.** There are about 2^256 ≈ 10^77 private keys; guessing one is as hopeless as guessing a particular atom among all atoms in the visible universe is for a human. The real risk is *bad randomness*, not brute force.
- **Quantum threat.** Shor's algorithm would solve ECDLP in polynomial time on a large quantum computer. Because addresses are hashes of public keys, unspent coins in never-reused addresses are partly protected until spending; post-quantum signatures are being researched.
- **Address generation theory.** Hashing the public key gives (a) a shorter identifier (20 bytes vs 33/65), (b) hides the public key until spend, (c) two-layer hash protection. The four-byte double-SHA256 checksum catches random errors with probability 1 - 2^-32.
- **Encoding.** *Hexadecimal* (base 16) for raw bytes, *Base58* for human-friendly strings. Base58Check = payload + checksum, then Base58. Newer SegWit addresses use *Bech32* (`bc1...`), which is case-insensitive and has stronger error detection.
- **Wallets.** A wallet is a keystore, not a coin store. *Non-deterministic wallets* hold independent random keys; *HD wallets* (BIP-32/39/44) derive all keys from one seed phrase (12/24 words), so one backup covers everything. Losing the private key means losing the coins permanently; there is no recovery.
- **Network prefixes.** Version bytes distinguish networks and types: `0x00` mainnet P2PKH (`1...`), `0x05` mainnet P2SH (`3...`), `0x6F` testnet P2PKH (`m`/`n`), `0x80` mainnet WIF.
- **Address types:** P2PKH (`1...`, legacy), P2SH (`3...`), P2WPKH (`bc1q...`, SegWit), P2TR (`bc1p...`, Taproot).
- **Vanity addresses and proof of work.** Both are brute-force searches whose cost grows exponentially with the number of constrained characters/bits; the difference is that mining's goal is set by the network.

## Theory for Experiment 5 - Consensus and Proof of Work

- **The double-spend problem.** Digital data can be copied, so how do you stop someone spending the same coin twice without a trusted bank? Bitcoin solves it with a public ledger everyone agrees on, which requires **consensus** among untrusting nodes.
- **Byzantine Generals Problem.** Distributed nodes must agree even when some are faulty or malicious. Classic BFT algorithms (PBFT) tolerate up to f faulty nodes out of 3f + 1 but need a known, small set of participants. Nakamoto consensus works in an open network by using computational work as the "vote", making identity (Sybil attacks) irrelevant: it's one-CPU-one-vote, not one-IP-one-vote.
- **Proof of Work (Hashcash, Adam Back 1997).** Originally an anti-spam idea. The miner finds a nonce so that `H(header) < target`. Properties: *hard to compute* (probabilistic, memoryless, so it is like a lottery weighted by hash power), *cheap to verify*, *progress-free*.
- **Block header (Bitcoin, 80 bytes):** version, previous block hash, Merkle root, timestamp, difficulty target (`nBits`), nonce. Miners hash the header twice with SHA-256. The nonce is only 32 bits, so miners also change the *extra nonce* in the coinbase transaction to get new Merkle roots.
- **Difficulty target.** The hash is interpreted as a 256-bit number and must be below the target. Lower target = harder. Expected attempts ≈ 2^256 / target. Retargeting every 2016 blocks (about two weeks) multiplies difficulty by (actual time / 20160 minutes), clamped to a factor of 4.
- **Incentives.** The miner of a valid block earns the **block subsidy** (50 BTC at launch, halving every 210,000 blocks, about four years) plus transaction fees. The first transaction in each block is the **coinbase** transaction creating the reward. Total supply is capped near 21 million BTC.
- **Longest-chain (most-work) rule and forks.** Nodes always extend the valid chain with the most cumulative work. Temporary forks (two blocks found at once) resolve when one branch becomes longer; the losing blocks become *orphaned/stale*. A transaction becomes safer with each **confirmation** (block on top); six confirmations is the convention.
- **51% attack.** If one entity controls over half the hash power it can reorganise recent history (double-spend its own transactions, censor others), but cannot steal other people's coins, forge signatures or change consensus rules.
- **Security vs cost.** Rewriting a block means redoing its work and all following blocks' work, so the cost grows linearly with depth; this is why PoW gives *probabilistic finality*.
- **Costs of PoW.** High electricity consumption, specialised hardware (ASICs) and mining pool centralisation.
- **Alternatives.**
  - *Proof of Stake* (Ethereum since 2022): validators lock coins as collateral and are chosen in proportion to stake; misbehaviour is punished by slashing; no energy-heavy mining.
  - *Delegated PoS*, *Proof of Authority* (known validators), *PBFT/Tendermint* (voting rounds, instant finality, small validator sets), *Proof of Elapsed Time*, *Proof of Space*.
  - Trade-offs follow the **CAP theorem / blockchain trilemma**: decentralisation, security and scalability are hard to maximise together.
- **Types of blockchains.** *Public permissionless* (Bitcoin, Ethereum), *public permissioned*, *private/consortium* (Hyperledger Fabric) which often use faster non-PoW consensus because participants are known.
- **Smart contracts (context).** Ethereum extended the idea so the chain stores and executes programs; Bitcoin Script is deliberately limited.

## Theory for Experiment 6 - Bitcoin transactions and Script

- **Transaction model.** A transaction consumes previous outputs (**inputs**) and creates new **outputs**. Each input points at a previous transaction ID and output index and supplies an unlocking script. Each output has an amount (satoshis; 1 BTC = 10^8 sat) and a locking script. The sum of inputs minus outputs is the **fee** for miners. Outputs are spent whole, so "change" goes back to the sender in an extra output.
- **UTXO set vs account model.** Bitcoin keeps the set of all unspent outputs; a "balance" is the sum of UTXOs you can unlock. Ethereum uses accounts with balances and nonces. UTXOs make parallel validation and privacy easier; accounts are simpler for contracts.
- **Script language.** Stack-based (Forth-like), reverse Polish notation, executed left to right, *not Turing-complete* (no loops), deterministic and limited in size and operations, so every node can validate it quickly and safely.
- **Standard script types:** P2PK (pay to public key), **P2PKH**, P2SH, multisig, P2WPKH/P2WSH (SegWit), P2TR (Taproot), and `OP_RETURN` (unspendable data carrier, used for timestamping/embedding hashes).
- **Why hash the public key (P2PKH vs P2PK).** Shorter, adds a hash layer (including a modest quantum-resistance bonus before first spend), and gives the familiar address format.
- **Signature hash types.** The signed message is a hash of a *modified copy* of the transaction. `SIGHASH_ALL` (default) commits to all inputs and outputs; `NONE` and `SINGLE` commit to fewer outputs; `ANYONECANPAY` lets others add inputs (crowdfunding-style transactions).
- **Transaction IDs and malleability.** The txid is a double SHA-256 of the serialised transaction. Before SegWit, third parties could alter the signature encoding and change the txid without invalidating it; SegWit moved signatures to a separate witness structure to fix this.
- **ECDSA vs Schnorr.** ECDSA (used here) needs a modular inversion and is not linear; Schnorr signatures (added with Taproot, 2021) are simpler, allow key/signature aggregation and provable security.
- **Validation by nodes.** A node checks: format; inputs exist and are unspent (no double spend); scripts evaluate to TRUE; amounts valid (inputs >= outputs); size and standardness rules. Valid transactions wait in the **mempool** until a miner includes them in a block.
- **Mining a transaction in practice:** broadcast -> relay by peer-to-peer gossip -> mempool -> included in a block -> confirmations.
- **Testnet and regtest.** Test networks with worthless coins (testnet) and a private local chain (regtest) let developers experiment safely. This lab simulates the script logic locally instead.

## Theory for Experiment 7 - Multisignature and P2SH

- **Multi-party authorisation.** An m-of-n scheme splits control among n keys with threshold m. It improves security (an attacker must compromise m keys) and resilience (any m keys suffice). The trade-off is between availability (lower m, higher n) and security (higher m).
- **Common patterns.**
  - *1-of-2*: shared account where either person can spend.
  - *2-of-2*: both must approve (joint account, payment channels, e.g. Lightning funding output).
  - *2-of-3*: escrow (buyer, seller, arbiter) or personal backup (phone, laptop, hardware wallet / recovery key).
  - *3-of-5*: organisational treasuries or exchanges.
- **Bare multisig limits:** scripts of up to 15 public keys (so addresses get very long), the large script sits in the sender's output, and the output is expensive to relay.
- **P2SH (BIP-16, 2012).** The output commits only to `HASH160(redeemScript)`. The redeem script is disclosed in the spending input, and nodes enforce it by executing it. Benefits: short `3...` addresses, sender need not know the details, the spender pays for complexity, and it supports arbitrary scripts (not just multisig). The special-case rule in the interpreter ("if the script is `HASH160 <h> EQUAL`, execute the redeem script") is how the soft fork was introduced without breaking old nodes.
- **P2WSH / SegWit multisig.** Newer, cheaper and malleability-resistant forms of the same idea, using Bech32 `bc1q...` addresses.
- **Threshold signatures / MuSig (Schnorr).** Instead of publishing several signatures, the parties combine keys into one aggregate public key and produce one signature that looks like a normal single-key spend: cheaper and more private. This is not what the lab does, but it is where multisig is heading with Taproot.
- **Security considerations.** Keys should be stored on separate devices/locations; the redeem script must be backed up (without it you can't spend even if you have the keys); keys should be generated independently; verify the address on all devices before funding.
- **Real-world usage.** Hardware-wallet setups, exchange cold storage, escrow services, and the 2-of-2 funding transaction of Lightning payment channels.

---

# More viva questions (theory)

## Mathematics and cryptography fundamentals
69. **What is a group? What is a field?** A group has one operation with closure, associativity, identity and inverses. A field has two operations (+, *) where every non-zero element has a multiplicative inverse.
70. **State Fermat's little theorem and one use.** `a^(p-1) ≡ 1 (mod p)` for prime p and p not dividing a; used to compute inverses as `a^(p-2)` and in primality tests.
71. **What is the order of a field/group?** The number of elements; F_p has order p, and the Bitcoin curve group has order n (about 2^256).
72. **Difference between encoding, encryption and hashing?** Encoding (Base58, hex) is reversible and for representation only; encryption is reversible with a key and hides data; hashing is one-way and creates a fingerprint.
73. **What is the avalanche effect?** A tiny change to the input changes about half of the output bits unpredictably.
74. **What is the birthday paradox and why does it matter for hashes?** Collisions appear after about 2^(n/2) tries, not 2^n, so an n-bit hash gives only n/2 bits of collision resistance.
75. **Why is SHA-256 applied twice in Bitcoin?** To protect against length-extension attacks and as a defensive design choice.
76. **What are MD5 and SHA-1 and why are they avoided?** Older hash functions with practical collision attacks.
77. **What is a MAC / HMAC?** A keyed hash that gives integrity and authenticity (needs a shared secret); we used HMAC to derive the deterministic nonce in ECDSA.
78. **What is a digital signature and how is it different from a MAC?** A signature uses a private key and is verifiable by anyone with the public key (gives non-repudiation); a MAC needs the same secret on both sides.
79. **What is the security basis of RSA vs ECC?** RSA: integer factorisation. ECC: elliptic curve discrete logarithm.
80. **Why is a 256-bit ECC key comparable to a 3072-bit RSA key?** Best known attacks on ECC are fully exponential (about sqrt(n)), while factoring has sub-exponential algorithms, so RSA needs much bigger keys.
81. **What is a trapdoor function?** Easy to compute forwards but hard to invert unless you know secret information.
82. **What is Kerckhoffs's principle?** Security should depend only on the secrecy of the key, not the algorithm.
83. **ECB vs CBC vs GCM?** ECB leaks patterns, CBC chains with an IV, GCM gives encryption plus authentication.
84. **What is Diffie-Hellman key exchange?** Two parties derive a shared secret over a public channel using discrete-log hardness (ECDH on elliptic curves).
85. **What is PKI and why does blockchain not need it?** PKI uses certificate authorities to bind identities to public keys; blockchains use the public key (or its hash) as the identity itself.
86. **What is a CSPRNG?** A cryptographically secure pseudo-random generator, whose output is unpredictable even to someone who has seen earlier output.

## Blockchain concepts
87. **What are the main features of a blockchain?** Decentralisation, immutability (tamper evidence), transparency, consensus-based validation, cryptographic security and traceability.
88. **What is a block made of?** A header (previous hash, Merkle root, timestamp, difficulty, nonce, version) and a list of transactions.
89. **What is a distributed ledger?** A database replicated across many nodes with no central owner, kept consistent by a consensus protocol.
90. **What is a node? Full node vs light node?** A participant running the software. A full node stores and validates the entire chain; a light (SPV) node keeps only headers and relies on Merkle proofs.
91. **What is the double-spend problem and how is it solved?** Spending the same coin twice; solved by an agreed ordering of transactions in the blockchain and by rejecting any transaction that spends an already spent output.
92. **Permissioned vs permissionless blockchains?** Permissionless: anyone can join (Bitcoin). Permissioned: known participants with access control (Hyperledger Fabric).
93. **What is the Byzantine Generals Problem?** Reaching agreement among distributed parties when some may be traitors/faulty; PoW gives a probabilistic solution for open networks.
94. **What is a Sybil attack and how does PoW resist it?** Creating many fake identities to gain influence; PoW weights influence by computing power, not identity count.
95. **What are confirmations?** The number of blocks built on top of a transaction's block; more confirmations means exponentially lower chance of reversal.
96. **What is the block reward and halving?** New coins given to the miner of a block, halved every 210,000 blocks (about four years), capping supply at about 21 million.
97. **What is a coinbase transaction?** The first transaction in a block that creates the reward and has no real inputs.
98. **What is a mempool?** The pool of valid, unconfirmed transactions waiting at a node to be mined.
99. **What is a fork? Soft fork vs hard fork?** A divergence in the chain. A soft fork tightens the rules (backward compatible, e.g. P2SH, SegWit); a hard fork loosens or changes them so non-upgraded nodes reject the new blocks (e.g. Bitcoin Cash).
100. **What is the blockchain trilemma?** The difficulty of achieving decentralisation, security and scalability at the same time.
101. **Proof of Work vs Proof of Stake?** PoW: security from energy and hardware spent; PoS: security from locked capital that can be slashed; PoS uses far less energy.
102. **Why is Bitcoin Script not Turing complete?** To guarantee termination and limit attack surface (no infinite loops), which keeps validation cheap for every node.
103. **What is SegWit?** Segregated Witness (2017) moves signature data out of the transaction body, fixes malleability, effectively raises capacity and enables Lightning.
104. **What is Taproot?** A 2021 upgrade adding Schnorr signatures and MAST so complex spending conditions (including multisig) look like ordinary single-key spends.
105. **What is the Lightning Network?** A layer-2 network of payment channels, opened with a 2-of-2 multisig output, enabling fast, cheap off-chain payments settled on Bitcoin.
106. **What is a smart contract?** Code stored and executed on a blockchain (e.g. Ethereum); Bitcoin Script supports limited contract-like conditions such as multisig and timelocks.
107. **What are timelocks (`OP_CHECKLOCKTIMEVERIFY`)?** Script conditions that prevent spending until a certain time or block height.
108. **Real-life applications of blockchain?** Cryptocurrencies, supply-chain tracking, academic credential verification, healthcare records, digital identity, voting, land registries, and notarisation/timestamping.
109. **Limitations of blockchain?** Throughput and latency limits, storage growth, energy use for PoW, immutability making errors hard to correct, regulatory and privacy issues (pseudonymous, not anonymous).
110. **Why is Bitcoin pseudonymous and not anonymous?** Addresses are not tied to names, but every transaction is public and can often be linked to people by analysis.
