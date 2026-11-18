"""Minimal pure-Python Bitcoin primitives (secp256k1, ECDSA, Base58Check, WIF, addresses).
Educational only - not constant-time, do not use with real funds."""
import hashlib, hmac, secrets

# ---- secp256k1 parameters ----
P = 2**256 - 2**32 - 977
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)


def point_add(a, b):
    if a is None: return b
    if b is None: return a
    if a[0] == b[0] and (a[1] + b[1]) % P == 0: return None
    if a == b:
        m = 3 * a[0] * a[0] * pow(2 * a[1], -1, P) % P
    else:
        m = (b[1] - a[1]) * pow(b[0] - a[0], -1, P) % P
    x = (m * m - a[0] - b[0]) % P
    return (x, (m * (a[0] - x) - a[1]) % P)


def point_mul(k, pt=G):
    r = None
    while k:
        if k & 1: r = point_add(r, pt)
        pt = point_add(pt, pt)
        k >>= 1
    return r


# ---- hashes ----
def sha256(b): return hashlib.sha256(b).digest()
def dsha256(b): return sha256(sha256(b))
def hash160(b): return hashlib.new("ripemd160", sha256(b)).digest()


# ---- Base58Check ----
B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def b58encode(b: bytes) -> str:
    n = int.from_bytes(b, "big")
    s = ""
    while n:
        n, r = divmod(n, 58)
        s = B58[r] + s
    pad = len(b) - len(b.lstrip(b"\0"))
    return "1" * pad + s

def b58decode(s: str) -> bytes:
    n = 0
    for c in s: n = n * 58 + B58.index(c)
    body = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return b"\0" * (len(s) - len(s.lstrip("1"))) + body

def b58check_encode(payload: bytes) -> str:
    return b58encode(payload + dsha256(payload)[:4])

def b58check_decode(s: str) -> bytes:
    raw = b58decode(s)
    payload, chk = raw[:-4], raw[-4:]
    if dsha256(payload)[:4] != chk: raise ValueError("bad checksum")
    return payload


# ---- keys ----
def gen_private_key() -> int:
    while True:
        k = secrets.randbelow(N)
        if k >= 1: return k

def pubkey_bytes(pt, compressed=True) -> bytes:
    x, y = pt
    if compressed:
        return bytes([2 + (y & 1)]) + x.to_bytes(32, "big")
    return b"\x04" + x.to_bytes(32, "big") + y.to_bytes(32, "big")

def pubkey_from_bytes(b: bytes):
    if b[0] == 4:
        return int.from_bytes(b[1:33], "big"), int.from_bytes(b[33:], "big")
    x = int.from_bytes(b[1:], "big")
    y = pow((x**3 + 7) % P, (P + 1) // 4, P)
    if (y & 1) != (b[0] & 1): y = P - y
    return x, y

def address_from_hash160(h: bytes, version=b"\x00") -> str:
    return b58check_encode(version + h)

def pubkey_to_address(pub: bytes, version=b"\x00") -> str:
    return address_from_hash160(hash160(pub), version)

def wif(priv: int, compressed=True, version=b"\x80") -> str:
    payload = version + priv.to_bytes(32, "big") + (b"\x01" if compressed else b"")
    return b58check_encode(payload)


# ---- ECDSA (RFC6979-style deterministic k) ----
def _k(priv, z):
    x = priv.to_bytes(32, "big"); h = z.to_bytes(32, "big")
    k = b"\x00" * 32; v = b"\x01" * 32
    k = hmac.new(k, v + b"\x00" + x + h, hashlib.sha256).digest(); v = hmac.new(k, v, hashlib.sha256).digest()
    k = hmac.new(k, v + b"\x01" + x + h, hashlib.sha256).digest(); v = hmac.new(k, v, hashlib.sha256).digest()
    while True:
        v = hmac.new(k, v, hashlib.sha256).digest()
        c = int.from_bytes(v, "big")
        if 1 <= c < N: return c
        k = hmac.new(k, v + b"\x00", hashlib.sha256).digest(); v = hmac.new(k, v, hashlib.sha256).digest()

def sign(priv: int, z: int):
    k = _k(priv, z)
    r = point_mul(k)[0] % N
    s = pow(k, -1, N) * (z + r * priv) % N
    if s > N // 2: s = N - s
    return r, s

def verify(pub, z: int, sig) -> bool:
    r, s = sig
    if not (1 <= r < N and 1 <= s < N): return False
    w = pow(s, -1, N)
    pt = point_add(point_mul(z * w % N), point_mul(r * w % N, pub))
    return pt is not None and pt[0] % N == r

def der_encode(sig) -> bytes:
    def enc(i):
        b = i.to_bytes(32, "big").lstrip(b"\0")
        if b[0] & 0x80: b = b"\0" + b
        return b"\x02" + bytes([len(b)]) + b
    body = enc(sig[0]) + enc(sig[1])
    return b"\x30" + bytes([len(body)]) + body

def der_decode(d: bytes):
    rl = d[3]; r = int.from_bytes(d[4:4 + rl], "big")
    sl = d[5 + rl]; s = int.from_bytes(d[6 + rl:6 + rl + sl], "big")
    return r, s
