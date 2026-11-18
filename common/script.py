"""Tiny Bitcoin Script interpreter (subset) for P2PKH, multisig and P2SH.
Simplification: the signature hash is dsha256(tx_message) instead of Bitcoin's full sighash serialization."""
from btc import *

OPS = {"OP_0": 0x00, "OP_DUP": 0x76, "OP_HASH160": 0xA9, "OP_EQUAL": 0x87, "OP_EQUALVERIFY": 0x88,
       "OP_CHECKSIG": 0xAC, "OP_CHECKMULTISIG": 0xAE, **{f"OP_{i}": 0x50 + i for i in range(1, 17)}}
NAMES = {v: k for k, v in OPS.items()}


def encode(script):
    """List of opcodes/bytes -> raw script bytes."""
    out = b""
    for item in script:
        if isinstance(item, str):
            out += bytes([OPS[item]])
        else:
            out += bytes([len(item)]) + item
    return out


def decode(raw):
    items, i = [], 0
    while i < len(raw):
        op = raw[i]; i += 1
        if 1 <= op <= 75:
            items.append(raw[i:i + op]); i += op
        else:
            items.append(NAMES[op])
    return items


def show(script):
    return " ".join(s if isinstance(s, str) else s.hex() for s in script)


def run(script, stack, z, trace=False):
    """Executes script items on stack (list). Returns True if no failure."""
    for item in script:
        if trace: print(f"    {show([item]) if True else ''}".ljust(60)[:60], "| stack before:", [s.hex()[:12] + ('..' if len(s) > 6 else '') for s in stack])
        if not isinstance(item, str):
            stack.append(item); continue
        if item == "OP_0": stack.append(b"")
        elif item.startswith("OP_") and item[3:].isdigit(): stack.append(bytes([int(item[3:])]))
        elif item == "OP_DUP": stack.append(stack[-1])
        elif item == "OP_HASH160": stack.append(hash160(stack.pop()))
        elif item == "OP_EQUAL": stack.append(b"\x01" if stack.pop() == stack.pop() else b"")
        elif item == "OP_EQUALVERIFY":
            if stack.pop() != stack.pop(): return False
        elif item == "OP_CHECKSIG":
            pub, sig = stack.pop(), stack.pop()
            stack.append(b"\x01" if verify(pubkey_from_bytes(pub), z, der_decode(sig)) else b"")
        elif item == "OP_CHECKMULTISIG":
            n = stack.pop()[0]; pubs = [stack.pop() for _ in range(n)][::-1]
            m = stack.pop()[0]; sigs = [stack.pop() for _ in range(m)][::-1]
            stack.pop()                                  # historical off-by-one dummy element
            ok, pi = True, 0
            for s in sigs:                               # sigs must match pubkeys in order
                while pi < n and not verify(pubkey_from_bytes(pubs[pi]), z, der_decode(s)): pi += 1
                if pi == n: ok = False; break
                pi += 1
            stack.append(b"\x01" if ok else b"")
        else:
            raise ValueError("unsupported opcode " + item)
    return True


def _validate(script_sig, script_pubkey, z, trace=False):
    """Run unlocking then locking script on one stack. Handles P2SH (OP_HASH160 <h> OP_EQUAL)."""
    stack = []
    if not run(script_sig, stack, z, trace): return False
    copy = list(stack)
    if not run(script_pubkey, stack, z, trace): return False
    if not stack or stack[-1] == b"": return False
    # P2SH: pubkey script is exactly HASH160 <20 bytes> EQUAL -> run the redeem script too
    if len(script_pubkey) == 3 and script_pubkey[0] == "OP_HASH160" and script_pubkey[2] == "OP_EQUAL":
        redeem = decode(copy[-1])
        if trace: print("  -- P2SH: hash matched, now executing redeem script:", show(redeem))
        stack = copy[:-1]
        if not run(redeem, stack, z, trace): return False
        return bool(stack) and stack[-1] != b""
    return True


def validate(script_sig, script_pubkey, z, trace=False):
    """Any script error (e.g. stack underflow) means the spend is invalid."""
    try:
        return _validate(script_sig, script_pubkey, z, trace)
    except (IndexError, ValueError, KeyError):
        return False
