"""Experiment 4 - Bitcoin keys, addresses, Base58Check, WIF, compressed/uncompressed, vanity address.
Usage: python keys.py [vanity_prefix]     (default prefix: 1Ka)"""
import sys, time
import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))
from btc import *

print("=" * 70)
print("1. PRIVATE KEY (random 256-bit integer in [1, n-1])")
priv = gen_private_key()
print("   hex :", f"{priv:064x}")

print("\n2. PUBLIC KEY  (K = k * G on secp256k1)")
pt = point_mul(priv)
print("   x   :", f"{pt[0]:064x}")
print("   y   :", f"{pt[1]:064x}")
unc = pubkey_bytes(pt, compressed=False)
com = pubkey_bytes(pt, compressed=True)
print("   uncompressed (65 B, 04||x||y):", unc.hex())
print("   compressed   (33 B, 02/03||x):", com.hex())

print("\n3. BITCOIN ADDRESS  (Base58Check(0x00 || RIPEMD160(SHA256(pubkey))))")
for name, pub in (("uncompressed", unc), ("compressed", com)):
    h = hash160(pub)
    print(f"   [{name}]")
    print("     hash160 :", h.hex())
    print("     payload :", (b"\x00" + h).hex())
    print("     checksum:", dsha256(b"\x00" + h)[:4].hex(), "(first 4 bytes of double SHA256)")
    print("     address :", pubkey_to_address(pub))

print("\n4. BASE58CHECK ENCODING demo")
demo = b"\x00" + hash160(com)
enc = b58check_encode(demo)
print("   encode:", enc)
print("   decode back ok:", b58check_decode(enc) == demo)

print("\n5. WIF (Wallet Import Format)")
print("   uncompressed WIF (starts with 5):", wif(priv, compressed=False))
print("   compressed   WIF (starts K or L):", wif(priv, compressed=True))
raw = b58check_decode(wif(priv, True))
print("   round-trip check (decode WIF):", int.from_bytes(raw[1:33], "big") == priv)

print("\n6. VANITY ADDRESS")
prefix = sys.argv[1] if len(sys.argv) > 1 else "1Ka"
print(f"   searching for address starting with '{prefix}' ...")
t0, tries = time.time(), 0
while True:
    tries += 1
    k = gen_private_key()
    addr = pubkey_to_address(pubkey_bytes(point_mul(k), True))
    if addr.startswith(prefix):
        break
print(f"   found after {tries} tries in {time.time() - t0:.1f}s")
print("   address     :", addr)
print("   private key :", f"{k:064x}")
print("   WIF         :", wif(k, True))
