"""Experiment 7 - 2-of-2 multisig (P2SH): create address, lock funds, spend (simulation)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))
from btc import *
from script import *

# 1. Two participants
alice_priv, bob_priv = gen_private_key(), gen_private_key()
alice_pub = pubkey_bytes(point_mul(alice_priv))
bob_pub = pubkey_bytes(point_mul(bob_priv))
print("Alice pubkey:", alice_pub.hex())
print("Bob   pubkey:", bob_pub.hex())

# 2. Redeem script: 2 <pubA> <pubB> 2 OP_CHECKMULTISIG
redeem = ["OP_2", alice_pub, bob_pub, "OP_2", "OP_CHECKMULTISIG"]
redeem_raw = encode(redeem)
print("\nREDEEM SCRIPT:", show(redeem))
print("   raw hex    :", redeem_raw.hex())

# 3. P2SH address = Base58Check(0x05 || HASH160(redeem script))
h = hash160(redeem_raw)
address = address_from_hash160(h, version=b"\x05")
print("\nP2SH 2-of-2 multisig address:", address, "(starts with 3)")

# 4. Lock funds: scriptPubKey = OP_HASH160 <hash> OP_EQUAL
script_pubkey = ["OP_HASH160", h, "OP_EQUAL"]
print("\nLOCKING SCRIPT (scriptPubKey):", show(script_pubkey))

# 5. Spend: needs BOTH signatures + the redeem script
tx_msg = b"Send 1.0 BTC from multisig UTXO def456:1 to Carol"
z = int.from_bytes(dsha256(tx_msg), "big")
sig_a = der_encode(sign(alice_priv, z))
sig_b = der_encode(sign(bob_priv, z))
script_sig = ["OP_0", sig_a, sig_b, redeem_raw]
print("\nUNLOCKING SCRIPT (scriptSig): OP_0 <sigAlice> <sigBob> <redeemScript>")

print("\nEXECUTION TRACE:")
print("\nSpend with both signatures ->", validate(script_sig, script_pubkey, z, trace=True))

# 6. Failure cases
print("\nOnly Alice signs (1 of 2)      ->", validate(["OP_0", sig_a, redeem_raw], script_pubkey, z))
mal = gen_private_key()
fake = der_encode(sign(mal, z))
print("Alice + attacker's signature   ->", validate(["OP_0", sig_a, fake, redeem_raw], script_pubkey, z))
print("Signatures in wrong order      ->", validate(["OP_0", sig_b, sig_a, redeem_raw], script_pubkey, z))
print("Wrong redeem script            ->", validate(["OP_0", sig_a, sig_b, encode(["OP_1", alice_pub, "OP_1", "OP_CHECKMULTISIG"])], script_pubkey, z))
