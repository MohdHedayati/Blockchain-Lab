"""Experiment 6 - Pay-to-Public-Key-Hash (P2PKH) locking script (simulation)."""
import sys
import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))
from btc import *
from script import *

# --- Recipient (Bob) generates a keypair and address ---
bob_priv = gen_private_key()
bob_pub = pubkey_bytes(point_mul(bob_priv), compressed=True)
bob_h160 = hash160(bob_pub)
address = address_from_hash160(bob_h160)
print("Recipient address :", address)
print("Public key hash   :", bob_h160.hex())

# --- Lock funds: address -> pubkey hash -> scriptPubKey ---
assert b58check_decode(address)[1:] == bob_h160
script_pubkey = ["OP_DUP", "OP_HASH160", bob_h160, "OP_EQUALVERIFY", "OP_CHECKSIG"]
print("\nLOCKING SCRIPT (scriptPubKey):")
print("  ", show(script_pubkey))
print("   raw hex:", encode(script_pubkey).hex(), "(76a914<20-byte hash>88ac)")

# --- Spend: Bob signs the transaction and supplies <sig> <pubkey> ---
tx_msg = b"Send 0.5 BTC from UTXO abc123:0 to Carol"     # stands in for the tx data being signed
z = int.from_bytes(dsha256(tx_msg), "big")
sig = der_encode(sign(bob_priv, z))
script_sig = [sig, bob_pub]
print("\nUNLOCKING SCRIPT (scriptSig):  <signature> <public key>")
print("   sig:", sig.hex())
print("   pub:", bob_pub.hex())

print("\nEXECUTION TRACE (scriptSig + scriptPubKey):")
ok = validate(script_sig, script_pubkey, z, trace=True)
print("\nValid spend by owner ->", ok)

# --- Failure cases ---
mallory_priv = gen_private_key()
mallory_pub = pubkey_bytes(point_mul(mallory_priv))
bad1 = validate([der_encode(sign(mallory_priv, z)), mallory_pub], script_pubkey, z)
print("Attacker with own key (wrong pubkey hash) ->", bad1)
bad2 = validate([der_encode(sign(mallory_priv, z)), bob_pub], script_pubkey, z)
print("Attacker using Bob's pubkey but own signature ->", bad2)
